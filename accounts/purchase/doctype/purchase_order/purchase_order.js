// Copyright (c) 2020, Moha and contributors
// For license information, please see license.txt

frappe.ui.form.on('Purchase Order', {
	// refresh: function(frm) {

	// }
	"product_list.qty" : function(frm) {
		console.log( frm.doc.product.product_name)
		console.log( frm.doc.product)
		qty = frm.doc.product.product_list.qty
		buying_price = frm.doc.product.product_list.buying_price
		frm.set_value("amount",qty*buying_price)
    }
});
