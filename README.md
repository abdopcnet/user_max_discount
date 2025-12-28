# User Max Discount

![Version](https://img.shields.io/badge/version-28.12.2025-blue)


Control discount limits for users in Sales Order and Sales Invoice documents.

## Features

- **User-Based Limits**: Set discount percentage limits per user
- **Item Level Validation**: Control discounts on individual items
- **Invoice Level Validation**: Control document-level discounts
- **Real-Time Validation**: Client-side validation on field changes
- **Server-Side Protection**: Validation hook on document save
- **Company Filtering**: Optional company-specific limits
- **Administrator Bypass**: Administrator has no restrictions

## Installation

```bash
bench get-app user_max_discount
bench --site [site] install-app user_max_discount
```

## Usage

1. Configure settings: Desk → User Discount
2. Add users to User Discount Table
3. Set Item Discount % and Invoice Discount % limits
4. Validation applies automatically in Sales Order/Invoice

## Supported Fields

**Items:**
- discount_percentage
- discount_amount

**Document:**
- additional_discount_percentage
- discount_amount

## License

MIT
