# Copyright (c) 2013, Moha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

from accounts.accounts.report.report_common import get_balances_by_root_type

def execute(filters=None):
	columns = get_columns()
	data, chart = get_data_chart(filters = filters, )

	return columns, data, None, chart

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




def get_data_chart(filters= None, ):
	company = filters.get("company") or frappe.defaults.get_user_default("Company")
	if not company:
		frappe.throw("Either set default company or set the company in filters")
	data = []
	income_account_balances = get_balances_by_root_type(company, "Income")
	print(income_account_balances[0])
	data.extend(income_account_balances)
	expense_account_balances = get_balances_by_root_type(company, "Expense")
	data.extend(expense_account_balances)
	profit = income_account_balances[0]['difference'] -  expense_account_balances[0]['difference']
	data.append(["Profit/ Loss (Income - Expense)", profit])

	chart = get_chart_data(income_account_balances, expense_account_balances, profit)


	return data, chart


def get_chart_data( income, expense, profit):
	datasets = []
	datasets.append({'name': _('Income'), 'values':  [income[0]['difference']]})
	datasets.append({'name': _('Expense'), 'values': [expense[0]['difference']]})
	datasets.append({'name': _('Net Profit/Loss'), 'values': [profit]})

	chart = {
		"data": {
			'labels': ["2020-21"],
			'datasets': datasets
		}
	}

	chart["type"] = "bar"
	chart["fieldtype"] = "Currency"

	return chart