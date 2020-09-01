# -*- coding: utf-8 -*-
# Copyright (c) 2020, Moha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class PaymentEntry(Document):
    def on_submit(self):
        # JEl1 = {
        #     "credit": self.total_amount,
        #     "debit": 0,
        #     "account": self.credit_account,
        #     "party_type": self.party_type,
        #     "party_name": self.party_name,
        # }
        # JEl2 = {
        #     "credit": 0,
        #     "debit": self.total_amount,
        #     "account": self.debit_account,
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
                "party_type": self.party_type,
                "party_name": self.party_name,
                "debit": self.total_amount,
                "credit": 0,
                "against": self.credit_account,
                "against_voucher": "Payment Entry",
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
                "party_type": self.party_type,
                "party_name": self.party_name,
                "debit": 0,
                "credit": self.total_amount,
                "against": self.debit_account,
                "against_voucher": "Payment Entry",
                "voucher_number": self.name,
                "company": self.company,
                "fiscal_year": "2020-2021"
            }
        )
        gl_entry.insert()

def set_missing_values(source, target):
    target.run_method("set_missing_values")
