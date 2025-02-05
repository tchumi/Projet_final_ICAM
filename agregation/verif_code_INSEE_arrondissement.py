import pandas as pd

# 📍 Chemin du fichier des communes
FILE_PATH = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data/Taille_agglo_commune_csv/codescommunescantons2014.csv"

# 📌 Chargement du fichier des communes
df_communes = pd.read_csv(FILE_PATH, sep=",", dtype={"codecommune": str})

# 📌 Affichage des premières lignes pour vérifier la structure
print("\n📌 Aperçu du fichier :")
print(df_communes.head())

# 📌 Sélection des colonnes utiles (adapter selon la structure réelle)
columns_to_keep = ["codecommune", "nomcommune"]
df_communes = df_communes[columns_to_keep]

# 📌 Liste des codes INSEE à vérifier (Paris, Lyon, Marseille)
codes_a_verifier = [str(code) for code in list(range(13201, 13217)) +  # Marseille
                                     list(range(69380, 69390)) +  # Lyon
                                     ["75056"]]  # Paris

# 📌 Filtrer le fichier pour voir si les codes sont présents
df_verification = df_communes[df_communes["codecommune"].isin(codes_a_verifier)]

# 📌 Affichage des résultats
print("\n📌 Résultats de la vérification :")
if df_verification.empty:
    print("⚠️ Aucun des codes recherchés n'a été trouvé.")
else:
    print(df_verification)

# 📌 Sauvegarde des résultats dans un fichier CSV
OUTPUT_PATH = "verification_codes_arrondissements.csv"
df_verification.to_csv(OUTPUT_PATH, index=False)

print(f"\n✅ Résultats enregistrés sous : {OUTPUT_PATH}")
