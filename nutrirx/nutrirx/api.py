# myapp/api.py
import frappe
from frappe.utils import flt

@frappe.whitelist()
def get_balance_qty(item_code, warehouse):
    """Return current balance quantity of an item in a specific warehouse."""
    balance = frappe.db.sql("""
        SELECT qty_after_transaction
          FROM `tabStock Ledger Entry`
         WHERE item_code=%s
           AND warehouse=%s
           AND is_cancelled=0
         ORDER BY posting_datetime DESC, creation DESC
         LIMIT 1
    """, (item_code, warehouse))

    return flt(balance[0][0]) if balance else 0.0
