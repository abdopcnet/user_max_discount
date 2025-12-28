# API Structure

## Whitelisted Methods

### Item Level

-   `validate_item_discount_percentage` - Validate item discount percentage
-   `validate_item_discount_amount` - Validate item discount amount (converts to %)

### Invoice Level

-   `validate_invoice_discount_percentage` - Validate invoice discount percentage
-   `validate_invoice_discount_amount` - Validate invoice discount amount (converts to %)

## Internal Functions

-   `_get_user_discount_limits` - Get user discount limits from settings
-   `validate_user_discount` - Server-side validation hook (Sales Order/Invoice)

## Response Format

```json
{
  "is_valid": bool,
  "message": str,
  "max_allowed": float,
  "calculated_percentage": float  // for amount validations
}
```
