import pandas as pd
import os

# 📍 Chemin du fichier
file_path = r"C:\Users\Admin.local\Documents\Projet_final_ICAM\df_final_cleaned.csv"

# 📌 Chargement des données
try:
    df = pd.read_csv(file_path, low_memory=False)
    print("✅ Fichier chargé avec succès !")
except FileNotFoundError:
    print("❌ Erreur : Le fichier n'a pas été trouvé.")
    exit()
except Exception as e:
    print(f"❌ Erreur lors du chargement du fichier : {e}")
    exit()

# 📌 Vérification des types de données
print("\n📊 Aperçu des types de colonnes :")
print(df.dtypes)

# 📌 Vérification des valeurs manquantes
missing_values = df.isnull().sum()
missing_values = missing_values[missing_values > 0]
missing_values_dict = missing_values.to_dict()  # Convertir en dictionnaire pour éviter l'erreur

if not missing_values.empty:
    print("\n🔍 Colonnes avec valeurs manquantes :")
    print(missing_values)
else:
    print("\n✅ Aucune valeur manquante détectée.")

# 📌 Vérification des types mixtes dans les colonnes
mixed_type_columns = []
for col in df.columns:
    unique_types = df[col].apply(type).nunique()
    if unique_types > 1:
        mixed_type_columns.append(col)

if mixed_type_columns:
    print("\n⚠️ Colonnes contenant des types de données mixtes :")
    print(mixed_type_columns)
else:
    print("\n✅ Aucune colonne avec des types mixtes détectée.")

# 📌 Vérification des valeurs aberrantes
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
outliers = {}

for col in numeric_columns:
    min_val = df[col].min()
    max_val = df[col].max()
    
    # Détection de valeurs aberrantes (ex : pourcentages > 100% ou valeurs négatives)
    if "p" in col.lower() and max_val > 100:
        outliers[col] = f"Max {max_val} > 100%"
    if min_val < 0:
        outliers[col] = f"Min {min_val} < 0"

if outliers:
    print("\n🚨 Variables avec valeurs aberrantes :")
    for key, value in outliers.items():
        print(f"{key} : {value}")
else:
    print("\n✅ Aucune valeur aberrante détectée.")

# 📌 Création du DataFrame récapitulatif des incohérences
coherence_report = pd.DataFrame({
    "Colonnes Manquantes": list(missing_values_dict.keys()),
    "Valeurs Manquantes": list(missing_values_dict.values()),
    "Colonnes Types Mixtes": mixed_type_columns + [""] * (len(missing_values_dict) - len(mixed_type_columns)),
    "Valeurs Aberrantes": list(outliers.keys()) + [""] * (len(missing_values_dict) - len(outliers))
})

# 📌 Option d'exportation des incohérences
export_choice = input("\n💾 Voulez-vous enregistrer les incohérences dans un fichier CSV ? (y/n) : ").strip().lower()
if export_choice == "y":
    export_path = "coherence_report.csv"
    coherence_report.to_csv(export_path, index=False)
    print(f"\n✅ Rapport exporté dans {export_path}")

print("\n🎯 Analyse terminée.")
