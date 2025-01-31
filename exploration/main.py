import pandas as pd
import os

# Répertoire contenant les fichiers
data_dir = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data"

# Fichiers à analyser
files = [
    "Revenus_csv/revcommunes.csv",
    "CSP_csv/cspcommunes.csv",
    "Diplomes_csv/diplomescommunes.csv",
    "Nationalites_csv/etrangerscommunes.csv",
    "Proprietaires_csv/proprietairescommunes.csv",
    "pres2017_csv/pres2017comm.csv"
]

# Explorer les premières lignes de chaque fichier et écrire le résultat dans un fichier texte
with open("exploration.txt", "w") as f:
    for file in files:
        path = os.path.join(data_dir, file)
        df = pd.read_csv(path, sep=",", nrows=5)  # Charger seulement 5 lignes pour inspection
        f.write(f"\n {file} :\n")
        f.write(f"{df.head()}\n")
        f.write(f"{df.columns}\n")
# # Explorer les premières lignes de chaque fichier
# for file in files:
#     path = os.path.join(data_dir, file)
#     df = pd.read_csv(path, sep=",", nrows=5)  # Charger seulement 5 lignes pour inspection
#     print(f"\n📌 {file} :")
#     print(df.head())
#     print(df.columns)
