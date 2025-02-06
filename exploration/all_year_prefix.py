import pandas as pd
import os

# 📍 Définition des répertoires et fichiers
DATA_DIR = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data"
OUTPUT_FILE = "all_year_prefix.txt"

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
        "file": "Age_csp/agesexcommunes.csv",
        "variables": [
            "pop",
            "propf",
            "prop014",
            "prop1539",
            "prop4059",
            "prop60p",
            "age",
        ],
    },
    "pib": {"file": "Revenus_csv/pibcommunes.csv", "variables": ["pibratio", "pibtot"]},
    "capital_immo": {
        "file": "Capital_immobilier_csv/capitalimmobiliercommunes.csv",
        "variables": ["capitalratio", "capitalimmo", "prixm2_"],
    },
    "isf": {"file": "Capital_immobilier_csv/isfcommunes.csv", "variables": ["pisf"]},
}

# 📌 Initialisation du fichier de sortie
with open(OUTPUT_FILE, "w", encoding="utf-8") as output_file:
    output_file.write(
        "Liste détaillée des années disponibles par variable (1960-2023)\n"
    )
    output_file.write("=" * 80 + "\n\n")

    # Parcours des datasets
    for key, params in DATASETS.items():
        file_path = os.path.join(DATA_DIR, params["file"])

        # Vérifier si le fichier existe
        if not os.path.exists(file_path):
            output_file.write(f"⚠️ Fichier introuvable : {file_path}\n")
            continue

        # Chargement du fichier CSV (lecture des en-têtes uniquement)
        df = pd.read_csv(file_path, nrows=1)  # Lire uniquement les en-têtes

        output_file.write(f"📂 {key} ({file_path})\n")

        # Extraire les années disponibles pour chaque variable
        for variable in params["variables"]:
            years_found = sorted(
                {
                    int(col[len(variable) :])
                    for col in df.columns
                    if col.startswith(variable) and col[len(variable) :].isdigit()
                }
            )

            # Filtrer les années entre 1960 et 2023
            years_filtered = [year for year in years_found if 1960 <= year <= 2023]

            # 📌 Écriture dans le fichier de sortie
            if years_filtered:
                output_file.write(
                    f"   - {variable}: {', '.join(map(str, years_filtered))}\n"
                )
            else:
                output_file.write(f"   - {variable}: ❌ Aucune année trouvée\n")

        output_file.write("\n")

print(f"✅ Vérification terminée. Résultats détaillés enregistrés dans {OUTPUT_FILE}")
