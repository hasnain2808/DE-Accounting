// Copyright (c) 2020, Moha and contributors
// For license information, please see license.txt

frappe.ui.form.on('Purchase Order Item', {
	"product" : function(frm) {
		console.log( frm.doc.product.product_name)
		console.log( frm.doc.product)
		frappe.call({
            "method": "frappe.client.get",
            args: {
                doctype: "Product",
                name: frm.doc.product.product_name
            },
            callback: function (data) {
                frappe.model.set_value(frm.doctype,
                    frm.docname, "buying_price",
                    data.message.buying_price)
            }
        })
    }
	// refresh: function(frm) {

	// }
});
