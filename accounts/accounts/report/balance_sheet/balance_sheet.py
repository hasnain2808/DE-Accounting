# Copyright (c) 2013, Moha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from accounts.accounts.report.report_common import get_balances_by_root_type

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters = filters, )
	return columns, data

def get_columns():
	return [
		{
            "fieldname": "account",
            "label": "Account",
            "fieldtype": "Link",
			"options": "Account",
            "width": 150,
        },
        {
            "fieldname": "difference",
            "label": "Dr/Cr",
            "fieldtype": "Currency",
            "width": 100,
        },
	]




def get_data(filters= None, ):
	company = filters.get("company") or frappe.defaults.get_user_default("Company")
	if not company:
		frappe.throw("Either set default company or set the company in filters")
	data = []
	assets_account_balances = get_balances_by_root_type(company, "Assets")
	data.extend(assets_account_balances)
	data.append({})
	data.append(["Total Assets(Debit)", assets_account_balances[0]['difference']])
	data.append({})
	liabilities_account_balances = get_balances_by_root_type(company, "Liabilities")
	data.extend(liabilities_account_balances)
	data.append({})
	data.append(["Total Liability(Credit)", liabilities_account_balances[0]['difference']])
	data.append({})
	income_account_balances = get_balances_by_root_type(company, "Income")
	expense_account_balances = get_balances_by_root_type(company, "Expense")
	data.append(["Provisional Profit/Loss (Credit)", income_account_balances[0]['difference'] -  expense_account_balances[0]['difference']])
	data.append({})
	data.append(["Total Credit", income_account_balances[0]['difference'] -  expense_account_balances[0]['difference'] +  liabilities_account_balances[0]['difference']])
	return data
