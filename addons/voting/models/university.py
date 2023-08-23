#-*- coding: utf-8 -*-

from odoo import models, fields


class UniversitySite(models.Model):
    _name = 'university.site'
    _description = 'Sites y/o Campus de la Universidad'

    name = fields.Char('Nombre Sede', related='country_id.name')
    address = fields.Char('Dirección Sede', required=True, copy=False)
    contact_number = fields.Integer('Telefono de Contacto', copy=False)
    country_id = fields.Many2one('res.country', 'País', ondelete='restrict')


class UniversityDean(models.Model):
    _name = 'university.dean'
    _description = 'Decanaturas Universidades'

    name = fields.Char('Nombre Decanatura', required=True, copy=False)
    lead_partner_id = fields.Many2one('res.partner', 'Decano', required=True, copy=False, domain=[('is_professor','=', True)])
    career_ids = fields.One2many('university.career', 'dean_id', readonly=True, copy=False)


class UniversityCareer(models.Model):
    _name = 'university.career'
    _description = 'Carreras Universitarias'

    name = fields.Char('Nombre Carrera', required=True, copy=False)
    career_type = fields.Selection([('tecnico', 'Tecnico'), 
                                     ('tecnologo', 'Tecnologo'),
                                     ('pregrado', 'Pregrado'),
                                     ('continuada', 'Educación Continuada'),
                                     ('especializacion', 'Especializacion'),
                                     ('posgrado', 'Posgrado'),
                                     ('maestria', 'Maestría')], 'Tipo Carrera', default='pregrado', required=True)
    is_virtual = fields.Boolean('Es Virtual')
    sites_ids = fields.Many2many('university.site', string='Sites en las que se da la carrera', required=True)
    dean_id = fields.Many2one('university.dean', 'Decanatura de Carrera', required=True)
