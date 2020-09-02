// Copyright (c) 2020, Moha and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Invoice', {
	refresh: function(frm) {
		frm.set_value("credit_account", "Sales - " + frm.doc.company)
		frm.set_value("debit_account", "Debtors - " + frm.doc.company)
		frm.refresh_fields();
		set_debit_account_filter(frm)
		set_credit_account_filter(frm)
		console.log("inside refresh event");
		frm.add_custom_button(__('Create Payment Entry'),function() {
			let method = "accounts.sales.doctype.sales_invoice.sales_invoice.get_payment_entry";
			return frappe.call({
				method: method,
				args: {
					"dt": frm.doc.doctype,
					"dn": frm.doc.name
				},
				callback: function(r) {
					let doclist = frappe.model.sync(r.message);
					frappe.set_route("Form", doclist[0].doctype, doclist[0].name);
				}
			});
		})
	},
	company: function (frm) {
		frm.set_value("credit_account", "Sales - " + frm.doc.company)
		frm.set_value("debit_account", "Debtors - " + frm.doc.company)
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
				"parent_account": "Accounts Receivable - " + frm.doc.company

			}
		};
	});
}

function set_credit_account_filter(frm) {
	frm.set_query("credit_account", function () {
		return {
			"filters": {
				"company_name": frm.doc.company,
				"parent_account": "Direct Income - " + frm.doc.company
			}
		};
	});
}

frappe.ui.form.on("Sales Invoice Item", {
	qty : update_total_amount,
	selling_price : update_total_amount,
})

// function update_total_amount(frm, cdt, cdn){
// 	let cur_doc = locals[cdt][cdn];
// 	cur_doc.amount = cur_doc.qty * cur_doc.selling_price;
// 	let sum = 0
// 	for (let row in locals[cdt]) {
// 		if (! isNaN(locals[cdt][row].amount)) {
// 			sum+=locals[cdt][row].amount;
// 		}	}
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

