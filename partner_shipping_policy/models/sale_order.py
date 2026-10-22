# Copyright 2024 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # Convert field to a computed
    picking_policy = fields.Selection(
        compute="_compute_picking_policy", store=True, readonly=False, precompute=True
    )

    @api.model
    def default_get(self, fields):
        # A default (field default or Settings) ends up in the create values
        # and would prevent the compute from applying the partner's policy.
        # Only a default explicitly given in the context is kept.
        res = super().default_get(fields)
        if "default_picking_policy" not in self.env.context:
            res.pop("picking_policy", None)
        return res

    @api.model
    def _get_default_picking_policy(self):
        # Return the default shipping policy (Settings, else field default).
        # Calls the parent ``default_get`` to bypass the override above, which
        # hides that default.
        return super().default_get(["picking_policy"]).get("picking_policy")

    @api.depends("partner_shipping_id", "partner_id")
    def _compute_picking_policy(self):
        default_policy = self._get_default_picking_policy()
        for order in self:
            order.picking_policy = (
                order.partner_shipping_id.picking_policy
                or order.partner_id.picking_policy
                or default_policy
            )
