SELECT
    order_id,
    customer_id,
    order_date::DATE AS order_date,
    TRIM(status) AS status
FROM {{ source('raw', 'orders') }}
