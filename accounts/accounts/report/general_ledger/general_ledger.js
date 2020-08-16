// Copyright (c) 2016, Moha and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["General Ledger"] = {
	"filters": [
        {
            fieldname: 'company',
            label: __('Company'),
            fieldtype: 'Link',
            options: 'Company',
        },
	]
};
