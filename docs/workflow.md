# Workflow Notes

This project is a Zapier automation for processing custom e-commerce order items.

## Main flow

1. Receive an order through a webhook.
2. Loop through each line item.
3. Build a stable unique key using `order_id + line_item_id`.
4. Find or create the item in Zapier Tables.
5. Stop the workflow if the item was already processed.
6. Send only the free-text customization notes to AI.
7. Validate required fields and confidence.
8. Update the item record with the extracted values and validation result.
9. Route the item:
   - `approved` → ClickUp
   - `needs_review` → Slack

## AI extraction

The AI step extracts:

- material
- size
- engraving
- gift_box
- extraction_confidence

The prompt is designed not to guess missing values.

## Validation

The validation step checks:

- material is present
- size is present
- engraving is present
- extraction confidence is at least 0.80

If any required field is missing, the item is marked `needs_review`.

## Status tracking

The main statuses are:

- `processing`
- `extracted_and_validated`
- `task_created`
- `review_notified`
- `failed`

## Error handling

Native Zapier error handlers are used for:

- AI extraction failure
- ClickUp task creation failure
- Slack notification failure

Each error handler updates the same item record and sets `status = failed`.

## Production integration

Hoppscotch was used only to test the webhook during development.

A real store can replace the webhook test source with Shopify, WooCommerce, or another system that can send order data to Zapier.
