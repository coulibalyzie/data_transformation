SELECT
    product_id,
    product_name,
    category,
    unit_cost,
    list_price
FROM {{ ref('stg_products') }}

