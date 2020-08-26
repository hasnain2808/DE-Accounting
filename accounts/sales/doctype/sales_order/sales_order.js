// Copyright (c) 2020, Moha and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Order', {
	refresh: function(frm) {
		console.log("inside refresh event");
		frm.add_custom_button(__('Create Delivery Note'),function() {
			frappe.model.open_mapped_doc({
				method: "accounts.sales.doctype.sales_order.sales_order.make_delivery_note",
				frm: frm
			})
		})
	}
});


frappe.ui.form.on("Sales Order Item", {
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