// Copyright (c) 2020, Moha and contributors
// For license information, please see license.txt

// frappe.ui.form.on('Purchase Order', {
// 	// refresh: function(frm) {

// 	// }
// });

frappe.ui.form.on("Purchase Order", {
	company : function(frm) {
		console.log("inside function");
	},
	refresh: function(frm) {
		frm.add_custom_button(__('Create Purchase Receipt'),function() {
			frappe.model.open_mapped_doc({
				method: "accounts.purchase.doctype.purchase_order.purchase_order.make_purchase_receipt",
				frm: frm
			})
		})
	},
})



frappe.ui.form.on("Purchase Order Item", {
	qty : update_total_amount,
	buying_price : update_total_amount,
})

function update_total_amount(frm, cdt, cdn){
	let cur_doc = locals[cdt][cdn];
	cur_doc.amount = cur_doc.qty * cur_doc.buying_price;
	let sum = 0
	for (let row in locals[cdt]) {
		if (! isNaN(locals[cdt][row].amount)) {
			sum+=locals[cdt][row].amount;
		}	}
	frm.set_value("total_amount", sum)
	frm.refresh_fields();
}

