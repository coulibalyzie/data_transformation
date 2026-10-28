# Sales Data Warehouse & Analytics

**Projet de Data Engineering et Analytics Engineering** : construire un entrepôt de données à partir de données commerciales synthétiques, les transformer avec dbt, tester leur qualité et exploiter les résultats dans Power BI.

## Présentation

Ce projet simule le système analytique d'un distributeur fictif de matériel informatique. Il met en œuvre une chaîne de traitement allant de la génération des données à la création d'indicateurs commerciaux.

Les données sont générées artificiellement à des fins pédagogiques. Elles ne proviennent pas d'une entreprise réelle.

### Objectifs

- Concevoir et alimenter une couche de données sources dans PostgreSQL.
- Modéliser un entrepôt de données selon une architecture en étoile.
- Transformer les données avec dbt et SQL.
- Contrôler la qualité des données à l'aide de tests automatisés.
- Construire des indicateurs commerciaux fiables.
- Visualiser les résultats dans un tableau de bord Power BI.

## Architecture

```text
Données synthétiques (CSV)
          |
          v
     Python / Pandas
          |
          v
PostgreSQL — Schéma dw_raw
          |
          v
   dbt : transformations SQL
          |
          v
PostgreSQL — Schéma analytics
          |
          v
       Power BI
          |
          v
Tableau de bord commercial
```

### Modèle de données

L'entrepôt repose sur une architecture en étoile, organisée autour d'une table de faits et de dimensions descriptives.

- **`fact_sales`** : lignes de commande, quantités, prix, remises, revenus et statut.
- **`dim_customer`** : informations sur les clients, leur pays et leur segment.
- **`dim_product`** : catalogue des produits, catégories et prix.
- **`dim_date`** : calendrier permettant les analyses temporelles.
- **`mart_sales_performance`** : indicateurs agrégés sur les commandes livrées.

Les modèles intermédiaires de staging assurent la préparation des données sources avant leur exploitation analytique.

## Technologies

| Technologie | Utilisation |
|---|---|
| Python | Génération et chargement des données |
| Pandas | Manipulation des données tabulaires |
| PostgreSQL | Stockage relationnel |
| Docker Compose | Environnement PostgreSQL local |
| dbt Core | Transformations SQL et tests |
| SQL | Requêtes, jointures et modélisation |
| Power BI Desktop | Visualisation et analyse |
| DAX | Calcul des indicateurs analytiques |
| Git / GitHub | Versionnement du projet |

## Structure du dépôt

```text
sales-data-warehouse/
├── data/
│   └── raw/
│       ├── generate_data.py
│       ├── customers.csv
│       ├── products.csv
│       ├── orders.csv
│       └── order_items.csv
├── sql/
│   └── source_schema.sql
├── src/
│   └── load_data.py
├── warehouse/
│   ├── dbt_project.yml
│   ├── models/
│   │   ├── staging/
│   │   │   ├── sources.yml
│   │   │   └── ...
│   │   └── ...
│   └── ...
├── powerbi/
├── .env.example
├── .gitignore
└── README.md
```

## Données utilisées

Le jeu de données comprend quatre fichiers CSV :

| Fichier | Nombre de lignes |
|---|---:|
| `customers.csv` | 30 |
| `products.csv` | 15 |
| `orders.csv` | 200 |
| `order_items.csv` | 512 |
| **Total** | **757** |

Les données couvrent l'année 2025 pour les commandes. Elles contiennent notamment les clients, les produits, les commandes, les quantités, les prix unitaires, les remises et les statuts de commande.

Le script de génération utilise une graine aléatoire fixe afin de faciliter la reproductibilité des résultats.

## Modélisation et transformations dbt

Le projet utilise dbt pour organiser les transformations SQL en modèles réutilisables et testables.

Les modèles sont répartis entre :

- **Staging** : préparation des données issues du schéma `dw_raw`.
- **Dimensions** : structuration des informations clients, produits et dates.
- **Table de faits** : centralisation des lignes de vente.
- **Mart analytique** : agrégation des performances commerciales.

Les tests dbt couvrent notamment les contraintes de présence, d'unicité, de relations et de validité des données.

### Résultats des tests

Lors de la dernière exécution de `dbt build`, les résultats étaient les suivants :

- 9 modèles exécutés avec succès.
- 57 tests de données réussis.
- 0 erreur.
- 0 avertissement.

Ces résultats correspondent à l'état du projet au moment de sa validation et pourront évoluer avec les modifications futures.

## Indicateurs commerciaux

Le tableau de bord Power BI présente cinq indicateurs principaux :

- **Chiffre d'affaires livré** : revenu net associé aux commandes livrées.
- **Commandes livrées** : nombre distinct de commandes livrées.
- **Quantités vendues** : unités associées aux commandes livrées.
- **Montant des remises** : différence entre le revenu brut et le revenu net.
- **Panier moyen livré** : chiffre d'affaires livré divisé par le nombre de commandes livrées.

Des visualisations complémentaires permettent d'analyser l'évolution mensuelle du chiffre d'affaires ainsi que sa répartition par catégorie de produit et par pays.

### Résultats obtenus

Sur le jeu de données généré, les indicateurs globaux sont les suivants :

| Indicateur | Résultat |
|---|---:|
| Chiffre d'affaires livré | 254 083,50 |
| Commandes livrées | 142 |
| Quantités vendues | 1 091 |
| Montant des remises | 11 785,50 |
| Panier moyen livré | 1 789,32 |

**Convention métier :** seules les commandes au statut `Livrée` sont comptabilisées dans les indicateurs de ventes réalisées. Les commandes annulées, expédiées ou en préparation sont exclues de ces indicateurs.

Les montants sont présentés dans l'unité monétaire conventionnelle du jeu de données synthétique ; aucune devise réelle n'est spécifiée.

## Installation et exécution

### Prérequis

- Python 3.10
- Docker Desktop avec Docker Compose
- PostgreSQL
- dbt Core et l'adaptateur PostgreSQL
- Power BI Desktop pour consulter le tableau de bord

Les commandes ci-dessous sont adaptées à Windows PowerShell.

### 1. Cloner le dépôt

```powershell
git clone https://github.com/coulibalyzie/data_transformation.git
cd sales-data-warehouse
```

### 2. Créer l'environnement Python

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install pandas "psycopg[binary]" python-dotenv dbt-core dbt-postgres
```

### 3. Configurer les variables d'environnement

Créer un fichier `.env` à partir du modèle fourni :

```powershell
Copy-Item .env.example .env
```

Renseigner les paramètres de connexion PostgreSQL dans `.env` :

```dotenv
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5433
POSTGRES_DB=sales_dw
POSTGRES_USER=pipeline_user
POSTGRES_PASSWORD=your_local_password
```

Ces valeurs sont des exemples de configuration locale. Le mot de passe doit rester privé et ne jamais être publié sur GitHub.

### 4. Préparer PostgreSQL

Démarrer l'environnement PostgreSQL utilisé par le projet :

```powershell
docker compose -f ..\sales-data-pipeline\docker-compose.yml up -d
```

Le schéma source `dw_raw` doit ensuite être créé à partir du fichier `sql/source_schema.sql` si ce n'est pas déjà fait.

Cette configuration réutilise le conteneur du projet `sales-data-pipeline`. Pour exécuter ce dépôt de manière indépendante, il faut prévoir son propre environnement PostgreSQL et adapter la configuration.

### 5. Générer les données

```powershell
python .\data\raw\generate_data.py
```

Cette commande génère les quatre fichiers CSV dans `data/raw/`.

### 6. Charger les données sources

```powershell
python .\src\load_data.py
```

Le script charge les données dans le schéma `dw_raw` et remplace les données existantes dans les quatre tables sources concernées.

**Attention :** le chargement réinitialise le contenu de ces tables avant insertion. Ne l'exécuter que sur une base de développement dont les données peuvent être remplacées.

### 7. Configurer et exécuter dbt

Le profil dbt `warehouse` doit être configuré dans `~/.dbt/profiles.yml` avec les paramètres de connexion correspondants et le schéma cible `analytics`.

Vérifier la connexion :

```powershell
dbt debug --project-dir .\warehouse
```

Exécuter les transformations et les tests :

```powershell
dbt build --project-dir .\warehouse
```

La commande `dbt build` construit les modèles et exécute les tests associés.

### 8. Consulter le tableau de bord

Ouvrir Power BI Desktop et se connecter à PostgreSQL avec les paramètres de la base `sales_dw`.

Charger les objets du schéma `analytics` :

- `fact_sales`
- `dim_customer`
- `dim_product`
- `dim_date`

Recréer ou ouvrir le rapport Power BI préparé dans le dossier `powerbi/`, selon les fichiers présents dans le dépôt. Vérifier les relations entre la table de faits et les dimensions, puis utiliser les mesures DAX du rapport pour analyser les performances commerciales.

## Qualité et limites

Ce projet constitue une démonstration technique sur un jeu de données synthétique. Il permet de travailler la modélisation, la transformation, la validation et la visualisation des données, mais ne représente pas une plateforme de production complète.

Les principales limites sont :

- données artificielles et volume réduit ;
- environnement local destiné au développement ;
- absence d'orchestration automatisée de bout en bout ;
- absence de supervision de production et de gestion avancée des accès.

Ces limites ouvrent des pistes d'amélioration, notamment l'orchestration des traitements, la surveillance de la qualité des données et l'automatisation des exécutions.

## Auteur

**Zie Coulibaly**

Ingénieur diplômé d'IMT Nord Europe, orienté Data Engineering, bases de données et systèmes d'information.
En formation M2 TIDE à l'Université Paris 1 Panthéon Sorbonne.

- GitHub : [github.com/coulibalyzie](https://github.com/coulibalyzie)
- Portfolio : [Portfolio personnel](https://coulibalyzie.github.io/portfolio/)

---
