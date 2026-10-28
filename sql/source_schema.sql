
CREATE SCHEMA IF NOT EXISTS dw_raw;

CREATE TABLE IF NOT EXISTS dw_raw.customers (
    customer_id      INTEGER PRIMARY KEY,
    customer_name    VARCHAR(100) NOT NULL,
    country          VARCHAR(100) NOT NULL,
    customer_segment VARCHAR(50) NOT NULL,
    created_at       DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS dw_raw.products (
    product_id   INTEGER PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category     VARCHAR(100) NOT NULL,
    unit_cost    NUMERIC(12, 2) NOT NULL CHECK (unit_cost >= 0),
    list_price   NUMERIC(12, 2) NOT NULL CHECK (list_price >= 0)
);

CREATE TABLE IF NOT EXISTS dw_raw.orders (
    order_id    INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL
        REFERENCES dw_raw.customers(customer_id),
    order_date  DATE NOT NULL,
    status      VARCHAR(30) NOT NULL
);

CREATE TABLE IF NOT EXISTS dw_raw.order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id      INTEGER NOT NULL
        REFERENCES dw_raw.orders(order_id),
    product_id    INTEGER NOT NULL
        REFERENCES dw_raw.products(product_id),
    quantity      INTEGER NOT NULL CHECK (quantity > 0),
    unit_price    NUMERIC(12, 2) NOT NULL CHECK (unit_price >= 0),
    discount_rate NUMERIC(5, 4) NOT NULL
        CHECK (discount_rate >= 0 AND discount_rate <= 1)
);
