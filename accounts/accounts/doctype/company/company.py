# -*- coding: utf-8 -*-
# Copyright (c) 2020, Moha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document
import frappe

Accounts = {
	'Assets':[
		{
			'Current Assets': [
				{
					'Accounts Receivable':['Debtors']
				},
				{
					'Bank Accounts':[]
				},
				{
					'Cash In Hand':['Cash']
				},
								{
					'Stock Assets':['Stock In Hand']
				},
			]
		}
	],
	'Liabilities':[
		{
			'Current Liabilities': [
				{
					'Accounts Payable':['Creditors']
				},
				{
					'Stock Liabilities': ['Asset Received But not Billed'],
				}
			],

		},
		{
			'Equity':['Shareholder Fund Account']
		}
	],
	'Expense':[
		{
			'Direct Expense': {
				'Stock Expense':['Cost of Goods Sold', 'Service']
			}
		}
	],
	'Income':[
		{
			'Direct Income': ['Sales', 'Service']
		}
	]
}



class Company(Document):
	def create_accounts(self, child, parent, company, root_type):
		if type(child) == type('string'):
			account = frappe.get_doc({
						"doctype": "Account",
						"account_name": child,
						"company_name": company,
						"parent_account": parent,
						"is_group": 0,
						"root_type": root_type,
			})
			account.insert()
		if type(child) == type({}):
			for key, value in child.items():

				account = frappe.get_doc({
							"doctype": "Account",
							"account_name": key,
							"company_name": company,
							"parent_account": parent,
							"is_group": 1,
							"root_type": root_type,
				})
				account.insert()

				for account_child in value:
					self.create_accounts(account_child, account.name, company, None)




	def on_update(self):
		print(Accounts)
		print('-'*255)
		self.create_accounts(Accounts, None, self.name, None)
