from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    bank_fee_account_id = fields.Many2one('account.account', 'Bank Fee Account',
                                          config_parameter="bank_fees.bank_fee_account_id")
