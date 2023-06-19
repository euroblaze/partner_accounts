from odoo import models, fields, api


class AccountAccount(models.Model):
    _inherit = "account.account"

    spec_partner_payable = fields.Many2one('res.partner', string='Specific Payable Partner')
    spec_partner_receivable = fields.Many2one('res.partner', string='Specific Receivable Partner')
