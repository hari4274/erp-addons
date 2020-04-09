# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields
from odoo.exceptions import ValidationError


class Partner(models.Model):
	_inherit = 'res.partner'

	need_approval = fields.Boolean('Need Approval')

	def action_validate(self):
		if self.env.user.has_group('base.group_no_one'):
			self.write({'need_approval': False, 'active': True})
		else:
			raise ValidationError('You are not allowed To validate partner !!! Contact Administrator.')
