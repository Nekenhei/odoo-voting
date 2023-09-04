# -*- coding: utf-8 -*-

import xlrd
import tempfile
import base64
from odoo import fields, models
from odoo.exceptions import UserError


class VotingImporter(models.TransientModel):
    _name = 'voting.importer'
    _description = 'Importador Votos'

    voting_id = fields.Many2one('voting.process', 'Votación', domain=[('state','=','in_progress')],
                                required=True)
    import_file = fields.Binary('Plantilla de Ejemplo (Archivo)', required=True)
    import_filename = fields.Char('Plantilla Importación', readonly=True)
    
    def button_import(self):
        def validate_int(value, col, row):
            try:
                int(value)
            except:
                raise UserError(f'Error de dato en la columna {col} en la fila {row}.')
        
        if not self.voting_id:
            raise UserError('Debe parametrizar una votación a la cual importar los votos.')
        
        if not self.import_file:
            raise UserError('Debe adjuntar un archivo.')
        
        cr = self._cr
        xlsx_temp = tempfile.NamedTemporaryFile(suffix='.xlsx')
        xlsx_temp.write(base64.b64decode(self.import_file))
        
        wb = xlrd.open_workbook(xlsx_temp.name)
        wb_sheet = wb.sheet_by_index(0)
        
        candidate_qry = f'''
            SELECT vpc.id, sc.candidate_identification 
            FROM voting_process_candidate vpc
            INNER JOIN student_candidate sc ON sc.id = vpc.candidate_id
            WHERE vpc.voting_id = {self.voting_id.id}'''
        
        cr.execute(candidate_qry)
        result = cr.fetchall()
        line_ids = [x[0] for x in result if x[0]] if result else []
        candidate_codes = [x[1] for x in result if x[1]] if result else []
        
        if not (line_ids and candidate_codes):
            raise UserError(f'La votación {self.voting_id.name} NO cuenta con candidatos parametrizados.')
        
        student_qry = f'''
            SELECT rp.student_identification
            FROM res_partner rp
            WHERE rp.site_id = {self.voting_id.site_id.id}'''
        cr.execute(student_qry)
        result = cr.fetchall()
        student_codes = [x[0] for x in result if x[0]] if result else []
        
        if not student_codes:
            raise UserError(f'El site {self.voting_id.site_id.name} NO cuenta con estudiantes parametrizados.')
        
        actual_votes_qry = f'''
            SELECT rp.student_identification 
            FROM candidate_vote cv
            INNER JOIN res_partner rp ON rp.id = cv.student_id
            WHERE voting_candidate_id IN ({','.join([str(x) for x in line_ids])})'''
        cr.execute(actual_votes_qry)
        result = cr.fetchall()
        actual_votes = [x[0] for x in result if x[0]] if result else []
        
        if wb_sheet.nrows < 2:
            raise UserError('El archivo no contiene suficiente información, por favor validar.')
        
        if wb_sheet.ncols != 2:
            raise UserError('Validar el archivo, la cantidad de columnas no es correcta.')
        
        student_env = self.env['res.partner']
        process_env = self.env['voting.process.candidate']
        candidate_env = self.env['student.candidate']
        dt_now = fields.Datetime.now()
        uid = self.env.user.id
        votes_list = []
        students_file = []
        
        for idx_row in range(1, wb_sheet.nrows):
            row = wb_sheet.row(idx_row)
            
            candidate_code = row[0].value
            validate_int(candidate_code, 'A', idx_row+1)
            student_code = row[1].value
            validate_int(student_code, 'B', idx_row+1)
            
            if candidate_code not in candidate_codes:
                raise UserError(f'Error en la fila {idx_row+1}, el # de candidato NO existe en la votación.')
            
            if student_code not in student_codes:
                raise UserError(f'Error en la fila {idx_row+1}, el # de Estudiante NO existe en el site.')
            
            if student_code in actual_votes:
                raise UserError(f'El estudiante {student_code} YA votó en está sesión. Debe eliminar el registro del archivo.')
            
            if student_code in students_file:
                raise UserError(f'El estudiante {student_code} está duplicado en el archivo. Debe eliminar el registro del archivo.')
            
                        
            candidate = candidate_env.search([('candidate_identification', '=', candidate_code)], limit=1)
            process = process_env.search([('voting_id', '=', self.voting_id.id), ('candidate_id', '=', candidate.id)])
            student = student_env.search([('student_identification', '=', student_code)])
            votes_list.append(f"({process.id}, {student.id}, '{str(dt_now)}', '{str(dt_now)}', {uid}, {uid})")
            students_file.append(student_code)
            
        
        insert_qry = f'''
            INSERT INTO candidate_vote (voting_candidate_id, student_id, create_date, write_date, create_uid, write_uid)
            VALUES {','.join(votes_list)}
        '''
        cr.execute(insert_qry)
        cr.commit()
        self.voting_id.voting_line_ids.get_voting_qty()
        
        action = self.env.ref('voting.action_voting_process_act_window').read()[0]
        action['view_mode'] = 'form'
        action['res_id'] = self.voting_id.id
        
        return action
