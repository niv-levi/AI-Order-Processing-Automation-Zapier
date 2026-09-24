# Workflow Details

This document explains the automation step by step.

## 1. Receive order data

The workflow starts with a webhook.

During development, Hoppscotch was used to send test orders.

In a real store, this can be replaced with Shopify, WooCommerce, or another order system.

## 2. Process each line item

An order can contain more than one product.

Looping by Zapier processes each line item separately so every item gets its own validation, status, and production result.

## 3. Build a unique item key

A short Python step combines:

```text
order_id + line_item_id
```

Example:

```text
ORD-1002_LI-2001
```

This key is used for duplicate protection.

## 4. Find or create the item record

Zapier Tables stores the processing log.

If the unique key already exists, the item is treated as a duplicate.

If it does not exist, a new record is created with:

```text
status = processing
```

## 5. Stop duplicates

The filter continues only when the item is new.

This prevents repeated webhook requests from creating duplicate AI calls, ClickUp tasks, or Slack messages.

## 6. Extract customization details with AI

Only the free-text customization note is sent to AI.

The AI returns structured fields:

- material
- size
- engraving
- gift_box
- extraction_confidence

The prompt is designed not to guess missing values.

## 7. Validate the result

The validation code checks:

- material is present
- size is present
- engraving is present
- extraction confidence is at least 0.80

Possible results:

```text
approved
needs_review
```

If a required field is missing, the result is `needs_review`.

## 8. Update the item record

The extracted values and validation result are saved in Zapier Tables.

The record is then marked:

```text
extracted_and_validated
```

## 9. Route the item

### Approved

If the item is approved:

- create a task in ClickUp
- save the ClickUp task ID
- set status to `task_created`

### Needs review

If information is missing:

- send a Slack message to `#order-review`
- include the original note
- include missing fields
- include the validation reason
- set status to `review_notified`

## 10. Error handling

Native Zapier error handlers are attached to:

- AI extraction
- ClickUp task creation
- Slack notification

If one of these actions fails, the same item record is updated to:

```text
status = failed
```

Other order data is left unchanged.

## Statuses used

```text
processing
extracted_and_validated
task_created
review_notified
failed
```

## Test scenarios

### Complete order

Input:

```text
Silver, 45cm, engraving NIV, gift box
```

Expected result:

```text
approved → ClickUp
```

### Missing size

Input:

```text
Gold, engraving Dana
```

Expected result:

```text
needs_review → Slack
```

### Duplicate

The same `order_id + line_item_id` is sent again.

Expected result:

```text
duplicate → stop before AI
```
