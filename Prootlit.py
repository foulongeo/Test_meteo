# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 10:42:47 2022

@author: foulo
"""

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches
import warnings
from IPython.display import Markdown, display
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn import preprocessing
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn import ensemble
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling  import RandomOverSampler
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.layers import Input, Dense 
from tensorflow.keras.models import Model
import time

warnings.filterwarnings('ignore')
sns.set_theme({'legend.frameon':True})

## MENU DE NAVIGATION ##

nav = st.sidebar.radio("Navigation", ["Accueil", "Introduction",
                                "Description du dataset",
                                "Les filouteries de Lise aka Kangooroo-Girl",
                                "Machine learning",
                                "Deep learning",
                                "🐰"])


    
pd.set_option("display.max_columns", None)

if nav == "Accueil":
    st.markdown("<p style='font-family:Cambria; color:#55557e; font-size: 25px;'><center>COMPTE RENDU DE PROJET<center></p>", unsafe_allow_html= True)
    st.markdown("<p style='font-family:Cambria; color:#3adfb2; font-size: 65px;'><center>PRÉVISIONS MÉTÉOROLOGIQUES EN AUSTRALIE<center></p>", unsafe_allow_html= True)
    st.markdown("<p style='font-family:Cambria; color:navy; font-size: 36px;'><center> par Lise Aujoulat et Geoffrey Foulon-Pinto </p>", unsafe_allow_html= True)
    st.markdown("<p style='font-family:Cambria; color:navy; font-size: 30px;'><center><i> supervision : Maxime Michel </i></p>", unsafe_allow_html= True)
    st.markdown("<br/><p style='font-family:Cambria; color:#8285a6; font-size: 30px;'><center> Promotion DataScientest Bootcamp Octobre 2021 </p>", unsafe_allow_html= True)
    st.markdown("<p style='font-family:Cambria; color:#8285a6; font-size: 30px;'><center> parcours Data scientist </p>", unsafe_allow_html= True)
    st.image(
            "https://365psd.com/images/istock/previews/9246/92468573-australian-flag-and-map.jpg",
            width=600,
        )
    
    if st.button('Lire le résumé 🦘'):
         st.markdown("""<p style='font-family:Cambria; font-size: 18px; text-align:justify'>La prédiction 
                     météorologique fait partie intégrante de notre quotidien et la fiabilité des prédictions 
                     est cruciale en de nombreux points. Ce projet avait pour objectif principal la 
                     <b>conception d’un modèle de machine learning</b> en apprentissage supervisé pour 
                     déterminer si des précipitations sont à attendre pour le jour suivant les observations.  
                     Le jeu de données utilisé contenait les relevés météorologiques de 49 stations réparties 
                     sur l’ensemble du territoire australien, à savoir <b>145 460 relevés datés</b>, sur une 
                     période de 10 ans (2007 - 2017).
La base de données brute comportait <b>22 variables</b> (température, pression atmosphérique, humidité…) 
en plus de la variable à prédire. Les entrées avec une valeur manquante sur la variable à prédire ont été 
supprimées. Les autres valeurs manquantes étaient remplacées par la valeur moyenne, médiane ou le mode sur 
le mois en cours, pour chaque station météorologique. Les données ont été ajustées par oversampling et 
undersampling.
Parmi les différents modèles de machine learning réalisés, le modèle <b>Random Forest</b> présentait les 
meilleures performances, avec une <b>précision</b> de <b>83 %</b>, un <b>rappel</b> de <b>63 %</b> et un
 <b>score f1</b> de <b>62 %</b>. Un modèle de <b>deep learning</b> utilisant 2 couches denses à 25 et
 50 neurones (activation par la fonction “relu”) a également été développé, offrant une <b>précision</b>
 de <b>86 %</b>. Enfin, une étude de <b>séries temporelles</b> a été menée sur la température maximale 
 via un autre set de données (s’étendant de 1995 à 2021) afin d’explorer différentes possibilités 
 d’études sur les données météorologiques. Les prédictions qui ont sont ressorties pour l’année 2021 
 semblent satisfaisantes. 
En conclusion, ce travail de data science montre que <b>les algorithmes de machine learning 
et de deep learning sont des outils prometteurs dans la prédiction météorologique</b> et 
pourraient être améliorés par la recherche de meilleurs paramètres. La connaissance des variables 
est également primordiale dans ce genre d’études et il serait intéressant de prendre en compte 
des phénomènes plus globaux tels que les anticyclones ou d’autres données telles que les images 
satellites pour obtenir de meilleures prédictions.</p>
                   """, unsafe_allow_html = True)
    else:
         st.write('☀☔🌡❄🌈')


elif nav == "Introduction":
    st.title("INTRODUCTION")
    st.markdown("""<p style='font-family:Cambria; font-size: 18px; text-align:justify'>\tLa météorologie est la 
                science qui s’intéresse aux phénomènes atmosphériques (formation des nuages, précipitations…)
                et l’Homme s’y intéresse depuis au moins l’Antiquité. En raison de la place centrale de 
                l’agriculture dans le développement des différentes civilisations, il devient très vite 
                nécessaire de comprendre et d’anticiper les phénomènes météorologiques. Depuis les premières 
                ébauches d’anémomètres réalisées au premier siècle avant Jésus-Christ, en passant par les 
                baromètres du XVIIème siècle, il existe aujourd’hui de très nombreux outils et techniques très performants pour étudier ces phénomènes météorologiques. Face au nombre et à la diversité des données météorologiques disponibles, la conception d’algorithmes de machine learning et de deep learning pourrait être une démarche très adaptée à la prédiction météorologique.
<br/><br/>Nous avons réalisé ce projet dans le cadre d’une formation en data science, dispensée d’octobre 2021 à janvier 2022 par DataScientest. Ce projet était pour nous l’occasion de mettre en pratique les savoirs théoriques acquis au fil de cette formation en travaillant sur des données en vie réelle. L’objectif de ce projet était de réaliser un modèle de prédiction de la survenue ou non de précipitations en Australie, à partir de données provenant du Bureau of Meteorology du gouvernement australien. La base de données contenait 145460 entrées et sera présentée plus en détail dans la suite de ce rapport. 
<br/><br/>Pour répondre à notre objectif de réalisation d’un modèle de prédiction de la pluie le lendemain des observations, nous avons tout d’abord étudié l’ensemble des données mises à disposition et procédé au traitement des valeurs manquantes. Nous avons réalisé un pré-processing sur la base de données pour avoir un format adapté à la modélisation. Nous avons conçu plusieurs modèles de machine learning pour déterminer le modèle le plus adapté et nous l’avons comparé à un modèle de deep learning. A travers ces modèles, nous nous sommes focalisés sur les métriques de précision et de rappel car nous voulions détecter les jours de pluie (plus rares que les jours secs en Australie). Enfin, puisque la nature des données s’y prêtait, nous avons réalisé une analyse de séries temporelles. Toute la partie programmation a été effectuée avec le langage Python 3.10.1. Les principales bibliothèques utilisées étaient Pandas, NumPy, Matplotlib.pyplot, Seaborn, Scikit-learn et Tensorflow.
</p>
                   """, unsafe_allow_html = True)
    


elif nav == "Description du dataset":

    st.title("DESCRIPTION DES VARIABLES 🦘")
    df = pd.read_csv("weatherAUS.csv")
    
    #Création d'un df de secours pour avoir une trace des données brutes.
    
    df_saved = pd.read_csv("weatherAUS.csv")
    
    
    st.markdown("<h4><u><font color = 'navy'>Affichage des premières lignes du dataframe.</h4></u>", unsafe_allow_html=True)
    st.write(df.head())
    st.write("\n------------------------------------------------------------------------")
    st.markdown("<h4><u><font color = 'navy'>Description statistique du dataframe.</h4></u>", unsafe_allow_html=True)
    st.write(round(df.describe(), 1))
    
    
    
    #Création de Year, Month & Day par slicing de la valeur de Date
    df["Year"] = df["Date"].apply(lambda x : int(x[:4]))
    df["Month"] = df["Date"].apply(lambda x : int(x[5:7]))
    df["Day"] = df["Date"].apply(lambda x : int(x[8:]))
    
    #Création du dictionnaire qui contient pour chaque état australien, les stations associées
    localites = {"SA" : ["Adelaide", "MountGambier", "Woomera", "Nuriootpa"],
                "WA" : ["Perth", "Albany", "PearceRAAF", "PerthAirport", "Walpole", "SalmonGums", "Witchcliffe"],
                "NSW" : ["Canberra", "Sydney", "Albury", "Wollongong", "MountGinini", "Tuggeranong", "Penrith", "Newcastle", "Cobar", "SydneyAirport", "BadgerysCreek", "WaggaWagga", "Moree", "Williamtown", "CoffsHarbour", "NorahHead", "Richmond"],
                "QLD" : ["Brisbane", "Townsville", "Cairns", "GoldCoast"],
                "TAS" : ["Hobart", "Launceston"],
                "VIC" : ["Melbourne", "Bendigo", "Ballarat", "Dartmoor", "Portland", "Mildura", "MelbourneAirport", "Sale", "Watsonia", "Nhil"],
                "NT" : ["Darwin", "AliceSprings", "Katherine", "Uluru"],
                "NI" : ["NorfolkIsland"]}
    
    #Création de la colonne State
    df["State"] = df.Location
    df["State"] = df["State"].replace(to_replace = ["Adelaide", "MountGambier", "Woomera", "Nuriootpa"], value = "SA")
    df["State"] = df["State"].replace(to_replace = ["Perth", "Albany", "PearceRAAF", "PerthAirport", "Walpole", "SalmonGums", "Witchcliffe"], value = "WA")
    df["State"] = df["State"].replace(to_replace = ["Canberra", "Sydney", "Albury", "Wollongong", "MountGinini", "Tuggeranong", "Penrith", "Newcastle", "Cobar", "SydneyAirport", "BadgerysCreek", "WaggaWagga", "Moree", "Williamtown", "CoffsHarbour", "NorahHead", "Richmond"], value = "NSW")
    df["State"] = df["State"].replace(to_replace = ["Brisbane", "Townsville", "Cairns", "GoldCoast"], value = "QLD")
    df["State"] = df["State"].replace(to_replace = ["Hobart", "Launceston"], value = "TAS")
    df["State"] = df["State"].replace(to_replace = ["Melbourne", "Bendigo", "Ballarat", "Dartmoor", "Portland", "Mildura", "MelbourneAirport", "Sale", "Watsonia", "Nhil"], value = "VIC")
    df["State"] = df["State"].replace(to_replace = ["Darwin", "AliceSprings", "Katherine", "Uluru"], value = "NT")
    df["State"] = df["State"].replace(to_replace = ["NorfolkIsland"], value = "NI")
    
    ##MENU DÉROULANT - CHOIX DES VARIABLES A AFFICHER
    
    st.markdown("<h4><u><font color = 'navy'>Exploration des variables.</h4></u>", unsafe_allow_html=True)
    
    var_a_afficher = st.selectbox(label = "Choisissez les variables à explorer dans le menu ci-dessous 🦘",
                                  options = ["Variables",
                                             "Date & lieu de relevé", 
                                             "Températures", 
                                             "Précipitations",
                                             "Ensoleillement, ennuagement",
                                             "Direction du vent",
                                             "Force du vent",
                                             "Pression atmosphérique", 
                                             "Pluie"])
    
    if var_a_afficher == "Date & lieu de relevé":
        st.markdown("<h2><u><center>Date, Location</center></u></h2>",unsafe_allow_html=True)
    
        #Définition des variables
        st.markdown("<h4><u><font color = 'navy'>Définition des variables :</u></h4>",unsafe_allow_html=True)
        st.markdown("<ul><li><b>Date</b> est définie comme <i>'The date of observation'</i>, c'est-à-dire la date de chaque relevé de mesure.</li><li><b>Location</b> est définie comme <i>'The common name of the location of the weather station'</i>, c'est-à-dire le nom de chaque lieu de relevé de mesure.</li></ul>",unsafe_allow_html=True)
        st.markdown("<h4><u><font color = 'navy'>Description des variables :</u></h4>",unsafe_allow_html=True)
        st.markdown("<h5><i>Date</i></h5>",unsafe_allow_html=True) 
        st.markdown("Les dates des relevés sont au format <b>yyyy-mm-dd</b>, les relevés vont du <b>{}</b> au <b>{}</b>. On constate qu'il n'y que <b>{}</b> relevés pour l'année <b>2007</b>, <b>{}</b> pour l'année <b>2008</b> et <b>{}</b> pour l'année <b>2017</b>. Pour les autres années, le nombre moyen de relevés est de <b>{}</b>.".format(
            df.Date.min(),
            df.Date.max(),
            df.Year[df["Year"] == 2007].count(),
            df.Year[df["Year"] == 2008].count(),
            df.Year[df["Year"] == 2017].count(),
            int(df.Year[(df["Year"] != 2007) & (df["Year"] != 2008) & (df["Year"] != 2017)].groupby(df.Year).count().mean())),unsafe_allow_html=True)
        
        st.markdown("<h5><i>Location</i></h5>",unsafe_allow_html=True)
        st.markdown("Le nombre médian de relevés par lieu est de <b>{}</b>. Il y'a au total <b>{}</b> lieux de relevé différents. Les lieux avec le plus de relevés sont <b>{}</b> ({} relevés) et <b>{}</b> ({} relevés). Trois lieux fournissent moins de relevés que les autres : <b>{}</b>, <b>{}</b> et <b>{}</b> ({} relevés chacun).".format(int(df.Location.value_counts().median()), len(set(df.Location)), df.Location.value_counts().keys()[0], df.Location.value_counts()[0], df.Location.value_counts().keys()[1], df.Location.value_counts()[1], df.Location.value_counts().keys()[-1], df.Location.value_counts().keys()[-2], df.Location.value_counts().keys()[-3], df.Location.value_counts()[-1]),unsafe_allow_html=True)
        
        #Valeurs manquantes
        st.markdown("<h4><u><font color = 'navy'>Valeurs manquantes :</u></h4>",unsafe_allow_html=True)
        st.markdown("Pas de valeurs manquantes pour ces deux variables.",unsafe_allow_html=True)
        
        #Création de variables (texte)
        st.markdown("<h4><u><font color = 'navy'>Création de variables :</u></h4>",unsafe_allow_html=True)
        st.markdown("<p>Création de la variable <b><i>State</i></b> qui représente la localisation des stations météorologiques par états.<ul><li>Les données de Canberra sont mutualisées avec la Nouvelle-Galle du Sud.</li><li>L'île de Norfolk est rattachée administrativement à l'état de Nouvelle-Galles du Sud, mais vu sa situation géographique (environ 1500km à l'est de l'Australie), les données seront traitées à part.</li><li>Si besoin, le classement par état est disponible dans le dictionnaire <i>localites</i>.</li></ul></p>",unsafe_allow_html=True)
        st.markdown("<p>Création des variables <b><i>Year</i></b>, <b><i>Month</i></b> et <b><i>Day</i></b>, des entiers représentant respectivement l'année, le mois et le jour.",unsafe_allow_html=True) 
            
        #Visualisation
        st.markdown("<h4><u><font color = 'navy'>Visualisation graphique :</u></h4>",unsafe_allow_html=True)
        
        fig1 = plt.figure(figsize = (6,3))
        sns.countplot("Year", data = df, palette = "cividis")
        plt.title("Nombre de relevés disponibles par année.", fontsize = 15, pad = 20)
        plt.xticks(size = 9)
        plt.yticks(size = 9)
        plt.xlabel('Années', fontsize=12)
        plt.ylabel('Nombre de relevés', fontsize=12)
        st.pyplot(fig1);
    
    ## TEMPERATURES 
        
    elif var_a_afficher == "Températures":
        st.markdown("<h2><u><center>MinTemp, MaxTemp, Temp9am, Temp3pm</center></u></h2>",unsafe_allow_html=True)
    
        #Définition des variables
        st.markdown("<h4><u><font color = 'navy'>Définition des variables :</u></h4>", unsafe_allow_html=True)
        st.markdown("""<ul><li><b>MinTemp</b> est définie comme <i>'The minimum temperature in degrees celsius'</i>, soit la température minimale relevée sur la journée.</li>
        <li><b>MaxTemp</b> est définie comme <i>'The maximum temperature in degrees celsius'</i>, soit la température maximale relevée sur la journée.</li>
        <li><b>Temp9am</b> est définie comme <i>'Temperature (degrees C) at 9am'</i>, soit la température relevée à 9h.</li>
        <li><b>Temp3pm</b> est définie comme <i>'Temperature (degrees C) at 3pm'</i>, soit la température relevée à 15h.</li></ul>""",unsafe_allow_html=True)
        
        #Description des variables
        st.markdown("<h4><u><font color = 'navy'>Description des variables :</u></h4>",unsafe_allow_html=True)
        st.markdown("<h5><i>MinTemp et MaxTemp :</i></h5>",unsafe_allow_html=True)
        st.markdown("""<div style="text-align: justify">Ces deux variables varient de façon similaire au fil des mois : 
        les températures les plus hautes sont retrouvées en janvier et les plus basses en juillet. Au mois de juillet, 
        les températures minimales et maximales moyennes sont de <b>{} ± {} °C</b> et <b>{} ± {} °C</b> respectivement, 
        tandis qu'au mois de janvier elles sont de <b>{} ± {} °C</b> et <b>{} ± {} °C</b> respectivement.</div>
        """.format(
            df[df["Month"] == 7].MinTemp.describe()["mean"].round(1),
            df[df["Month"] == 7].MinTemp.describe()["std"].round(1),
            df[df["Month"] == 7].MaxTemp.describe()["mean"].round(1),
            df[df["Month"] == 7].MaxTemp.describe()["std"].round(1),
            df[df["Month"] == 1].MinTemp.describe()["mean"].round(1),
            df[df["Month"] == 1].MinTemp.describe()["std"].round(1),
            df[df["Month"] == 1].MaxTemp.describe()["mean"].round(1),
            df[df["Month"] == 1].MaxTemp.describe()["std"].round(1)),unsafe_allow_html=True)
        
        st.markdown("<h5><i><br/>Temp9am et Temp3pm:</i></h5>",unsafe_allow_html=True)
        st.markdown("""<div style="text-align: justify">La température moyenne à 9h est <b>plus basse les jours de pluie</b> (<b>{} ± {} °C</b>) que les jours sans pluie (<b>{} ± {} °C</b>).
        La variabilité est assez similaire qu'il pleuve ou non et il y'a de nombreux outliers, principalement dans les valeurs hautes.
        D'une localité à l'autre, la température matinale semble peu varier, mais plusieurs villes du nord se distinguent par leur températures
        plus élevées : Brisbane, Cairns, Gold Coast, Townsville, Alice Springs, Darwin, Katherine et Uluru. Les températures matinales 
        sont minimales au mois de <b>juillet</b>, qu'il pleuve ou non, et avec une variabilité par mois limitée et stable d'une année 
        sur l'autre. Les minimales moyennes en juillet sont de <b>{} ± {} °C</b> les jours de pluie, <b>{} ± {} °C</b> sinon. Les températures 
        matinales maximales sont observées au mois de <b>janvier</b> et sont de <b>{} ± {} °C</b> les jours de pluie, {} ± {} °C sinon.
        Les observations à 15h suivent les <b>mêmes tendances</b> qu'à 9h. La température moyenne à 15h est plus basse les jours de pluie
        <b>({} ± {} °C)</b> que les jours sans pluie <b>({} ± {} °C)</b>. Enfin, les températures l'après-midi sont maximales en <b>juillet</b>, 
        <b>{} ± {} °C</b> les jours de pluie, <b>{} ± {} °C</b> sinon. Au mois de <b>janvier</b>, elles sont de <b>{} ± {} °C</b> 
        es jours de pluie, <b>{} ± {} °C</b> sinon.</div>
        """.format(
            df[df["RainToday"] == "Yes"].Temp9am.describe()["mean"].round(1),
            df[df["RainToday"] == "Yes"].Temp9am.describe()["std"].round(1),
            df[df["RainToday"] == "No"].Temp9am.describe()["mean"].round(1),
            df[df["RainToday"] == "No"].Temp9am.describe()["std"].round(1),
            df[(df["RainToday"] == "Yes") & (df["Month"] == 7)].Temp9am.describe()["mean"].round(1),
            df[(df["RainToday"] == "Yes") & (df["Month"] == 7)].Temp9am.describe()["std"].round(1),
            df[(df["RainToday"] == "No") & (df["Month"] == 7)].Temp9am.describe()["mean"].round(1),
            df[(df["RainToday"] == "No") & (df["Month"] == 7)].Temp9am.describe()["std"].round(1),
            df[(df["RainToday"] == "Yes") & (df["Month"] == 1)].Temp9am.describe()["mean"].round(1),
            df[(df["RainToday"] == "Yes") & (df["Month"] == 1)].Temp9am.describe()["std"].round(1),
            df[(df["RainToday"] == "No") & (df["Month"] == 1)].Temp9am.describe()["mean"].round(1),
            df[(df["RainToday"] == "No") & (df["Month"] == 1)].Temp9am.describe()["std"].round(1),
            df[df["RainToday"] == "Yes"].Temp3pm.describe()["mean"].round(1),
            df[df["RainToday"] == "Yes"].Temp3pm.describe()["std"].round(1),
            df[df["RainToday"] == "No"].Temp3pm.describe()["mean"].round(1),
            df[df["RainToday"] == "No"].Temp3pm.describe()["std"].round(1),
            df[(df["RainToday"] == "Yes") & (df["Month"] == 7)].Temp3pm.describe()["mean"].round(1),
            df[(df["RainToday"] == "Yes") & (df["Month"] == 7)].Temp3pm.describe()["std"].round(1),
            df[(df["RainToday"] == "No") & (df["Month"] == 7)].Temp3pm.describe()["mean"].round(1),
            df[(df["RainToday"] == "No") & (df["Month"] == 7)].Temp3pm.describe()["std"].round(1),
            df[(df["RainToday"] == "Yes") & (df["Month"] == 1)].Temp3pm.describe()["mean"].round(1),
            df[(df["RainToday"] == "Yes") & (df["Month"] == 1)].Temp3pm.describe()["std"].round(1),
            df[(df["RainToday"] == "No") & (df["Month"] == 1)].Temp3pm.describe()["mean"].round(1),
            df[(df["RainToday"] == "No") & (df["Month"] == 1)].Temp3pm.describe()["std"].round(1)
        ),unsafe_allow_html=True)
        
        #Valeurs manquantes
        st.markdown("<h4><u><font color = 'navy'>Valeurs manquantes :</u></h4>",unsafe_allow_html=True)
        st.markdown("<ul><li>MinTemp : <i><b>{}</b> valeurs manquantes ({} %)</i></li> <li>MaxTemp : <i><b>{}</b> valeurs manquantes ({} %)</i></li> <li>Temp9am : <i><b>{}</b> valeurs manquantes ({} %)</i></li> <li>Temp3pm : <i><b>{}</b> valeurs manquantes ({} %)</i>.</li></ul>".format(
            df_saved.MinTemp.isna().sum(),
            ((100*df_saved.MinTemp.isna().sum())/df_saved.shape[0]).round(1),
            df_saved.MaxTemp.isna().sum(),
            ((100*df_saved.MaxTemp.isna().sum())/df_saved.shape[0]).round(1),
            df_saved.Temp9am.isna().sum(),
            ((100*df_saved.Temp9am.isna().sum())/df_saved.shape[0]).round(1),
            df_saved.Temp3pm.isna().sum(),
            ((100*df_saved.Temp3pm.isna().sum())/df_saved.shape[0]).round(1)),unsafe_allow_html=True)
        
        #Visualisation graphique
        st.markdown("<h4><u><font color = 'navy'>Visualisation graphique :</u></h4>",unsafe_allow_html=True)
        
        fig_temp = plt.figure(figsize = (10, 15))
        plt.suptitle("Variation mensuelle des températures", fontsize = 24, fontweight = "bold")
        plt.subplot(3,1,1)
        plt.title("Températures maximales et minimales.", fontsize = 18, pad = 20)
        sns.lineplot(x = "Month", y = "MaxTemp", data = df, label = "Température maximale", color = "orange", marker = "o")
        sns.lineplot(x = "Month", y = "MinTemp", data = df, label = "Température minimale", color = "teal", marker = "D")
        plt.ylabel("Température", fontsize = 15)
        plt.xlabel("Mois", fontsize = 15)
        plt.legend(facecolor = 'white')
        plt.grid(axis = "y")
        plt.ylim([0,30])
        plt.yticks(range(0,31,2), size = 12)
        plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], ["jan.", "fev.", "mar.", "avr.", "mai", "juin", "juil", "août", "sep.", "oct.", "nov.", "déc."], size = 12)
        
        plt.subplot(3,1,2)
        plt.title("Températures à 9h.", fontsize = 18, pad = 20)
        sns.lineplot(x = "Month", y = "Temp9am", data = df[df["RainToday"] == "Yes"], label = "Pluie", color = "navy", marker = "o")
        sns.lineplot(x = "Month", y = "Temp9am", data = df[df["RainToday"] == "No"], label = "Pas de pluie", color = "red", marker = "o")
        plt.xlabel("Mois", fontsize = 15)
        plt.ylabel("Température", size = 15)
        plt.legend(facecolor = 'white')
        plt.grid(axis = "y")
        plt.ylim([0,30])
        plt.yticks(range(0,31,2), size = 12)
        plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], ["jan.", "fev.", "mar.", "avr.", "mai", "juin", "juil", "août", "sep.", "oct.", "nov.", "déc."], size = 12)
        
        plt.subplot(3,1,3)
        plt.title("Températures à 15h.", fontsize = 18, pad = 20)
        sns.lineplot(x = "Month", y = "Temp3pm", data = df[df["RainToday"] == "Yes"], label = "Pluie", color = "navy", marker = "o")
        sns.lineplot(x = "Month", y = "Temp3pm", data = df[df["RainToday"] == "No"], label = "Pas de pluie", color = "red", marker = "o")
        plt.xlabel("Mois", fontsize = 15)
        plt.ylabel("Température", size = 15)
        plt.legend(facecolor = 'white')
        plt.grid(axis = "y")
        plt.ylim([0,30])
        plt.yticks(range(0,31,2), size = 12)
        plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], ["jan.", "fev.", "mar.", "avr.", "mai", "juin", "juil", "août", "sep.", "oct.", "nov.", "déc."], size = 12)
        
        plt.tight_layout(pad=3)
        st.pyplot(fig_temp);        
    
    ##PRECIPITATIONS
        
    elif var_a_afficher == "Précipitations":
    
        #RAINFALL, EVAPORATION, HUMIDITY9AM, HUMIDITY3PM
        st.markdown("<h2><u><center>Rainfall, Evaporation, Humidity9am, Humidity3pm</center></u></h2>",unsafe_allow_html=True)
        
        #Définition des variables
        st.markdown("<h4><u><font color = 'navy'>Définition des variables :</u></h4>",unsafe_allow_html=True)
        st.markdown("""<ul><li><b>Rainfall</b> est définie comme <i>'The amount of rainfall recorded for the day in mm'</i>, soit la hauteur des précipitations en mm.</li>
        <li><b>Evaporation</b> est définie comme <i>'The so-called Class A pan evaporation (mm) in the 24 hours to 9am'</i>, soit hauteur évaporée sur la journée, relevée à 9h.</li>
        <li><b>Humidity9am</b> est définie comme <i>'Humidity (percent) at 9am'</i>, soit le pourcentage d'humidité relevé à 9h.</li>
        <li><b>Humidity3pm</b> est définie comme <i>'Humidity (percent) at 3pm'</i>, soit le pourcentage d'humidité relevé à 15h.</li></ul>""",unsafe_allow_html=True)
        
        #Description des variables
        st.markdown("<h4><u><font color = 'navy'>Description des variables :</u></h4>",unsafe_allow_html=True)
        st.markdown("<h5><i>Rainfall :</i></h5>",unsafe_allow_html=True)
        st.markdown("""<div style="text-align: justify">Il y'a <b>{}</b> relevés qui concernent des jours de pluie (soit <b>{} %</b> des relevés), avec une grande variabilité 
        de la hauteur de précipitations. En effet, les jours de pluie la hauteur moyenne des précipitations est de <b>{} ± {} cm</b>, 
        avec une valeur maximale de <b>{} cm</b>. Attention, les moyennes sont biaisées par des valeurs hautes, la hauteur médiane 
        des précipitations étant de <b>{} cm</b>, IQR : (<b>{} - {}</b>). Enfin, cette variable est directement liée à RainToday : 
        RainToday = '<i>no</i>' quand Rainfall ≤ 1.0 et RainToday = '<i>yes</i>' quand Rainfall > 1.0 cm.</div>
        """.format(
            df.Rainfall[df["Rainfall"] > 1].count(),
            (100*(df.Rainfall[df["Rainfall"] > 1].count())/len(df.Rainfall)).round(2),
            df.groupby("RainToday")["Rainfall"].describe()["mean"][1].round(1),
            df.groupby("RainToday")["Rainfall"].describe()["std"][1].round(1),
            df.groupby("RainToday")["Rainfall"].describe()["max"][1],
            df.groupby("RainToday")["Rainfall"].describe()["50%"][1],
            df.groupby("RainToday")["Rainfall"].describe()["25%"][1],
            df.groupby("RainToday")["Rainfall"].describe()["75%"][1]),unsafe_allow_html=True)    
        
        st.markdown("<h5><i><br/>Evaporation :</i></h5>",unsafe_allow_html=True)
        st.markdown(("""<div style="text-align: justify">Evaporation présente beaucoup d'outliers et est visiblement correlée à RainToday. 
        Le phénomène d'évaporation est plus imporant les jours sans pluie, aussi cette variable semble se comporter 
        inversement à Rainfall en fonction de RainToday. La hauteur d'évaporation médiane est de <b>{} cm</b>, 
        IQR (<b>{} - {}</b>) les jours de pluie et de <b>{} cm</b>, IQR (<b>{} - {}</b>) les jours sans pluie.</div>
        """.format(
            df.groupby("RainToday")["Evaporation"].describe()["50%"][1],
            df.groupby("RainToday")["Evaporation"].describe()["25%"][1],
            df.groupby("RainToday")["Evaporation"].describe()["75%"][1],
            df.groupby("RainToday")["Evaporation"].describe()["50%"][0],
            df.groupby("RainToday")["Evaporation"].describe()["25%"][0],
            df.groupby("RainToday")["Evaporation"].describe()["75%"][0])),unsafe_allow_html=True)
        
        st.markdown("<h5><i><br/>Humidity9am :</i></h5>",unsafe_allow_html=True)
        st.markdown("""<div style="text-align: justify">Le pourcentage d'humidité à 9h moyen est de <b>{} ± {} %</b> les jours de pluie et de 
        <b>{} ± {} %</b> les jours sans pluie. L'humidité à 9h ne semble pas corrélée à l'humidité à 15h ; en
        revanche une corrélation avec la hauteur des précipitations pourrait exister
        (notamment pour les hautes précipitations), mais limitée par la forte variabilité existant pour le taux 
        d'humidité. Le taux d'humidité à 9h varie relativement peu d'une localité à l'autre, à l'exception de certaines 
        zones situées dans les terres (Alice Springs, Woomera, Cobar, Uluru...) qui présentent des taux plus bas. 
        On remarque dans l'ensemble de nombreux outliers pour les valeurs d'humidité plus basses, et il apprait 
        que l'humidité à 9h varie au fil des mois, de façon assez similaire qu'il pleuve ou non, et avec une variabilité 
        par mois limitée et stable d'une année sur l'autre.</div>
        """.format(
            df[df["RainToday"] == "Yes"].Humidity9am.describe()["mean"].round(1),
            df[df["RainToday"] == "Yes"].Humidity9am.describe()["std"].round(1),
            df[df["RainToday"] == "No"].Humidity9am.describe()["mean"].round(1),
            df[df["RainToday"] == "No"].Humidity9am.describe()["std"].round(1)),unsafe_allow_html=True)
                
        st.markdown("<h5><i><br/>Humidity3pm :</i></h5>",unsafe_allow_html=True)
        st.markdown("""<div style="text-align: justify">Le pourcentage d'humidité à 15h moyen est de <b>{} ± {} %</b> les jours de pluie 
        et de <b>{} ± {} %</b> les jours sans pluie. Il existe une variabilité notoire pour le taux d'humidité à 15h 
        d'une localité à l'autre. A la différence de l'humidité à 9h, il existe aussi des outliers pour les valeurs
        hautes ; les autres observations à 9h sont transposables à 15h. Enfin, le taux d'humidité à 15h est globalement
        plus faible que celui relevé à 9h.</div>
        """.format(
            df[df["RainToday"] == "Yes"].Humidity3pm.describe()["mean"].round(1),
            df[df["RainToday"] == "Yes"].Humidity3pm.describe()["std"].round(1),
            df[df["RainToday"] == "No"].Humidity3pm.describe()["mean"].round(1),
            df[df["RainToday"] == "No"].Humidity3pm.describe()["std"].round(1)),unsafe_allow_html=True)
        
        #Valeurs manquantes
        st.markdown("<h4><u><font color = 'navy'>Valeurs manquantes :</u></h4>",unsafe_allow_html=True)
        st.markdown("<ul><li>Rainfall : <i><b>{}</b> valeurs manquantes ({} %)</i></li> <li>Evaporation : <i><b>{}</b> valeurs manquantes ({} %)</i></li> <li>Humidity9am : <i><b>{}</b> valeurs manquantes ({} %)</i></li> <li>Humidity3pm : <i><b>{}</b> valeurs manquantes ({} %)</i>.</li></ul>".format(
            df_saved.Rainfall.isna().sum(),
            ((100*df_saved.Rainfall.isna().sum())/df_saved.shape[0]).round(1),
            df_saved.Evaporation.isna().sum(),
            ((100*df_saved.Evaporation.isna().sum())/df_saved.shape[0]).round(1),
            df_saved.Humidity9am.isna().sum(),
            ((100*df_saved.Humidity9am.isna().sum())/df_saved.shape[0]).round(1),
            df_saved.Humidity3pm.isna().sum(),
            ((100*df_saved.Humidity3pm.isna().sum())/df_saved.shape[0]).round(1)),unsafe_allow_html=True)
        
        #Visualisation graphique
        st.markdown("<h4><u><font color = 'navy'>Visualisation graphique :</u></h4>",unsafe_allow_html=True)
        
        #histogrammes
        fig_precipitations_1 = plt.figure(figsize = (13,13))
        plt.suptitle("Distribution des variables Rainfall, Evaporation, Humidity9am et Humidity3pm", fontsize = 22, fontweight = "bold")
        
        plt.subplot(221)
        plt.title("Hauteur des précipitations\n (les jours de pluie)", fontsize = 18, pad = 20)
        sns.histplot(x = "Rainfall", data = df[df["Rainfall"] > 1], bins = 200)
        plt.xticks(range(0,51,5), size = 14)
        plt.xlim(0,50)
        plt.xlabel("Rainfall", size = 16)
        plt.yticks(size = 14)
        plt.ylabel("Compte", size = 16)
        
        plt.subplot(222)
        plt.title("Hauteur de l'évaporation", fontsize = 18, pad = 20)
        sns.histplot(x = "Evaporation", data = df, hue = "RainToday", hue_order= ["Yes", "No"], bins = 150)
        plt.xlim(0,25)
        plt.xticks(range(0,26,5), size = 14)
        plt.xticks()
        plt.xlabel("Evaporation", size = 16)
        plt.yticks(size = 14)
        plt.ylabel("Compte", size = 16)
        plt.legend(labels=["Pas de pluie","Pluie"], facecolor = 'white')
        
        plt.subplot(223)
        plt.title("Pourcentage d'humidité\n (relevé à 9h)", fontsize = 18, pad = 20)
        sns.histplot(x = "Humidity9am", data = df, hue = "RainToday", hue_order= ["Yes", "No"], bins = 15)
        plt.xticks(range(0,101,10), size = 14)
        plt.xlabel("Humidity9am", size = 16)
        plt.yticks(size = 14)
        plt.ylabel("Compte", size = 16)
        plt.legend(labels=["Pas de pluie","Pluie"], facecolor = 'white')
        
        plt.subplot(224)
        plt.title("Pourcentage d'humidité\n (relevé à 15h)", fontsize = 18, pad = 20)
        sns.histplot(x = "Humidity3pm", data = df, hue = "RainToday", hue_order= ["Yes", "No"], bins = 15)
        plt.xticks(range(0,101,10), size = 14)
        plt.xlabel("Humidity3pm", size = 16)
        plt.yticks(size = 14)
        plt.ylabel("Compte", size = 16)
        plt.legend(labels=["Pas de pluie","Pluie"], facecolor = 'white')
        
        plt.tight_layout(pad=2)
        st.pyplot(fig_precipitations_1);
        
        #boxplots
        fig_precipitations_2 = plt.figure(figsize = (11,11))
        plt.suptitle("Distribution comparée en fonction de la pluie", fontsize = 22, fontweight = "bold")
        
        plt.subplot(221)
        plt.title("Hauteur des précipitations", fontsize = 18, pad = 20)
        sns.boxplot(y = "Rainfall", data = df, x = "RainToday", palette = ["orange", "lightblue"], width=0.3)
        plt.xticks(ticks = [0,1], labels = ["Pas de pluie", "Pluie"], size = 16)
        plt.xlabel(None)
        plt.yticks(size = 14)
        plt.ylabel("Rainfall (mm)", size =16)
        plt.ylim([0,50])
        
        plt.subplot(222)
        plt.title("Hauteur de l'évaporation", fontsize = 18, pad = 20)
        sns.boxplot(y = "Evaporation", data = df, x = "RainToday", palette = ["orange", "lightblue"], width=0.3)
        plt.xticks(ticks = [0,1], labels = ["Pas de pluie", "Pluie"], size = 16)
        plt.xlabel(None)
        plt.yticks(size = 14)
        plt.ylabel("Evaporation (mm)", size =16)
        plt.ylim([0,25])
        
        plt.subplot(223)
        plt.title("Pourcentage d'humidité\n (relevé à 9h)", fontsize = 18, pad = 20)
        sns.boxplot(y = "Humidity9am", data = df, x = "RainToday", palette = ["orange", "lightblue"], width=0.3)
        plt.xticks(ticks = [0,1], labels = ["Pas de pluie", "Pluie"], size = 16)
        plt.xlabel(None)
        plt.yticks(size = 14)
        plt.ylabel("Humidity9am (%)", size =16)
        
        plt.subplot(224)
        plt.title("Pourcentage d'humidité\n (relevé à 15h)", fontsize = 18, pad = 20)
        sns.boxplot(y = "Humidity3pm", data = df, x = "RainToday", palette = ["orange", "lightblue"], width=0.3)
        plt.xticks(ticks = [0,1], labels = ["Pas de pluie", "Pluie"], size = 16)
        plt.xlabel(None)
        plt.yticks(size = 14)
        plt.ylabel("Humidity3pm (%)", size =16)
        
        plt.tight_layout(pad=3)
        st.pyplot(fig_precipitations_2);
        
        st.markdown("<i>Pour une meilleure visualisation, les données de Rainfall sont représentées jusqu'à 50 mm, les outliers vont jusque {} mm. Les données pour Evaporation sont représentées jusqu'à 25 mm, les outliers vont jusque {} mm.</i>".format(
        df.Rainfall.describe()["max"],
        df.Evaporation.describe()["max"]),unsafe_allow_html=True)    
    
    ##ENSOLEILLEMENT, ENNUAGEMENT.
    
    elif var_a_afficher == "Ensoleillement, ennuagement":        
              
        #SUNSHINE, CLOUDS9AM, CLOUDS3PM
        st.markdown("<h2><u><center>Sunshine, Clouds9am, Clouds3pm</center></u></h2>",unsafe_allow_html=True)
        
        #Définition des variables
        st.markdown("<h4><u><font color = 'navy'>Définition des variables :</u></h4>", unsafe_allow_html=True)
        st.markdown("""<ul><li><b>Sunshine</b> est définie comme <i>'The number of hours of bright sunshine in the day.'</i>, soit le nombre d'heures d'ensoleillement sur la journée.</li>
        <li><b>Cloud9am</b> est définie comme <i>'Fraction of sky obscured by cloud at 9am. This is measured in "oktas", which are a unit of eigths. It records how many'</i>, soit le degré de couverture du ciel, mesuré en octas à 9h.</li>
        <li><b>Cloud3pm</b> est définie comme <i>'Fraction of sky obscured by cloud at 3pm. This is measured in "oktas", which are a unit of eigths. It records how many'</i>, soit le degré de couverture du ciel, mesuré en octas à 15h.</li>
        </ul>""",unsafe_allow_html=True)
        
        #Description des variables
        st.markdown("<h4><u><font color = 'navy'>Description des variables :</u></h4>",unsafe_allow_html=True)
        st.markdown("<h5><i>Sunshine :</i></h5>",unsafe_allow_html=True)
        st.markdown("""<div style="text-align: justify">L'ensoleillement médian est de <b>{} heures</b> 
        les jours de pluie et de <b>{} heures</b> les jours sans pluie. Toute météo confondue, la durée d'ensoleillement est 
        <b>maximale</b> entre <b>décembre et février</b> (<b>{} heures</b>) et <b>minimale</b> entre <b>mai et juillet</b> 
        (<b>{} heures</b>). D'une année à l'autre, mois par mois, il existe une variabilité de l'ensoleillement plus importante 
        les jours de pluie que les jours sans pluie.</div>
        """.format(
            df[df["RainToday"] == "Yes"].Sunshine.median(),
            df[df["RainToday"] == "No"].Sunshine.median(),
            df[(df["Month"] == 12) | (df["Month"] == 1) | (df["Month"] == 2)].Sunshine.median(),
            df[(df["Month"] == 5) | (df["Month"] == 6) | (df["Month"] == 7)].Sunshine.median()),unsafe_allow_html=True)
        
        st.markdown("<h5><i><br/>Cloud9am :</i></h5>",unsafe_allow_html=True)       
        st.markdown("""<div style="text-align: justify">L'ennuagement médian à 9h est de <b>{}</b> les jours 
        de pluie et de <b>{}</b> les jours sans pluie.La variabilité est nettement plus importante les jours sans pluie. 
        L'ennuagement à 9h est très inconstant d'une localité à l'autre, toutefois il y a dans l'ensemble <b>peu d'outliers</b>. 
        L'ennuagement à 9h est totalement décorrélé de celui à 15h. <b>Douze localités</b> n'ont <b>aucun relevé</b>
        d'ennuagement à 9h : Badgery Creek, Norah Head, Penrith, Tuggeranong, Mount Ginini, Nhil, Dartmoor, Gold Coast, 
        Adelaide, Witchcliffe, Salmon Gums et Walpole. Enfin, l'ennuagement à 9h varie au fil des mois, de façon assez 
        similaire qu'il pleuve ou non, et avec une variabilité par mois limitée et stable d'une année sur l'autre.</div>
        """.format(
            round(df[df["RainToday"] == "Yes"].Cloud9am.median(),1),
            round(df[df["RainToday"] == "No"].Cloud9am.median(),1)),unsafe_allow_html=True)
        
        st.markdown("<h5><i><br/>Cloud3pm :</i></h5>",unsafe_allow_html=True)       
        st.markdown("""<div style="text-align: justify">L'ennuagement médian à 15 est de <b>{}</b> les jours de pluie 
        et de <b>{}</b> les jours sans pluie. En dépit de l'absence de corrélation avec l'ennuagement matinal, Cloud3pm se comporte similairement à Cloud9am.</div>
        """.format(
            round(df[df["RainToday"] == "Yes"].Cloud3pm.median(),1),
            round(df[df["RainToday"] == "No"].Cloud3pm.median(),1)),unsafe_allow_html=True)
        
        #Valeurs manquantes
        st.markdown("<h4><u><font color = 'navy'>Valeurs manquantes :</u></h4>",unsafe_allow_html=True)
        st.markdown("<ul><li>Sunshine : <i><b>{}</b> nans ({} %)</i></li> <li>Clouds9am : <i><b>{}</b> nans ({} %)</i></li> <li>Clouds3pm : <i><b>{}</b> nans ({} %)</i></li></ul>".format(
            df_saved.Sunshine.isna().sum(),
            ((100*df_saved.Sunshine.isna().sum())/df_saved.shape[0]).round(1),
            df_saved.Cloud9am.isna().sum(),
            ((100*df_saved.Cloud9am.isna().sum())/df_saved.shape[0]).round(1),
            df_saved.Cloud3pm.isna().sum(),
            ((100*df_saved.Cloud3pm.isna().sum())/df_saved.shape[0]).round(1)),unsafe_allow_html=True)      
        
        #Visualisation graphique
        st.markdown("<h4><u><font color = 'navy'>Visualisation graphique :</u></h4>",unsafe_allow_html=True)
        
        #histogrammes
        fig_soleil_1 = plt.figure(figsize = (12,12))
        plt.suptitle("Distribution des variables Sunshine, Cloud9am et Cloud3pm", fontsize = 22)
        
        plt.subplot(221)
        plt.title("Ensoleillement", fontsize = 18, pad = 20)
        sns.histplot(x = "Sunshine", data = df, hue = "RainToday", hue_order= ["Yes", "No"], bins = 15)
        plt.xticks(size = 14)
        #plt.xlim(0,50)
        plt.xlabel("Sunshine", size = 16)
        plt.yticks(size = 14)
        plt.ylabel("Compte", size = 16)
        plt.legend(labels=["Pas de pluie","Pluie"], facecolor = 'white')
        
        plt.subplot(223)
        plt.title("Ennuagement\n (relevé à 9h)", fontsize = 18, pad = 20)
        sns.histplot(x = "Cloud9am", data = df, hue = "RainToday", hue_order= ["Yes", "No"], bins = 9)
        #plt.xlim(0,25)
        plt.xticks(range(0,10,1), size = 14)
        plt.xticks()
        plt.xlabel("Cloud9am", size = 16)
        plt.yticks(size = 14)
        plt.ylabel("Compte", size = 16)
        plt.legend(labels=["Pas de pluie","Pluie"], facecolor = 'white')
        
        plt.subplot(224)
        plt.title("Ennuagement\n (relevé à 15h)", fontsize = 18, pad = 20)
        sns.histplot(x = "Cloud3pm", data = df, hue = "RainToday", hue_order= ["Yes", "No"], bins = 9)
        plt.xticks(range(0,10,1), size = 14)
        plt.xlabel("Cloud3pm", size = 16)
        plt.yticks(size = 14)
        plt.ylabel("Compte", size = 16)
        plt.legend(labels=["Pas de pluie","Pluie"], facecolor = 'white')
        
        plt.tight_layout(pad=3)
        st.pyplot(fig_soleil_1);
        
        #boxplots
        fig_soleil_2 = plt.figure(figsize = (12,12))
        plt.suptitle("Distribution comparée en fonction de la pluie", fontsize = 22)
        
        plt.subplot(221)
        plt.title("Ensoleillement", fontsize = 18, pad = 20)
        sns.boxplot(y = "Sunshine", data = df, x = "RainToday", palette = ["orange", "lightblue"], width=0.3)
        plt.xticks(ticks = [0,1], labels = ["Pas de pluie", "Pluie"], size = 16)
        plt.xlabel(None)
        plt.yticks(range(0,17,2),size = 14)
        plt.ylabel("Sunshine (h)", size =16)
        plt.ylim(0,16)
        
        plt.subplot(223)
        plt.title("Ennuagement\n (relevé à 9h)", fontsize = 18, pad = 20)
        sns.boxplot(y = "Cloud9am", data = df, x = "RainToday", palette = ["orange", "lightblue"], width=0.3)
        plt.xticks(ticks = [0,1], labels = ["Pas de pluie", "Pluie"], size = 16)
        plt.xlabel(None)
        plt.yticks(range(0,10,1), size = 14)
        plt.ylabel("Cloud9am (octa)", size =16)
        
        plt.subplot(224)
        plt.title("Ennuagement\n (relevé à 15h)", fontsize = 18, pad = 20)
        sns.boxplot(y = "Cloud3pm", data = df, x = "RainToday", palette = ["orange", "lightblue"], width=0.3)
        plt.xticks(ticks = [0,1], labels = ["Pas de pluie", "Pluie"], size = 16)
        plt.xlabel(None)
        plt.yticks(range(0,10,1), size = 14)
        plt.ylabel("Cloud3pm (octa)", size =16)
        
        plt.tight_layout(pad=3)
        st.pyplot(fig_soleil_2);
        
        display(Markdown("""<i>L'obscurcissement du ciel par les nuages (variables Cloud9am et Cloud3pm) est mesurés en octa : 
        un ciel parfaitement clair est indiqué par la valeur de 0 octa, alors qu'un ciel complètement couvert est estimé à 8 octas. 
        La valeur spéciale de 9 octas est utilisée quand le ciel n'est pas observable en raison d'une obstruction à la visibilité 
        (par exemple en cas de brouillard).</i>"""))
    
    ##DIRECTION DU VENT.
    
    elif var_a_afficher == "Direction du vent":
        
        st.markdown("<h2><u><center>WindGustDir, WindDir9am, WindDir3pm</center></u></h2>", unsafe_allow_html=True)
        
        #Définition des variables
        st.markdown("<h4><u><font color = 'navy'>Définition des variables :</u></h4>",unsafe_allow_html=True)
        st.markdown("""<ul><li><b>WindGustDir</b> est définie comme <i>'The direction of the strongest wind gust in the 24 hours to 
        midnight.'</i>, soit la direction de la plus forte rafale de vent sur 24h.</li>
        <li><b>WindDir9am</b> est définie comme <i>'Direction of the wind at 9am'</i>, soit la direction du vent à 9h.</li>
        <li><b>WindDir3pm</b> est définie comme <i>'Direction of the wind at 3pm'</i>, soit la direction du vent à 15h.</li>
        </ul>""", unsafe_allow_html=True)
        
        #Description des variables
        st.markdown("<h4><u><font color = 'navy'>Description des variables :</u></h4>", unsafe_allow_html=True)
        st.markdown("<h5><i>WindGustDir :</i></h5>", unsafe_allow_html=True)
        st.markdown("""<div style="text-align: justify">Cette variable comporte <b>16 modalités</b> (Nord, Nord-Nord-Est, Nord-Est, Est-Nord-Est, Est...).
         Au sein d'un même état, les vents dominants ne sont jamais largement majoritaires : il existe une
         <b>importante variabilité</b> des directions qu'il pleuve ou non.
         Deux stations n'ont <b>aucun relevé</b> : <b>Albany</b> et <b>Newcastle</b>.</div>
        """, unsafe_allow_html=True)
        st.markdown("<h5><i><br/>WindDir9am et WindDir3pm :</i></h5>", unsafe_allow_html=True)
        st.markdown("""<div style="text-align: justify">Ces deux variables sont comportent les 16 mêmes modalités que WindGustDir.
         La matrice de confusion entre les données mesurées à 9h et à 15h montre qu'à la fois,
          s'il est très fréquent que la direction du vent ne soit pas la même entre ces deux horaires,
           il reste assez rare que le vent change complètement d'orientation. 
           Par exemple, pour un vent venant du Sud à 9h, les principales directions à 15h sont Sud, 
           Sud-Sud-Est, Sud-Est, Sud-Sud-Ouest et Sud-Ouest.</div>
        """, unsafe_allow_html=True)
        
        #Valeurs manquantes
        st.markdown("<h4><u><font color = 'navy'>Valeurs manquantes :</u></h4>", unsafe_allow_html=True)
        st.markdown("<ul><li>WindGustDir : <i><b>{}</b> valeurs manquantes ({} %)</i></li> <li>WindDir9am : <i><b>{}</b> valeurs manquantes ({} %)</i></li> <li>WindDir3pm : <i><b>{}</b> valeurs manquantes ({} %)</i></li></ul>".format(
            df_saved.WindGustDir.isna().sum(),
            ((100*df_saved.WindGustDir.isna().sum())/df_saved.shape[0]).round(1),
            df_saved.WindDir9am.isna().sum(),
            ((100*df_saved.WindDir9am.isna().sum())/df_saved.shape[0]).round(1),
            df_saved.WindDir3pm.isna().sum(),
            ((100*df_saved.WindDir3pm.isna().sum())/df_saved.shape[0]).round(1)),unsafe_allow_html=True)   
        
    elif var_a_afficher == "Force du vent":
        #WINDGUSTSPEED, WINDSPEED9AM, WINDSPEED3PM,
        st.markdown("<h2><u><center>WindGustSpeed, WindSpeed9am, WindSpeed3pm</center></u></h2>", unsafe_allow_html=True)
        
        #Définition des variables
        st.markdown("<h4><u><font color = 'navy'>Définition des variables :</u></h4>", unsafe_allow_html=True)
        st.markdown("""<ul><li><b>WindGustSpeed</b> est définie comme <i>'The speed (km/h) of the strongest wind gust in the 24 hours to midnight'</i>, soit la vitesse de la plus forte rafale de vent sur 24h.</li>
        <li><b>WindSpeed9am</b> est définie comme <i>'Wind speed (km/hr) averaged over 10 minutes prior to 9am'</i>, soit la vitesse moyenne du vent entre 8:50 et 9:00.</li>
        <li><b>WindSpeed3pm</b> est définie comme <i>'Wind speed (km/hr) averaged over 10 minutes prior to 3pm'</i>, soit la vitesse moyenne du vent entre 14:50 et 15:00.</li>
        </ul>""",unsafe_allow_html=True)
        
        #Description des variables
        st.markdown("<h4><u><font color = 'navy'>Description des variables :</u></h4>", unsafe_allow_html=True)
        st.markdown("<h5><i>WindGustSpeed :</i></h5>",unsafe_allow_html=True)
        st.markdown("""<div style = 'text-align : justify'>Les relevés vont de <b>{}</b> à <b>{} km/h</b>, 
        avec une vitesse moyenne de <b>{} km/h</b>. Il existe de nombreux outliers dans les valeurs hautes, 
        mais leur impact reste limité (vitesse médiane : <b>{} km/h</b>). Similairement à la variable WindGustDir, 
        il n'y a <b>aucun relevé</b> pour les stations <b>Albany</b> et <b>Newcastle</b>. De façon intéressante, 
        les données suggèrent que le vent souffle plus fort les jours de pluie : <b>{} km/h</b> en moyenne 
         contre <b>{} km/h</b> les jours sans pluie. Enfin, la variabilité semble plus importante les jours de pluie.</div>
        """.format(df.WindGustSpeed.describe()["min"],
                   df.WindGustSpeed.describe()["max"],
                   df.WindGustSpeed.describe()["mean"].round(1),
                   df.WindGustSpeed.describe()["50%"],
                   df[df["RainToday"] == "Yes"].WindGustSpeed.describe()["mean"].round(1),
                   df[df["RainToday"] == "No"].WindGustSpeed.describe()["mean"].round(1)), unsafe_allow_html=True)
        
        st.markdown("<h5><i><br/>WindSpeed9am :</i></h5>", unsafe_allow_html=True)
        st.markdown("""<div style = 'text-align : justify'>La vitesse moyenne du vent à 9h est de <b>{} ± {} km/h</b> 
        les jours de pluie, et de <b>{} ± {} km/h</b> les jours sans pluie. Les données à 9h sont grossièrement corrélées 
        à celles mesurées à 15h, ainsi qu'avec le relevé de vitesse de la plus forte rafale,
        avec toutefois une importante variabilité.</div>
        """.format(df[df["RainToday"] == "Yes"].WindSpeed9am.describe()["mean"].round(1),
                   df[df["RainToday"] == "Yes"].WindSpeed9am.describe()["std"].round(1),
                   df[df["RainToday"] == "No"].WindSpeed9am.describe()["mean"].round(1),
                   df[df["RainToday"] == "No"].WindSpeed9am.describe()["std"].round(1)), unsafe_allow_html=True)
        
        st.markdown("<h5><i><br/>WindSpeed3pm :</i></h5>", unsafe_allow_html=True)
        st.markdown("""<div style = 'text-align : justify'>La vitesse moyenne du vent à 15h est de <b>{} ± {} km/h</b> 
        les jours de pluie, et de <b>{} ± {} km/h</b> les jours sans pluie. Les données à 15h sont grossièrement 
        corrélées avec le relevé de vitesse de la plus forte rafale, avec toutefois une importante variabilité.</div>
        """.format(df[df["RainToday"] == "Yes"].WindSpeed3pm.describe()["mean"].round(1),
                   df[df["RainToday"] == "Yes"].WindSpeed3pm.describe()["std"].round(1),
                   df[df["RainToday"] == "No"].WindSpeed3pm.describe()["mean"].round(1),
                   df[df["RainToday"] == "No"].WindSpeed3pm.describe()["std"].round(1)), unsafe_allow_html=True)
        
        st.markdown("<h4><u><font color = 'navy'>Valeurs manquantes :</u></h4>", unsafe_allow_html=True)
        st.markdown("<ul><li>WindGustSpeed : <i><b>{}</b> valeurs manquantes ({} %)</i></li> <li>WindSpeed9am : <i><b>{}</b> valeurs manquantes ({} %)</i></li> <li>WindSpeed3pm : <i><b>{}</b> valeurs manquantes ({} %)</i></li></ul>".format(
            df_saved.WindGustSpeed.isna().sum(),
            ((100*df_saved.WindGustSpeed.isna().sum())/df_saved.shape[0]).round(1),
            df_saved.WindSpeed9am.isna().sum(),
            ((100*df_saved.WindSpeed9am.isna().sum())/df_saved.shape[0]).round(1),
            df_saved.WindSpeed3pm.isna().sum(),
            ((100*df_saved.WindSpeed3pm.isna().sum())/df_saved.shape[0]).round(1)), unsafe_allow_html=True)      
        
        #Visualisation graphique
        st.markdown("<h4><u><font color = 'navy'>Visualisation graphique :</u></h4>", unsafe_allow_html=True)
        
        #histogrammes
        fig_vent_1 = plt.figure(figsize = (12,12))
        plt.suptitle("Distribution des variables WindGustSpeed, WindSpeed9am et WindSpeed3pm", fontsize = 22, fontweight = "bold")
        
        plt.subplot(221)
        plt.title("Vitesse du vent\n (plus forte rafale)", fontsize = 18, pad = 20)
        sns.histplot(x = "WindGustSpeed", data = df, hue = "RainToday", hue_order= ["Yes", "No"], bins = 24)
        plt.xticks(range(0,101,10), size = 14)
        plt.xlim(0,100)
        plt.xlabel("WindGustSpeed", size = 16)
        plt.yticks(size = 14)
        plt.ylabel("Compte", size = 16)
        plt.legend(labels=["Pas de pluie","Pluie"], facecolor = 'white')
        
        plt.subplot(223)
        plt.title("Vitesse du vent\n (relevée à 9h)", fontsize = 18, pad = 20)
        sns.histplot(x = "WindSpeed9am", data = df, hue = "RainToday", hue_order= ["Yes", "No"], bins = 30)
        plt.xlim(0,60)
        plt.xticks(size = 14)
        plt.xticks()
        plt.xlabel("WindSpeed9am", size = 16)
        plt.yticks(size = 14)
        plt.ylabel("Compte", size = 16)
        plt.legend(labels=["Pas de pluie","Pluie"], facecolor = 'white')
        
        plt.subplot(224)
        plt.title("Vitesse du vent\n (relevée à 15h)", fontsize = 18, pad = 20)
        sns.histplot(x = "WindSpeed3pm", data = df, hue = "RainToday", hue_order= ["Yes", "No"], bins = 20)
        plt.xticks(size = 14)
        plt.xlim(0,60)
        plt.xlabel("WindSpeed3pm", size = 16)
        plt.yticks(size = 14)
        plt.ylabel("Compte", size = 16)
        plt.legend(labels=["Pas de pluie","Pluie"], facecolor = 'white')
        
        plt.tight_layout(pad=3)
        st.pyplot(fig_vent_1);
        
        st.markdown("""<i>Pour une meilleure visualisation, les données de WindGustSpeed sont représentées jusqu'à 100 km/h,
        les outliers vont jusque {} km/h. Les données pour WindSpeed 9am et 3am sont représentées jusqu'à 60 km/h, 
        les outliers vont jusque {} km/h (9am) et jusque {} km/h (3pm).</i>""".format(
        df.WindGustSpeed.describe()["max"],
        df.WindSpeed9am.describe()["max"],
        df.WindSpeed3pm.describe()["max"]), unsafe_allow_html=True)
        
        #boxplots
        fig_vent_2 = plt.figure(figsize = (12,12))
        plt.suptitle("Distribution comparée en fonction de la pluie", fontsize = 22, fontweight = "bold")
        
        plt.subplot(221)
        plt.title("Vitesse du vent\n (plus forte rafale)", fontsize = 18, pad = 20)
        sns.boxplot(y = "WindGustSpeed", data = df, x = "RainToday", palette = ["orange", "lightblue"], width=0.3)
        plt.xticks(ticks = [0,1], labels = ["Pas de pluie", "Pluie"], size = 16)
        plt.xlabel(None)
        plt.yticks(size = 14)
        plt.ylabel("WindGustSpeed (km/h)", size =16)
        #plt.ylim(0,16)
        
        plt.subplot(223)
        plt.title("Vitesse du vent\n (relevée à 9h)", fontsize = 18, pad = 20)
        sns.boxplot(y = "WindSpeed9am", data = df, x = "RainToday", palette = ["orange", "lightblue"], width=0.3)
        plt.xticks(ticks = [0,1], labels = ["Pas de pluie", "Pluie"], size = 16)
        plt.xlabel(None)
        plt.yticks(size = 14)
        plt.ylabel("WindSpeed9am (km/h)", size =16)
        
        plt.subplot(224)
        plt.title("Vitesse du vent\n (relevée à 15h)", fontsize = 18, pad = 20)
        sns.boxplot(y = "WindSpeed3pm", data = df, x = "RainToday", palette = ["orange", "lightblue"], width=0.3)
        plt.xticks(ticks = [0,1], labels = ["Pas de pluie", "Pluie"], size = 16)
        plt.xlabel(None)
        plt.yticks(size = 14)
        plt.ylabel("WindSpeed3pm (km/h)", size =16)
        
        plt.tight_layout(pad=3)
        st.pyplot(fig_vent_2);
    
    ##FORCE DU VENT.
    
    elif var_a_afficher == "Pression atmosphérique":
        st.markdown("<h2><u><center>Pressure9am, Pressure3pm</center></u></h2>", unsafe_allow_html=True)
        
        #Définition des variables
        st.markdown("<h4><u><font color = 'navy'>Définition des variables :</u></h4>", unsafe_allow_html=True)
        st.markdown("""<ul><li><b>Pressure9am</b> est définie comme <i>'Atmospheric pressure (hpa) reduced to mean sea level at 9am'</i>, soit la pression atmosphérique en fonction du niveau de la mer, à 9h.</li>
        <li><b>Pressure3pm</b> est définie comme <i>'Atmospheric pressure (hpa) reduced to mean sea level at 3pm'</i>, soit la pression atmosphérique en fonction du niveau de la mer, à 15h.</li>
        </ul>""", unsafe_allow_html=True)
        
        #Description des variables
        st.markdown("<h4><u><font color = 'navy'>Description des variables :</u></h4>", unsafe_allow_html=True)
        st.markdown("<h5><i>Pressure9am :</i></h5>", unsafe_allow_html=True)
        st.markdown("""<div style = "text-align : justify">La pression atmosphérique moyenne à 9h est <b>plus basse</b> 
        les jours de pluie (<b>{} ± {} hpa</b>) que les jours sans pluie (<b>{} ± {} hpa</b>). Il y'a de nombreux outliers, 
        pour les valeurs hautes comme pour les valeurs basses. Cette variable est remarquablement constante d'une localité 
        à l'autre, avec une amplitude qui varie très peu. Exception notable pour quatre localités : Darwin (NT), Katherine (NT), 
        Cairns (QLD) et Townsville (QLD) qui ont des <b>pressions plus faibles</b> (toutes situées dans la partie 
        <b>Nord de l'Australie</b>). <b>Quatre localités</b> n'ont <b>aucun relevé</b> de pression atmosphérique à 9h : 
        Newcastle, Penrith, Mount Ginini et Salmon Gums.</div>
        """.format(df[df["RainToday"] == "Yes"].Pressure9am.describe()["mean"].round(1),
                  df[df["RainToday"] == "Yes"].Pressure9am.describe()["std"].round(1),
                  df[df["RainToday"] == "No"].Pressure9am.describe()["mean"].round(1),
                  df[df["RainToday"] == "No"].Pressure9am.describe()["std"].round(1)), unsafe_allow_html=True)
        
        st.markdown("<h5><i><br/>Pressure3pm :</i></h5>", unsafe_allow_html=True)
        st.markdown("""<div style = "text-align : justify">La pression atmosphérique moyenne à 15h est <b>plus basse</b> 
        les jours de pluie (<b>{} ± {} hpa</b>) que les jours sans pluie (<b>{} ± {} hpa</b>).
        La distribution de la pression atmosphérique est <b>très similaire à 15h et à 9h</b>. Toutefois à 15h, la différence 
        de pression entre les jours avec et sans pluie est moins marquée qu'à 9h. Il y'a également, à 15h, de nombreux outliers, 
        pour les valeurs hautes comme pour les valeurs basses.</div>
        """.format(df[df["RainToday"] == "Yes"].Pressure3pm.describe()["mean"].round(1),
                   df[df["RainToday"] == "Yes"].Pressure3pm.describe()["std"].round(1),
                   df[df["RainToday"] == "No"].Pressure3pm.describe()["mean"].round(1),
                   df[df["RainToday"] == "No"].Pressure3pm.describe()["std"].round(1)
                  ), unsafe_allow_html=True)
        
        st.markdown("<h4><u><font color = 'navy'>Valeurs manquantes :</u></h4>", unsafe_allow_html=True)
        st.markdown("<ul><li>Pressure9am : <i><b>{}</b> valeurs manquantes ({} %)</i></li> <li>Pressure3pm : <i><b>{}</b> valeurs manquantes ({} %)</i></li></ul>".format(
            df_saved.Pressure9am.isna().sum(),
            ((100*df_saved.Pressure9am.isna().sum())/df_saved.shape[0]).round(1),
            df_saved.Pressure3pm.isna().sum(),
            ((100*df_saved.Pressure3pm.isna().sum())/df_saved.shape[0]).round(1)), unsafe_allow_html=True)
        
        #Visualisation graphique
        st.markdown("<h4><u><font color = 'navy'>Visualisation graphique :</u></h4>", unsafe_allow_html=True)
        
        #histogrammes
        fig_pression_1 = plt.figure(figsize = (12,12))
        plt.suptitle("Distribution des variables Pressure9am et Pressure3pm", fontsize = 22, fontweight = 'bold')
        
        plt.subplot(221)
        plt.title("Pression atmosphérique\n (relevée à 9h)", fontsize = 18, pad = 20)
        sns.histplot(x = "Pressure9am", data = df, hue = "RainToday", hue_order= ["Yes", "No"], bins = 25)
        plt.xticks(size = 14)
        plt.xlabel("Pressure9am", size = 16)
        plt.yticks(size = 14)
        plt.ylabel("Compte", size = 16)
        plt.legend(labels=["Pas de pluie","Pluie"], facecolor = 'white')
        
        plt.subplot(222)
        plt.title("Pression atmosphérique\n (relevée à 15h)", fontsize = 18, pad = 20)
        sns.histplot(x = "Pressure3pm", data = df, hue = "RainToday", hue_order= ["Yes", "No"], bins = 25)
        plt.xticks(size = 14)
        plt.xticks()
        plt.xlabel("Pressure3pm", size = 16)
        plt.yticks(size = 14)
        plt.ylabel("Compte", size = 16)
        plt.legend(labels=["Pas de pluie","Pluie"], facecolor = 'white')
        
        plt.subplot(223)
        plt.title("Corrélation entre la pression atmosphérique\n à 9h et à 15h", fontsize = 18, pad = 20)
        sns.scatterplot("Pressure9am", "Pressure3pm", data = df)
        plt.xticks(size = 14)
        plt.xlabel("Pressure9am", size = 16)
        plt.yticks(size = 14)
        plt.ylabel("Pressure3pm", size = 16)
        
        plt.tight_layout(pad=3)
        st.pyplot(fig_pression_1);
        
        #boxplots
        fig_pression_2 = plt.figure(figsize = (12,6))
        plt.suptitle("Distribution comparée en fonction de la pluie", fontsize = 22, fontweight = 'bold')
        
        plt.subplot(121)
        plt.title("Pression atmosphérique\n (relevée à 9h)", fontsize = 18, pad = 20)
        sns.boxplot(y = "Pressure9am", data = df, x = "RainToday", palette = ["orange", "lightblue"], width=0.3)
        plt.xticks(ticks = [0,1], labels = ["Pas de pluie", "Pluie"], size = 16)
        plt.xlabel(None)
        plt.yticks(size = 14)
        plt.ylabel("Pressure9am (hpa)", size =16)
        
        plt.subplot(122)
        plt.title("Pression atmosphérique\n (relevée à 15h)", fontsize = 18, pad = 20)
        sns.boxplot(y = "Pressure3pm", data = df, x = "RainToday", palette = ["orange", "lightblue"], width=0.3)
        plt.xticks(ticks = [0,1], labels = ["Pas de pluie", "Pluie"], size = 16)
        plt.xlabel(None)
        plt.yticks(size = 14)
        plt.ylabel("Pressure3pm (km/h)", size =16)
        
        plt.tight_layout(pad=3)
        st.pyplot(fig_pression_2);
        
    ##PLUIE.    
        
    elif var_a_afficher == "Pluie":
    
        st.markdown("<h2><u><center>RainToday, RainTomorrow</center></u></h2>", unsafe_allow_html=True)
        
        #Définition des variables
        st.markdown("<h4><u><font color = 'navy'>Définition des variables :</u></h4>", unsafe_allow_html=True)
        st.markdown("""<ul><li><b>RainToday</b> est définie comme <i>'Boolean: 1 if precipitation (mm) in the 24 hours to 9am exceeds 1mm, otherwise 0'</i>, soit 1 pour un jour de pluie (défini pour une hauteur de précipitation > 1 mm, 0 sinon.</li>
        <li><b>RainTomorrow</b> est définie comme <i>'The amount of next day rain in mm. Used to create response variable RainTomorrow. A kind of measure of the "risk".'</i>, soit hauteur de précipitations le jour suivant.</li>
        </ul>""", unsafe_allow_html=True)
        st.markdown("Attention, les définitions fournies avec le dataset sont inexactes. Il s'agit pour les deux de variables catégorielles binaires, codées 'Yes' ou 'No' suivant s'il pleuvait ou non les jours considérés.", unsafe_allow_html=True)
        
        #Description des variables
        st.markdown("<h4><u><font color = 'navy'>Description des variables :</u></h4>",unsafe_allow_html=True)
        st.markdown("<h5><i>RainToday :</i></h5>", unsafe_allow_html=True)
        
        st.markdown("""<div style = 'text-align : justify'>Sur l'ensemble des données, il y a <b>{} jours de pluie</b> (<b>{} %</b>) et <b>{} jours sans pluie</b> (<b>{} %</b>).</div>
        """.format(df[df["RainToday"] == "Yes"]["RainToday"].count(),
                   (100*(df[df["RainToday"] == "Yes"]["RainToday"].count())/df.shape[0]).round(1),
                   df[df["RainToday"] == "No"]["RainToday"].count(),
                   (100*(df[df["RainToday"] == "No"]["RainToday"].count())/df.shape[0]).round(1)), unsafe_allow_html=True)
        
        st.markdown("<h5><i><br/>RainTomorrow :</i></h5>", unsafe_allow_html=True)   
        st.markdown("Il s'agit de la variable à prédire", unsafe_allow_html=True)
        
        #Valeurs manquantes
        st.markdown("<h4><u><font color = 'navy'>Valeurs manquantes :</u></h4>", unsafe_allow_html=True)
        st.markdown("<ul><li>RainToday : <i><b>{}</b> valeurs manquantes ({} %)</i></li> <li>RainTomorrow : <i><b>{}</b> valeurs manquantes ({} %)</i></li></ul>".format(
            df_saved.RainToday.isna().sum(),
            ((100*df_saved.RainToday.isna().sum())/df_saved.shape[0]).round(1),
            df_saved.RainTomorrow.isna().sum(),
            ((100*df_saved.RainTomorrow.isna().sum())/df_saved.shape[0]).round(1)),unsafe_allow_html=True)     
        
elif nav == "Machine learning":
    st.title("ESSAI D'AMÉLIORATION DU MODÈLE DE MACHINE LEARNING 🦘")
    st.markdown("<h4><u><font color = 'navy'>Révision du préprocessing.</h4></u>", unsafe_allow_html=True)
    st.markdown("""<i>Remplacement des valeurs manquantes par regroupement géographique.</i>""", unsafe_allow_html = True)

    if st.button('Démarrer le second préprocessing 🦘'):
        df = pd.read_csv("weatherAUS.csv")
        df_saved = pd.read_csv("weatherAUS.csv")
        #Création de Year, Month & Day par slicing de la valeur de Date
        df["Year"] = df["Date"].apply(lambda x : int(x[:4]))
        df["Month"] = df["Date"].apply(lambda x : int(x[5:7]))
        df["Day"] = df["Date"].apply(lambda x : int(x[8:]))
        
        #Création du dictionnaire qui contient pour chaque état australien, les stations associées
        localites = {"SA" : ["Adelaide", "MountGambier", "Woomera", "Nuriootpa"],
                    "WA" : ["Perth", "Albany", "PearceRAAF", "PerthAirport", "Walpole", "SalmonGums", "Witchcliffe"],
                    "NSW" : ["Canberra", "Sydney", "Albury", "Wollongong", "MountGinini", "Tuggeranong", "Penrith", "Newcastle", "Cobar", "SydneyAirport", "BadgerysCreek", "WaggaWagga", "Moree", "Williamtown", "CoffsHarbour", "NorahHead", "Richmond"],
                    "QLD" : ["Brisbane", "Townsville", "Cairns", "GoldCoast"],
                    "TAS" : ["Hobart", "Launceston"],
                    "VIC" : ["Melbourne", "Bendigo", "Ballarat", "Dartmoor", "Portland", "Mildura", "MelbourneAirport", "Sale", "Watsonia", "Nhil"],
                    "NT" : ["Darwin", "AliceSprings", "Katherine", "Uluru"],
                    "NI" : ["NorfolkIsland"]}
        
        #Création de la colonne State
        df["State"] = df.Location
        df["State"] = df["State"].replace(to_replace = ["Adelaide", "MountGambier", "Woomera", "Nuriootpa"], value = "SA")
        df["State"] = df["State"].replace(to_replace = ["Perth", "Albany", "PearceRAAF", "PerthAirport", "Walpole", "SalmonGums", "Witchcliffe"], value = "WA")
        df["State"] = df["State"].replace(to_replace = ["Canberra", "Sydney", "Albury", "Wollongong", "MountGinini", "Tuggeranong", "Penrith", "Newcastle", "Cobar", "SydneyAirport", "BadgerysCreek", "WaggaWagga", "Moree", "Williamtown", "CoffsHarbour", "NorahHead", "Richmond"], value = "NSW")
        df["State"] = df["State"].replace(to_replace = ["Brisbane", "Townsville", "Cairns", "GoldCoast"], value = "QLD")
        df["State"] = df["State"].replace(to_replace = ["Hobart", "Launceston"], value = "TAS")
        df["State"] = df["State"].replace(to_replace = ["Melbourne", "Bendigo", "Ballarat", "Dartmoor", "Portland", "Mildura", "MelbourneAirport", "Sale", "Watsonia", "Nhil"], value = "VIC")
        df["State"] = df["State"].replace(to_replace = ["Darwin", "AliceSprings", "Katherine", "Uluru"], value = "NT")
        df["State"] = df["State"].replace(to_replace = ["NorfolkIsland"], value = "NI")
        
        st.markdown("")
        
        #Création des deux listes nécessaires au remplacement des nans.
        loclst = []
        locgroup = ["NorfolkIsland", "Portland", "MountGinini", "Adelaide", "Darwin", "MountGambier", "GoldCoast", "Canberra", "Newcastle", "Woomera",
                   "Witchcliffe", "Moree", "Wollongong", "Bendigo", "Mildura", "WaggaWagga", "Dartmoor","Hobart", "SalmonGums", "Williamtown",
                    "Townsville", "PerthAirport", "Sydney", "Perth", "Katherine", "Albury", "Ballarat", "MelbourneAirport",
                   "BagerysCreek", "Melbourne", "Cairns", "NorahHead", "PearceRAAF", "Uluru", "Nhil", "Sale", "Richmond", 
                    "Cobar", "Penrith", "CoffsHarbour", "Nuriootpa", "Albany", "SydneyAirport", "Tuggeranong",
                    "Lauceston", "Brisbane", "Watsonia", "Walpole", "AliceSprings"]
        
        #Boucle de remplacement géographique des nans. Cette boucle ajoute les fragments du df initial, stations par stations.
        #Les dfs de chaque station sont créés. 
        for loc in locgroup:
            loclst.append(df[df["Location"] == loc])
        
        df_NorfolkIsland = loclst[0]  
        df_Portland = loclst[1]
        df_MountGinini = loclst[2]   
        df_Adelaide = loclst[3]
        df_Darwin = loclst[4]
        df_MountGambier = loclst[5]
        df_GoldCoast = loclst[6]
        df_Canberra = loclst[7]
        df_Newcastle = loclst[8]
        df_Woomera = loclst[9]
        df_Witchcliffe = loclst[10]
        df_Moree = loclst[11]
        df_Wollongong = loclst[12]
        df_Bendigo = loclst[13]
        df_Mildura = loclst[14]
        df_WaggaWagga = loclst[15]
        df_Dartmoor = loclst[16]
        df_Hobart = loclst[17]
        df_SalmonGums = loclst[18]
        df_Williamtown = loclst[19]
        df_Townsville = loclst[20]
        df_PerthAirport = loclst[21]
        df_Sydney = loclst[22]
        df_Perth = loclst[23]
        df_Katherine = loclst[24]
        df_Albury = loclst[25]
        df_Ballarat = loclst[26]
        df_MelbourneAirport = loclst[27]
        df_BadgerysCreek = loclst[28]
        df_Melbourne = loclst[29]
        df_Cairns = loclst[30]
        df_NorahHead = loclst[31]
        df_PearceRAAF = loclst[32]
        df_Uluru = loclst[33]
        df_Nhil = loclst[34]
        df_Sale = loclst[35]
        df_Richmond = loclst[36]
        df_Cobar = loclst[37]
        df_Penrith = loclst[38]
        df_CoffsHarbour = loclst[39]
        df_Nuriootpa = loclst[40]
        df_Albany = loclst[41]
        df_SydneyAirport = loclst[42]
        df_Tuggeranong = loclst[43]
        df_Lauceston = loclst[44]
        df_Brisbane = loclst[45]
        df_Watsonia = loclst[46]
        df_Walpole = loclst[47]
        df_AliceSprings = loclst[48]
        
        #Dictionnaire permettant le rappel des regroupements géographiques
        geogroup = {"df_Perth2" : "Perth, PerthAirport, PearceRAAF",
                   "df_Albany2" : "Albany, Witchcliffe, Walpole",
                   "df_Alice2" : "AliceSprings, Uluru",
                   "df_Adelaide2" : "Adelaide, Nuriootpa",
                   "df_Nhil2" : "Nhil, Mildura, Bendigo",
                   "df_Portland2" : "Portland, Dartmoor, MountGambier",
                   "df_Melbourne2" : "Melbourne, MelbourneAirport, Ballarat, Watsonia, Sale",
                   "df_Albury2" : "Albury, WaggaWagga",
                   "df_Canberra2" : "Canberra, Tugganong",
                   "df_Sydney2" : "Sydney, SydneyAirport, Richmond, Penrith, BadgeryCreeks, Wollongong",
                   "df_Newcastle2" : "Newcastle, NorahHead, Williamtown",
                   "df_Cobar2" : "Cobar, Moree",
                   "df_Brisbane2" : "Brisbane, GoldCoast, CoffsHarbour",
                   "df_Cairns2" : "Townsville, Cairns",
                   "df_Hobart2" : "Hobart, Launceston",
                   "non_poolés" : "SalmonGums, Darwin, Katherine, Woomera, MountGinini, NorfolkIsland"}
        
        #Création des dataframes pour remplacement des nans par regroupement géographique
        df_Perth2 = pd.concat([df_Perth, df_PerthAirport, df_PearceRAAF])
        df_Albany2 = pd.concat([df_Albany, df_Witchcliffe, df_Walpole])
        df_Alice2 = pd.concat([df_AliceSprings, df_Uluru])
        df_Adelaide2 = pd.concat([df_Adelaide, df_Nuriootpa])
        df_Nhil2 = pd.concat([df_Nhil, df_Mildura, df_Bendigo])
        df_Portland2 = pd.concat([df_Portland, df_Dartmoor, df_MountGambier])
        df_Melbourne2 = pd.concat([df_Melbourne, df_MelbourneAirport, df_Ballarat, df_Watsonia, df_Sale])
        df_Albury2 = pd.concat([df_Albury, df_WaggaWagga])
        df_Canberra2 = pd.concat([df_Canberra, df_Tuggeranong])
        df_Sydney2 = pd.concat([df_Sydney, df_SydneyAirport, df_Richmond, df_Penrith, df_BadgerysCreek, df_Wollongong])
        df_Newcastle2 = pd.concat([df_Newcastle, df_NorahHead, df_Williamtown])
        df_Cobar2 = pd.concat([df_Cobar, df_Moree])
        df_Brisbane2 = pd.concat([df_Brisbane, df_GoldCoast, df_CoffsHarbour])
        df_Cairns2 = pd.concat([df_Townsville, df_Cairns])
        df_Hobart2 = pd.concat([df_Hobart, df_Lauceston])
        
        geolist_brute = [df_Perth2, df_Albany2, df_Alice2, df_Adelaide2, df_Nhil2, df_Portland2, df_Melbourne2,
        df_Albury2, df_Canberra2, df_Sydney2, df_Newcastle2, df_Cobar2, df_Brisbane2, df_Cairns2, df_Hobart2,
                   df_SalmonGums, df_Darwin, df_Katherine, df_Woomera, df_MountGinini, df_NorfolkIsland]
        
        geolist_str = ["df_Perth2", "df_Albany2", "df_Alice2", "df_Adelaide2", "df_Nhil2", "df_Portland2", "df_Melbourne2",
        "df_Albury2", "df_Canberra2", "df_Sydney2", "df_Newcastle2", "df_Cobar2", "df_Brisbane2", "df_Cairns2", "df_Hobart2",
                   "df_SalmonGums", "df_Darwin", "df_Katherine", "df_Woomera", "df_MountGinini", "df_NorfolkIsland"]
        #Remplacement des nans et régénération des df groupés
        
        geolist_clean = []
        k = 0
        
        for df in geolist_brute:
            df_temp = df
            st.markdown("In progress: <i>{}</i>. <b>{}</b> nans before cleaning (<b>{} %</b>).".format(geolist_str[k], geolist_brute[k].isna().sum().sum(), round(100*(geolist_brute[k].isna().sum().sum())/(geolist_brute[k].shape[0]*geolist_brute[k].shape[1]),1)), unsafe_allow_html = True)
        
            #Elimination des nans sur RainToday et RainTomorrow
            df_temp.dropna(axis = 0, how = "any", inplace = True, subset = ["RainToday", "RainTomorrow"])
        
            for i in range(1,13,1):
                          
                #Remplacement des nans de MinTemp
                df_temp.MinTemp[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")] = df_temp.MinTemp[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].fillna(df_temp.MinTemp[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].mean())
                df_temp.MinTemp[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")] = df_temp.MinTemp[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].fillna(df_temp.MinTemp[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].mean())
                    
                #Remplacement des nans de MaxTemp
                df_temp.MaxTemp[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")] = df_temp.MaxTemp[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].fillna(df_temp.MaxTemp[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].mean())
                df_temp.MaxTemp[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")] = df_temp.MaxTemp[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].fillna(df_temp.MaxTemp[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].mean())
                
                #Remplacement de Rainfall
                df_temp.Rainfall[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")] = df_temp.Rainfall[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].fillna(df_temp.Rainfall[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].median())
                df_temp.Rainfall[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")] = df_temp.Rainfall[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].fillna(df_temp.Rainfall[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].median())
                        
                #Evaporation :
                df_temp.Evaporation[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")] = df_temp.Evaporation[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].fillna(df_temp.Evaporation[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].median())
                df_temp.Evaporation[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")] = df_temp.Evaporation[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].fillna(df_temp.Evaporation[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].median())
                
                #Sunshine :
                df_temp.Sunshine[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")] = df_temp.Sunshine[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].fillna(df_temp.Sunshine[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].median())
                df_temp.Sunshine[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")] = df_temp.Sunshine[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].fillna(df_temp.Sunshine[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].median())
                
                #WindGustdir :
                df_temp.WindGustDir[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")] = df_temp.WindGustDir[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].fillna(df_temp.WindGustDir[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].mode())
                df_temp.WindGustDir[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")] = df_temp.WindGustDir[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].fillna(df_temp.WindGustDir[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].mode())
                
                #WindGustSpeed :
                df_temp.WindGustSpeed[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")] = df_temp.WindGustSpeed[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].fillna(df_temp.WindGustSpeed[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].mean())
                df_temp.WindGustSpeed[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")] = df_temp.WindGustSpeed[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].fillna(df_temp.WindGustSpeed[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].mean())
                        
                #WindDir9am :
                df_temp.WindGustDir[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")] = df_temp.WindGustDir[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].fillna(df_temp.WindGustDir[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].mode([0]))
                df_temp.WindGustDir[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")] = df_temp.WindGustDir[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].fillna(df_temp.WindGustDir[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].mode([0]))
                        
                #WindDir3pm :
                df_temp.WindGustDir[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")] = df_temp.WindGustDir[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].fillna(df_temp.WindGustDir[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].mode([0]))
                df_temp.WindGustDir[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")] = df_temp.WindGustDir[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].fillna(df_temp.WindGustDir[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].mode([0]))
                
                #WindSpeed9am :
                df_temp.WindSpeed9am[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")] = df_temp.WindSpeed9am[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].fillna(df_temp.WindSpeed9am[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].mean())
                df_temp.WindSpeed9am[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")] = df_temp.WindSpeed9am[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].fillna(df_temp.WindSpeed9am[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].mean())
                
                #WindSpeed3pm :
                df_temp.WindSpeed3pm[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")] = df_temp.WindSpeed3pm[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].fillna(df_temp.WindSpeed3pm[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].mean())
                df_temp.WindSpeed3pm[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")] = df_temp.WindSpeed3pm[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].fillna(df_temp.WindSpeed3pm[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].mean())
                   
                #Humidity9am
                df_temp.Humidity9am[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")] = df_temp.Humidity9am[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].fillna(df_temp.Humidity9am[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].mean())
                df_temp.Humidity9am[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")] = df_temp.Humidity9am[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].fillna(df_temp.Humidity9am[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].mean())
                    
                #Humidity3pm
                df_temp.Humidity3pm[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")] = df_temp.Humidity3pm[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].fillna(df_temp.Humidity3pm[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].mean())
                df_temp.Humidity3pm[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")] = df_temp.Humidity3pm[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].fillna(df_temp.Humidity3pm[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].mean())
        
                #Pressure9am
                df_temp.Pressure9am[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")] = df_temp.Pressure9am[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].fillna(df_temp.Pressure9am[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].mean())
                df_temp.Pressure9am[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")] = df_temp.Pressure9am[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].fillna(df_temp.Pressure9am[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].mean())
        
                #Pressure9am
                df_temp.Pressure3pm[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")] = df_temp.Pressure3pm[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].fillna(df_temp.Pressure3pm[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].mean())
                df_temp.Pressure3pm[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")] = df_temp.Pressure3pm[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].fillna(df_temp.Pressure3pm[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].mean())
        
                #Cloud9am
                df_temp.Cloud9am[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")] = df_temp.Cloud9am[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].fillna(df_temp.Cloud9am[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].mean())
                df_temp.Cloud9am[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")] = df_temp.Cloud9am[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].fillna(df_temp.Cloud9am[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].mean())
        
                #Cloud3pm
                df_temp.Cloud3pm[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")] = df_temp.Cloud3pm[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].fillna(df_temp.Cloud3pm[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].mean())
                df_temp.Cloud3pm[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")] = df_temp.Cloud3pm[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].fillna(df_temp.Cloud3pm[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].mean())
        
                #Temp9am
                df_temp.Temp9am[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")] = df_temp.Temp9am[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].fillna(df_temp.Temp9am[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].mean())
                df_temp.Temp9am[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")] = df_temp.Temp9am[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].fillna(df_temp.Temp9am[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].mean())
                    
                #Temp3pm
                df_temp.Temp3pm[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")] = df_temp.Temp3pm[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].fillna(df_temp.Temp3pm[(df_temp["Month"] == i) & (df_temp["RainToday"] == "Yes")].mean())
                df_temp.Temp3pm[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")] = df_temp.Temp3pm[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].fillna(df_temp.Temp3pm[(df_temp["Month"] == i) & (df_temp["RainToday"] == "No")].mean())
                
            geolist_clean.append(df_temp)
            st.markdown("\tCleaning done: <i>{}</i>. <b>{}</b> nans remaining (<b>{} %</b>). <br/>-------------------------------------------".format(geolist_str[k], df_temp.isna().sum().sum(), round(100*(df_temp.isna().sum().sum())/(df_temp.shape[0]*df_temp.shape[1]),1)), unsafe_allow_html = True)
        
            k+=1
            
        st.write("Cleaning complete.")
        
        df_Perth2 = geolist_clean[0]
        df_Albany2 = geolist_clean[1]
        df_Alice2 = geolist_clean[2]
        df_Adelaide2 = geolist_clean[3]
        df_Nhil2 = geolist_clean[4]
        df_Portland2 = geolist_clean[5]
        df_Melbourne2 = geolist_clean[6]
        df_Albury2 = geolist_clean[7]
        df_Canberra2 = geolist_clean[8]
        df_Sydney2 = geolist_clean[9]
        df_Newcastle2 = geolist_clean[10]
        df_Cobar2 = geolist_clean[11]
        df_Brisbane2 = geolist_clean[12]
        df_Cairns2 = geolist_clean[13]
        df_Hobart2 = geolist_clean[14]
        df_SalmonGums = geolist_clean[15]
        df_Darwin = geolist_clean[16]
        df_Katherine = geolist_clean[17]
        df_Woomera = geolist_clean[18]
        df_MountGinini = geolist_clean[19]
        df_NorfolkIsland = geolist_clean[20]
        
        #Reconstitution du df global
        
        data_full = pd.concat(geolist_clean)
        
        #Suppression des variables avec trop de nans
        
        data = data_full.drop(["Sunshine", "WindGustDir", "WindDir9am", "WindDir3pm"], axis = 1)
        
        #Supression des nans restant
        data = data.dropna()
        
        st.markdown("""<div style="text-align: justify">Il y avait initialement <b>{} valeurs manquantes</b> dans la base de données (<b>{} %</b> des données totales), répartis sur {} entrées.
        Le preprocessing a permis de réduire le nombre de valeurs manquantes à <b>{}</b> : <b>{} %</b> des valeurs manquantes initiales ont été remplacés.
        Après suppression de 4 colonnes comportant trop de valeurs manquantes, et suppression des valeurs manquantes restantes, il reste <b>{} relevés</b> dans la base.
        <br/>Au total, <b>{} % des relevés météorologiques ont été conservés</b>.
        </div>""".format(
            df_saved.isna().sum().sum(),
            round(100*df_saved.isna().sum().sum()/(df_saved.shape[0]*df_saved.shape[1]),1),
            df_saved.shape[0],
            data_full.isna().sum().sum(),
            100-round(100*data_full.isna().sum().sum()/df_saved.isna().sum().sum(), 1),
            data.shape[0],
            round(100*data.shape[0]/df_saved.shape[0],1)
        ), unsafe_allow_html = True)
        
        #CREATION DES VARIABLES SUPPLEMENTAIRES
        #State, Year, Month, Day
        
        #WindSpeedDiff, HumidityDiff, TempDiff
        data["WindSpeedDiff"] = data["WindSpeed3pm"] - data["WindSpeed9am"]
        data["HumidityDiff"] = data["Humidity3pm"] - data["Humidity9am"]
        data["TempDiff"] = data["Temp3pm"] - data["Temp9am"]
        
        #MinMaxDiff
        data["MinMaxDiff"] = data["MaxTemp"] - data["MinTemp"]
        
        #PressureDiff
        data["PressureDiff"] = data["Pressure3pm"] - data["Pressure9am"]
        
        #CloudDiff
        data["CloudDiff"] = data["Cloud3pm"] - data["Cloud9am"]
        
        #Encodage de RainToday et RainTomorrow
        encoder = LabelEncoder()
        LE_cols = ["RainToday", "RainTomorrow"]
        for col in LE_cols:
            data[col] = encoder.fit_transform(data[col])
        
        feats = data.drop(["RainTomorrow", "Date", "Year", "Month", "Day", "State", "Location"], axis = 1)
        target = data["RainTomorrow"]
        
        # On sépare les données en un ensemble d'apprentissage et un ensemble de test, avec le ratio 80/20
        X_train, X_test, y_train, y_test = train_test_split(feats, target, test_size = 0.2, random_state = 55)
        
        # RANDOM FOREST
        
        # Instanciation d'un modèle
        rf1 = RandomForestClassifier()
        
        # Rééquilibrage des données: 3 possibilités testées
        
        over = RandomOverSampler(sampling_strategy = 0.6) # Fraction 60/40 
        under = RandomUnderSampler() 
        
        # a) Over puis under Sample
        X_ov, y_ov = over.fit_resample(X_train, y_train) 
        X_res, y_res = under.fit_resample(X_ov, y_ov) 
        
        # b) Seulement un under Sample:
        X_un, y_un = under.fit_resample(X_train, y_train)
        
        # c) Seulement avec Over (X_ov, y_ov)
        
        # ENTRAÎNEMENT DU MODÈLE avec solution a)Over puis Under Sample
        rf1.fit(X_res, y_res)
        
        # EVALUATION DE LA PERFORMANCE
        y_pred1 = rf1.predict(X_test)
        precis = metrics.classification_report(y_test, y_pred1, output_dict=True)
        
        st.markdown("""<h2><center><u>PREMIER MODÈLE DE MACHINE LEARNING</u></center></h2>
        <h4><u><font color = 'navy'>Récapitulatif du modèle :</h4></u></font>
        <ul><li>Modèle <b>random forest</b>.</li>
        <li> préprocessing = <b>oversampling</b> puis <b>undersampling</b>.</li></ul>
        <h4><u><font color = 'navy'>Résultats du modèle :</font></u></h4>
        <ul><li> Prédiction des <b>jours de pluie</b> avec une précision de <b>{} %</b> (<i>recall = <b>{} %</b>, f1-score = <b>{} %</b></i>)</li>
        <li> Prédiction des <b>jours sans pluie</b> avec une précision de <b>{} %</b> (<i>recall = <b>{} %</b>, f1-score = <b>{} %</b></i>).</li>
        <li>La précision globale du modèle est de <b>{} %</b>.</li></ul>
        Les paramètres de ce premier modèle ont été fixés de façon plus ou moins arbritraire. Les 
        performances de ce modèle sont globalement satisfaisantes, voire très satisfaisantes pour la détection des jours sans pluie.
        Il serait toutefois intéressant d'améliorer la prédiction de jours de pluie.
        """.format(
            round(100*precis["1"]["precision"],2),
            round(100*precis["1"]["recall"],2),
            round(100*precis["1"]["f1-score"],2),
            round(100*precis["0"]["precision"],2),
            round(100*precis["0"]["recall"],2),
            round(100*precis["0"]["f1-score"],2),
            round(100*precis["accuracy"],2)
        ), unsafe_allow_html = True)
        st.markdown("<p style='font-family:Cambria; color:#3adfb2; font-size: 20px;'><i><b>Rapport de classification</p></b></i>", unsafe_allow_html = True)
        st.write(metrics.classification_report(y_test, y_pred1))
        st.markdown("<p style='font-family:Cambria; color:#3adfb2; font-size: 20px;'><i><b>Matrice de confusion</p></b></i>", unsafe_allow_html = True)
        st.write(pd.crosstab(y_test, y_pred1, rownames = ['Classe réelle'], colnames = ['Classe prédite']))
        
        # ENTRAÎNEMENT DU MODÈLE avec solution b) UnderSample
        rf2 = RandomForestClassifier()
        rf2.fit(X_un, y_un)
        
        # EVALUATION DE LA PERFORMANCE
        y_pred2 = rf2.predict(X_test)
        precis = metrics.classification_report(y_test, y_pred2, output_dict=True)
        
        st.markdown("""<h2><center><u>SECOND MODÈLE DE MACHINE LEARNING</u></center></h2>
        <h4><u><font color = 'navy'>Récapitulatif du modèle :</font></u></h4>
        <ul><li>Modèle <b>random forest</b>.</li>
        <li> préprocessing = <b>undersampling</b>.</li></ul>
        <h4><u><font color = 'navy'>Résultats du modèle :</font></u></h4>
        <ul><li> Prédiction des <b>jours de pluie</b> avec une précision de <b>{} %</b> (<i>recall = <b>{} %</b>, f1-score = <b>{} %</b></i>)</li>
        <li> Prédiction des <b>jours sans pluie</b> avec une précision de <b>{} %</b> (<i>recall = <b>{} %</b>, f1-score = <b>{} %</b></i>).</li>
        <li>La précision globale du modèle est de <b>{} %</b>.</li></ul>
        Les paramètres de ce premier modèle ont été fixés de façon plus ou moins arbritraire. Les 
        performances de ce modèle sont globalement satisfaisantes, voire très satisfaisantes pour la détection des jours sans pluie.
        Il serait toutefois intéressant d'améliorer la prédiction de jours de pluie.
        """.format(
            round(100*precis["1"]["precision"],2),
            round(100*precis["1"]["recall"],2),
            round(100*precis["1"]["f1-score"],2),
            round(100*precis["0"]["precision"],2),
            round(100*precis["0"]["recall"],2),
            round(100*precis["0"]["f1-score"],2),
            round(100*precis["accuracy"],2)
        ), unsafe_allow_html = True)
        
        st.markdown("<p style='font-family:Cambria; color:#3adfb2; font-size: 20px;'><i><b>Rapport de classification</p></b></i>", unsafe_allow_html = True)
        st.write(metrics.classification_report(y_test, y_pred2))
        st.markdown("<p style='font-family:Cambria; color:#3adfb2; font-size: 20px;'><i><b>Matrice de confusion</p></b></i>", unsafe_allow_html = True)
        st.write(pd.crosstab(y_test, y_pred2, rownames = ['Classe réelle'], colnames = ['Classe prédite']))
        
        # ENTRAÎNEMENT DU MODÈLE avec solution c) OverSample
        rf3 = RandomForestClassifier()
        rf3.fit(X_ov, y_ov)
        
        # EVALUATION DE LA PERFORMANCE
        y_pred3 = rf3.predict(X_test)
        precis = metrics.classification_report(y_test, y_pred3, output_dict=True)
        
        st.markdown("""<h2><center><u>TROISIÈME MODÈLE DE MACHINE LEARNING</u></h2></center>
        <h4><u><font color = 'navy'>Récapitulatif du modèle :</h4></u></font>
        <ul><li>Modèle <b>random forest</b>.</li>
        <li> préprocessing = <b>oversampling</b>.</li></ul>
        <h4><u><font color = 'navy'>Résultats du modèle :</h4></u></font>
        <ul><li> Prédiction des <b>jours de pluie</b> avec une précision de <b>{} %</b> (<i>recall = <b>{} %</b>, f1-score = <b>{} %</b></i>)</li>
        <li> Prédiction des <b>jours sans pluie</b> avec une précision de <b>{} %</b> (<i>recall = <b>{} %</b>, f1-score = <b>{} %</b></i>).</li>
        <li>La précision globale du modèle est de <b>{} %</b>.</li></ul>
        Les paramètres de ce premier modèle ont été fixés de façon plus ou moins arbritraire. Les 
        performances de ce modèle sont globalement satisfaisantes, voire très satisfaisantes pour la détection des jours sans pluie.
        Il serait toutefois intéressant d'améliorer la prédiction de jours de pluie.
        """.format(
            round(100*precis["1"]["precision"],2),
            round(100*precis["1"]["recall"],2),
            round(100*precis["1"]["f1-score"],2),
            round(100*precis["0"]["precision"],2),
            round(100*precis["0"]["recall"],2),
            round(100*precis["0"]["f1-score"],2),
            round(100*precis["accuracy"],2)
        ), unsafe_allow_html = True)
        
        st.markdown("<p style='font-family:Cambria; color:#3adfb2; font-size: 20px;'><i><b>Rapport de classification</p></b></i>", unsafe_allow_html = True)
        st.write(metrics.classification_report(y_test, y_pred3))
        st.markdown("<p style='font-family:Cambria; color:#3adfb2; font-size: 20px;'><i><b>Matrice de confusion</p></b></i>", unsafe_allow_html = True)
        st.write(pd.crosstab(y_test, y_pred3, rownames = ['Classe réelle'], colnames = ['Classe prédite']))
    

elif nav == "Deep learning":
    st.title("MODÈLE DE DEEP LEARNING 🦘")

    data = pd.read_csv("weatherAUS_geoclean.csv")
    df_saved = pd.read_csv("weatherAUS_geoclean.csv")
            
    #Encodage de RainToday et RainTomorrow
    encoder = LabelEncoder()
    LE_cols = ["RainToday", "RainTomorrow"]
    for col in LE_cols:
        data[col] = encoder.fit_transform(data[col])

    feats = data.drop(["RainTomorrow", "Date", "Year", "Month", "Day", "State", "Location"], axis = 1)
    target = data["RainTomorrow"]
    encoder = LabelEncoder()
    
    Y = encoder.fit_transform(target)
    
    X_train, X_test, y_train, y_test = train_test_split(feats, Y, test_size = 0.2, random_state = 55) 
    
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    st.markdown("<h4><u><font color = 'navy'>Exploration des différents modèles.</font></h4></u>", unsafe_allow_html=True)
    
    param_DL = st.selectbox(label = "Choisissez le paramètre à moduler dans le menu ci-dessous 🦘",
                                  options = ["premier modèle", "neurones", "epochs", "batch", "activation", "couches"])
    
    if param_DL == "premier modèle":

        st.markdown("""<h2><center><u>PREMIER MODÈLE DE DEEP LEARNING</u></h2></center>
        <br/><i>modélisation en cours...</i>🐊
        """, unsafe_allow_html = True)
        EPOCHS = 6
        BATCHS = 32
        
        UNITS1 = 25
        UNITS2 = 50
        UNITS3 = None
        UNITS4 = None
        UNITS5 = None
        UNITSOUT = 2
        
        ACTIV1 = "relu"
        ACTIV2 = "relu"
        ACTIV3 = None
        ACTIV4 = None
        ACTIV5 = None
        
        inputs = Input(shape = X_train_scaled.shape[1], name = "Input")
        dense1 = Dense(units = UNITS1, activation = ACTIV1, kernel_initializer = "normal", name = "Dense_1")
        dense2 = Dense(units = UNITS2, activation = ACTIV2, kernel_initializer = "normal", name = "Dense_2")
        dense3 = Dense(units = UNITSOUT, activation = "softmax", name = "Dense_3")
        
        x = dense1(inputs)
        x = dense2(x)
        outputs = dense3(x)
        
        model = Model(inputs = inputs, outputs = outputs)
        model.compile(loss = "sparse_categorical_crossentropy", optimizer = "adam", metrics = ["accuracy"])
        training_history = model.fit(X_train_scaled, y_train, epochs = EPOCHS, batch_size = BATCHS, validation_data=(X_test_scaled,y_test))
        
        #calcul du score
        #score = model.evaluate(X_test_scaled, y_test)
        
        #prédiction
        test_pred = model.predict(X_test_scaled)
        
        y_test_class = y_test
        y_pred_class = np.argmax(test_pred, axis = 1)
        
        #Résultats
        precis = classification_report(y_test_class, y_pred_class,output_dict=True)
        
        #Output
        st.markdown("<i><center>...modélisation terminée !🦘</center></i> ", unsafe_allow_html = True)

        st.markdown("""<h4><u><font color = 'navy'>Récapitulatif du modèle :</font></u></h4>
        Ce premier modèle avait 2 couches denses :
        <ul><li>la première avec <b>{} neurones</b> et une fonction d'activation <b>{}</b>.</li>
        <li> la seconde avec <b>{} neurones</b> et une fonction d'activation <b>{}</b>.</li>
        <li> la couche de sortie comportait <b>2 neurones</b> et une fonction d'activation <b>softmax</b>.</li>
        <li> apprentissage sur <b>{} epochs</b> par batch de <b>{}</b>.</li></ul>
        """.format(UNITS1, ACTIV1, UNITS2, ACTIV2, EPOCHS, BATCHS), unsafe_allow_html = True)
                
        st.markdown("""<h4><u><font color = 'navy'>Résultats du modèle :</h4></u></font>
        <ul><li> Prédiction des <b>jours de pluie</b> avec une précision de <b>{} %</b> (<i>recall = <b>{} %</b></i>)</li>
        <li> Prédiction des <b>jours sans pluie</b> avec une précision de <b>{} %</b> (<i>recall = <b>{} %</b></i>).
        <li>La précision globale du modèle est de <b>{} %</b>.</li></ul>
        Les paramètres de ce premier modèle ont été fixés de façon plus ou moins arbritraire. Les 
        performances de ce modèle sont globalement satisfaisantes, voire très satisfaisantes pour la détection des jours sans pluie.
        Il serait toutefois intéressant d'améliorer la prédiction de jours de pluie.
        """.format(
            round(100*precis["1"]["precision"],2),
            round(100*precis["1"]["recall"],2),
            round(100*precis["0"]["precision"],2),
            round(100*precis["0"]["recall"],2),
            round(100*precis["accuracy"],2)
        ), unsafe_allow_html = True)
        
        st.markdown("<p style='font-family:Cambria; color:#3adfb2; font-size: 20px;'><i><b>Rapport de classification</p></b></i>", unsafe_allow_html = True)
        st.write(classification_report(y_test_class, y_pred_class))
        st.markdown("<p style='font-family:Cambria; color:#3adfb2; font-size: 20px;'><i><b>Matrice de confusion</p></b></i>", unsafe_allow_html = True)
        st.write(confusion_matrix(y_test_class, y_pred_class))
        
    
    elif param_DL == "neurones":
        st.markdown("""<h2><center><u>EFFET DU NOMBRE DE NEURONES SUR LE MODÈLE DE DEEP LEARNING</u></h2></center>
        <h4><u><font color = 'navy'>Récapitulatif du premièr modèle :</font></u></h4>
        <ul><li>Prédiction jour de pluie - précision : <b>76,4 %</b> ;  recall : <b>47,6 %</b></li>
        <li>Prédiction jour de pluie - précision : <b>86,9 %</b> ;  recall : <b>96,0 %</b></li></ul>
        <br/><i>modélisation en cours...</i>🐊""", unsafe_allow_html = True)
        
        EPOCHS = 6
        BATCHS = 32
        
        UNITS1 = 250
        UNITS2 = 500
        UNITS3 = None
        UNITS4 = None
        UNITS5 = None
        UNITSOUT = 2
        
        ACTIV1 = "relu"
        ACTIV2 = "relu"
        ACTIV3 = None
        ACTIV4 = None
        ACTIV5 = None
        
        inputs = Input(shape = X_train_scaled.shape[1], name = "Input")
        dense1 = Dense(units = UNITS1, activation = ACTIV1, kernel_initializer = "normal", name = "Dense_1")
        dense2 = Dense(units = UNITS2, activation = ACTIV2, kernel_initializer = "normal", name = "Dense_2")
        dense3 = Dense(units = UNITSOUT, activation = "softmax", name = "Dense_3")
        
        
        x = dense1(inputs)
        x = dense2(x)
        outputs = dense3(x)
        
        model = Model(inputs = inputs, outputs = outputs)
        model.compile(loss = "sparse_categorical_crossentropy", optimizer = "adam", metrics = ["accuracy"])
        training_history = model.fit(X_train_scaled, y_train, epochs = EPOCHS, batch_size = BATCHS, validation_data=(X_test_scaled,y_test))
        
        #calcul du score
        score = model.evaluate(X_test_scaled, y_test)
        
        #prédiction
        test_pred = model.predict(X_test_scaled)
        
        y_test_class = y_test
        y_pred_class = np.argmax(test_pred, axis = 1)
        
        #Résultats
        precis = classification_report(y_test_class, y_pred_class,output_dict=True)
        
        #Output
        st.markdown("<i><center>...modélisation terminée !🦘</center></i> ", unsafe_allow_html = True)

        st.markdown("""<h4><u><font color = 'navy'>Récapitulatif du modèle :</h4></u></font>
        Ce modèle avait 2 couches denses :
        <ul><li>la première avec <b>{} neurones</b> et une fonction d'activation <b>{}</b>.</li>
        <li> la seconde avec <b>{} neurones</b> et une fonction d'activation <b>{}</b>.</li>
        <li> la couche de sortie comportait <b>2 neurones</b> et une fonction d'activation <b>softmax</b>.</li>
        <li> apprentissage sur <b>{} epochs</b> par batch de <b>{}</b>.</li></ul>
        """.format(UNITS1, ACTIV1, UNITS2, ACTIV2, EPOCHS, BATCHS), unsafe_allow_html = True)
                
        st.markdown("""<h4><u><font color = 'navy'>Résultats du modèle :</h4></u></font>
        <ul><li> Prédiction des <b>jours de pluie</b> avec une précision de <b>{} %</b> (<i>recall = <b>{} %</b></i>).</li>
        <li> Prédiction des <b>jours sans pluie</b> avec une précision de <b>{} %</b> (<i>recall = <b>{} %</b></i>).</li>
        <li>La précision globale du modèle est de <b>{} %</b>.</li></ul>
        Le simple ajout de neurones (ici 10 fois plus nombreux dans chaque couche par rapport au modèle initial) 
        ne semble pas modifier les performances.
        """.format(
            round(100*precis["1"]["precision"],2),
            round(100*precis["1"]["recall"],2),
            round(100*precis["0"]["precision"],2),
            round(100*precis["0"]["recall"],2),
            round(100*precis["accuracy"],2)
        ), unsafe_allow_html = True)
        
        st.markdown("<p style='font-family:Cambria; color:#3adfb2; font-size: 20px;'><i><b>Rapport de classification</p</b></i>", unsafe_allow_html = True)
        st.write(classification_report(y_test_class, y_pred_class))
        st.markdown("<p style='font-family:Cambria; color:#3adfb2; font-size: 20px;'><i><b>Matrice de confusion</p></b></i>", unsafe_allow_html = True)
        st.write(confusion_matrix(y_test_class, y_pred_class))
        
    elif param_DL == "epochs":
        st.markdown("""<h2><center><u>EFFET DU NOMBRE D'EPOCHS SUR LE MODÈLE DE DEEP LEARNING</u></h2></center>
        <h4><u><font color = 'navy'>Récapitulatif du premièr modèle :</font></u></h4>
        <ul><li>Prédiction <b>jour de pluie</b> - précision : <b>76,4 %</b> ;  recall : <b>47,6 %</b></li>
        <li>Prédiction jour <b>sans pluie</b> - précision : <b>86,9 %</b> ;  recall : <b>96,0 %</b></li></ul>
        <br/><i>modélisation en cours...</i>🐊""", unsafe_allow_html = True)
        
        EPOCHS = 18
        BATCHS = 32
        
        UNITS1 = 25
        UNITS2 = 50
        UNITS3 = None
        UNITS4 = None
        UNITS5 = None
        UNITSOUT = 2
        
        ACTIV1 = "relu"
        ACTIV2 = "relu"
        ACTIV3 = None
        ACTIV4 = None
        ACTIV5 = None
        
        inputs = Input(shape = X_train_scaled.shape[1], name = "Input")
        dense1 = Dense(units = UNITS1, activation = ACTIV1, kernel_initializer = "normal", name = "Dense_1")
        dense2 = Dense(units = UNITS2, activation = ACTIV2, kernel_initializer = "normal", name = "Dense_2")
        dense3 = Dense(units = UNITSOUT, activation = "softmax", name = "Dense_3")
        
        x = dense1(inputs)
        x = dense2(x)
        outputs = dense3(x)
        
        model = Model(inputs = inputs, outputs = outputs)
        model.compile(loss = "sparse_categorical_crossentropy", optimizer = "adam", metrics = ["accuracy"])
        training_history = model.fit(X_train_scaled, y_train, epochs = EPOCHS, batch_size = BATCHS, validation_data=(X_test_scaled,y_test))
        
        #calcul du score
        score = model.evaluate(X_test_scaled, y_test)
        
        #prédiction
        test_pred = model.predict(X_test_scaled)
        
        y_test_class = y_test
        y_pred_class = np.argmax(test_pred, axis = 1)
        
        #Résultats
        precis = classification_report(y_test_class, y_pred_class,output_dict=True)
        
        #Output
        st.markdown("<i><center>...modélisation terminée !🦘</center></i> ", unsafe_allow_html = True)

        st.markdown("""<h4><u><font color = 'navy'>Récapitulatif du modèle :</h4></u></font>
        Ce modèle avait 2 couches denses :
        <ul><li>la première avec <b>{} neurones</b> et une fonction d'activation <b>{}</b>.</li>
        <li> la seconde avec <b>{} neurones</b> et une fonction d'activation <b>{}</b>.</li>
        <li> la couche de sortie comportait <b>2 neurones</b> et une fonction d'activation <b>softmax</b>.</li>
        <li> apprentissage sur <b>{} epochs</b> par batch de <b>{}</b>.</li></ul>
        """.format(UNITS1, ACTIV1, UNITS2, ACTIV2, EPOCHS, BATCHS), unsafe_allow_html = True)
        
        model.summary()
        
        st.markdown("""<h4><u><font color = 'navy'>Résultats du modèle :</h4></u></font>
        <ul><li> Prédiction des <b>jours de pluie</b> avec une précision de <b>{} %</b> (<i>recall = <b>{} %</b></i>)</li>
        <li> Prédiction des <b>jours sans pluie</b> avec une précision de <b>{} %</b> (<i>recall = <b>{} %</b></i>).
        <li>La précision globale du modèle est de <b>{} %</b>.</li></ul>
        L'entrainement sur un nombre plus important d'epochs (ici 18 soit 3 fois plus par rapport au modèle initial) 
        ne semble pas modifier les performances.
        """.format(
            round(100*precis["1"]["precision"],2),
            round(100*precis["1"]["recall"],2),
            round(100*precis["0"]["precision"],2),
            round(100*precis["0"]["recall"],2),
            round(100*precis["accuracy"],2)
        ), unsafe_allow_html = True)
        
        st.markdown("<p style='font-family:Cambria; color:#3adfb2; font-size: 20px;'><i><b>Rapport de classification</p</b></i>", unsafe_allow_html = True)
        st.write(classification_report(y_test_class, y_pred_class))
        st.markdown("<p style='font-family:Cambria; color:#3adfb2; font-size: 20px;'><i><b>Matrice de confusion</p></b></i>", unsafe_allow_html = True)
        st.write(confusion_matrix(y_test_class, y_pred_class))    
        
    elif param_DL == "batch":
        st.markdown("""<h2><center><u>EFFET DE LA TAILLE DES BATCHS SUR LE MODÈLE DE DEEP LEARNING</u></h2></center>
        <h4><u><font color = 'navy'>Récapitulatif du premièr modèle :</font></u></h4>
        <ul><li>Prédiction <b>jour de pluie</b> - précision : <b>76,4 %</b> ;  recall : <b>47,6 %</b></li>
        <li>Prédiction <b>jour sans pluie</b> - précision : <b>86,9 %</b> ;  recall : <b>96,0 %</b></li></ul>
        <br/><i>modélisation en cours...</i>🐊""", unsafe_allow_html = True)
        
        EPOCHS = 6
        BATCHS = 320
        
        UNITS1 = 25
        UNITS2 = 50
        UNITS3 = None
        UNITS4 = None
        UNITS5 = None
        UNITSOUT = 2
        
        ACTIV1 = "relu"
        ACTIV2 = "relu"
        ACTIV3 = None
        ACTIV4 = None
        ACTIV5 = None
        
        inputs = Input(shape = X_train_scaled.shape[1], name = "Input")
        dense1 = Dense(units = UNITS1, activation = ACTIV1, kernel_initializer = "normal", name = "Dense_1")
        dense2 = Dense(units = UNITS2, activation = ACTIV2, kernel_initializer = "normal", name = "Dense_2")
        dense3 = Dense(units = UNITSOUT, activation = "softmax", name = "Dense_3")
        
        x = dense1(inputs)
        x = dense2(x)
        outputs = dense3(x)
        
        model = Model(inputs = inputs, outputs = outputs)
        
        model.compile(loss = "sparse_categorical_crossentropy", optimizer = "adam", metrics = ["accuracy"])
        
        training_history = model.fit(X_train_scaled, y_train, epochs = EPOCHS, batch_size = BATCHS, validation_data=(X_test_scaled,y_test))
        
        #calcul du score
        score = model.evaluate(X_test_scaled, y_test)
        
        #prédiction
        test_pred = model.predict(X_test_scaled)
        
        y_test_class = y_test
        y_pred_class = np.argmax(test_pred, axis = 1)
        
        #Résultats
        precis = classification_report(y_test_class, y_pred_class,output_dict=True)
        
        #Output
        st.markdown("<i><center>...modélisation terminée !🦘</center></i> ", unsafe_allow_html = True)
        st.markdown("""<h4><u><font color = 'navy'>Récapitulatif du modèle :</h4></u></font>
        Ce modèle avait 2 couches denses :
        <ul><li>la première avec <b>{} neurones</b> et une fonction d'activation <b>{}</b>.</li>
        <li> la seconde avec <b>{} neurones</b> et une fonction d'activation <b>{}</b>.</li>
        <li> la couche de sortie comportait <b>2 neurones</b> et une fonction d'activation <b>softmax</b>.</li>
        <li> apprentissage sur <b>{} epochs</b> par batch de <b>{}</b>.</li></ul>
        """.format(UNITS1, ACTIV1, UNITS2, ACTIV2, EPOCHS, BATCHS), unsafe_allow_html = True)
        
        model.summary()
                         
        st.markdown("""<h4><u><font color = 'navy'>Résultats du modèle :</h4></u></font>
        <ul><li> Prédiction des <b>jours de pluie</b> avec une précision de <b>{} %</b> (<i>recall = <b>{} %</b></i>)</li>
        <li> Prédiction des <b>jours sans pluie</b> avec une précision de <b>{} %</b> (<i>recall = <b>{} %</b></i>).
        <li>La précision globale du modèle est de <b>{} %</b>.</li></ul>
        L'entrainement sur des batchs de plus grande taille (ici 320 soit 10 fois plus grands par rapport au modèle initial) 
        ne semble pas modifier les performances, en revanche la vitesse d'execution du modèle est considérablement réduite.
        """.format(
            round(100*precis["1"]["precision"],2),
            round(100*precis["1"]["recall"],2),
            round(100*precis["0"]["precision"],2),
            round(100*precis["0"]["recall"],2),
            round(100*precis["accuracy"],2)
        ), unsafe_allow_html = True)
        
        st.markdown("<p style='font-family:Cambria; color:#3adfb2; font-size: 20px;'><i><b>Rapport de classification</p</b></i>", unsafe_allow_html = True)
        st.write(classification_report(y_test_class, y_pred_class))
        st.markdown("<p style='font-family:Cambria; color:#3adfb2; font-size: 20px;'><i><b>Matrice de confusion</p></b></i>", unsafe_allow_html = True)
        st.write(confusion_matrix(y_test_class, y_pred_class))
        
    elif param_DL == "activation":
        st.markdown("""<h2><center><u>EFFET DES FONCTIONS D'ACTIVATION SUR LE MODÈLE DE DEEP LEARNING</u></h2></center>
        <h4><u><font color = 'navy'>Récapitulatif du premièr modèle :</font></u></h4>
        <ul><li>Prédiction <b>jour de pluie</b> - précision : <b>76,4 %</b> ;  recall : <b>47,6 %</b></li>
        <li>Prédiction <b>jour sans pluie</b> - précision : <b>86,9 %</b> ;  recall : <b>96,0 %</b></li></ul>
        <br/><i>modélisation en cours...</i>🐊""", unsafe_allow_html = True)
        
        EPOCHS = 6
        BATCHS = 32
        
        UNITS1 = 25
        UNITS2 = 50
        UNITS3 = None
        UNITS4 = None
        UNITS5 = None
        UNITSOUT = 2
        
        ACTIV1 = "tanh"
        ACTIV2 = "tanh"
        ACTIV3 = None
        ACTIV4 = None
        ACTIV5 = None
        
        
        inputs = Input(shape = X_train_scaled.shape[1], name = "Input")
        dense1 = Dense(units = UNITS1, activation = ACTIV1, kernel_initializer = "normal", name = "Dense_1")
        dense2 = Dense(units = UNITS2, activation = ACTIV2, kernel_initializer = "normal", name = "Dense_2")
        dense3 = Dense(units = UNITSOUT, activation = "softmax", name = "Dense_3")
        
        x = dense1(inputs)
        x = dense2(x)
        outputs = dense3(x)
        
        model = Model(inputs = inputs, outputs = outputs)
        model.compile(loss = "sparse_categorical_crossentropy", optimizer = "adam", metrics = ["accuracy"])
        training_history = model.fit(X_train_scaled, y_train, epochs = EPOCHS, batch_size = BATCHS, validation_data=(X_test_scaled,y_test))
        
        #calcul du score
        score = model.evaluate(X_test_scaled, y_test)
        
        #prédiction
        test_pred = model.predict(X_test_scaled)
        
        y_test_class = y_test
        y_pred_class = np.argmax(test_pred, axis = 1)
        
        #Résultats
        precis = classification_report(y_test_class, y_pred_class,output_dict=True)
        
        #Output
        st.markdown("<i><center>...modélisation terminée !🦘</center></i> ", unsafe_allow_html = True)
        st.markdown("""<h4><u><font color = 'navy'>Récapitulatif du modèle :</h4></u></font>
        Ce modèle avait 2 couches denses :
        <ul><li>la première avec <b>{} neurones</b> et une fonction d'activation <b>{}</b>.</li>
        <li> la seconde avec <b>{} neurones</b> et une fonction d'activation <b>{}</b>.</li>
        <li> la couche de sortie comportait <b>2 neurones</b> et une fonction d'activation <b>softmax</b>.</li>
        <li> apprentissage sur <b>{} epochs</b> par batch de <b>{}</b>.</li></ul>
        """.format(UNITS1, ACTIV1, UNITS2, ACTIV2, EPOCHS, BATCHS), unsafe_allow_html = True)
        
        
        st.markdown("""<h4><u><font color = 'navy'>Résultats du modèle :</h4></u></font>
        <ul><li> Prédiction des <b>jours de pluie</b> avec une précision de <b>{} %</b> (<i>recall = <b>{} %</b></i>)</li>
        <li> Prédiction des <b>jours sans pluie</b> avec une précision de <b>{} %</b> (<i>recall = <b>{} %</b></i>).
        <li>La précision globale du modèle est de <b>{} %</b>.</li></ul>
        L'activation des couches denses par la fonction tangente hyperbolique (au lieu de relu dans modèle initial) 
        ne semble pas modifier les performances.
        """.format(
            round(100*precis["1"]["precision"],2),
            round(100*precis["1"]["recall"],2),
            round(100*precis["0"]["precision"],2),
            round(100*precis["0"]["recall"],2),
            round(100*precis["accuracy"],2)
        ), unsafe_allow_markdown = True)
        
        st.markdown("<p style='font-family:Cambria; color:#3adfb2; font-size: 20px;'><i><b>Rapport de classification</p</b></i>", unsafe_allow_html = True)
        st.write(classification_report(y_test_class, y_pred_class))
        st.markdown("<p style='font-family:Cambria; color:#3adfb2; font-size: 20px;'><i><b>Matrice de confusion</p></b></i>", unsafe_allow_html = True)
        st.write(confusion_matrix(y_test_class, y_pred_class))
        
    elif param_DL == "couches":
        st.markdown("""<h2><center><u>EFFET DU NOMBRE DE COUCHES DE NEURONES SUR LE MODÈLE DE DEEP LEARNING</u></h2></center>
        <h4><u><font color = 'navy'>Récapitulatif du premièr modèle :</font></u></h4>
        <ul><li>Prédiction <b>jour de pluie</b> - précision : <b>76,4 %</b> ;  recall : <b>47,6 %</b></li>
        <li>Prédiction <b>jour sans pluie</b> - précision : <b>86,9 %</b> ;  recall : <b>96,0 %</b></li></ul>
        <br/><i>modélisation en cours...</i>🐊""", unsafe_allow_html = True)
        
        EPOCHS = 6
        BATCHS = 32
        
        UNITS1 = 25
        UNITS2 = 50
        UNITS3 = 50
        UNITS4 = None
        UNITS5 = None
        UNITSOUT = 2
        
        ACTIV1 = "relu"
        ACTIV2 = "relu"
        ACTIV3 = "relu"
        ACTIV4 = None
        ACTIV5 = None
        
        
        inputs = Input(shape = X_train_scaled.shape[1], name = "Input")
        dense1 = Dense(units = UNITS1, activation = ACTIV1, kernel_initializer = "normal", name = "Dense_1")
        dense2 = Dense(units = UNITS2, activation = ACTIV2, kernel_initializer = "normal", name = "Dense_2")
        dense3 = Dense(units = UNITS3, activation = ACTIV3, kernel_initializer = "normal", name = "Dense_3")
        dense4 = Dense(units = UNITSOUT, activation = "softmax", name = "Dense_4")
        
        x = dense1(inputs)
        x = dense2(x)
        x = dense3(x)
        outputs = dense4(x)
        
        model = Model(inputs = inputs, outputs = outputs)
        model.compile(loss = "sparse_categorical_crossentropy", optimizer = "adam", metrics = ["accuracy"])
        training_history = model.fit(X_train_scaled, y_train, epochs = EPOCHS, batch_size = BATCHS, validation_data=(X_test_scaled,y_test))
        
        #calcul du score
        score = model.evaluate(X_test_scaled, y_test)
        
        #prédiction
        test_pred = model.predict(X_test_scaled)
        
        y_test_class = y_test
        y_pred_class = np.argmax(test_pred, axis = 1)
        
        #Résultats
        precis = classification_report(y_test_class, y_pred_class,output_dict=True)
        
        #Output
        st.markdown("<i><center>...modélisation terminée !🦘</center></i> ", unsafe_allow_html = True)
        st.markdown("""<h4><u><font color = 'navy'>Récapitulatif du modèle :</h4></u></font>
        Ce modèle avait 3 couches denses :
        <ul><li>la première avec <b>{} neurones</b> et une fonction d'activation <b>{}</b>.</li>
        <li> la seconde avec <b>{} neurones</b> et une fonction d'activation <b>{}</b>.</li>
        <li> la troisième avec <b>{} neurones</b> et une fonction d'activation <b>{}</b>.</li>
        <li> la couche de sortie comportait <b>2 neurones</b> et une fonction d'activation <b>softmax</b>.</li>
        <li> apprentissage sur <b>{} epochs</b> par batch de <b>{}</b>.</li></ul>
        """.format(UNITS1, ACTIV1, UNITS2, ACTIV2, UNITS3, ACTIV3, EPOCHS, BATCHS), unsafe_allow_html = True)
        
        
        st.markdown("""<h4><u><font color = 'navy'>Résultats du modèle :</h4></u></font color = 'navy>
        <ul><li> Prédiction des <b>jours de pluie</b> avec une précision de <b>{} %</b> (<i>recall = <b>{} %</b></i>)</li>
        <li> Prédiction des <b>jours sans pluie</b> avec une précision de <b>{} %</b> (<i>recall = <b>{} %</b></i>).
        <li>La précision globale du modèle est de <b>{} %</b>.</li></ul>
        L'activation des couches denses par la fonction tangente hyperbolique (au lieu de relu dans modèle initial) 
        ne semble pas modifier les performances.
        """.format(
            round(100*precis["1"]["precision"],2),
            round(100*precis["1"]["recall"],2),
            round(100*precis["0"]["precision"],2),
            round(100*precis["0"]["recall"],2),
            round(100*precis["accuracy"],2)
        ), unsafe_allow_html = True)
        
        st.markdown("<p style='font-family:Cambria; color:#3adfb2; font-size: 20px;'><i><b>Rapport de classification</p</b></i>", unsafe_allow_html = True)
        st.write(classification_report(y_test_class, y_pred_class))
        st.markdown("<p style='font-family:Cambria; color:#3adfb2; font-size: 20px;'><i><b>Matrice de confusion</p></b></i>", unsafe_allow_html = True)
        st.write(confusion_matrix(y_test_class, y_pred_class))
    
elif nav == "Les filouteries de Lise aka Kangooroo-Girl":
     st.image(
            "https://st.depositphotos.com/1033604/2008/i/600/depositphotos_20086857-stock-photo-kangaroo-posing-very-much-like.jpg",
            width=800,
        )
    

elif nav == "🐰":
    st.image(
            "https://m1.quebecormedia.com/emp/emp/matrixcbbb9deff-9126-47fc-b1fe-85c645ff9b6c_ORIGINAL.jpg?impolicy=crop-resize&x=0&y=0&w=0&h=0&width=925&height=925",
            width=800,
        )