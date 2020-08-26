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
	var cur_doc = locals[cdt][cdn];
	var total_debit = 0
	var total_credit = 0
	for(var row in locals[cdt]){
		console.log(row)
		if (! isNaN(locals[cdt][row].debit)) {
			total_debit+=locals[cdt][row].debit;
		}
		if (! isNaN(locals[cdt][row].credit)) {
			total_credit+=locals[cdt][row].credit;
		}
	}
	frm.set_value("total_debit", total_debit)
	frm.set_value("total_credit", total_credit)
	frm.refresh_fields();
}