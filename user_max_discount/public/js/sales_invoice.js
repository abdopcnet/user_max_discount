// Copyright (c) 2025, Hadeel NRD and contributors
// For license information, please see license.txt

// Item Level - Sales Invoice Item
frappe.ui.form.on("Sales Invoice Item", {
	discount_percentage: function(frm, cdt, cdn) {
		if (frm.doc.docstatus === 0 || frm.doc.__islocal) {
			let row = frappe.get_doc(cdt, cdn);
			if (row.discount_percentage) {
				validate_item_discount_percentage_si(frm, row.discount_percentage, cdt, cdn);
			}
		}
	},
	
	discount_amount: function(frm, cdt, cdn) {
		if (frm.doc.docstatus === 0 || frm.doc.__islocal) {
			let row = frappe.get_doc(cdt, cdn);
			if (row.discount_amount) {
				validate_item_discount_amount_si(frm, row.discount_amount, row.price_list_rate, row.qty, cdt, cdn);
			}
		}
	}
});

// Document Level - Sales Invoice
frappe.ui.form.on("Sales Invoice", {
	additional_discount_percentage: function(frm) {
		if (frm.doc.docstatus === 0 || frm.doc.__islocal) {
			if (frm.doc.additional_discount_percentage) {
				validate_invoice_discount_percentage_si(frm, frm.doc.additional_discount_percentage);
			}
		}
	},
	
	discount_amount: function(frm) {
		if (frm.doc.docstatus === 0 || frm.doc.__islocal) {
			if (frm.doc.discount_amount) {
				validate_invoice_discount_amount_si(frm, frm.doc.discount_amount, frm.doc.base_grand_total);
			}
		}
	}
});

// Independent validation functions - each makes its own API call
function validate_item_discount_percentage_si(frm, value, cdt, cdn) {
	frappe.call({
		method: "user_max_discount.user_max_discount.doctype.user_discount.user_discount.validate_item_discount_percentage",
		args: {
			user: frappe.session.user,
			company: frm.doc.company,
			discount_percentage: value
		},
		callback: function(r) {
			if (r.message && !r.message.is_valid) {
				frappe.msgprint({
					message: r.message.message || "Discount not allowed",
					indicator: "red",
					title: "Discount Limit Exceeded"
				});
				frappe.model.set_value(cdt, cdn, "discount_percentage", 0);
			}
		},
		error: function(err) {
			console.log('[Sales Invoice Item] method: validate_item_discount_percentage');
		}
	});
}

function validate_item_discount_amount_si(frm, amount, price_list_rate, qty, cdt, cdn) {
	frappe.call({
		method: "user_max_discount.user_max_discount.doctype.user_discount.user_discount.validate_item_discount_amount",
		args: {
			user: frappe.session.user,
			company: frm.doc.company,
			discount_amount: amount,
			price_list_rate: price_list_rate,
			qty: qty
		},
		callback: function(r) {
			if (r.message && !r.message.is_valid) {
				frappe.msgprint({
					message: r.message.message || "Discount not allowed",
					indicator: "red",
					title: "Discount Limit Exceeded"
				});
				frappe.model.set_value(cdt, cdn, "discount_amount", 0);
			}
		},
		error: function(err) {
			console.log('[Sales Invoice Item] method: validate_item_discount_amount');
		}
	});
}

function validate_invoice_discount_percentage_si(frm, value) {
	frappe.call({
		method: "user_max_discount.user_max_discount.doctype.user_discount.user_discount.validate_invoice_discount_percentage",
		args: {
			user: frappe.session.user,
			company: frm.doc.company,
			discount_percentage: value
		},
		callback: function(r) {
			if (r.message && !r.message.is_valid) {
				frappe.msgprint({
					message: r.message.message || "Discount not allowed",
					indicator: "red",
					title: "Discount Limit Exceeded"
				});
				frm.set_value("additional_discount_percentage", 0);
			}
		},
		error: function(err) {
			console.log('[Sales Invoice] method: validate_invoice_discount_percentage');
		}
	});
}

function validate_invoice_discount_amount_si(frm, amount, base_grand_total) {
	frappe.call({
		method: "user_max_discount.user_max_discount.doctype.user_discount.user_discount.validate_invoice_discount_amount",
		args: {
			user: frappe.session.user,
			company: frm.doc.company,
			discount_amount: amount,
			base_grand_total: base_grand_total
		},
		callback: function(r) {
			if (r.message && !r.message.is_valid) {
				frappe.msgprint({
					message: r.message.message || "Discount not allowed",
					indicator: "red",
					title: "Discount Limit Exceeded"
				});
				frm.set_value("discount_amount", 0);
			}
		},
		error: function(err) {
			console.log('[Sales Invoice] method: validate_invoice_discount_amount');
		}
	});
}

