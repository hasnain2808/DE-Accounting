// Copyright (c) 2020, Moha and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Invoice', {
	refresh: function(frm) {
		console.log("inside refresh event");
		frm.add_custom_button(__('Create Payment Entry'),function() {
			let method = "accounts.sales.doctype.sales_invoice.sales_invoice.get_payment_entry";
			return frappe.call({
				method: method,
				args: {
					"dt": frm.doc.doctype,
					"dn": frm.doc.name
				},
				callback: function(r) {
					let doclist = frappe.model.sync(r.message);
					frappe.set_route("Form", doclist[0].doctype, doclist[0].name);
				}
			});
		})
	},
});



frappe.ui.form.on("Sales Invoice Item", {
	qty : update_total_amount,
	selling_price : update_total_amount,
})

function update_total_amount(frm, cdt, cdn){
	let cur_doc = locals[cdt][cdn];
	cur_doc.amount = cur_doc.qty * cur_doc.selling_price;
	let sum = 0
	for (let row in locals[cdt]) {
		if (! isNaN(locals[cdt][row].amount)) {
			sum+=locals[cdt][row].amount;
		}	}
	frm.set_value("total_amount", sum)
	frm.refresh_fields();
}
