# -*- coding: utf-8 -*-
# Copyright (c) 2020, Moha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import nowdate, now


class PurchaseReceipt(Document):
    def on_submit(self):
        # stock_account = frappe.get_list(
        #     "Account",
        #     filters={"company_name": self.company, "account_name": "Stock in Hand"},
        # )
        # print(stock_account)
        # rec_not_billed = frappe.get_list(
        #     "Account",
        #     filters={
        #         "company_name": self.company,
        #         "account_name": "Asset Received But not Billed",
        #     },
        # )
        # print(rec_not_billed)

        # JEl1 = {
        #     "credit": 0,
        #     "debit": self.total_amount,
        #     "account": stock_account[0].name,
        # }
        # JEl2 = {
        #     "debit": 0,
        #     "credit": self.total_amount,
        #     "account": rec_not_billed[0].name,
        #     "party_type": "Supplier",
        #     "party_name": self.supplier,
        # }
        # JE = frappe.get_doc(
        #     {
        #         "doctype": "Journal Entry",
        #         "company": self.company,
        #         "entry_date": self.posting_date,
        #         "entry_lines": [JEl1, JEl2],
        #     }
        # )
        # JE.insert()

        gl_entry = frappe.get_doc(
            {
                "doctype": "GL Entry",
                "posting_date": self.posting_date,
                "transaction_date": self.posting_date,
                "account": self.debit_account,
                "party_type": "Supplier",
                "party": self.supplier,
                "debit": self.total_amount,
                "credit": 0,
                "against": self.credit_account,
                "against_voucher": "Purchase Receipt",
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
                "party_type": "Supplier",
                "party": self.supplier,
                "debit": 0,
                "credit": self.total_amount,
                "against": self.debit_account,
                "against_voucher": "Purchase Receipt",
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
            (now(), frappe.session.user, "Purchase Receipt", self.name))

        gl_entry = frappe.get_doc(
            {
                "doctype": "GL Entry",
                "posting_date": self.posting_date,
                "transaction_date": self.posting_date,
                "account": self.credit_account,
                "party_type": "Supplier",
                "party": self.supplier,
                "debit": self.total_amount,
                "credit": 0,
                "against": self.debit_account,
                "against_voucher": "Purchase Receipt",
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
                "party_type": "Supplier",
                "party": self.supplier,
                "debit": 0,
                "credit": self.total_amount,
                "against": self.credit_account,
                "against_voucher": "Purchase Receipt",
                "voucher_number": self.name,
                "company": self.company,
                "fiscal_year": "2020-2021",
                "is_cancelled" : 1
            }
        )
        gl_entry.insert()



def set_missing_values(source, target):
    target.run_method("set_missing_values")


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
                },
            },
        },
        target_doc,
        set_missing_values,
    )
    return doc

