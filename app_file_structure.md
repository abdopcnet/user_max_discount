# File Structure

## Directory Tree

```
user_max_discount/
├── user_max_discount/
│   ├── hooks.py
│   ├── modules.txt
│   ├── patches.txt
│   ├── user_max_discount/
│   │   ├── __init__.py
│   │   ├── doctype/
│   │   │   ├── __init__.py
│   │   │   ├── user_discount/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── user_discount.py
│   │   │   │   ├── user_discount.json
│   │   │   │   └── user_discount.js
│   │   │   └── user_discount_table/
│   │   │       ├── __init__.py
│   │   │       ├── user_discount_table.py
│   │   │       └── user_discount_table.json
│   │   └── workspace/
│   ├── public/
│   │   └── js/
│   │       ├── sales_order.js
│   │       └── sales_invoice.js
│   └── templates/
├── license.txt
├── pyproject.toml
├── README.md
├── app_api_tree.md
├── app_file_structure.md
├── app_workflow.md
└── app_plan.md
```

## Key Files

### Configuration
- `hooks.py` - App hooks configuration (doc_events, doctype_js)
- `modules.txt` - Module definition

### DocTypes
- `user_discount/` - Single DocType for discount settings
- `user_discount_table/` - Child table for user discount limits

### Client Scripts
- `public/js/sales_order.js` - Client-side validation for Sales Order
- `public/js/sales_invoice.js` - Client-side validation for Sales Invoice

## File Descriptions

### user_discount.py
- Contains UserDiscount class with validate method
- API methods for discount validation
- Server-side validation function

### sales_order.js / sales_invoice.js
- Client-side event handlers
- Real-time validation on field changes
- Independent API calls per field

