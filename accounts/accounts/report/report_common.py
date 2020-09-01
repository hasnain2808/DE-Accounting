

from __future__ import unicode_literals
import frappe

def get_balances_by_root_type(company, root_type):
	accounts = get_accounts(company, root_type)
	accounts_by_name, parent_children_map = filter_accounts(accounts)
	account_balances = get_leaf_account_balance(company, root_type)
	calculate_non_leaf_account_balance(None, parent_children_map, account_balances)
	if root_type == "Liability" or root_type == "Income":
		for key,value in account_balances.items():
			value['difference'] *= -1
	ordered_account_balances = []
	max_indent = 0
	for d in accounts:
		if account_balances[d['name']]['difference']!=0:
			max_indent = max(max_indent, account_balances[d['name']]['indent'])
			ordered_account_balances.append(account_balances[d['name']])
	for d in ordered_account_balances:
		d['indent'] = max_indent - d['indent']


	return ordered_account_balances

def filter_accounts(accounts, depth=10):
	parent_children_map = {}
	accounts_by_name = {}
	for d in accounts:
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
		account, parent_account, sum(credit) AS credit, sum(debit) AS debit, ( sum(debit) - sum(credit)) AS difference
		from `tabGL Entry` inner join `tabAccount`
		on `tabGL Entry`.account = `tabAccount`.name
		where `tabGL Entry`.company like '{company}' and `tabAccount`.root_type = '{root_type}'
		group by (account);
		"""
	account_balances = {d['account']: d for d in frappe.db.sql(query, as_dict=True)}
	return account_balances


def calculate_non_leaf_account_balance(account, parent_children_map, account_balances, parent_account= None):
	print(account_balances)
	if account in account_balances:
		print(account)
		account_balances[account]['indent'] = 1
		return
	else:
		account_balances[account] = {
			'account': account,
			'parent_account': parent_account,
			'debit': 0,
			'credit': 0,
			'difference': 0,
			'indent': 0
			}
		if account in parent_children_map:
			children = parent_children_map[account]
			indents = []
			for child in children:
				calculate_non_leaf_account_balance(child['name'], parent_children_map, account_balances, account)
				account_balances[account]['debit'] += account_balances[child['name']]['debit']
				account_balances[account]['credit'] += account_balances[child['name']]['credit']
				account_balances[account]['difference'] += account_balances[child['name']]['difference']
				indents.append( account_balances[child['name']]['indent'] )
			account_balances[account]['indent'] = min(indents) + 1


