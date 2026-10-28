
WITH date_bounds AS (
    SELECT
        MIN(order_date) AS min_date,
        MAX(order_date) AS max_date
    FROM {{ ref('stg_orders') }}
),

calendar AS (
    SELECT
        generate_series(
            min_date,
            max_date,
            INTERVAL '1 day'
        )::DATE AS date_day
    FROM date_bounds
)

SELECT
    TO_CHAR(date_day, 'YYYYMMDD')::INTEGER AS date_key,
    date_day AS full_date,
    EXTRACT(YEAR FROM date_day)::INTEGER AS year,
    EXTRACT(QUARTER FROM date_day)::INTEGER AS quarter,
    EXTRACT(MONTH FROM date_day)::INTEGER AS month,
    TO_CHAR(date_day, 'TMMonth') AS month_name,
    EXTRACT(DAY FROM date_day)::INTEGER AS day_of_month,
    EXTRACT(ISODOW FROM date_day)::INTEGER AS day_of_week,
    TO_CHAR(date_day, 'TMDay') AS day_name,
    CASE
        WHEN EXTRACT(ISODOW FROM date_day) IN (6, 7)
        THEN TRUE
        ELSE FALSE
    END AS is_weekend
FROM calendar
