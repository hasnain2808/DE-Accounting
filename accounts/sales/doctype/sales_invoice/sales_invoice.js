// Copyright (c) 2020, Moha and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Invoice', {
	refresh: function(frm) {
		console.log("inside refresh event");
		cur_frm.add_custom_button(__('Payment Entry'),function() {
			var method = "accounts.sales.doctype.sales_invoice.sales_invoice.get_payment_entry";
			return frappe.call({
				method: method,
				args: {
					"dt": frm.doc.doctype,
					"dn": frm.doc.name
				},
				callback: function(r) {
					var doclist = frappe.model.sync(r.message);
					frappe.set_route("Form", doclist[0].doctype, doclist[0].name);
				}
			});
		})
	},
});
