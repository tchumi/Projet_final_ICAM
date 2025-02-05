"""
Ce script enrichit un fichier CSV contenant des codes de communes avec des informations sur les arrondissements de Paris, Lyon et Marseille.
Modules importés:
- pandas as pd
- os
Variables:
- DATA_DIR: Chemin du répertoire contenant les fichiers de données.
- COMMUNE_FILE: Chemin du fichier CSV des codes de communes.
- OUTPUT_FILE: Chemin du fichier CSV de sortie enrichi.
Étapes principales:
1. Chargement du fichier des communes dans un DataFrame.
2. Création d'une table de correspondance des arrondissements de Paris, Lyon et Marseille.
3. Création d'un DataFrame pour les arrondissements.
4. Ajout des arrondissements au DataFrame des communes.
5. Tri des données par codecommune.
6. Sauvegarde du fichier enrichi dans un nouveau fichier CSV.
Sortie:
- Un fichier CSV enrichi avec les arrondissements, enregistré sous le chemin spécifié dans OUTPUT_FILE.

"""
import pandas as pd
import os

# 📍 Chemin des fichiers
DATA_DIR = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data/Taille_agglo_commune_csv"
COMMUNE_FILE = os.path.join(DATA_DIR, "codescommunes2014.csv")
OUTPUT_FILE = os.path.join(DATA_DIR, "codescommunes2014_enrichi.csv")

# 📌 Chargement du fichier des communes
df_communes = pd.read_csv(COMMUNE_FILE, sep=",", dtype=str)

# 📌 Table de correspondance des arrondissements de Paris, Lyon et Marseille
data_arrondissements = [
    ["75", "Paris", "75056", "Paris", "", "", ""],
    ["69", "Rhône", "69380", "Lyon", "", "", ""],
    ["69", "Rhône", "69381", "Lyon 1er Arrondissement", "", "", ""],
    ["69", "Rhône", "69382", "Lyon 2e Arrondissement", "", "", ""],
    ["69", "Rhône", "69383", "Lyon 3e Arrondissement", "", "", ""],
    ["69", "Rhône", "69384", "Lyon 4e Arrondissement", "", "", ""],
    ["69", "Rhône", "69385", "Lyon 5e Arrondissement", "", "", ""],
    ["69", "Rhône", "69386", "Lyon 6e Arrondissement", "", "", ""],
    ["69", "Rhône", "69387", "Lyon 7e Arrondissement", "", "", ""],
    ["69", "Rhône", "69388", "Lyon 8e Arrondissement", "", "", ""],
    ["69", "Rhône", "69389", "Lyon 9e Arrondissement", "", "", ""],
    ["13", "Bouches-du-Rhône", "13201", "Marseille 1er Arrondissement", "", "", ""],
    ["13", "Bouches-du-Rhône", "13202", "Marseille 2e Arrondissement", "", "", ""],
    ["13", "Bouches-du-Rhône", "13203", "Marseille 3e Arrondissement", "", "", ""],
    ["13", "Bouches-du-Rhône", "13204", "Marseille 4e Arrondissement", "", "", ""],
    ["13", "Bouches-du-Rhône", "13205", "Marseille 5e Arrondissement", "", "", ""],
    ["13", "Bouches-du-Rhône", "13206", "Marseille 6e Arrondissement", "", "", ""],
    ["13", "Bouches-du-Rhône", "13207", "Marseille 7e Arrondissement", "", "", ""],
    ["13", "Bouches-du-Rhône", "13208", "Marseille 8e Arrondissement", "", "", ""],
    ["13", "Bouches-du-Rhône", "13209", "Marseille 9e Arrondissement", "", "", ""],
    ["13", "Bouches-du-Rhône", "13210", "Marseille 10e Arrondissement", "", "", ""],
    ["13", "Bouches-du-Rhône", "13211", "Marseille 11e Arrondissement", "", "", ""],
    ["13", "Bouches-du-Rhône", "13212", "Marseille 12e Arrondissement", "", "", ""],
    ["13", "Bouches-du-Rhône", "13213", "Marseille 13e Arrondissement", "", "", ""],
    ["13", "Bouches-du-Rhône", "13214", "Marseille 14e Arrondissement", "", "", ""],
    ["13", "Bouches-du-Rhône", "13215", "Marseille 15e Arrondissement", "", "", ""],
    ["13", "Bouches-du-Rhône", "13216", "Marseille 16e Arrondissement", "", "", ""],
    ["23","Creuse","26383","Soumans","","",""]
]

# 📌 Création d'un DataFrame pour les arrondissements
df_arrondissements = pd.DataFrame(data_arrondissements, columns=df_communes.columns)

# 📌 Ajout des arrondissements au fichier des communes
df_communes_enrichi = pd.concat([df_communes, df_arrondissements], ignore_index=True)

# 📌 Trier les données par codecommune
df_communes_enrichi = df_communes_enrichi.sort_values(by="codecommune")

# 📌 Sauvegarde du fichier enrichi
df_communes_enrichi.to_csv(OUTPUT_FILE, index=False)

print(f"✅ Fichier enrichi avec les arrondissements enregistré sous : {OUTPUT_FILE}")
