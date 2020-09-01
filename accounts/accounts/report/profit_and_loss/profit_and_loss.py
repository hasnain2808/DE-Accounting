# Copyright (c) 2013, Moha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters = filters, )
	print(data)
	return columns, data

def get_columns():
	return [
		{
            "fieldname": "Account",
            "label": "Account",
            "fieldtype": "Link",
			"options": "Account",
            "width": 150,
        },
        {
            "fieldname": "Dr/Cr",
            "label": "Dr/Cr",
            "fieldtype": "Currency",
            "width": 100,
        },
	]




def get_data(filters= None, ):
	company = filters.get("company") or frappe.defaults.get_user_default("Company")
	if not company:
		frappe.throw("Either set default company or set the company in filters")

	income_account_balances = get_balances_by_root_type(company, "Income")
	expense_account_balances = get_balances_by_root_type(company, "Expense")





	data = []
	for key,value in income_account_balances.items():
		data.append([key, value['difference']])

	for key,value in expense_account_balances.items():
		data.append([key, value['difference']])

	return data

def get_balances_by_root_type(company, root_type):
	accounts = get_accounts(company, root_type)
	# print(accounts)
	accounts_by_name, parent_children_map = filter_accounts(accounts)

	# print("accounts_by_name")
	# print(accounts_by_name)
	# print("parent_children_map")
	print(parent_children_map)


	account_balances = get_leaf_account_balance(company, root_type)
	print(account_balances)
	calculate_non_leaf_account_balance(None, parent_children_map, account_balances)
	print(account_balances)
	if root_type == "Liability" or root_type == "Income":
		for key,value in account_balances.items():
			value['difference'] *= -1
	return account_balances





def filter_accounts(accounts, depth=10):
	parent_children_map = {}
	accounts_by_name = {}
	for d in accounts:
		# print(d.name)
		accounts_by_name[d.name] = d
		parent_children_map.setdefault(d.parent_account or None, []).append(d)

	return accounts_by_name, parent_children_map


def get_accounts(company, root_type):
	return frappe.db.sql("""
		select name, account_name, company_name, is_group, account_number, root_type, lft, rgt, is_group, old_parent, parent_account
		from `tabAccount`
		where company_name=%s and root_type=%s order by lft""", (company, root_type), as_dict=True)

def get_leaf_account_balance(company, root_type):
	query = f"""
		select
		account, sum(credit) AS credit, sum(debit) AS debit, ( sum(debit) - sum(credit)) AS difference
		from `tabGL Entry` inner join `tabAccount`
		on `tabGL Entry`.account = `tabAccount`.name
		where `tabGL Entry`.company like '{company}' and `tabAccount`.root_type = '{root_type}'
		group by (account);
		"""
	# print(frappe.db.sql(query, as_dict=True))
	account_balances = {d['account']: d for d in frappe.db.sql(query, as_dict=True)}
	# print(account_balances)
	return account_balances


def calculate_non_leaf_account_balance(account, parent_children_map, account_balances):
	if account in account_balances:
		return
	else:
		account_balances[account] = {
			'account': account,
			'debit': 0,
			'credit': 0,
			'difference': 0
			}
		if account in parent_children_map:
			children = parent_children_map[account]

			for child in children:
				# print(child)
				calculate_non_leaf_account_balance(child['name'], parent_children_map, account_balances)
				account_balances[account]['debit'] += account_balances[child['name']]['debit']
				account_balances[account]['credit'] += account_balances[child['name']]['credit']
				account_balances[account]['difference'] += account_balances[child['name']]['difference']



