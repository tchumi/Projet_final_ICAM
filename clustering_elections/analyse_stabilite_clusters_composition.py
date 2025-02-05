import pandas as pd
import os

# 📍 Chemin du fichier des clusters
DATA_DIR = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data"
CLUSTER_FILE = os.path.join(DATA_DIR, "clusters_elections.csv")
REPORT_FILE = os.path.join(DATA_DIR, "rapport_stabilite_clusters_composition.txt")

# 📌 Chargement des données
df_clusters = pd.read_csv(CLUSTER_FILE, sep=",", dtype={"codecommune": str})

# 📌 Fonction pour analyser la stabilité des clusters entre deux élections successives
def analyse_stabilite_clusters(df):
    rapport = []
    
    for annee1, annee2 in zip(sorted(df["année"].unique())[:-1], sorted(df["année"].unique())[1:]):
        df_prev = df[df["année"] == annee1]
        df_next = df[df["année"] == annee2]
        
        # Fusionner pour suivre les communes
        df_merged = df_prev.merge(df_next, on="codecommune", suffixes=(f"_{annee1}", f"_{annee2}"))
        
        # Statistiques sur la stabilité des clusters (1er tour)
        stability_1er = {}
        for cluster in df_prev["cluster_1er_tour"].unique():
            communes_initiales = df_prev[df_prev["cluster_1er_tour"] == cluster]["codecommune"]
            communes_retenues = df_merged[df_merged["cluster_1er_tour_"+str(annee1)] == cluster]["codecommune"]
            
            ratio_stable = len(set(communes_retenues) & set(communes_initiales)) / len(communes_initiales)
            stability_1er[cluster] = ratio_stable
        
        # Statistiques sur la stabilité des clusters (2nd tour)
        stability_2nd = {}
        for cluster in df_prev["cluster_2nd_tour"].unique():
            communes_initiales = df_prev[df_prev["cluster_2nd_tour"] == cluster]["codecommune"]
            communes_retenues = df_merged[df_merged["cluster_2nd_tour_"+str(annee1)] == cluster]["codecommune"]
            
            ratio_stable = len(set(communes_retenues) & set(communes_initiales)) / len(communes_initiales)
            stability_2nd[cluster] = ratio_stable

        rapport.append(f"\n📌 Transition de {annee1} à {annee2} :")
        rapport.append(f" - Stabilité des clusters du 1er tour : {stability_1er}")
        rapport.append(f" - Stabilité des clusters du 2nd tour : {stability_2nd}")

    return "\n".join(rapport)

# 📌 Génération du rapport
rapport_final = "📊 Analyse de la stabilité de la composition des clusters\n"
rapport_final += "======================================\n\n"
rapport_final += analyse_stabilite_clusters(df_clusters)

# 📌 Sauvegarde du rapport
with open(REPORT_FILE, "w", encoding="utf-8") as file:
    file.write(rapport_final)

print(f"✅ Rapport généré : {REPORT_FILE}")
