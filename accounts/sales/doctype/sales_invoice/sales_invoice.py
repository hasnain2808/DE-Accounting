# -*- coding: utf-8 -*-
# Copyright (c) 2020, Moha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import nowdate
from frappe import _, scrub
from frappe.utils import nowdate, now


class SalesInvoice(Document):
    def on_submit(self):
        # sales_account = frappe.get_list(
        #     "Account", filters={"company_name": self.company, "account_name": "Sales"}
        # )
        # print(sales_account)
        # debtors_account = frappe.get_list(
        #     "Account", filters={"company_name": self.company, "account_name": "Debtors"}
        # )
        # print(debtors_account)
        # JEl1 = {
        #     "credit": self.total_amount,
        #     "debit": 0,
        #     "account": sales_account[0].name,
        #     "party_type": "Customer",
        #     "party_name": self.customer,
        # }
        # JEl2 = {
        #     "credit": 0,
        #     "debit": self.total_amount,
        #     "account": debtors_account[0].name,
        # }
        # JE = frappe.get_doc(
        #     {
        #         "doctype": "Journal Entry",
        #         "company": self.company,
        #         "entry_date": self.posting_date,
        #         "entry_lines": [JEl1, JEl2],
        #     }
        # )
        # JE.insert()
        gl_entry = frappe.get_doc(
            {
                "doctype": "GL Entry",
                "posting_date": self.posting_date,
                "transaction_date": self.posting_date,
                "account": self.debit_account,
                "party_type": "Customer",
                "party": self.customer,
                "debit": self.total_amount,
                "credit": 0,
                "against": self.credit_account,
                "against_voucher": "Sales Invoice",
                "voucher_number": self.name,
                "company": self.company,
                "fiscal_year": "2020-2021"
            }
        )
        gl_entry.insert()
        gl_entry = frappe.get_doc(
            {
                "doctype": "GL Entry",
                "posting_date": self.posting_date,
                "transaction_date": self.posting_date,
                "account": self.credit_account,
                "party_type": "Customer",
                "party": self.customer,
                "debit": 0,
                "credit": self.total_amount,
                "against": self.debit_account,
                "against_voucher": "Sales Invoice",
                "voucher_number": self.name,
                "company": self.company,
                "fiscal_year": "2020-2021"
            }
        )
        gl_entry.insert()


    def on_cancel(self):
        frappe.db.sql("""update `tabGL Entry` set `is_cancelled` = 1,
            modified=%s, modified_by=%s
            where against_voucher=%s and voucher_number=%s and is_cancelled = 0""",
            (now(), frappe.session.user, "Sales Invoice", self.name))

        gl_entry = frappe.get_doc(
            {
                "doctype": "GL Entry",
                "posting_date": self.posting_date,
                "transaction_date": self.posting_date,
                "account": self.credit_account,
                "party_type": "Customer",
                "party": self.customer,
                "debit": self.total_amount,
                "credit": 0,
                "against": self.debit_account,
                "against_voucher": "Sales Invoice",
                "voucher_number": self.name,
                "company": self.company,
                "fiscal_year": "2020-2021",
                "is_cancelled" : 1
            }
        )
        gl_entry.insert()
        gl_entry = frappe.get_doc(
            {
                "doctype": "GL Entry",
                "posting_date": self.posting_date,
                "transaction_date": self.posting_date,
                "account": self.debit_account,
                "party_type": "Customer",
                "party": self.customer,
                "debit": 0,
                "credit": self.total_amount,
                "against": self.credit_account,
                "against_voucher": "Sales Invoice",
                "voucher_number": self.name,
                "company": self.company,
                "fiscal_year": "2020-2021",
                "is_cancelled" : 1
            }
        )
        gl_entry.insert()


@frappe.whitelist()
def get_payment_entry(dt, dn, party_amount=None, bank_account=None, bank_amount=None):
    doc = frappe.get_doc(dt, dn)

    debtors_account = frappe.get_list(
        "Account", filters={"company_name": doc.company, "account_name": "Debtors"},
    )
    print(debtors_account)
    bank_account = frappe.get_list(
        "Account",
        filters={"company_name": doc.company, "account_name": "Bank Accounts",},
    )
    chosen_bank_account = frappe.get_list(
        "Account",
        filters={"company_name": doc.company, "parent_account": bank_account[0].name},
    )

    print(doc)
    print("-" * 200)
    party_type = "Customer"
    payment_type = "Receive"
    total_amount = doc.get("total_amount")
    print(total_amount)
    pe = frappe.new_doc("Payment Entry")
    pe.payment_type = payment_type
    pe.company = doc.company
    pe.posting_date = nowdate()
    pe.party_type = party_type
    pe.party_name = doc.get(scrub(party_type))
    pe.total_amount = total_amount
    pe.debit_account = chosen_bank_account[0].name
    pe.credit_account = debtors_account[0].name
    pe.append(
        "reference",
        {
            "reference_type": "Sales Invoice",
            "reference_name": doc.get("name"),  # doc.get('purchase_invoice'),
            "total_amount": total_amount,
        },
    )
    print("-" * 200)
    print(pe)
    return pe

