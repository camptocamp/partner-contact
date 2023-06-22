# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _get_contact_name(self, partner, name):
        if self.env.context.get("_two_lines_partner_address"):
            company_name = partner.commercial_company_name
            partner_name = partner.name
            if company_name and partner_name:
                # Only display two lines if both values are found,
                # otherwise revert to the standard behavior.
                return "{}\n {}".format(company_name, partner_name)
        return super()._get_contact_name(partner, name)
