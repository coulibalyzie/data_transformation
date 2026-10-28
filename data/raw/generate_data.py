
import csv
import random
from datetime import date, timedelta
from pathlib import Path

# Reproductibilité : les données seront identiques à chaque exécution.
random.seed(42)

OUTPUT_DIR = Path(__file__).resolve().parent

# 1. Clients
countries = ["France", "Belgique", "Allemagne", "Espagne", "Italie"]
segments = ["Particulier", "PME", "Grande entreprise"]

customers = []

for customer_id in range(1, 31):
    customers.append({
        "customer_id": customer_id,
        "customer_name": f"Client {customer_id:03d}",
        "country": random.choice(countries),
        "customer_segment": random.choice(segments),
        "created_at": date(2024, 1, 1) + timedelta(
            days=random.randint(0, 730)
        ),
    })

# 2. Produits
catalogue = [
    ("Ordinateur portable Pro", "Ordinateurs", 650, 999),
    ("Ordinateur portable Air", "Ordinateurs", 480, 749),
    ("Écran 24 pouces", "Écrans", 90, 159),
    ("Écran 27 pouces", "Écrans", 150, 279),
    ("Clavier mécanique", "Accessoires", 45, 89),
    ("Souris sans fil", "Accessoires", 15, 35),
    ("Station d'accueil USB-C", "Accessoires", 70, 129),
    ("Casque professionnel", "Audio", 35, 79),
    ("Webcam HD", "Audio", 25, 59),
    ("Disque SSD 1 To", "Stockage", 55, 99),
    ("Disque SSD 2 To", "Stockage", 95, 169),
    ("Disque dur externe", "Stockage", 40, 79),
    ("Routeur Wi-Fi", "Réseau", 60, 119),
    ("Switch réseau", "Réseau", 45, 95),
    ("Tablette professionnelle", "Tablettes", 280, 499),
]

products = []

for product_id, (name, category, cost, price) in enumerate(catalogue, start=1):
    products.append({
        "product_id": product_id,
        "product_name": name,
        "category": category,
        "unit_cost": cost,
        "list_price": price,
    })

# 3. Commandes
orders = []
order_items = []
start_date = date(2025, 1, 1)

for order_id in range(1, 201):
    order_date = start_date + timedelta(days=random.randint(0, 364))

    orders.append({
        "order_id": order_id,
        "customer_id": random.randint(1, len(customers)),
        "order_date": order_date,
        "status": random.choices(
            ["Livrée", "Expédiée", "En préparation", "Annulée"],
            weights=[70, 15, 10, 5],
            k=1,
        )[0],
    })

    # Une commande contient entre 1 et 4 produits différents.
    selected_products = random.sample(
        products,
        k=random.randint(1, 4),
    )

    for product in selected_products:
        order_items.append({
            "order_item_id": len(order_items) + 1,
            "order_id": order_id,
            "product_id": product["product_id"],
            "quantity": random.randint(1, 5),
            "unit_price": product["list_price"],
            "discount_rate": random.choice([0, 0, 0, 0.05, 0.10, 0.15]),
        })


def write_csv(filename, rows):
    """Écrit une liste de dictionnaires dans un fichier CSV."""
    path = OUTPUT_DIR / filename

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"{filename} : {len(rows)} lignes générées")


if __name__ == "__main__":
    write_csv("customers.csv", customers)
    write_csv("products.csv", products)
    write_csv("orders.csv", orders)
    write_csv("order_items.csv", order_items)

    print("\nGénération terminée.")
