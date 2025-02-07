"""
Ce script analyse plusieurs fichiers CSV contenant des données socio-économiques et produit deux fichiers de sortie :
1. `all_year_prefix.txt` : Liste détaillée des années disponibles pour chaque variable entre 1960 et 2023.
2. `all_year_counts.txt` : Nombre de valeurs non nulles par variable et par année.
Fonctionnalités principales :
- Définition des répertoires et fichiers de données.
- Initialisation des fichiers de sortie avec des en-têtes descriptifs.
- Parcours des différents jeux de données définis dans le dictionnaire `DATASETS`.
- Vérification de l'existence de chaque fichier CSV.
- Chargement des fichiers CSV et extraction des années disponibles pour chaque variable.
- Filtrage des années entre 1960 et 2023.
- Écriture des années disponibles et des comptages de valeurs non nulles dans les fichiers de sortie.
Variables :
- `DATA_DIR` : Répertoire contenant les fichiers de données.
- `OUTPUT_YEARS` : Nom du fichier de sortie pour les années disponibles.
- `OUTPUT_COUNTS` : Nom du fichier de sortie pour les comptages de valeurs non nulles.
- `DATASETS` : Dictionnaire contenant les informations sur les différents jeux de données (fichiers et variables).
Sorties :
- `all_year_prefix.txt` : Contient la liste des années disponibles pour chaque variable.
- `all_year_counts.txt` : Contient le nombre de valeurs non nulles pour chaque variable et chaque année.
Exécution :
- Le script vérifie l'existence de chaque fichier CSV.
- Charge les données et extrait les années disponibles pour chaque variable.
- Filtre les années entre 1960 et 2023.
- Écrit les résultats dans les fichiers de sortie.

"""
import pandas as pd
import os

# 📍 Définition des répertoires et fichiers
DATA_DIR = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data"
OUTPUT_YEARS = "all_year_prefix.txt"
OUTPUT_COUNTS = "all_year_counts.txt"

DATASETS = {
    "revenus": {
        "file": "Revenus_csv/revcommunes.csv",
        "variables": ["revmoy", "revmoyfoy", "revratio"],
    },
    "csp": {
        "file": "CSP_csv/cspcommunes.csv",
        "variables": ["pchom", "pouvr", "pcadr"],
    },
    "diplomes": {
        "file": "Diplomes_csv/diplomescommunes.csv",
        "variables": ["pbac", "psup"],
    },
    "etrangers": {
        "file": "Nationalites_csv/etrangerscommunes.csv",
        "variables": ["petranger"],
    },
    "proprietaires": {
        "file": "Proprietaires_csv/proprietairescommunes.csv",
        "variables": ["ppropri"],
    },
    "ages": {
        "file": "Age_csp/agesexcommunes_modified.csv",
        "variables": [
            "pop_",
            "propf_",
            "prop014_",
            "prop1539_",
            "prop4059_",
            "prop60p_",
            "age_",
        ],
    },
    "pib": {"file": "Revenus_csv/pibcommunes.csv", "variables": ["pibratio", "pibtot"]},
    "capital_immo": {
        "file": "Capital_immobilier_csv/capitalimmobiliercommunes.csv",
        "variables": ["capitalratio", "capitalimmo", "prixm2_"],
    },
    "isf": {"file": "Capital_immobilier_csv/isfcommunes.csv", "variables": ["pisf"]},
}

# 📌 Initialisation des fichiers de sortie
with open(OUTPUT_YEARS, "w", encoding="utf-8") as output_years, open(OUTPUT_COUNTS, "w", encoding="utf-8") as output_counts:
    output_years.write("Liste détaillée des années disponibles par variable (1960-2023)\n")
    output_years.write("=" * 80 + "\n\n")

    output_counts.write("Nombre de valeurs non nulles par variable et par année\n")
    output_counts.write("=" * 80 + "\n\n")

    # Parcours des datasets
    for key, params in DATASETS.items():
        file_path = os.path.join(DATA_DIR, params["file"])

        # Vérifier si le fichier existe
        if not os.path.exists(file_path):
            output_years.write(f"⚠️ Fichier introuvable : {file_path}\n")
            output_counts.write(f"⚠️ Fichier introuvable : {file_path}\n")
            continue

        # Chargement complet du fichier CSV
        df = pd.read_csv(file_path, low_memory=False)

        output_years.write(f"📂 {key} ({file_path})\n")
        output_counts.write(f"📂 {key} ({file_path})\n")

        # Extraire les années disponibles pour chaque variable et compter les valeurs non nulles
        for variable in params["variables"]:
            years_found = sorted(
                {
                    int(col[len(variable):])
                    for col in df.columns
                    if col.startswith(variable) and col[len(variable):].isdigit()
                }
            )

            # Filtrer les années entre 1960 et 2023
            years_filtered = [year for year in years_found if 1960 <= year <= 2023]

            # 📌 Écriture dans le fichier de sortie des années disponibles
            if years_filtered:
                output_years.write(f"   - {variable}: {', '.join(map(str, years_filtered))}\n")
            else:
                output_years.write(f"   - {variable}: ❌ Aucune année trouvée\n")

            # 📌 Comptage des valeurs non nulles pour chaque année
            for year in years_filtered:
                col_name = f"{variable}{year}"
                if col_name in df.columns:
                    count_non_null = df[col_name].notna().sum()
                    output_counts.write(f"{variable}{year}: {count_non_null} valeurs non nulles\n")

        output_years.write("\n")
        output_counts.write("\n")

print(f"✅ Vérification terminée. Résultats enregistrés dans {OUTPUT_YEARS} et {OUTPUT_COUNTS}")
