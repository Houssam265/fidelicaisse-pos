from odoo import models, fields, api


class LoyaltyTransaction(models.Model):
    _name = 'loyalty.transaction'
    _description = 'Transaction de points de fidélité'
    _order = 'date desc'

    member_id = fields.Many2one('loyalty.member', string='Membre', required=True, ondelete='cascade')
    pos_order_id = fields.Many2one('pos.order', string='Commande POS')
    type = fields.Selection([
        ('gain', 'Gain'),
        ('utilisation', 'Utilisation'),
    ], string='Type', required=True, default='gain')
    points = fields.Integer(string='Points', required=True)
    date = fields.Datetime(string='Date', default=fields.Datetime.now)