SELECT
    order_item_id,
    order_id,
    product_id,
    quantity::INTEGER AS quantity,
    unit_price::NUMERIC(12, 2) AS unit_price,
    discount_rate::NUMERIC(5, 4) AS discount_rate,
    (
        quantity * unit_price * (1 - discount_rate)
    )::NUMERIC(12, 2) AS line_revenue
FROM {{ source('raw', 'order_items') }}
