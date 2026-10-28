
WITH source AS (

    SELECT
        customer_id,
        customer_name,
        country,
        customer_segment,
        created_at
    FROM {{ source('raw', 'customers') }}

),

cleaned AS (

    SELECT
        customer_id,
        TRIM(customer_name) AS customer_name,
        TRIM(country) AS country,
        TRIM(customer_segment) AS customer_segment,
        created_at::DATE AS created_at
    FROM source

)

SELECT *
FROM cleaned
