from odoo import models, fields, api


class AccountAccount(models.Model):
    _inherit = "account.account"

    spec_partner_payable = fields.Many2one('res.partner', string='Specific Payable Partner')
    spec_partner_receivable = fields.Many2one('res.partner', string='Specific Receivable Partner')

    @api.model
    def create(self, vals):
        if not vals.get('code') and self._context.get('create_spec_account', False):
            vals['code'] = self.env['ir.sequence'].next_by_code('spec.account.receivable')
        return super().create(vals)

