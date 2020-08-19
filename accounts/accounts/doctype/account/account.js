// Copyright (c) 2020, Moha and contributors
// For license information, please see license.txt

// frappe.ui.form.on('Account', {
// 	// refresh: function(frm) {

// 	// }
	
// });


frappe.ui.form.on("Account", {
	"account_number" : function(frm) {
		console.log("inside function");
	},
	refresh: function(frm) {
		console.log("inside refresh event");
	},
})