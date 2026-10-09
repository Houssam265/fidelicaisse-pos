from odoo import http
from odoo.http import request


class FideliCaisseController(http.Controller):

    @http.route('/fidelicaisse/solde/<string:code_carte>',
                type='jsonrpc', auth='public', csrf=False)
    def get_solde_points(self, code_carte):
        member = request.env['loyalty.member'].sudo().search(
            [('code_carte', '=', code_carte)], limit=1
        )
        if not member:
            return {'error': 'Carte introuvable'}
        return {
            'nom': member.partner_id.name,
            'solde_points': member.solde_points,
            'niveau': member.niveau,
        }

    @http.route('/fidelicaisse/carte', type='http', auth='public',
                methods=['GET'], csrf=False)
    def page_carte(self, code=None, **kwargs):
        code = (code or '').strip().upper()
        member = None
        erreur = None
        if code:
            member = request.env['loyalty.member'].sudo().search(
                [('code_carte', '=', code)], limit=1
            )
            if not member:
                erreur = "Carte introuvable. Vérifiez le code saisi."
        return request.render('fideli_caisse.page_carte', {
            'code': code,
            'member': member,
            'erreur': erreur,
        })