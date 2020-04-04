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
	export_field_line = fields.One2many('export.field.line', 'export_id', string='Field Lines')
	is_attachment = fields.Boolean("Download Related Documents from Attachments", default=True, help='Download related documents from attachments')

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
		model = self.model_id
		filename = model.model.replace('.', '_') + '-Data'
		t_zip = tempfile.TemporaryFile()
		with zipfile.ZipFile(t_zip, 'a', compression=zipfile.ZIP_DEFLATED, allowZip64=True) as zipf:
			if self.is_attachment:
				records = self.env['ir.attachment'].search([('res_model', '=', model.model), ('res_id', 'in', record_ids)])
				if records:
					for file_name, datas in [('[{0}-{1}]{2}'.format(attach.res_model.replace('.', '_'), attach.res_id, attach.name), attach.datas) for attach in records]:
						zipf.writestr(file_name, base64.b64decode(datas))
			elif self.export_field_line:
				records = self.env[model.model].browse(record_ids)
				if records:
					data_list = []
					field_data = {line.bname_field_id.name: line.binary_field_id.name for line in self.export_field_line}
					for record in records:
						for fname_field, datas_field in field_data.items():
							file_name = '[{0}-{1}-{2}]{3}'.format(model.model.replace('.', '_'), record.id, datas_field, getattr(record, fname_field))
							datas = getattr(record, datas_field)
							zipf.writestr(file_name, base64.b64decode(datas))
		t_zip.seek(0)
		return filename, t_zip


class ExportFieldLine(models.Model):
	_name = 'export.field.line'
	_description = 'Export Field Lines'
	_rec_name = 'export_id'

	export_id = fields.Many2one('export.attachments', string='Export Attachment')
	binary_field_id = fields.Many2one('ir.model.fields', string='Binary Data Field')
	bname_field_id = fields.Many2one('ir.model.fields', string='Binary Filename Field')
