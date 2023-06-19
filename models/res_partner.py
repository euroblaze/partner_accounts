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

    @api.depends('spec_account_receivable_id', 'spec_account_payable_id')
    def compute_show_spec_accounts(self):
        for rec in self:
            rec.show_spec_accounts = True if (rec.spec_account_receivable_id or rec.spec_account_payable_id) else False

    @api.onchange('use_specific_accounts')
    def _onchange_display_accounts(self):
        if not self.use_specific_accounts:
            self.property_account_payable_id = self.display_account_payable_id
            self.property_account_receivable_id = self.display_account_receivable_id
        else:
            self.property_account_payable_id = self.spec_account_payable_id if self.spec_account_payable_id else self.display_account_payable_id
            self.property_account_receivable_id = self.spec_account_receivable_id if self.spec_account_receivable_id else self.display_account_receivable_id

    @api.model
    def update_display_partner_accounts(self):
        for rec in self.env['res.partner'].sudo().search([]):
            rec.sudo().write({
                'display_account_payable_id': rec.property_account_payable_id,
                'display_account_receivable_id': rec.property_account_receivable_id
            })

    def create_spec_account_receivable(self):
        self.ensure_one()
        if self.env['account.account'].sudo().search([('spec_partner_receivable', '=', self.id)]):
            raise ValidationError(_("This partner already had the specific receivable account!"))
        user_type_id = self.property_account_receivable_id.user_type_id.id if self.property_account_receivable_id \
            else self.env['account.account.type'].sudo().search([('type', '=', 'receivable')], limit=1).id
        new_receivable_acc = self.env['account.account'].sudo().with_context(create_spec_account=True).create({
            'name': self.name,
            'code': self.env['ir.sequence'].next_by_code('seq_spec_receivable_partner_account'),
            'internal_type': 'receivable',
            'deprecated': False,
            'reconcile': True,
            'spec_partner_receivable': self.id,
            'user_type_id': user_type_id,
        })
        self.sudo().write({
            'spec_account_receivable_id': new_receivable_acc.id,
            'property_account_receivable_id': new_receivable_acc.id,
            'use_specific_accounts': True
        })
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'message': 'Specific receivable account created successfully!',
                'type': 'success',
                'sticky': False,
                'next': {'type': 'ir.actions.client', 'tag': 'reload'},
            }
        }

    def create_spec_account_payable(self):
        self.ensure_one()
        if self.env['account.account'].sudo().search([('spec_partner_payable', '=', self.id)]):
            raise ValidationError(_("This partner already had the specific payable account!"))
        user_type_id = self.property_account_payable_id.user_type_id.id if self.property_account_payable_id \
            else self.env['account.account.type'].sudo().search([('type', '=', 'payable')], limit=1).id
        new_payable_acc = self.env['account.account'].sudo().with_context(create_spec_account=True).create({
            'name': self.name,
            'code': self.env['ir.sequence'].next_by_code('seq_spec_payable_partner_account'),
            'internal_type': 'payable',
            'reconcile': True,
            'deprecated': False,
            'spec_partner_payable': self.id,
            'user_type_id': user_type_id,
        })
        self.sudo().write({
            'spec_account_payable_id': new_payable_acc.id,
            'property_account_payable_id': new_payable_acc.id,
            'use_specific_accounts': True
        })
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'message': 'Specific payable account created successfully!',
                'type': 'success',
                'sticky': False,
                'next': {'type': 'ir.actions.client', 'tag': 'reload'},
            }
        }
