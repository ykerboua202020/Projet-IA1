import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.sidebar.title('Navigation')
menu = st.sidebar.selectbox('Choisir un volet', ['Accueil', 'Analyse et corrélation des variables', 'Visualisations dynamiques', 'Rapport conclusif'])

df = pd.read_csv("pollution.csv")
num_cols = df.columns
df[num_cols] = df[num_cols].fillna(df[num_cols].median())

df_out = df.copy()
outlier_count = {}
for col in num_cols:
    Q1 = df_out[col].quantile(0.25)
    Q3 = df_out[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    
    outliers = df_out[(df_out[col] < lower) | (df_out[col] > upper)][col].count()
    outlier_count[col] = outliers

    df_out[col] = df_out[col].clip(lower, upper)

if menu == 'Accueil':
    st.title("Analyse de la qualité d'air")

    df = pd.read_csv("pollution.csv")
    st.dataframe(df)

    st.subheader("Valeurs manquantes")
    st.write(df.isna().sum())

elif menu == 'Analyse et corrélation des variables':
    st.subheader("Analyse descriptive des variables")
    describe_df = df_out.describe()
    st.dataframe(describe_df)

    if "Qualite_air" in df_out.columns:
        df_out["Qualite_air"] = df_out["Qualite_air"].astype(int)
    corr_matrix = df_out.corr()

    st.write("### Matrice de corrélation (Pearson)")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig)

    if "Qualite_air" in df_out.columns:
        st.write("### Corrélation des variables avec la qualité de l'air")
        corr_target = corr_matrix["Qualite_air"].sort_values(ascending=False)
        st.write(corr_target)

elif menu == 'Visualisations dynamiques':
    st.subheader("Visualisations dynamiques")

    st.write("Sélectionnez une variable pour l'analyse graphique :")

    selected_var = st.selectbox("Variable :", num_cols)

    st.write(f"### Histogramme de {selected_var}")
    fig_hist, ax_hist = plt.subplots()
    ax_hist.hist(df_out[selected_var], bins=30)
    ax_hist.set_xlabel(selected_var)
    ax_hist.set_ylabel("Fréquence")
    st.pyplot(fig_hist)

    st.write(f"### Boite à moustache de {selected_var}")
    fig_box, ax_box = plt.subplots()
    ax_box.boxplot(df_out[selected_var])
    ax_box.set_ylabel(selected_var)
    st.pyplot(fig_box)

    if "Qualite_air" in df_out.columns:
        st.write(f"### Relation entre {selected_var} et la qualité de l'air")
        fig_scatter, ax_scatter = plt.subplots()
        ax_scatter.scatter(df_out[selected_var], df_out["Qualite_air"])
        ax_scatter.set_xlabel(selected_var)
        ax_scatter.set_ylabel("Qualité de l'air")
        st.pyplot(fig_scatter)

elif menu == 'Rapport conclusif':
    st.title('Conclusion et Analyse Globale')
    st.write("""
            L’étude menée sur le jeu de données de qualité de l'air permet d’analyser les principaux facteurs environnementaux influençant la pollution atmosphérique dans une région donnée. Le jeu de données contient 5000 échantillons et 10 variables quantitatives, dont la variable cible représentant le niveau de qualité de l’air codé de 0 (bonne) à 3 (dangereuse).
             
            Une première exploration a mis en évidence la présence de valeurs manquantes dans presque toutes les variables environnementales, entre 1 et 5 pour chaque, à l’exception des variables Proximite_zones_industrielles et Qualite_air. Ces valeurs ont été traitées par une imputation à l’aide de la médiane, une méthode robuste adaptée aux données environnementales souvent influencées par des valeurs extrêmes. De plus, des valeurs aberrantes ont été détectées sur certaines variables, notamment les concentrations de PM2.5 et PM10. Celles-ci ont été corrigées par winsorisation basée sur l’intervalle interquartile, permettant de conserver l’ensemble des données tout en limitant l’impact des valeurs extrêmes.
             
            L’analyse descriptive a permis de résumer les caractéristiques des principales variables. Par exemple, la concentration moyenne en PM2.5 est d’environ 21,6 µg/m³, avec une médiane de 21,5 µg/m³ et un écart-type de 3,6, tandis que la concentration en PM10 présente une moyenne de 25,2 µg/m³ et un écart-type de 5,4. Les quartiles du monoxyde de carbone (CO) se situent entre 0,65 ppm (Q1) et 1,41 ppm (Q3), indiquant une distribution relativement homogène autour de la médiane.
             
            L’analyse de corrélation révèle que les polluants atmosphériques CO, NO2 et SO2 sont les principaux contributeurs à la dégradation de la qualité de l’air. Ces variables présentent des coefficients de corrélation élevés avec la variable cible, indiquant que leur augmentation est directement associée à une détérioration de la qualité de l'air. La température et la densité de population jouent également un rôle notable dans l'augmentation des niveaux de pollution, tandis que la proximité des zones industrielles affiche une corrélation négative, confirmant que les zones proches des industries présentent souvent des niveaux de pollution plus élevés.
             
            Une corrélation positive modérée a été observée entre l'humidité et la qualité de l'air, ce qui peut s'expliquer par le fait que des conditions humides peuvent parfois favoriser la stagnation des particules fines. De plus, l'analyse des relations entre densité de population et PM2.5 montre une tendance nette : les zones plus densément peuplées présentent des niveaux plus élevés de particules fines, pouvant s’expliquer par une activité humaine plus importante (transport, chauffage, industries, etc.).
             
            En conclusion, cette analyse démontre que les concentrations de CO, NO2 et SO2, la densité de population et la proximité des zones industrielles sont les principaux facteurs associés à la détérioration de la qualité de l'air. La méthodologie suivie - comprenant le traitement des valeurs manquantes, la correction des valeurs aberrantes, l’analyse descriptive et la visualisation des corrélations - permet de garantir une interprétation fiable et cohérente des données. Ces résultats peuvent être exploités pour orienter les actions de prévention et les décisions politiques visant à limiter les émissions polluantes, améliorer la surveillance environnementale et renforcer les initiatives en matière d’urbanisme durable.
             """)