order_id = input_data["order_id"]
line_item_id = input_data["line_item_id"]

output = {
    "unique_key": f"{order_id}_{line_item_id}"
}
