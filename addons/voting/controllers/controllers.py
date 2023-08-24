# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class WebsiteForm(http.Controller):
    @http.route(['/voting'], type='http', auth="user", website=True)
    def voting(self):
        logged_partner = request.env.user.partner_id
        logged_usr_site = logged_partner.site_id
        
        open_voting_session = request.env['voting.process'].sudo().search([('state', '=', 'in_progress'),
                                                                            ('site_id', '=', logged_usr_site.id)])
        if open_voting_session:
            open_voting_session = open_voting_session
            candidates = open_voting_session.voting_line_ids.mapped('candidate_id')
            values = {
                'ok': True,
                'open_voting_session': open_voting_session,
                'candidates': candidates,
                'logged_partner': logged_partner
            }
        elif not open_voting_session or len(open_voting_session) > 1:
            values = {
                'ok': False,
                'open_voting_sessions': False,
                'candidates': False,
                'students': False
            }
        
        return request.render("voting.voting_template", values)
    
    @http.route(['/voting/submit'], type='http', auth="user", website=True)
    def voting_submit(self, **kwargs):
        vote_env = request.env['candidate.vote'].sudo()
        
        cantidate_id = kwargs.get('candidate_id')
        voting_id = kwargs.get('voting_id')
        partner_vote_id = kwargs.get('partner_vote_id')
        
        partner = request.env['res.partner'].sudo().browse(partner_vote_id)
        vote_line = request.env['voting.process.candidate'].sudo().search([('candidate_id', '=', int(cantidate_id)),
                                                                           ('voting_id', '=', int(voting_id))])
        
        vote_env.create({
            'voting_candidate_id': vote_line.id,
            'student_id': partner.id
        })
        return request.render("voting.voting_done_template")