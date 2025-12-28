# Copyright (c) 2025, Hadeel NRD and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class UserDiscount(Document):
	def validate(self):
		"""Validate that each user appears only once in the table"""
		users = []
		for row in self.user_discount_table or []:
			if row.user:
				if row.user in users:
					frappe.throw(
						_("User {0} appears multiple times in the table. Each user should appear only once.").format(
							frappe.bold(row.user)
						)
					)
				users.append(row.user)
				
				# Validate percentages are between 0-100
				if row.item_discount_percentage and (flt(row.item_discount_percentage) < 0 or flt(row.item_discount_percentage) > 100):
					frappe.throw(
						_("Item Discount Percentage for user {0} must be between 0 and 100.").format(
							frappe.bold(row.user)
						)
					)
				
				if row.invoice_discount_percentage and (flt(row.invoice_discount_percentage) < 0 or flt(row.invoice_discount_percentage) > 100):
					frappe.throw(
						_("Invoice Discount Percentage for user {0} must be between 0 and 100.").format(
							frappe.bold(row.user)
						)
					)


def _get_user_discount_limits(user, company=None):
	"""
	Internal function to get user discount limits from User Discount settings
	
	Args:
		user: User email
		company: Company name (optional, for filtering)
	
	Returns:
		dict: {
			'item_discount_percentage': float or None,
			'invoice_discount_percentage': float or None
		}
	"""
	try:
		user_discount = frappe.get_single("User Discount")
		
		# Filter by company if provided and company is set in settings
		if company and user_discount.company and user_discount.company != company:
			return {'item_discount_percentage': None, 'invoice_discount_percentage': None}
		
		# Search for user in the table
		for row in user_discount.user_discount_table or []:
			if row.user == user:
				return {
					'item_discount_percentage': flt(row.item_discount_percentage) if row.item_discount_percentage else None,
					'invoice_discount_percentage': flt(row.invoice_discount_percentage) if row.invoice_discount_percentage else None
				}
		
		# User not found in table - no limits (unrestricted)
		return {'item_discount_percentage': None, 'invoice_discount_percentage': None}
		
	except Exception as e:
		frappe.log_error('[user_discount.py] method: _get_user_discount_limits', 'User Discount')
		# If error, return None (no restrictions)
		return {'item_discount_percentage': None, 'invoice_discount_percentage': None}


@frappe.whitelist()
def validate_item_discount_percentage(user=None, company=None, discount_percentage=None):
	"""
	Validate item discount_percentage against user's item_discount_percentage limit
	
	Args:
		user: User email (defaults to current session user)
		company: Company name
		discount_percentage: Discount percentage value to validate
	
	Returns:
		dict: {
			'is_valid': bool,
			'message': str,
			'max_allowed': float or None
		}
	"""
	if not user:
		user = frappe.session.user
	
	# Skip Administrator
	if user == "Administrator":
		return {'is_valid': True, 'message': '', 'max_allowed': None}
	
	# Get user limits
	limits = _get_user_discount_limits(user, company)
	item_limit = limits.get('item_discount_percentage')
	
	# If no limit set, allow any discount
	if item_limit is None:
		return {'is_valid': True, 'message': '', 'max_allowed': None}
	
	# Validate
	discount_pct = flt(discount_percentage) if discount_percentage else 0
	
	if discount_pct > item_limit:
		return {
			'is_valid': False,
			'message': _("Max Allowed Discount on Item is {0}%.").format(item_limit),
			'max_allowed': item_limit
		}
	
	return {'is_valid': True, 'message': '', 'max_allowed': item_limit}


@frappe.whitelist()
def validate_item_discount_amount(user=None, company=None, discount_amount=None, price_list_rate=None, qty=None):
	"""
	Validate item discount_amount by calculating percentage and checking against user's item_discount_percentage limit
	
	Args:
		user: User email (defaults to current session user)
		company: Company name
		discount_amount: Discount amount value to validate
		price_list_rate: Price list rate for the item
		qty: Quantity
	
	Returns:
		dict: {
			'is_valid': bool,
			'message': str,
			'max_allowed': float or None,
			'calculated_percentage': float or None
		}
	"""
	if not user:
		user = frappe.session.user
	
	# Skip Administrator
	if user == "Administrator":
		return {'is_valid': True, 'message': '', 'max_allowed': None, 'calculated_percentage': None}
	
	# Get user limits
	limits = _get_user_discount_limits(user, company)
	item_limit = limits.get('item_discount_percentage')
	
	# If no limit set, allow any discount
	if item_limit is None:
		return {'is_valid': True, 'message': '', 'max_allowed': None, 'calculated_percentage': None}
	
	# Calculate percentage from amount
	discount_amt = flt(discount_amount) if discount_amount else 0
	price_rate = flt(price_list_rate) if price_list_rate else 0
	quantity = flt(qty) if qty else 0
	
	if price_rate <= 0 or quantity <= 0:
		return {'is_valid': True, 'message': '', 'max_allowed': item_limit, 'calculated_percentage': 0}
	
	total_item_price = price_rate * quantity
	if total_item_price <= 0:
		return {'is_valid': True, 'message': '', 'max_allowed': item_limit, 'calculated_percentage': 0}
	
	calculated_percentage = (discount_amt / total_item_price) * 100
	
	# Validate calculated percentage
	if calculated_percentage > item_limit:
		return {
			'is_valid': False,
			'message': _("Max Allowed Discount on Item is {0}%.").format(item_limit),
			'max_allowed': item_limit,
			'calculated_percentage': calculated_percentage
		}
	
	return {'is_valid': True, 'message': '', 'max_allowed': item_limit, 'calculated_percentage': calculated_percentage}


@frappe.whitelist()
def validate_invoice_discount_percentage(user=None, company=None, discount_percentage=None):
	"""
	Validate invoice additional_discount_percentage against user's invoice_discount_percentage limit
	
	Args:
		user: User email (defaults to current session user)
		company: Company name
		discount_percentage: Discount percentage value to validate
	
	Returns:
		dict: {
			'is_valid': bool,
			'message': str,
			'max_allowed': float or None
		}
	"""
	if not user:
		user = frappe.session.user
	
	# Skip Administrator
	if user == "Administrator":
		return {'is_valid': True, 'message': '', 'max_allowed': None}
	
	# Get user limits
	limits = _get_user_discount_limits(user, company)
	invoice_limit = limits.get('invoice_discount_percentage')
	
	# If no limit set, allow any discount
	if invoice_limit is None:
		return {'is_valid': True, 'message': '', 'max_allowed': None}
	
	# Validate
	discount_pct = flt(discount_percentage) if discount_percentage else 0
	
	if discount_pct > invoice_limit:
		return {
			'is_valid': False,
			'message': _("Max Allowed Discount on Invoice is {0}%.").format(invoice_limit),
			'max_allowed': invoice_limit
		}
	
	return {'is_valid': True, 'message': '', 'max_allowed': invoice_limit}


@frappe.whitelist()
def validate_invoice_discount_amount(user=None, company=None, discount_amount=None, base_grand_total=None):
	"""
	Validate invoice discount_amount by calculating percentage and checking against user's invoice_discount_percentage limit
	
	Args:
		user: User email (defaults to current session user)
		company: Company name
		discount_amount: Discount amount value to validate
		base_grand_total: Base grand total for percentage calculation
	
	Returns:
		dict: {
			'is_valid': bool,
			'message': str,
			'max_allowed': float or None,
			'calculated_percentage': float or None
		}
	"""
	if not user:
		user = frappe.session.user
	
	# Skip Administrator
	if user == "Administrator":
		return {'is_valid': True, 'message': '', 'max_allowed': None, 'calculated_percentage': None}
	
	# Get user limits
	limits = _get_user_discount_limits(user, company)
	invoice_limit = limits.get('invoice_discount_percentage')
	
	# If no limit set, allow any discount
	if invoice_limit is None:
		return {'is_valid': True, 'message': '', 'max_allowed': None, 'calculated_percentage': None}
	
	# Calculate percentage from amount
	discount_amt = flt(discount_amount) if discount_amount else 0
	grand_total = flt(base_grand_total) if base_grand_total else 0
	
	if grand_total <= 0 and discount_amt <= 0:
		return {'is_valid': True, 'message': '', 'max_allowed': invoice_limit, 'calculated_percentage': 0}
	
	# Calculate percentage: discount_amount / (base_grand_total + discount_amount) * 100
	total_with_discount = grand_total + discount_amt
	if total_with_discount <= 0:
		return {'is_valid': True, 'message': '', 'max_allowed': invoice_limit, 'calculated_percentage': 0}
	
	calculated_percentage = (discount_amt / total_with_discount) * 100
	
	# Validate calculated percentage
	if calculated_percentage > invoice_limit:
		return {
			'is_valid': False,
			'message': _("Max Allowed Discount on Invoice is {0}%.").format(invoice_limit),
			'max_allowed': invoice_limit,
			'calculated_percentage': calculated_percentage
		}
	
	return {'is_valid': True, 'message': '', 'max_allowed': invoice_limit, 'calculated_percentage': calculated_percentage}


def validate_user_discount(doc, method):
	"""
	Validate discount limits for current user in Sales Order and Sales Invoice
	Works only on draft/local documents
	"""
	# Skip if document is submitted or cancelled
	if doc.docstatus != 0:
		return
	
	# Skip if not local (already saved to DB)
	if not doc.get("__islocal"):
		return
	
	# Skip Administrator
	current_user = frappe.session.user
	if current_user == "Administrator":
		return
	
	# Get user limits
	limits = _get_user_discount_limits(current_user, doc.company)
	
	# Validate item-level discounts
	if limits.get('item_discount_percentage') is not None:
		item_limit = limits['item_discount_percentage']
		
		for item in doc.get("items") or []:
			# Validate discount_percentage
			if item.get("discount_percentage"):
				discount_pct = flt(item.discount_percentage)
				if discount_pct > item_limit:
					frappe.throw(
						_("Max Allowed Discount on Item is {0}%.").format(item_limit),
						title=_("Discount Limit Exceeded")
					)
			
			# Validate discount_amount
			if item.get("discount_amount") and item.get("price_list_rate") and item.get("qty"):
				discount_amt = flt(item.discount_amount)
				price_rate = flt(item.price_list_rate)
				quantity = flt(item.qty)
				
				if price_rate > 0 and quantity > 0:
					total_item_price = price_rate * quantity
					if total_item_price > 0:
						calculated_pct = (discount_amt / total_item_price) * 100
						if calculated_pct > item_limit:
							frappe.throw(
								_("Max Allowed Discount on Item is {0}%.").format(item_limit),
								title=_("Discount Limit Exceeded")
							)
	
	# Validate document-level discounts
	if limits.get('invoice_discount_percentage') is not None:
		invoice_limit = limits['invoice_discount_percentage']
		
		# Validate additional_discount_percentage
		if doc.get("additional_discount_percentage"):
			discount_pct = flt(doc.additional_discount_percentage)
			if discount_pct > invoice_limit:
				frappe.throw(
					_("Max Allowed Discount on Invoice is {0}%.").format(invoice_limit),
					title=_("Discount Limit Exceeded")
				)
		
		# Validate discount_amount
		if doc.get("discount_amount") and doc.get("base_grand_total"):
			discount_amt = flt(doc.discount_amount)
			grand_total = flt(doc.base_grand_total)
			
			if grand_total > 0 or discount_amt > 0:
				total_with_discount = grand_total + discount_amt
				if total_with_discount > 0:
					calculated_pct = (discount_amt / total_with_discount) * 100
					if calculated_pct > invoice_limit:
						frappe.throw(
							_("Max Allowed Discount on Invoice is {0}%.").format(invoice_limit),
							title=_("Discount Limit Exceeded")
						)
