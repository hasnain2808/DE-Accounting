# Copyright (c) 2013, Moha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


def execute(filters=None):
    # for i in frappe.db.sql("select * from `tabJournal Entry` inner join `tabJournal Entry lines`"):
    # 	print(i)

    columns = [
        {
            "fieldname": "entry_date",
            "label": "Entry Date",
            "fieldtype": "Date",
            "width": 100,
        },
        {
            "fieldname": "debit_account",
            "label": "Account",
            "fieldtype": "Link",
            "width": 175,
            "options": "Account",
        },
        {"fieldname": "debit", "label": "Debit", "fieldtype": "Currency", "width": 80,},
        {
            "fieldname": "credit",
            "label": "Credit",
            "fieldtype": "Currency",
            "width": 80,
        },
        {
            "fieldname": "credit_account",
            "label": "Against Account",
            "fieldtype": "Link",
            "width": 175,
            "options": "Account",
        },
        {
            "fieldname": "party_type",
            "label": "Party Type",
            "fieldtype": "Link",
            "width": 100,
            "options": "Doctype",
        },
        {
            "fieldname": "party_name",
            "label": "Party Name",
            "fieldtype": "Dynamic Link",
            "width": 100,
            "options": "party_type",
        },
        {
            "fieldname": "reference_number",
            "label": "Reference Number",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "fieldname": "reference_date",
            "label": "Reference Date",
            "fieldtype": "Data",
            "width": 120,
        },
    ]

    company = filters.get("company") or frappe.defaults.get_user_default("Company")
    # print(entries)

    # select credit.parent as parent, debit_account,debit, credit_account,credit, concat_ws(' ',debit.party_name, credit.party_name) as party_name, concat_ws(' ',debit.party_type, credit.party_type) as party_type  from (select  parent,  debit, account as debit_account, party_type, party_name from `tabJournal Entry lines` where debit <> 0) as debit inner join (select parent, credit, account as credit_account, party_type, party_name from `tabJournal Entry lines` where credit <> 0) as credit  on debit.parent = credit.parent

    # select * from (select credit.parent as parent, debit_account,debit, credit_account,credit, concat_ws(' ',debit.party_name, credit.party_name) as party_name, concat_ws(' ',debit.party_type, credit.party_type) as party_type  from (select  parent,  debit, account as debit_account, party_type, party_name from `tabJournal Entry lines` where debit <> 0) as debit inner join (select parent, credit, account as credit_account, party_type, party_name from `tabJournal Entry lines` where credit <> 0) as credit  on debit.parent = credit.parent) As lines  inner join `tabJournal Entry` as entry on lines.parent=entry.name
    query = """select
        entry_date, debit_account,debit,credit,credit_account, party_type, party_name, reference_number, reference_date
        from
        `tabJournal Entry`
        inner join
        (
            select credit.parent as parent, debit_account,debit, credit_account,credit,
            concat_ws(' ',debit.party_name, credit.party_name) as party_name,
            concat_ws(' ',debit.party_type, credit.party_type) as party_type
            from (
                select  parent,  debit, account as debit_account, party_type, party_name from `tabJournal Entry lines` where debit <> 0
            ) as debit
            inner join
            (
                select parent, credit, account as credit_account, party_type, party_name from `tabJournal Entry lines` where credit <> 0
            ) as credit
            on debit.parent = credit.parent
        ) as entr_lines
        on entr_lines.parent = `tabJournal Entry`.name"""

    # entries = frappe.db.sql("select company, entry_date, reference_number, reference_date, party_type, party_name, credit, debit, account from `tabJournal Entry` inner join `tabJournal Entry lines` where company=%s", company)
    entries = frappe.db.sql(query)
    # entries = frappe.get_all('Journal Entry', filters={'Company': company}, fields=['company', 'entry_date', 'reference_number', 'reference_date'])
    print(entries)
    for i in entries:
        print(i)
    data = entries
    # columns, data = [], []
    return columns, data
