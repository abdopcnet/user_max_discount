# API Structure

## Overview
User Max Discount app provides API methods for validating discount limits in Sales Order and Sales Invoice documents.

## API Methods

### Item Level Validation

#### validate_item_discount_percentage
- **Path**: `user_max_discount.user_max_discount.doctype.user_discount.user_discount.validate_item_discount_percentage`
- **Type**: Whitelisted
- **Parameters**:
  - `user` (optional): User email, defaults to session user
  - `company` (optional): Company name
  - `discount_percentage`: Discount percentage value to validate
- **Returns**: 
  ```json
  {
    "is_valid": bool,
    "message": str,
    "max_allowed": float or None
  }
  ```

#### validate_item_discount_amount
- **Path**: `user_max_discount.user_max_discount.doctype.user_discount.user_discount.validate_item_discount_amount`
- **Type**: Whitelisted
- **Parameters**:
  - `user` (optional): User email, defaults to session user
  - `company` (optional): Company name
  - `discount_amount`: Discount amount value to validate
  - `price_list_rate`: Price list rate for the item
  - `qty`: Quantity
- **Returns**: 
  ```json
  {
    "is_valid": bool,
    "message": str,
    "max_allowed": float or None,
    "calculated_percentage": float or None
  }
  ```

### Document Level Validation

#### validate_invoice_discount_percentage
- **Path**: `user_max_discount.user_max_discount.doctype.user_discount.user_discount.validate_invoice_discount_percentage`
- **Type**: Whitelisted
- **Parameters**:
  - `user` (optional): User email, defaults to session user
  - `company` (optional): Company name
  - `discount_percentage`: Discount percentage value to validate
- **Returns**: 
  ```json
  {
    "is_valid": bool,
    "message": str,
    "max_allowed": float or None
  }
  ```

#### validate_invoice_discount_amount
- **Path**: `user_max_discount.user_max_discount.doctype.user_discount.user_discount.validate_invoice_discount_amount`
- **Type**: Whitelisted
- **Parameters**:
  - `user` (optional): User email, defaults to session user
  - `company` (optional): Company name
  - `discount_amount`: Discount amount value to validate
  - `base_grand_total`: Base grand total for percentage calculation
- **Returns**: 
  ```json
  {
    "is_valid": bool,
    "message": str,
    "max_allowed": float or None,
    "calculated_percentage": float or None
  }
  ```

## Internal Functions

### _get_user_discount_limits
- **Path**: Internal function
- **Type**: Private
- **Parameters**:
  - `user`: User email
  - `company` (optional): Company name for filtering
- **Returns**: 
  ```json
  {
    "item_discount_percentage": float or None,
    "invoice_discount_percentage": float or None
  }
  ```

## Document Hooks

### validate_user_discount
- **Hook**: Document Event (validate)
- **Applied to**: Sales Order, Sales Invoice
- **Path**: `user_max_discount.user_max_discount.doctype.user_discount.user_discount.validate_user_discount`
- **Purpose**: Server-side validation on document save (draft/local only)

