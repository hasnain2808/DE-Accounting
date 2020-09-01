// Copyright (c) 2016, Moha and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Profit and Loss Statement"] = {
	"filters": [
        {
            fieldname: 'company',
            label: __('Company'),
            fieldtype: 'Link',
            options: 'Company',
        },
	]
};
