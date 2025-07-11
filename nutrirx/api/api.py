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


def custom_on_update(doc, method):
    """Update custom stock fields in mr_items child table when saving Production Plan"""
    for item in doc.mr_items:
        if item.item_code and item.from_warehouse:
            # Get current balance from warehouse
            current_stock = get_balance_qty(item.item_code, item.from_warehouse)
            
            # Update custom fields
            item.custom_current_stock = current_stock
            item.custom_shortage_material = flt(current_stock) - flt(item.quantity)

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
