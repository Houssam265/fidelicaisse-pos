from odoo import models, fields, api
import random
import string


class LoyaltyMember(models.Model):
    _name = 'loyalty.member'
    _description = 'Membre du programme de fidélité'
    _rec_name = 'partner_id'

    partner_id = fields.Many2one('res.partner', string='Client', required=True)
    code_carte = fields.Char(string='Code carte', readonly=True, copy=False)
    solde_points = fields.Integer(
        string='Solde de points',
        compute='_compute_solde_points',
        store=True
    )
    date_inscription = fields.Date(string="Date d'inscription", default=fields.Date.today)
    niveau = fields.Selection([
        ('bronze', 'Bronze'),
        ('argent', 'Argent'),
        ('or', 'Or'),
    ], string='Niveau', default='bronze', compute='_compute_niveau', store=True)
    transaction_ids = fields.One2many('loyalty.transaction', 'member_id', string='Transactions')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('code_carte'):
                vals['code_carte'] = ''.join(
                    random.choices(string.ascii_uppercase + string.digits, k=8)
                )
        return super().create(vals_list)

    @api.depends('transaction_ids.points', 'transaction_ids.type')
    def _compute_solde_points(self):
        for rec in self:
            gagnes = sum(rec.transaction_ids.filtered(lambda t: t.type == 'gain').mapped('points'))
            utilises = sum(rec.transaction_ids.filtered(lambda t: t.type == 'utilisation').mapped('points'))
            rec.solde_points = gagnes - utilises

    @api.depends('solde_points')
    def _compute_niveau(self):
        for rec in self:
            if rec.solde_points >= 500:
                rec.niveau = 'or'
            elif rec.solde_points >= 200:
                rec.niveau = 'argent'
            else:
                rec.niveau = 'bronze'