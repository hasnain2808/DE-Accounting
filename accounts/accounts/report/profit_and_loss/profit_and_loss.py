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
	income_account_balances = get_balances_by_root_type(company, "Income")
	data.extend(income_account_balances)
	expense_account_balances = get_balances_by_root_type(company, "Expense")
	data.extend(expense_account_balances)
	data.append(["Profit/ Loss (Income - Expense)", income_account_balances[0]['difference'] -  expense_account_balances[0]['difference']])
	return data
