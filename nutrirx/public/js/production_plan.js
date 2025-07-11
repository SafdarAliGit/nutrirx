// myapp/public/js/production_plan.js

frappe.ui.form.on("Production Plan", {
    // setup: function(frm) {
    //     frm.add_fetch("from_warehouse", "from_warehouse", "temp_wh");
    // }
});

frappe.ui.form.on("Material Request Plan Item", {
    from_warehouse: function(frm, cdt, cdn) {
        set_current_stock(frm, cdt, cdn);
    },
    item_code: function(frm, cdt, cdn) {
        set_current_stock(frm, cdt, cdn);
    }
});

function set_current_stock(frm, cdt, cdn) {
    let d = locals[cdt][cdn];
    if (d.item_code && d.from_warehouse) {
        frappe.call({
            method: "nutrirx.api.get_balance_qty",
            args: {
                item_code: d.item_code,
                warehouse: d.from_warehouse
            },
            callback: function(r) {
                if (r.message !== undefined) {
                    frappe.model.set_value(cdt, cdn, "custom_current_stock", r.message);
                    frappe.model.set_value(cdt, cdn, "custom_shortage_material", r.message - d.quantity);
                }
            }
        });
    }
}
