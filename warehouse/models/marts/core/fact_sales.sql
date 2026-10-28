
WITH order_items AS (
    SELECT
        order_item_id,
        order_id,
        product_id,
        quantity,
        unit_price,
        discount_rate,
        line_revenue
    FROM {{ ref('stg_order_items') }}
),

orders AS (
    SELECT
        order_id,
        customer_id,
        order_date,
        status
    FROM {{ ref('stg_orders') }}
)

SELECT
    oi.order_item_id,
    o.order_id,
    o.customer_id,
    oi.product_id,
    TO_CHAR(o.order_date, 'YYYYMMDD')::INTEGER AS date_key,
    o.order_date,
    o.status,
    oi.quantity,
    oi.unit_price,
    oi.discount_rate,
    oi.line_revenue,
    (oi.quantity * oi.unit_price)::NUMERIC(12, 2) AS gross_revenue
FROM order_items AS oi
INNER JOIN orders AS o
    ON oi.order_id = o.order_id
