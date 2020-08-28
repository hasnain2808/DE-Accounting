# -*- coding: utf-8 -*-
# Copyright (c) 2020, Moha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt
from frappe.model.document import Document

class JournalEntry(Document):
	def on_update(self):
		if self.total_debit != self.total_credit:
			frappe.throw(_(f"Total Debit must be equal to Total Credit. The difference is {abs(flt(self.total_debit) - flt(self.total_credit))}"))
		entry_date = self.entry_date
		reference_number = self.reference_number
		reference_date = self.reference_date
		debit_accounts = []
		credit_accounts = []
		for entry_line in self.entry_lines:
			if entry_line.debit != 0:
				debit_accounts.append(entry_line.account)
			elif entry_line.credit != 0:
				credit_accounts.append(entry_line.account)
		debit_accounts = ", ".join(debit_accounts)
		credit_accounts = ", ".join(credit_accounts)
		for entry_line in self.entry_lines:
			gl_entry = frappe.get_doc(
				{
					"doctype": "GL Entry",
					"posting_date": entry_date,
					"transaction_date": entry_date,
					"account": entry_line.account,
					"party_type": entry_line.party_type,
					"party": entry_line.party_name,
					"debit": entry_line.debit,
					"credit": entry_line.credit,
					"against": debit_accounts if entry_line.debit == 0 else credit_accounts,
					"against_voucher": "Journal Entry",
					"voucher_number": self.name,
					"company": self.company,
					"fiscal_year": "2020-2021"
				}
			)
			gl_entry.insert()

	def on_cancel(self):
		print(self.docstatus)
