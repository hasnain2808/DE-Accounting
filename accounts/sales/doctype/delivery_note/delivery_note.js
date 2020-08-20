// Copyright (c) 2020, Moha and contributors
// For license information, please see license.txt

frappe.ui.form.on('Delivery Note', {
	refresh: function(frm) {
		console.log("inside refresh event");
		cur_frm.add_custom_button(__('Invoice'),function() {
			frappe.model.open_mapped_doc({
				method: "accounts.sales.doctype.delivery_note.delivery_note.make_sales_invoice",
				frm: cur_frm
			})
		})
	}
});
frappe.ui.form.on("Delivery Note Item", {
	qty : function(frm, cdt, cdn) {
		var cur_doc = locals[cdt][cdn];
		cur_doc.amount = cur_doc.qty * cur_doc.selling_price;
		console.log(cur_doc.qty * cur_doc.selling_price)
		var sum = 0
		for(var row in locals[cdt]){
			console.log(typeof(row))
			sum+=locals[cdt][row].amount;
		}
		frm.set_value("total_amount", sum)
		frm.refresh_fields();
	},
})