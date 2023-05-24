from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    use_specific_accounts = fields.Boolean('Use Specific Accounts', default=False)
    show_spec_accounts = fields.Boolean(compute='compute_show_spec_accounts')
    spec_account_receivable_id = fields.Many2one('account.account',
        string="Specific Account Receivable",
        domain="[('company_id', '=', current_company_id)]")
    spec_account_payable_id = fields.Many2one('account.account',
        string="Specific Account Payable",
        domain="[('company_id', '=', current_company_id)]")
    display_account_receivable_id = fields.Many2one('account.account',
        string="Account Receivable",
        domain="[('company_id', '=', current_company_id)]",
        help="This account will be used instead of the default one as the receivable account for the current partner",
        required=True)
    display_account_payable_id = fields.Many2one('account.account',
        string="Account Payable",
        domain="[('company_id', '=', current_company_id)]",
        help="This account will be used instead of the default one as the payable account for the current partner",
        required=True)

    def action_create_spec_account(self):
        self.ensure_one()
        if self.spec_account_receivable_id and self.spec_account_payable_id:
            raise ValidationError(_("This partner already had the specific accounts!"))
        return {
            "name": "Specific Partner Accounts",
            "type": "ir.actions.act_window",
            "res_model": "partner.account.wizard",
            "view_mode": "form",
            "target": "new",
        }

    @api.depends('write_date', 'write_uid')
    def compute_show_spec_accounts(self):
        for rec in self:
            rec.show_spec_accounts = True if rec.spec_account_receivable_id and rec.spec_account_payable_id else False

    @api.onchange('display_account_payable_id', 'display_account_receivable_id', 'use_specific_accounts')
    def _onchange_display_accounts(self):
        if (self.display_account_payable_id or self.display_account_receivable_id) and not self.use_specific_accounts:
            self.property_account_payable_id = self.display_account_payable_id
            self.property_account_receivable_id = self.display_account_receivable_id
        elif self.use_specific_accounts:
            self.property_account_payable_id = self.spec_account_payable_id
            self.property_account_receivable_id = self.spec_account_receivable_id

    @api.onchange('spec_account_receivable_id', 'spec_account_payable_id')
    def _onchange_spec_accounts(self):
        if not self.spec_account_receivable_id and not self.spec_account_payable_id:
            self.use_specific_accounts = False
        elif self.spec_account_receivable_id and self.spec_account_payable_id and self.use_specific_accounts:
            self.property_account_payable_id = self.spec_account_payable_id
            self.property_account_receivable_id = self.spec_account_receivable_id

    @api.model
    def update_display_partner_accounts(self):
        for rec in self.env['res.partner'].sudo().search([]):
            rec.sudo().with_context(install_update=False).write({
                'display_account_payable_id': rec.property_account_payable_id,
                'display_account_receivable_id': rec.property_account_receivable_id})
