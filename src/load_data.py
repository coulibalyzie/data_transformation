
import csv
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data" / "raw"

load_dotenv(ROOT_DIR / ".env")

TABLES = {
    "customers": [
        "customer_id",
        "customer_name",
        "country",
        "customer_segment",
        "created_at",
    ],
    "products": [
        "product_id",
        "product_name",
        "category",
        "unit_cost",
        "list_price",
    ],
    "orders": [
        "order_id",
        "customer_id",
        "order_date",
        "status",
    ],
    "order_items": [
        "order_item_id",
        "order_id",
        "product_id",
        "quantity",
        "unit_price",
        "discount_rate",
    ],
}


def read_csv(filename):
    """Lit un CSV UTF-8 et retourne ses lignes sous forme de dictionnaires."""
    path = DATA_DIR / filename

    with path.open("r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def load_table(cursor, table_name, columns, rows):
    """Charge les données d'une table dans le schéma dw_raw."""
    if not rows:
        raise ValueError(f"Aucune donnée trouvée pour {table_name}.")

    column_sql = ", ".join(columns)
    placeholders = ", ".join(["%s"] * len(columns))

    query = (
        f"INSERT INTO dw_raw.{table_name} ({column_sql}) "
        f"VALUES ({placeholders})"
    )

    values = [
        tuple(row[column] for column in columns)
        for row in rows
    ]

    cursor.executemany(query, values)
    print(f"{table_name} : {len(rows)} lignes insérées")


def main():
    required_vars = [
        "POSTGRES_HOST",
        "POSTGRES_PORT",
        "POSTGRES_DB",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
    ]

    missing = [
        name for name in required_vars
        if not os.getenv(name)
    ]

    if missing:
        raise RuntimeError(
            "Variables absentes du fichier .env : "
            + ", ".join(missing)
        )

    connection_params = {
        "host": os.environ["POSTGRES_HOST"],
        "port": os.environ["POSTGRES_PORT"],
        "dbname": os.environ["POSTGRES_DB"],
        "user": os.environ["POSTGRES_USER"],
        "password": os.environ["POSTGRES_PASSWORD"],
    }

    datasets = {
        "customers": read_csv("customers.csv"),
        "products": read_csv("products.csv"),
        "orders": read_csv("orders.csv"),
        "order_items": read_csv("order_items.csv"),
    }

    # La connexion est transactionnelle : une exception annule
    # les insertions de cette exécution.
    with psycopg.connect(**connection_params) as connection:
        with connection.cursor() as cursor:
            # Évite de mélanger les données si le script est relancé.
            # Les tables sources de ce projet sont dédiées à ce chargement.
            cursor.execute(
                """
                TRUNCATE TABLE
                    dw_raw.order_items,
                    dw_raw.orders,
                    dw_raw.products,
                    dw_raw.customers
                """
            )

            for table_name, columns in TABLES.items():
                load_table(
                    cursor,
                    table_name,
                    columns,
                    datasets[table_name],
                )

    print("\nChargement terminé avec succès.")


if __name__ == "__main__":
    main()
