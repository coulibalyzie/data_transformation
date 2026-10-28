SELECT
    product_id,
    TRIM(product_name) AS product_name,
    TRIM(category) AS category,
    unit_cost::NUMERIC(12, 2) AS unit_cost,
    list_price::NUMERIC(12, 2) AS list_price
FROM {{ source('raw', 'products') }}
