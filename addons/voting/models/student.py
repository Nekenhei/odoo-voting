# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    career_id = fields.Many2one('university.career', 'Carrera Universitaria', required=True)
    site_id = fields.Many2one('university.site', 'Site Universidad')
    type_career = fields.Selection([('presencial', 'Presencial'),
                                    ('virtual', 'Virtual')], 'Modalidad Estudio', readonly=True, 
                                   compute='_compute_type_career', default='presencial')
    student_identification = fields.Integer('Código Estudiante', required=True, copy=False)
    
    _sql_constraints = [
        ('student_identification_uniq', 'UNIQUE (student_identification)', 
         'El Código Estudiante debe ser unico para cada estudiante.')
    ]
    
    @api.depends('career_id')
    def _compute_type_career(self):
        for record in self:
            record.type_career = 'virtual' if record.career_id and record.career_id.is_virtual else 'presencial'


class StudentCandidate(models.Model):
    _name = 'student.candidate'
    _description = 'Candidatos de Votación'

    partner_id = fields.Many2one('res.partner', 'Estudiante', required=True, copy=False)
    candidate_identification = fields.Integer('# Asignado para Tarjeton', required=True, copy=False)
    name = fields.Char('Nombre', compute='_get_name', readonly=True)
    voting_line_ids = fields.One2many('voting.process.candidate', 'candidate_id', 'Votaciones', readonly=True, copy=False)
    
    _sql_constraints = [
        ('candidate_uniq', 'UNIQUE (partner_id, candidate_identification)',
         'El # de Tarjeton asignado debe ser unico por cada candidato en cada ciclo de Votación'
        )
    ]
    
    @api.model
    def create(self, values):
        iden = values.get('candidate_identification', self.candidate_identification)
        
        partner_name = 'N/A'
        partner_id = values.get('partner_id', False)
        if partner_id:
            partner = self.env['res.partner'].browse(partner_id)
            partner_name = partner.name
        values['name'] = '(' + str(iden) + ') ' + partner_name
        return super(StudentCandidate, self).create(values)
    
    def _get_name(self):
        for record in self:
            if record.partner_id:
                name = '[' + str(record.candidate_identification) + '] ' + record.partner_id.name
            else:
                name = 'N/A'
            record.name = name
