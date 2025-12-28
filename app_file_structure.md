# File Structure

```
user_max_discount/
├── user_max_discount/
│   ├── hooks.py                           # DocType hooks, client scripts
│   ├── user_max_discount/
│   │   ├── doctype/
│   │   │   ├── user_discount/            # Settings DocType
│   │   │   │   ├── user_discount.py      # API methods, validation
│   │   │   │   ├── user_discount.js      # Client script
│   │   │   │   └── user_discount.json
│   │   │   └── user_discount_table/      # Child table
│   │   └── workspace/
│   └── public/js/
│       ├── sales_order.js                # Client validation
│       └── sales_invoice.js              # Client validation
├── README.md
└── [documentation files]
```

## Key Files
- `user_discount.py` - All API methods and server validation
- `sales_order.js` / `sales_invoice.js` - Client-side validation handlers
- `hooks.py` - Event hooks configuration
