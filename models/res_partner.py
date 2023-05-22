from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    use_specific_accounts = fields.Boolean('Use Specific Accounts', default=False)
    spec_account_receivable_id = fields.Many2one('account.account', company_dependent=True,
        string="Specific Account Receivable",
        domain="[('internal_type', '=', 'receivable'), ('deprecated', '=', False), ('company_id', '=', current_company_id)]")
    spec_account_payable_id = fields.Many2one('account.account', company_dependent=True,
        string="Specific Account Payable",
        domain="[('internal_type', '=', 'payable'), ('deprecated', '=', False), ('company_id', '=', current_company_id)]")
    display_account_receivable_id = fields.Many2one('account.account', company_dependent=True,
        string="Account Receivable",
        domain="[('internal_type', '=', 'receivable'), ('deprecated', '=', False), ('company_id', '=', current_company_id)]",
        help="This account will be used instead of the default one as the receivable account for the current partner",
        required=True)
    display_account_payable_id = fields.Many2one('account.account', company_dependent=True,
        string="Account Payable",
        domain="[('internal_type', '=', 'payable'), ('deprecated', '=', False), ('company_id', '=', current_company_id)]",
        help="This account will be used instead of the default one as the payable account for the current partner",
        required=True)

    def action_create_spec_account(self):
        return {
            "name": "Specific Partner Accounts",
            "type": "ir.actions.act_window",
            "res_model": "partner.account.wizard",
            "view_mode": "form",
            "target": "new",
        }
