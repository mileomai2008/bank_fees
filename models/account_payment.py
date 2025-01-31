# -*- coding: utf-8 -*-

from odoo import models, fields, _
from odoo.exceptions import ValidationError


class AccountPayment(models.Model):
    _inherit = "account.payment"

    fees = fields.Monetary("Bank Fees")
    fee_included = fields.Selection([
        ('included', 'Included Fees'),
        ('excluded', 'Excluded Fees')], 'Bank Fees')
    

    def _prepare_move_line_default_vals(self, write_off_line_vals=None):
        line_vals_list = super()._prepare_move_line_default_vals(write_off_line_vals)
        bank_fee_account_id = int(self.env['ir.config_parameter'].sudo().get_param('bank_fees.bank_fee_account_id')) or False
        if not bank_fee_account_id:
            raise ValidationError(_("Please add the bank fees account form the settings."))

        if self.payment_type == 'outbound' and self.fees:
            if self.fee_included == 'excluded':
                for line in line_vals_list:
                    if line['account_id'] == self.outstanding_account_id.id:
                        line['credit'] += self.fees
                        break

            elif self.fee_included == 'included':
                for line in line_vals_list:
                    if line['account_id'] == self.destination_account_id.id:
                        line['debit'] -= self.fees
                        break
            line_vals_list += [{
                    'name': _('Bank Fee'),
                    'date_maturity': self.date,
                    'partner_id': self.partner_id.id,
                    'debit': self.fees,
                    'credit': 0.0,
                    'account_id': bank_fee_account_id,
                }]

        return line_vals_list
