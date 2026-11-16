from odoo import api, models

from .whatsapp_membership import (
    filter_partner_commands,
    internal_partner_ids,
    is_whatsapp_values,
)


class DiscussChannel(models.Model):
    _inherit = "discuss.channel"

    @api.model_create_multi
    def create(self, vals_list):
        if not any(
            is_whatsapp_values(values) and "channel_partner_ids" in values
            for values in vals_list
        ):
            return super().create(vals_list)
        blocked_partner_ids = internal_partner_ids(self.env)
        filtered = []
        for values in vals_list:
            if is_whatsapp_values(values) and "channel_partner_ids" in values:
                values = {
                    **values,
                    "channel_partner_ids": filter_partner_commands(
                        values["channel_partner_ids"], blocked_partner_ids
                    ),
                }
            filtered.append(values)
        return super().create(filtered)

    def write(self, vals):
        if "channel_partner_ids" not in vals:
            return super().write(vals)
        whatsapp_channels = self.filtered(
            lambda channel: channel.channel_type == "whatsapp"
        )
        if not whatsapp_channels:
            return super().write(vals)
        other_channels = self - whatsapp_channels
        if other_channels:
            super(DiscussChannel, other_channels).write(vals)
        blocked_partner_ids = internal_partner_ids(self.env)
        whatsapp_vals = {
            **vals,
            "channel_partner_ids": filter_partner_commands(
                vals["channel_partner_ids"], blocked_partner_ids
            ),
        }
        return super(DiscussChannel, whatsapp_channels).write(whatsapp_vals)
