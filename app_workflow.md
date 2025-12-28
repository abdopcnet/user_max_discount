# Workflow Diagram

## Discount Validation Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    User Enters Discount                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
        ┌─────────────────────────────┐
        │  Document State Check       │
        │  (docstatus === 0           │
        │   or __islocal === true)    │
        └─────┬───────────────────────┘
              │
              ▼ (Yes)
┌─────────────────────────────────────────────────────────────┐
│              Client Script Triggers                         │
│  (Sales Order Item / Sales Invoice Item /                   │
│   Sales Order / Sales Invoice field events)                 │
└─────┬───────────────────────────────────────────────────────┘
      │
      ├─► discount_percentage ──► validate_item_discount_percentage()
      ├─► discount_amount ──────► validate_item_discount_amount()
      ├─► additional_discount_percentage ──► validate_invoice_discount_percentage()
      └─► discount_amount ──────► validate_invoice_discount_amount()
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│              API Call (Independent)                         │
│  user_max_discount...validate_*_discount_*                  │
└─────┬───────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│        _get_user_discount_limits()                          │
│  - Get User Discount single doctype                         │
│  - Filter by company (if set)                               │
│  - Find user in user_discount_table                         │
└─────┬───────────────────────────────────────────────────────┘
      │
      ├─► User Not Found ──► Return None (No Limits)
      └─► User Found ──────► Return Limits
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│              Validation Check                               │
│  Compare entered discount vs user limit                     │
└─────┬───────────────────────────────────────────────────────┘
      │
      ├─► Valid ──────► Allow Value
      └─► Invalid ────► Show Error + Clear Value
```

## Server-Side Validation Flow

```
┌─────────────────────────────────────────────────────────────┐
│              Document Save (validate hook)                  │
└─────┬───────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│        validate_user_discount()                             │
│  - Check docstatus === 0 and __islocal                      │
│  - Skip Administrator                                        │
│  - Get user limits                                           │
└─────┬───────────────────────────────────────────────────────┘
      │
      ├─► Item Level Validation
      │   ├─► discount_percentage check
      │   └─► discount_amount (calculate %) check
      │
      └─► Document Level Validation
          ├─► additional_discount_percentage check
          └─► discount_amount (calculate %) check
              │
              ▼
      ┌───────────────┐
      │ All Valid?    │
      └───┬───────┬───┘
          │       │
       Yes│       │No
          │       │
          ▼       ▼
      Allow   Throw Error
      Save    (Block Save)
```

## Settings Configuration Flow

```
┌─────────────────────────────────────────────────────────────┐
│              User Discount Settings                         │
│  (Single DocType)                                           │
└─────┬───────────────────────────────────────────────────────┘
      │
      ├─► Company (optional filter)
      │
      └─► User Discount Table (child table)
          ├─► User (Link)
          ├─► Item Discount Percentage
          └─► Invoice Discount Percentage
```

