# -*- coding: utf-8 -*-
# Copyright (c) 2020, Moha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.utils.nestedset import NestedSet
import frappe

class Account(NestedSet):
	def autoname(self):
		print(self.company_name + self.account_name)
		self.name = self.account_name + " - " + self.company_name

@frappe.whitelist()
def get_children(doctype, parent = None,  is_root=False, company=frappe.defaults.get_user_default('Company'),):

	filters = [['docstatus', '<', '2']]

	# if task:
	# 	filters.append(['parent_task', '=', task])
	if parent and not is_root:
		# via expand child
		filters.append(['parent_account', '=', parent])
	else:
		filters.append(['ifnull(`parent_account`, "")', '=', ''])

	if company:
		filters.append(['company_name', '=', company])

	accounts = frappe.get_list(doctype, fields=[
		'name as value',
		'is_group as expandable'
	], filters=filters, order_by='name')

	# return tasks
	return accounts
