# -*- coding: utf-8 -*-
# Copyright (c) 2020, Moha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class PurchaseOrder(Document):
	pass


@frappe.whitelist()
def make_purchase_receipt(source_name, target_doc=None):

	doc = get_mapped_doc("Purchase Order", source_name,	{
		"Purchase Order": {
			"doctype": "Purchase Receipt",
			"field_map": {
			},
			"validation": {
			}
		},
		"Purchase Order Item": {
			"doctype": "Purchase Receipt Items",
			"field_map": {
				"name": "purchase_receipt_items",
				"parent": "purchase_receipt",
				# "bom": "bom",
				# "material_request": "material_request",
				# "material_request_item": "material_request_item"
			},
		},
		# "Purchase Taxes and Charges": {
		# 	"doctype": "Purchase Taxes and Charges",
		# 	"add_if_empty": True
		# }
	}, target_doc, set_missing_values)
	return doc
def set_missing_values(source, target):
	target.run_method("set_missing_values")
	# target.run_method("calculate_taxes_and_totals")