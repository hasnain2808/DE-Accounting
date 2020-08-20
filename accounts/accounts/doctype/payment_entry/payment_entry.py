# -*- coding: utf-8 -*-
# Copyright (c) 2020, Moha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class PaymentEntry(Document):
    def on_update(self):
        JEl1 = {
            "credit": self.total_amount,
            "debit": 0,
            "account": self.credit_account,
            "party_type": self.party_type,
            "party_name": self.party_name,
        }
        JEl2 = {
            "credit": 0,
            "debit": self.total_amount,
            "account": self.debit_account,
        }
        JE = frappe.get_doc(
            {
                "doctype": "Journal Entry",
                "company": self.company,
                "entry_date": self.posting_date,
                "entry_lines": [JEl1, JEl2],
            }
        )
        JE.insert()


def set_missing_values(source, target):
    target.run_method("set_missing_values")
