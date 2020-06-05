# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
from odoo.addons.http_routing.models.ir_http import slug, unslug
from odoo.http import Controller, request, route, content_disposition

_logger = logging.getLogger(__name__)


class ExportAttachmentController(Controller):

    @route('/download_attachments/<model("export.attachments"):export_id>', type='http', auth='user')
    def download_attachments_control(self, export_id, **kwargs):
        record_ids = eval(kwargs.get('record_ids', '[]'))
        try:
            filename, t_zip = export_id._get_data_file(record_ids)
        except Exception as e:
            return "No Attachments found"
        headers = [
            ('Content-Type', 'application/octet-stream; charset=binary'),
            ('Content-Disposition', content_disposition('%s.zip' % filename))
            ]
        _logger.info('Download Attachments zip: %s', filename)
        return request.make_response(t_zip, headers=headers)
