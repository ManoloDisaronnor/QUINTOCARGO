# -*- coding: utf-8 -*-
# from odoo import http


# class QuintoCargo(http.Controller):
#     @http.route('/quinto_cargo/quinto_cargo/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/quinto_cargo/quinto_cargo/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('quinto_cargo.listing', {
#             'root': '/quinto_cargo/quinto_cargo',
#             'objects': http.request.env['quinto_cargo.quinto_cargo'].search([]),
#         })

#     @http.route('/quinto_cargo/quinto_cargo/objects/<model("quinto_cargo.quinto_cargo"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('quinto_cargo.object', {
#             'object': obj
#         })
