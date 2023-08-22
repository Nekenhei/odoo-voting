# -*- coding: utf-8 -*-
# from odoo import http


# class Voting(http.Controller):
#     @http.route('/voting/voting', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/voting/voting/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('voting.listing', {
#             'root': '/voting/voting',
#             'objects': http.request.env['voting.voting'].search([]),
#         })

#     @http.route('/voting/voting/objects/<model("voting.voting"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('voting.object', {
#             'object': obj
#         })
