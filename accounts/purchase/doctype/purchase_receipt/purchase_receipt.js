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
	qty : function(frm, cdt, cdn) {
		var cur_doc = locals[cdt][cdn];
		cur_doc.amount = cur_doc.qty * cur_doc.buying_price;
		var sum = 0
		for(var row in locals[cdt]){
			console.log(typeof(row))
			sum+=locals[cdt][row].amount;
		}
		frm.set_value("total_amount", sum)
		frm.refresh_fields();
	},
})