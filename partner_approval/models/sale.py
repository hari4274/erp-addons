# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        for order in self:
            if order.partner_id.need_approval:
                # Customer Approval Validation
                raise ValidationError('You are not allowed to use this Customer, need validation !!!')
        return super(SaleOrder, self).action_confirm()

    def action_quotation_send(self):
        self.ensure_one()
        if self.partner_id.need_approval:
            raise ValidationError('You are not allowed to use this Customer, need validation !!!')
        return super(SaleOrder, self).action_quotation_send()
