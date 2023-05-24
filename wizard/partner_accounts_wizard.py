from odoo import models, fields


class PartnerAccountWizard(models.TransientModel):
    _name = "partner.account.wizard"
    _description = "Specific Partner Accounts Wizard"

    spec_account_receivable_id = fields.Many2one('account.account', company_dependent=True,
                                                 string="Specific Account Receivable",
                                                 domain="[('internal_type', '=', 'receivable'), ('deprecated', '=', False), ('company_id', '=', current_company_id)]")
    spec_account_payable_id = fields.Many2one('account.account', company_dependent=True,
                                              string="Specific Account Payable",
                                              domain="[('internal_type', '=', 'payable'), ('deprecated', '=', False), ('company_id', '=', current_company_id)]")

    def action_confirm(self):
        active_id = self._context.get('active_id', False)
        if not active_id or not (self.spec_account_receivable_id and self.spec_account_payable_id):
            return
        partner = self.env['res.partner'].browse(active_id).sudo()
        partner.write({'spec_account_receivable_id': self.spec_account_receivable_id.id,
                       'spec_account_payable_id': self.spec_account_payable_id.id,
                       'property_account_payable_id': self.spec_account_payable_id.id,
                       'property_account_receivable_id': self.spec_account_receivable_id.id,
                       'use_specific_accounts': True})
        return True

