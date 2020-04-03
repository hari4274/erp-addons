# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64
import tempfile
import zipfile
from odoo import api, models, fields
from odoo.addons.http_routing.models.ir_http import slug, unslug
from odoo.exceptions import ValidationError


class ExportAttachments(models.Model):
	_name = 'export.attachments'
	_description = 'Export Attachments Action'
	_rec_name = 'model_id'

	model_id = fields.Many2one('ir.model', string='Model')
	server_action_id = fields.Many2one('ir.actions.server', string='Server Action')
	bind_model_id = fields.Many2one(related='server_action_id.binding_model_id', string='Binding Model')
	active = fields.Boolean('Active', default=True)

	def get_server_action_data(self):
		model_id = self.model_id
		if not model_id:
			raise ValidationError('Please Fill Model !!!')
		return {
			'name': 'Export Attachments',
			'model_id': model_id.id,
			'binding_model_id': model_id.id,
			'state': 'code',
			'code': """
				if records:
					action = env['export.attachments'].with_context({'record_ids': records.ids}).browse(%s).download_attachments()
			""" % (self.id)
		}

	def create_server_action(self):
		if self.server_action_id:
			raise ValidationError('Already Server Action Created !!!')
		self.server_action_id = self.env['ir.actions.server'].create(self.get_server_action_data())
	
	def update_server_action(self):
		if not self.server_action_id:
			raise ValidationError('Please Create Server action, and try again !!!')
		self.server_action_id.write(self.get_server_action_data())

	def create_action(self):
		if not self.server_action_id:
			raise ValidationError('Please Create Server action, and try again !!!')
		self.server_action_id.create_action()

	def unlink_action(self):
		if self.server_action_id:
			self.server_action_id.unlink_action()

	def download_attachments(self):
		attach_ids = []
		base_url = self.env['ir.config_parameter'].get_param('web.base.url')
		context = self.env.context
		return {
			'name': ("Download Attachments"),
			'type': 'ir.actions.act_url',
			'url': '%s/download_attachments/%s?record_ids=%s' % (
				base_url,
				slug(self),
				context.get('record_ids'),
			),
			'target': 'new',
		}
	
	def _get_data_file(self, record_ids):
		filename = 'Download-attachments'
		t_zip = tempfile.TemporaryFile()
		records = self.env[self.model_id.model].browse(record_ids)
		print(records)
		with zipfile.ZipFile(t_zip, 'a', compression=zipfile.ZIP_DEFLATED, allowZip64=True) as zipf:
			for file_name, data in [(attach.datas_fname, attach.datas) for attach in attach_ids]:
				zipf.writestr(file_name, base64.b64decode(data))
		t_zip.seek(0)
		return filename, t_zip
