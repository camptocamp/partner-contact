# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models
from odoo.exceptions import ValidationError


class Contact(models.Model):
    _inherit = "res.partner"

    @api.constrains("customer_rank", "supplier_rank")
    def _constrains_single_rank(self):
        for record in self:
            if record.customer_rank > 0 and record.supplier_rank > 0:
                raise ValidationError(
                    self.env._("A contact cannot be both a customer and a supplier.")
                )

    def _increase_rank(self, field, n=1):
        # OVERRIDE: to check single rank before increasing
        # Because of direct SQL update in the super method,
        # the ``res.partner::_constrains_single_rank`` method is not enough.
        # It's not called when the invoice is posted outside UI directly in code.
        # So, we need to check the single rank before increasing it.
        if self.ids and field in ["customer_rank", "supplier_rank"]:
            for record in self:
                crank_incr_allowed = (
                    field == "customer_rank" and record.supplier_rank == 0
                )
                srank_incr_allowed = (
                    field == "supplier_rank" and record.customer_rank == 0
                )
                if not (crank_incr_allowed or srank_incr_allowed):
                    raise ValidationError(
                        self.env._(
                            "Cannot increase %s for partner %s as it already "
                            "has a non-zero %s."
                        )
                        % (
                            field,
                            record.display_name,
                            "supplier_rank"
                            if field == "customer_rank"
                            else "customer_rank",
                        )
                    )
        return super()._increase_rank(field, n=n)
