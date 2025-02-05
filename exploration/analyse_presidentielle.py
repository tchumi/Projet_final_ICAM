"""
Ce script analyse les fichiers électoraux des élections présidentielles pour vérifier certaines hypothèses concernant les votes du premier et du second tour.
Fonctions:
    detect_elections(base_dir):
        Détecte les fichiers CSV des élections présidentielles dans le répertoire spécifié.
    analyze_election(file_path, election_year):
        Analyse un fichier électoral pour vérifier les hypothèses sur les votes du premier et du second tour.
Variables:
    base_dir (str): Chemin du dossier contenant les données électorales.
    synthese (list): Liste pour stocker la synthèse des analyses.
    election_files (dict): Dictionnaire contenant les chemins des fichiers électoraux détectés.
Étapes principales:
    1. Détection des fichiers électoraux disponibles.
    2. Analyse des fichiers électoraux pour vérifier les hypothèses.
    3. Stockage des résultats de l'analyse dans un fichier de synthèse.

"""

import os
import pandas as pd

# Chemin du dossier contenant les données électorales
base_dir = "D:/Projet_final_data/Piketty_data"

# Liste pour stocker la synthèse
synthese = []


# Fonction pour détecter les fichiers CSV des élections
def detect_elections(base_dir):
    elections = {}
    for folder in os.listdir(base_dir):
        if folder.startswith("pres") and folder.endswith("_csv"):
            folder_path = os.path.join(base_dir, folder)
            for file in os.listdir(folder_path):
                if file.endswith(".csv"):
                    elections[folder] = os.path.join(folder_path, file)
    return elections


# Détecte les fichiers électoraux disponibles
election_files = detect_elections(base_dir)


# Fonction pour analyser les fichiers électoraux
def analyze_election(file_path, election_year):
    try:
        df = pd.read_csv(file_path, sep=",", dtype=str)
        columns = df.columns.tolist()

        # Vérification de la présence des colonnes nécessaires
        required_columns = ["voteTG", "voteTD", "exprimes"]
        has_second_tour = (
            "exprimesT2" in columns
        )  # Vérifier si le second tour est disponible

        if not all(col in columns for col in required_columns):
            synthese.append(
                f"⚠️ **Élection {election_year} : Colonnes manquantes pour l'analyse**"
            )
            return

        # Conversion des colonnes en numériques
        for col in required_columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        if has_second_tour:
            df["exprimesT2"] = pd.to_numeric(df["exprimesT2"], errors="coerce")

        # Calcul des totaux
        total_tg_td = df["voteTG"].sum() + df["voteTD"].sum()
        total_exprimes = df["exprimes"].sum()
        total_exprimes_t2 = df["exprimesT2"].sum() if has_second_tour else 0

        # Vérification de l'égalité entre TG+TD et exprimes (1er tour)
        ecart_1er_tour = abs(total_tg_td - total_exprimes)

        # Vérification de l'égalité entre TG+TD et exprimes (2 tours cumulés)
        ecart_total_tours = (
            abs(total_tg_td - (total_exprimes + total_exprimes_t2))
            if has_second_tour
            else 0
        )

        # Stockage de la synthèse pour cette élection
        synthese.append(f"🗳️ **Élection {election_year}**")
        synthese.append(f"📂 Fichier : {file_path}")

        # Hypothèse : TG + TD doit être égal aux voix du 1er tour
        if ecart_1er_tour < 1:
            synthese.append(
                f"🔹 Hypothèse 4 (TG + TD totalise les voix du 1er tour) : ✅ Vérifiée"
            )
        else:
            synthese.append(
                f"🔹 Hypothèse 4 (TG + TD totalise les voix du 1er tour) : ⚠️ Écart détecté : {ecart_1er_tour:,.0f} voix"
            )

        # Hypothèse : TG + TD ne doit PAS totaliser les 2 tours
        if has_second_tour:
            if ecart_total_tours > 1:
                synthese.append(
                    f"🔹 Hypothèse 5 (TG + TD inclut le 2nd tour ?) : ✅ Vérifiée (pas de mélange)"
                )
            else:
                synthese.append(
                    f"🔹 Hypothèse 5 (TG + TD inclut le 2nd tour ?) : ⚠️ **Problème détecté** : il semble y avoir un mélange 1er et 2nd tour."
                )

        synthese.append("\n" + "-" * 80 + "\n")

    except Exception as e:
        print(f"❌ Erreur lors de l'analyse du fichier {file_path}: {e}")


# Parcours et analyse des fichiers électoraux
for election, file_path in election_files.items():
    year = election.replace("pres", "").replace("_csv", "")
    analyze_election(file_path, year)

# Sauvegarde du fichier de synthèse dans le répertoire courant du script
output_file = os.path.join(os.getcwd(), "presidentiel_verif_tours.txt")
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(synthese))

print(f"✅ Analyse terminée ! Résultats enregistrés dans {output_file}")
