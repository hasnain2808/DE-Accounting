# -*- coding: utf-8 -*-
# Copyright (c) 2020, Moha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document

class Account(Document):
	def autoname(self):
		print(self.company_name + self.account_name)
		self.name = str(self.account_number) + " - " + self.account_name + " - " + self.company_name

