# Copyright (c) 2013, Moha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import functools

def execute(filters=None):
	company = filters.get("company") or frappe.defaults.get_user_default("Company")
	accounts = get_accounts(company, "Income")
	print(accounts)
	income_accounts_by_name, income_parent_children_map = filter_accounts(accounts)

	# print("accounts_by_name")
	# print(accounts_by_name)
	# print("parent_children_map")
	# print(parent_children_map)

	accounts = get_accounts(company, "Expense")
	# print(accounts)
	expense_accounts_by_name, expense_parent_children_map = filter_accounts(accounts)

	# print("accounts_by_name")
	# print(accounts_by_name)
	# print("parent_children_map")
	# print(parent_children_map)
	account_balances = get_leaf_account_balance(company)
	calculate_non_leaf_account_balance(None, income_parent_children_map, account_balances)
	columns, data = [], []
	return columns, data


def filter_accounts(accounts, depth=10):
	parent_children_map = {}
	accounts_by_name = {}
	for d in accounts:
		print(d.name)
		accounts_by_name[d.name] = d
		parent_children_map.setdefault(d.parent_account or None, []).append(d)

	return accounts_by_name, parent_children_map


def get_accounts(company, root_type):
	return frappe.db.sql("""
		select name, account_name, company_name, is_group, account_number, root_type, lft, rgt, is_group, old_parent, parent_account
		from `tabAccount`
		where company_name=%s and root_type=%s order by lft""", (company, root_type), as_dict=True)

def get_leaf_account_balance(company):
	query = f"""
		select
		account, sum(credit), sum(debit)
		from `tabJournal Entry` inner join `tabJournal Entry lines`
		on  `tabJournal Entry`.name=`tabJournal Entry lines`.parent
		where company like '{company}'
		group by (account);
		"""
	# print(query)
	account_balances = frappe.db.sql(query, as_dict=True)
	# print(account_balances)
	return account_balances


def calculate_non_leaf_account_balance(account, parent_children_map, account_balances):
	if account in account_balances:
		return account_balances[account]
	else:
		children = parent_children_map[account]
		# credit = debit = 0
		# for i in children:
			

