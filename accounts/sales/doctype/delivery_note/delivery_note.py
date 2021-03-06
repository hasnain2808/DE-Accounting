# -*- coding: utf-8 -*-
# Copyright (c) 2020, Moha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import nowdate, now


class DeliveryNote(Document):
    def on_submit(self):
        # stock_account = frappe.get_list(
        #     "Account",
        #     filters={"company_name": self.company, "account_name": "Stock in Hand"},
        # )
        # print(stock_account)
        # expense = frappe.get_list(
        #     "Account",
        #     filters={"company_name": self.company, "account_name": "Stock Expense"},
        # )
        # print(expense)
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
                "account": self.debit_account,
                "party_type": "Customer",
                "party": self.customer,
                "debit": self.total_amount,
                "credit": 0,
                "against": self.credit_account,
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
                "account": self.credit_account,
                "party_type": "Customer",
                "party": self.customer,
                "debit": 0,
                "credit": self.total_amount,
                "against": self.debit_account,
                "against_voucher": "Delivery Note",
                "voucher_number": self.name,
                "company": self.company,
                "fiscal_year": "2020-2021"
            }
        )
        gl_entry.insert()

    def on_cancel(self):
        frappe.db.sql("""update `tabGL Entry` set `is_cancelled` = 1,
            modified=%s, modified_by=%s
            where against_voucher=%s and voucher_number=%s and is_cancelled = 0""",
            (now(), frappe.session.user, "Delivery Note", self.name))

        gl_entry = frappe.get_doc(
            {
                "doctype": "GL Entry",
                "posting_date": self.posting_date,
                "transaction_date": self.posting_date,
                "account": self.credit_account,
                "party_type": "Customer",
                "party": self.customer,
                "debit": self.total_amount,
                "credit": 0,
                "against": self.debit_account,
                "against_voucher": "Delivery Note",
                "voucher_number": self.name,
                "company": self.company,
                "fiscal_year": "2020-2021",
                "is_cancelled" : 1
            }
        )
        gl_entry.insert()
        gl_entry = frappe.get_doc(
            {
                "doctype": "GL Entry",
                "posting_date": self.posting_date,
                "transaction_date": self.posting_date,
                "account": self.debit_account,
                "party_type": "Customer",
                "party": self.customer,
                "debit": 0,
                "credit": self.total_amount,
                "against": self.credit_account,
                "against_voucher": "Delivery Note",
                "voucher_number": self.name,
                "company": self.company,
                "fiscal_year": "2020-2021",
                "is_cancelled" : 1
            }
        )
        gl_entry.insert()

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
                },
            },
        },
        target_doc
    )
    return doc
