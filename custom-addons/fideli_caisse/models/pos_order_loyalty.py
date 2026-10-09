from odoo import models, fields, api


class PosOrder(models.Model):
    _inherit = 'pos.order'

    loyalty_points_traites = fields.Boolean(default=False, copy=False)

    def write(self, vals):
        result = super().write(vals)
        if vals.get('state') in ('paid', 'done', 'invoiced'):
            for order in self:
                if not order.loyalty_points_traites and order.partner_id:
                    order._attribuer_points_fidelite()
        return result

    def _attribuer_points_fidelite(self):
        self.ensure_one()
        member = self.env['loyalty.member'].search(
            [('partner_id', '=', self.partner_id.id)], limit=1
        )
        if not member:
            return

        points = int(self.amount_total // 10)  # 1 point par 10 MAD dépensés
        if points <= 0:
            return

        self.env['loyalty.transaction'].create({
            'member_id': member.id,
            'pos_order_id': self.id,
            'type': 'gain',
            'points': points,
        })
        self.loyalty_points_traites = True