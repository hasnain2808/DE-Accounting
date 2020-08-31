// Copyright (c) 2020, Moha and contributors
// For license information, please see license.txt

frappe.ui.form.on('Purchase Receipt', {
	// refresh: function(frm) {

	// },
	refresh: function (frm) {
		frm.add_custom_button(__('Create Purchase Invoice'), function () {
			frappe.model.open_mapped_doc({
				method: "accounts.purchase.doctype.purchase_receipt.purchase_receipt.make_purchase_invoice",
				frm: frm
			})
		})
	},
	company: function (frm) {
		frm.set_value("debit_account", "Stock in Hand - " + frm.doc.company)
		frm.set_value("credit_account", "Asset Received But not Billed - " + frm.doc.company)
		frm.refresh_fields();
		set_debit_account_filter(frm)
		set_credit_account_filter(frm)
	},
});

function set_debit_account_filter(frm) {
	frm.set_query("debit_account", function () {
		return {
			"filters": {
				"company_name": frm.doc.company,
				"parent_account": "Stock Assets - " + frm.doc.company

			}
		};
	});
}

function set_credit_account_filter(frm) {
	frm.set_query("debit_account", function () {
		return {
			"filters": {
				"company_name": frm.doc.company,
				"parent_account": "Stock Liabilities - " + frm.doc.company
			}
		};
	});
}

frappe.ui.form.on("Purchase Receipt Items", {
	qty: update_total_amount,
	buying_price: update_total_amount,
})

function update_total_amount(frm, cdt, cdn) {
	let cur_doc = locals[cdt][cdn];
	cur_doc.amount = cur_doc.qty * cur_doc.buying_price;
	let sum = 0.0
	frm.doc.product_list.forEach(element => {
		console.log(element)
		if (!(isNaN(element) && isNaN(element.amount))) {
			sum += flt(element.amount);
			console.log(sum)
		}
	});
	console.log(sum)
	frm.set_value("total_amount", sum)
	frm.refresh_fields();
}