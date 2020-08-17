frappe.provide("frappe.treeview_settings");

frappe.treeview_settings['Account'] = {
	get_tree_nodes: "accounts.accounts.doctype.account.account.get_children",
	// add_tree_node: "accounts.projects.doctype.account.account.add_node",
	filters: [
		{
			fieldname: "company",
			fieldtype:"Link",
			options: "Company",
			label: __("Company"),
		}
	]
};
