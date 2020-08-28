// Copyright (c) 2020, Moha and contributors
// For license information, please see license.txt

frappe.ui.form.on('Journal Entry', {
	// refresh: function(frm) {

	// }
});


frappe.ui.form.on("Journal Entry lines", {
	credit : populate_total,
	debit : populate_total,
	account : populate_total,
})


function populate_total(frm, cdt, cdn){
	// let cur_doc = locals[cdt][cdn];
	// let cur_dt = locals[cdt];
	// let total_debit = flt(0);
	// let total_credit = flt(0);
	// for(let row in cur_dt){
	// 	console.log(total_credit)
	// 	console.log(total_credit)
	// 	if (! isNaN(cur_dt[row].debit)) {
	// 		total_debit+=flt(cur_dt[row].debit);
	// 	}
	// 	if (! isNaN(cur_dt[row].credit)) {
	// 		total_credit+=flt(cur_dt[row].credit);
	// 	}
	// }
	// console.log(total_credit)
	// console.log(total_credit)
	// frm.set_value("total_debit", total_debit)
	// frm.set_value("total_credit", total_credit)
	// frm.refresh_fields();
	let cur_doc = locals[cdt][cdn];
	// console.log(frm.doc.product_list)
	// cur_doc.amount = cur_doc.qty * cur_doc.buying_price;
	let sum = 0.0
	let total_debit = flt(0);
	let total_credit = flt(0);

	// if (! isNaN(frm.doc) ) {
		console.log("inside")
		frm.doc.entry_lines.forEach(element => {
			console.log(element)

			if (! isNaN(element.debit)) {
				total_debit+=flt(element.debit);
			}
			if (! isNaN(element.credit)) {
				total_credit+=flt(element.credit);
			}

		});
	// }
	frm.set_value("total_debit", total_debit)
	frm.set_value("total_credit", total_credit);
	frm.refresh_fields();

}


// function update_total_amount(frm, cdt, cdn){
// 	let cur_doc = locals[cdt][cdn];
// 	// console.log(frm.doc.product_list)
// 	// cur_doc.amount = cur_doc.qty * cur_doc.buying_price;
// 	let sum = 0.0
// 	let total_debit = flt(0);
// 	let total_credit = flt(0);

// 	if (! isNaN(frm.doc) ) {
// 		frm.doc.entry_lines.forEach(element => {
// 			console.log(element)

// 			if (! isNaN(element.debit)) {
// 				total_debit+=flt(element.debit);
// 			}
// 			if (! isNaN(element.credit)) {
// 				total_credit+=flt(element.credit);
// 			}

// 		});
// 	}
// 	frm.set_value("total_debit", total_debit)
// 	frm.set_value("total_credit", total_credit);
// }




// let cur_dt = locals[cdt];
// let total_debit = flt(0);
// let total_credit = flt(0);
// for(let row in cur_dt){
// 	console.log(total_credit)
// 	console.log(total_credit)
// 	if (! isNaN(cur_dt[row].debit)) {
// 		total_debit+=flt(cur_dt[row].debit);
// 	}
// 	if (! isNaN(cur_dt[row].credit)) {
// 		total_credit+=flt(cur_dt[row].credit);
// 	}
// }
// console.log(total_credit)
// console.log(total_credit)
// frm.set_value("total_debit", total_debit)
// frm.set_value("total_credit", total_credit)