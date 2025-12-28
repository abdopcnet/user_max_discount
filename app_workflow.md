# Workflow

## Validation Flow

```
User Input → Client Script → API Call → Check Limits → Validate/Error
     ↓
Document Save → Server Hook → Validate All → Allow/Block
```

## Settings Configuration

```
User Discount (Single DocType)
├── Company (optional filter)
└── User Discount Table (child)
    ├── User
    ├── Item Discount % Limit
    └── Invoice Discount % Limit
```

## Validation Rules
- Works only on draft/local documents
- Administrator bypassed
- Company filtering (optional)
- Item level: discount_percentage, discount_amount
- Invoice level: additional_discount_percentage, discount_amount
