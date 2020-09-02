// Copyright (c) 2016, Moha and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Balance Sheet"] = {
	"filters": [
        {
            fieldname: 'company',
            label: __('Company'),
            fieldtype: 'Link',
            options: 'Company',
        },
	],
	"treeView": true,
	"name_field": "account",
	"parent_field": "parent_account",
	"initial_depth": 2
};
