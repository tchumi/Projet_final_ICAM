"""
Ce script effectue le suivi des clusters des élections au fil du temps en utilisant l'algorithme de K-means et l'algorithme de Hongrois pour stabiliser les labels des clusters.
Fonctionnalités principales :
1. Chargement des données d'élections depuis un fichier CSV.
2. Sélection des colonnes pertinentes pour l'analyse.
3. Création des matrices de transition entre les différentes années d'élections.
4. Utilisation de l'algorithme de Hongrois pour stabiliser les labels des clusters entre les années.
5. Application des labels corrigés dans le dataframe.
6. Enregistrement du fichier mis à jour avec les clusters stabilisés.
7. Visualisation des flux de clusters avec un diagramme de Sankey (si plotly est installé).
Modules requis :
- pandas
- numpy
- matplotlib.pyplot
- seaborn
- scipy.optimize.linear_sum_assignment
- plotly.graph_objects (optionnel pour la visualisation Sankey)
Variables :
- DATA_PATH : Chemin vers le fichier CSV contenant les données d'élections.
- df : DataFrame contenant les données chargées.
- elections : Liste des années d'élections présentes dans les données.
- transition_matrices : Dictionnaire stockant les matrices de transition entre les années d'élections.
- cluster_mapping : Dictionnaire stockant la correspondance des clusters entre les années d'élections.
- OUTPUT_PATH : Chemin vers le fichier CSV de sortie avec les clusters stabilisés.
Fonctions :
- match_clusters(matrix) : Utilise l'algorithme de Hongrois pour trouver la correspondance optimale des clusters entre deux années.

"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import linear_sum_assignment

# 📌 Chemin des données
DATA_PATH = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data/elections_fusionnees_cleaned_with_names_clusters.csv"
OUTPUT_PATH = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data/elections_fusionnees_tracking_1er_tour.csv"
REPORT_PATH = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data/rapport_tracking_cluster_tour_1.txt"

# 📌 Chargement des données
df = pd.read_csv(DATA_PATH, sep=",", dtype={"codecommune": str})

# 📌 Sélection des colonnes pertinentes
# df = df[["codecommune", "année", "cluster_1er_tour"]]

# 📌 Liste des élections
elections = sorted(df["année"].unique())
transition_matrices = {}

# 📌 Ouverture du rapport pour l'enregistrement de la sortie
with open(REPORT_PATH, "w", encoding="utf-8") as report:
    
    # 📌 Création de la matrice de transition
    for i in range(len(elections) - 1):
        year_prev = elections[i]
        year_next = elections[i + 1]

        # 📌 Sélection des communes présentes aux deux élections
        df_prev = df[df["année"] == year_prev].set_index("codecommune")
        df_next = df[df["année"] == year_next].set_index("codecommune")

        common_communes = df_prev.index.intersection(df_next.index)

        df_prev = df_prev.loc[common_communes]
        df_next = df_next.loc[common_communes]

        # 📌 Construction de la matrice de transition
        transition_matrix = pd.crosstab(df_prev["cluster_1er_tour"], df_next["cluster_1er_tour"], normalize="index")

        # 📌 Sauvegarde de la matrice
        transition_matrices[(year_prev, year_next)] = transition_matrix

        # 📌 Écriture du rapport
        report.write(f"📊 Matrice de transition {year_prev} → {year_next}\n")
        report.write(transition_matrix.to_string() + "\n\n")

    # 📌 Algorithme de Hongrois pour stabiliser les labels des clusters
    def match_clusters(matrix):
        cost_matrix = -matrix.values  # On minimise le coût donc on met des valeurs négatives
        row_ind, col_ind = linear_sum_assignment(cost_matrix)
        return dict(zip(matrix.index[row_ind], matrix.columns[col_ind]))

    # 📌 Création du mapping des clusters dans le temps
    cluster_mapping = {}

    for (year_prev, year_next), matrix in transition_matrices.items():
        mapping = match_clusters(matrix)
        cluster_mapping[(year_prev, year_next)] = mapping

    # 📌 Enregistrement des correspondances dans le rapport
    report.write("\n📌 Correspondance des clusters entre élections :\n")
    for k, v in cluster_mapping.items():
        report.write(f"{k} : {v}\n")

# 📌 Application des labels corrigés dans le dataframe
df["cluster_corrige_1er_tour"] = df["cluster_1er_tour"]

for (year_prev, year_next), mapping in cluster_mapping.items():
    df.loc[df["année"] == year_next, "cluster_corrige_1er_tour"] = df.loc[df["année"] == year_next, "cluster_1er_tour"].replace(mapping)

# 📌 Enregistrement du fichier mis à jour
df.to_csv(OUTPUT_PATH, index=False)

print(f"✅ Fichier sauvegardé avec clusters stabilisés : {OUTPUT_PATH}")
print(f"📄 Rapport généré : {REPORT_PATH}")

# 📌 Visualisation des flux avec Sankey Diagram
try:
    import plotly.graph_objects as go

    links = []
    for (year_prev, year_next), matrix in transition_matrices.items():
        for c1, c2 in matrix.stack().index:
            value = matrix.loc[c1, c2]
            if value > 0.05:  # Filtrer les flux faibles
                links.append({
                    "source": f"{year_prev}-{c1}",
                    "target": f"{year_next}-{c2}",
                    "value": value
                })

    nodes = list(set([link["source"] for link in links] + [link["target"] for link in links]))
    node_indices = {node: i for i, node in enumerate(nodes)}

    sankey_fig = go.Figure(go.Sankey(
        node=dict(
            pad=15, thickness=20, line=dict(color="black", width=0.5),
            label=nodes
        ),
        link=dict(
            source=[node_indices[link["source"]] for link in links],
            target=[node_indices[link["target"]] for link in links],
            value=[link["value"] for link in links]
        )
    ))

    sankey_fig.update_layout(title_text="Évolution des Clusters du 1er Tour", font_size=10)
    sankey_fig.show()

except ImportError:
    print("⚠️ plotly non installé : graphique Sankey non généré.")