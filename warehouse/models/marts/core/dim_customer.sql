WITH customers AS (

    SELECT
        customer_id,
        customer_name,
        country,
        customer_segment,
        created_at
    FROM {{ ref('stg_customers') }}

)

SELECT
    customer_id,
    customer_name,
    country,
    customer_segment,
    created_at
FROM customers
