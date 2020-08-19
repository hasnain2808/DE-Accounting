# -*- coding: utf-8 -*-
# Copyright (c) 2020, Moha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class PurchaseReceipt(Document):
	def on_update(self):
		stock_account = frappe.get_list('Account',
			filters={'company_name': self.company, 'account_name': 'Stock in Hand'}
		)
		print(stock_account)
		rec_not_billed = frappe.get_list('Account',
			filters={'company_name': self.company, 'account_name': 'Asset Received But not Billed'}
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
				"party_type":"Supplier",
				"party_name":self.supplier,
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


