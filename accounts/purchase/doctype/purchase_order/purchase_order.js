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
		console.log("inside refresh event");
		// frm.add_custom_button(__("Generate Purchase Receipt"), function() {
		// 		frappe.route_options = {
		// 			supplier: frm.doc.supplier,
		// 			company: frm.doc.company,
		// 			product_list: frm.doc.product_list,
		// 			total_amount: frm.doc.total_amount
		// 		},
		// 		console.log(frappe.route_options)
		// 		frappe.set_route("Form", "Purchase Receipt", "New Purchase Receipt", );
		// 	});
		cur_frm.add_custom_button(__('Purchase Receipt'),function() {
			frappe.model.open_mapped_doc({
				method: "accounts.purchase.doctype.purchase_order.purchase_order.make_purchase_receipt",
				frm: cur_frm
			})
		})
	},
})



frappe.ui.form.on("Purchase Order Item", {
	qty : function(frm, cdt, cdn) {
		var cur_doc = locals[cdt][cdn];
		cur_doc.amount = cur_doc.qty * cur_doc.buying_price;
		var sum = 0;
		for(var row in locals[cdt]){
			console.log(typeof(row))
			sum+=locals[cdt][row].amount;
		}
		console.log(sum)
		frm.set_value("total_amount", sum)
		frm.refresh_fields();
	},
})



var add_button = function(frm)
{
		frm.add_custom_button(__("Create "), function() {
			frappe.route_options = {
				"first_name": frm.doc.first_name
			},
			frappe.set_route("Form", "Second Doctype Name" , "New Second Doctype Name");
		});
}



