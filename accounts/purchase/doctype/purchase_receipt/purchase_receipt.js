// Copyright (c) 2020, Moha and contributors
// For license information, please see license.txt

frappe.ui.form.on('Purchase Receipt', {
	// refresh: function(frm) {

	// },
	refresh: function(frm) {
		console.log("inside refresh event");
		frm.add_custom_button(__('Create Purchase Invoice'),function() {
			frappe.model.open_mapped_doc({
				method: "accounts.purchase.doctype.purchase_receipt.purchase_receipt.make_purchase_invoice",
				frm: frm
			})
		})
	},
});


frappe.ui.form.on("Purchase Receipt Items", {
	qty: update_total_amount,
	buying_price: update_total_amount,
})

// function update_total_amount(frm, cdt, cdn){
// 	let cur_doc = locals[cdt][cdn];
// 	cur_doc.amount = cur_doc.qty * cur_doc.buying_price;
// 	let sum = 0
// 	for (let row in locals[cdt]) {
// 		if (! isNaN(locals[cdt][row].amount)) {
// 			sum+=locals[cdt][row].amount;
// 		}
// 	}
// 	frm.set_value("total_amount", sum)
// 	frm.refresh_fields();
// }


function update_total_amount(frm, cdt, cdn){
	let cur_doc = locals[cdt][cdn];
	// console.log(frm.doc.product_list)
	cur_doc.amount = cur_doc.qty * cur_doc.buying_price;
	let sum = 0.0
	if (! isNaN(frm.doc) ) {
		frm.doc.product_list.forEach(element => {
			console.log(element)
			if (!( isNaN(element) && isNaN(element.amount))) {
				sum+=flt(element.amount);
				console.log(sum)
			}
		});
	}
	frm.set_value("total_amount", sum)
	frm.refresh_fields();
}

