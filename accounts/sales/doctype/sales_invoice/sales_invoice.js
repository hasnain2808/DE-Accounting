// Copyright (c) 2020, Moha and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Invoice', {
	refresh: function(frm) {
		console.log("inside refresh event");
		cur_frm.add_custom_button(__('Create Payment Entry'),function() {
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



frappe.ui.form.on("Sales Invoice Item", {
	qty: function (frm, cdt, cdn) {
		var cur_doc = locals[cdt][cdn];
		cur_doc.amount = cur_doc.qty * cur_doc.buying_price;
		var sum = 0
		for (var row in locals[cdt]) {
			console.log(typeof (row))
			sum += locals[cdt][row].amount;
		}
		frm.set_value("total_amount", sum)
		frm.refresh_fields();
	},
})