from odoo import api, models

from .whatsapp_membership import filter_member_values, internal_partner_ids


class DiscussChannelMember(models.Model):
    _inherit = "discuss.channel.member"

    @api.model_create_multi
    def create(self, vals_list):
        channel_ids = sorted(
            {values.get("channel_id") for values in vals_list if values.get("channel_id")}
        )
        if not channel_ids:
            return super().create(vals_list)
        channels = self.env["discuss.channel"].sudo().browse(channel_ids)
        whatsapp_channel_ids = set(
            channels.filtered(lambda channel: channel.channel_type == "whatsapp").ids
        )
        if not whatsapp_channel_ids:
            return super().create(vals_list)
        return super().create(
            filter_member_values(
                vals_list,
                whatsapp_channel_ids,
                internal_partner_ids(self.env),
            )
        )
