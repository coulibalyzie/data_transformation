SELECT
    COUNT(DISTINCT order_id) AS delivered_orders,
    SUM(quantity) AS units_sold,
    ROUND(SUM(line_revenue), 2) AS net_revenue,
    ROUND(SUM(gross_revenue - line_revenue), 2) AS discounts_amount,
    ROUND(
        SUM(line_revenue) / NULLIF(COUNT(DISTINCT order_id), 0),
        2
    ) AS average_order_value
FROM {{ ref('fact_sales') }}
WHERE status = 'Livrée'
