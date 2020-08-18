# -*- coding: utf-8 -*-
# Copyright (c) 2020, Moha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

# import frappe
from frappe.model.document import Document


class Product(Document):
    def autoname(self):
        print(self.product_code + self.product_name)
        self.name = self.product_code + " - " + self.product_name
