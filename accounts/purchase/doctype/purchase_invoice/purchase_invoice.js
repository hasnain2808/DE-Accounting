// Copyright (c) 2020, Moha and contributors
// For license information, please see license.txt

frappe.ui.form.on('Purchase Invoice', {
	refresh: function(frm) {
		console.log(frappe.route_options)
	}
});

frappe.ui.form.on("Purchase Invoice Item", {
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