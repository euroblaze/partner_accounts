from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    use_specific_accounts = fields.Boolean('Use Specific Accounts', default=False)
    show_spec_accounts = fields.Boolean(compute='compute_show_spec_accounts')
    spec_account_receivable_id = fields.Many2one('account.account',
        string="Specific Account Receivable",
        domain="[('internal_type', '=', 'receivable'), ('deprecated', '=', False), ('company_id', '=', current_company_id)]")
    spec_account_payable_id = fields.Many2one('account.account',
        string="Specific Account Payable",
        domain="[('internal_type', '=', 'payable'), ('deprecated', '=', False), ('company_id', '=', current_company_id)]")
    display_account_receivable_id = fields.Many2one('account.account',
        string="Account Receivable",
        domain="[('internal_type', '=', 'receivable'), ('deprecated', '=', False), ('company_id', '=', current_company_id)]",
        help="This account will be used instead of the default one as the receivable account for the current partner",
        required=True)
    display_account_payable_id = fields.Many2one('account.account',
        string="Account Payable",
        domain="[('internal_type', '=', 'payable'), ('deprecated', '=', False), ('company_id', '=', current_company_id)]",
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

    def write(self, vals):
        res = super().write(vals)
        account_fields = ['use_specific_accounts',
                          'spec_account_receivable_id',
                          'spec_account_payable_id',
                          'display_account_payable_id',
                          'display_account_receivable_id']
        if any(field in vals for field in account_fields):
            for rec in self:
                if rec.use_specific_accounts and rec.spec_account_receivable_id and rec.spec_account_payable_id:
                    rec.property_account_payable_id = rec.spec_account_payable_id
                    rec.property_account_receivable_id = rec.spec_account_receivable_id
                else:
                    rec.property_account_payable_id = rec.display_account_payable_id
                    rec.property_account_receivable_id = rec.display_account_receivable_id
        return res
