# -*- coding: utf-8 -*-
# Copyright (c) 2020, Moha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc


class DeliveryNote(Document):
    def on_submit(self):
        stock_account = frappe.get_list(
            "Account",
            filters={"company_name": self.company, "account_name": "Stock in Hand"},
        )
        print(stock_account)
        expense = frappe.get_list(
            "Account",
            filters={"company_name": self.company, "account_name": "Stock Expense"},
        )
        print(expense)
        # JEl1 = {
        #     "credit": self.total_amount,
        #     "debit": 0,
        #     "account": stock_account[0].name,
        #     "party_type": "Customer",
        #     "party_name": self.customer,
        # }
        # JEl2 = {
        #     "credit": 0,
        #     "debit": self.total_amount,
        #     "account": expense[0].name,
        # }
        # JE = frappe.get_doc(
        #     {
        #         "doctype": "Journal Entry",
        #         "company": self.company,
        #         "entry_date": self.posting_date,
        #         "entry_lines": [JEl1, JEl2]
        #         # "reference_number": ,
        #         # "reference_date": ,
        #     }
        # )
        # JE.insert()

        gl_entry = frappe.get_doc(
            {
                "doctype": "GL Entry",
                "posting_date": self.posting_date,
                "transaction_date": self.posting_date,
                "account": expense[0].name,
                "party_type": "Customer",
                "party": self.customer,
                "debit": self.total_amount,
                "credit": 0,
                "against": stock_account[0].name,
                "against_voucher": "Delivery Note",
                "voucher_number": self.name,
                "company": self.company,
                "fiscal_year": "2020-2021"
            }
        )
        gl_entry.insert()
        gl_entry = frappe.get_doc(
            {
                "doctype": "GL Entry",
                "posting_date": self.posting_date,
                "transaction_date": self.posting_date,
                "account": stock_account[0].name,
                "party_type": "Customer",
                "party": self.customer,
                "debit": 0,
                "credit": self.total_amount,
                "against": expense[0].name,
                "against_voucher": "Delivery Note",
                "voucher_number": self.name,
                "company": self.company,
                "fiscal_year": "2020-2021"
            }
        )
        gl_entry.insert()


def set_missing_values(source, target):
    # if len(target.get("items")) == 0:
    # 	frappe.throw(_("All items have already been Invoiced/Returned"))

    doc = frappe.get_doc(target)
    doc.ignore_pricing_rule = 1
    doc.run_method("onload")
    doc.run_method("set_missing_values")


@frappe.whitelist()
def make_sales_invoice(source_name, target_doc=None):

    doc = get_mapped_doc(
        "Delivery Note",
        source_name,
        {
            "Delivery Note": {
                "doctype": "Sales Invoice",
                "field_map": {},
                "validation": {},
            },
            "Delivery Note Item": {
                "doctype": "Sales Invoice Item",
                "field_map": {
                    "name": "sales_invoice_item",
                    "parent": "sales_invoice",
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


def set_missing_values(source, target):
    target.run_method("set_missing_values")
    # target.run_method("calculate_taxes_and_totals")
