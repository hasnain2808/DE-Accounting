# -*- coding: utf-8 -*-
# Copyright (c) 2020, Moha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc


class SalesOrder(Document):
    pass


@frappe.whitelist()
def make_delivery_note(source_name, target_doc=None):

    doc = get_mapped_doc(
        "Sales Order",
        source_name,
        {
            "Sales Order": {
                "doctype": "Delivery Note",
                "field_map": {
                    "per_billed": "per_billed",
                    "supplier_warehouse": "supplier_warehouse",
                },
                "validation": {
                    # "docstatus": ["=", 1],
                },
            },
            "Sales Order Item": {
                "doctype": "Delivery Note Item",
                "field_map": {
                    "name": "delivery_note_item",
                    "parent": "delivery_note",
                    # "bom": "bom",
                    # "material_request": "material_request",
                    # "material_request_item": "material_request_item"
                },
            },
            # "Purchase Taxes and Charges": {
            # 	"doctype": "Purchase Taxes and Charges",
            # 	"add_if_empty": True
            # }
        },
        target_doc
    )

    return doc

