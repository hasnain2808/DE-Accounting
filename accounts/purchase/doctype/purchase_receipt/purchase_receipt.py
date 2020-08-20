# -*- coding: utf-8 -*-
# Copyright (c) 2020, Moha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc


class PurchaseReceipt(Document):
    def on_update(self):
        stock_account = frappe.get_list(
            "Account",
            filters={"company_name": self.company, "account_name": "Stock in Hand"},
        )
        print(stock_account)
        rec_not_billed = frappe.get_list(
            "Account",
            filters={
                "company_name": self.company,
                "account_name": "Asset Received But not Billed",
            },
        )
        print(rec_not_billed)

        JEl1 = {
            "credit": 0,
            "debit": self.total_amount,
            "account": stock_account[0].name,
        }
        JEl2 = {
            "debit": 0,
            "credit": self.total_amount,
            "account": rec_not_billed[0].name,
            "party_type": "Supplier",
            "party_name": self.supplier,
        }
        JE = frappe.get_doc(
            {
                "doctype": "Journal Entry",
                "company": self.company,
                "entry_date": self.posting_date,
                "entry_lines": [JEl1, JEl2]
                # "reference_number": ,
                # "reference_date": ,
            }
        )
        JE.insert()


def set_missing_values(source, target):
    target.run_method("set_missing_values")
    # target.run_method("calculate_taxes_and_totals")


@frappe.whitelist()
def make_purchase_invoice(source_name, target_doc=None):
    doc = get_mapped_doc(
        "Purchase Receipt",
        source_name,
        {
            "Purchase Receipt": {
                "doctype": "Purchase Invoice",
                "field_map": {},
                "validation": {},
            },
            "Purchase Receipt Items": {
                "doctype": "Purchase Invoice Item",
                "field_map": {
                    "name": "purchase_invoice_item",
                    "parent": "purchase_invoice",
                    # "bom": "bom",
                    # "material_request": "material_request",
                    # "material_request_item": "material_request_item"
                },
            },
            # "Purchase Taxes and Charges": {
            # 	"doctype": "Purchase Taxes and Charges",
            # 	"add_if_empty": True
            # }
        },
        target_doc,
        set_missing_values,
    )
    return doc
