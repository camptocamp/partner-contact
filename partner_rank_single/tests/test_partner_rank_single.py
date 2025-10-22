# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import Command, fields
from odoo.exceptions import ValidationError
from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestPartnerRankSingle(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Partner = cls.env["res.partner"]
        cls.customer = cls.Partner.create(
            {
                "name": "Customer",
                "is_company": True,
            }
        )
        cls.supplier = cls.Partner.create(
            {
                "name": "Supplier",
                "is_company": True,
            }
        )

    @classmethod
    def _create_invoice(cls, move_type, date, partner_id, **kwargs):
        move = cls.env["account.move"].create(
            {
                "invoice_date": date,
                "partner_id": partner_id.id,
                **kwargs,
                "move_type": move_type,
                "date": date,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "product_id": cls.product_a.id,
                            "price_unit": 120.0,
                            "tax_ids": [],
                            **line_kwargs,
                        }
                    )
                    for line_kwargs in kwargs.get("invoice_line_ids", [{}])
                ],
            }
        )
        return move.action_post()

    def test_00_customer_rank_single(self):
        self._create_invoice(
            move_type="out_invoice", date=fields.Date.today(), partner_id=self.customer
        )
        with self.assertRaises(
            ValidationError, msg="A contact cannot be both a customer and a supplier."
        ):
            self._create_invoice(
                move_type="in_invoice",
                date=fields.Date.today(),
                partner_id=self.customer,
            )

    def test_01_supplier_rank_single(self):
        self._create_invoice(
            move_type="in_invoice", date=fields.Date.today(), partner_id=self.supplier
        )
        with self.assertRaises(
            ValidationError, msg="A contact cannot be both a customer and a supplier."
        ):
            self._create_invoice(
                move_type="out_invoice",
                date=fields.Date.today(),
                partner_id=self.supplier,
            )
