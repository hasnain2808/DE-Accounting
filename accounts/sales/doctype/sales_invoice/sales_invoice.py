# -*- coding: utf-8 -*-
# Copyright (c) 2020, Moha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc


class SalesInvoice(Document):
    def on_update(self):
        sales_account = frappe.get_list(
            "Account", filters={"company_name": self.company, "account_name": "Sales"}
        )
        print(sales_account)
        debtors_account = frappe.get_list(
            "Account", filters={"company_name": self.company, "account_name": "Debtors"}
        )
        print(debtors_account)
        JEl1 = {
            "credit": self.total_amount,
            "debit": 0,
            "account": sales_account[0].name,
            "party_type": "Customer",
            "party_name": self.customer,
        }
        JEl2 = {
            "credit": 0,
            "debit": self.total_amount,
            "account": debtors_account[0].name,
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
    # if len(target.get("items")) == 0:
    # 	frappe.throw(_("All items have already been Invoiced/Returned"))

    doc = frappe.get_doc(target)
    doc.ignore_pricing_rule = 1
    doc.run_method("onload")
    doc.run_method("set_missing_values")
