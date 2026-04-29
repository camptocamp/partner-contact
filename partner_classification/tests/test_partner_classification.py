# Copyright 2026 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo.tests.common import TransactionCase


class TestPartnerClassification(TransactionCase):
    def setUp(self):
        super().setUp()
        self.Classification = self.env["res.partner.classification"]
        self.Partner = self.env["res.partner"]

        self.class_a = self.Classification.create(
            {
                "name": "Specialist Retailer",
            }
        )

    def test_classification_assignment(self):
        partner = self.Partner.create(
            {
                "name": "Test Company",
                "classification_id": self.class_a.id,
            }
        )

        self.assertEqual(partner.classification_id, self.class_a)

    def test_commercial_field_propagation(self):
        company = self.Partner.create(
            {
                "name": "Parent Company",
                "classification_id": self.class_a.id,
                "is_company": True,
            }
        )

        contact = self.Partner.create(
            {
                "name": "Child Contact",
                "parent_id": company.id,
            }
        )

        self.assertEqual(
            contact.classification_id,
            self.class_a,
            "Classification should propagate to child contacts",
        )

    def test_change_propagation(self):
        company = self.Partner.create(
            {
                "name": "Company",
                "is_company": True,
            }
        )

        contact = self.Partner.create(
            {
                "name": "Contact",
                "parent_id": company.id,
            }
        )

        company.classification_id = self.class_a

        self.assertEqual(
            contact.classification_id,
            self.class_a,
            "Updating parent should propagate classification",
        )

    def test_multi_company_isolation(self):
        company_2 = self.env["res.company"].create(
            {
                "name": "Second Company",
            }
        )

        classification = self.Classification.with_company(company_2).create(
            {
                "name": "Export",
                "company_id": company_2.id,
            }
        )

        self.assertEqual(classification.company_id, company_2)
