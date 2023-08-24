# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError


class VotingProcess(models.Model):
    _name = 'voting.process'
    _description = 'Proceso de Votación'

    name = fields.Char('Name', default='/', readonly=True)
    semester = fields.Selection([('first', '1er Semestre'), ('second', '2o Semestre')], 'Semestre Votación', store=True,
                                compute='_get_year_semester', readonly=True)
    year = fields.Integer('Año Votación', readonly=True, compute='_get_year_semester', store=True)
    description = fields.Html('Descripción Proceso Votación', copy=False)
    start_date = fields.Datetime('Fecha Inicio', required=True, copy=False)
    end_date = fields.Datetime('Fecha Fin', required=True, copy=False)
    state = fields.Selection([('draft', 'Borrador'), ('in_progress', 'En Progreso'), ('done', 'Cerrada'), 
                              ('cancel', 'Cancelado')], 'Estado', readonly=True, copy=False, default='draft')
    site_id = fields.Many2one('university.site', 'Site Votación', required=True)
    voting_line_ids = fields.One2many('voting.process.candidate', 'voting_id', 'Candidatos', copy=False)
    
    _sql_constraints = [
        ('voting_uniq', 'UNIQUE (semester, year, site_id)', 
         'Los procesos de Votación deben ser unicos para cada combinación de Año/Semestre')
    ]
    
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        vot_env = self.env['voting.process']
        for record in self:
            if record.end_date < record.start_date:
                raise UserError(f'Las fecha de Inicio debe ser menor a la Fecha Fin del proceso.')
            
            days_diff = (record.end_date - record.start_date).days
            if days_diff > 1:
                raise UserError('Las votaciones deben ser llevadas a cabo el mismo día')
            
            votings = vot_env.search([('site_id', '=', record.site_id.id), ('semester', '=', record.semester), 
                                      ('year', '=', record.year), ('state', '!=', 'cancel'), ('id', '!=', record.id)])
            if votings:
                raise UserError('Ya existe una votación para el semestre y site indicados')
            
    @api.constrains('state', 'site_id')
    def _check_dates(self):
        vot_env = self.env['voting.process']
        for record in self:
            open_votes = vot_env.search([('state', '=', 'in_progress'), ('site_id', '=', record.site_id.id), ('id', '!=', record.id)])
            if open_votes:
                raise UserError(f'Ya existen votaciones en curso para el site {record.site_id.name}')
    
    @api.model
    def create(self, values):
        values['name'] = self.env['ir.sequence'].next_by_code('voting.process.seq')
        return super(VotingProcess, self).create(values)
    
    @api.depends('start_date')
    def _get_year_semester(self):
        for record in self:
            if record.start_date:
                start_date = record.start_date
                if start_date.month <= 6:
                    semester = 'first'
                else:
                    semester = 'second'
                
                record.year = start_date.year
                record.semester = semester
    
    def button_start(self):
        dt_now = fields.Datetime.now()
        if self.start_date < dt_now or dt_now > self.end_date:
            raise UserError('La votación no se puede iniciar fuera de los horarios estipulados.')
        
        if not self.voting_line_ids:
            raise UserError('Se debe indicar los candidatos para la presente votación')
        
        self.write({
            'state': 'in_progress'
        })
        
    def button_close(self):
        if self.state != 'in_progress':
            raise UserError('Solo se pueden finalizar votaciones que estén en estado En Progreso')
        
        dt_now = fields.Datetime.now()
        if dt_now < self.end_date: 
            raise UserError(f'La votación está programada a ser finalizada hasta las {self.end_date}. Aún no se puede cerrar.')
        
        voting_cnt = sum(x.voting_qty for x in self.voting_line_ids)
        if voting_cnt < 1:
            raise UserError(f'La votación no presentó Votos. Debe cancelarla y crear una nueva con una nueva programación')
        
        self.write({
            'state': 'done'
        })
    
    def button_cancel(self):
        if self.state not in ('draft', 'in_progress'):
            raise UserError('Solo se pueden cancelar votaciones en Borrador o En Progreso')
        
        self.write({
            'state': 'cancel'
        })


class VotingProcessCandidate(models.Model):
    _name = 'voting.process.candidate'
    _description = 'Candidatos por Proceso de Votación'
    
    def _get_voting_qty(self):
        for record in self:
            record.voting_qty = len(record.vote_ids)

    candidate_id = fields.Many2one('student.candidate', 'Candidato', copy=False, required=True)
    voting_id = fields.Many2one('voting.process', 'Proceso Votación', copy=False, required=True)
    voting_qty = fields.Integer('Cantidad Votos Candidato', readonly=True, compute='_get_voting_qty')
    vote_ids = fields.One2many('candidate.vote', 'voting_candidate_id')


class CandidateVote(models.Model):
    _name = 'candidate.vote'
    _description = 'Votos por cada candidato'

    voting_candidate_id = fields.Many2one('voting.process.candidate', 'Candidato Votación', readonly=True, copy=False, 
                                          required=True)
    student_id = fields.Many2one('res.partner', 'Votante', readonly=True, copy=False, required=True)
    
    _sql_constraints = [
        ('uniq_vote', 'UNIQUE (voting_candidate_id, student_id)', 
         'El voto solo puede ejecutarse una unica vez por cada estudiante en un proceso de votación.')
    ]
