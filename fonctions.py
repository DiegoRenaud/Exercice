import requests
import folium
import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import seaborn as sns
import sklearn.metrics

#importation des donnees
def importer(url):
    contenu = requests.get(url)
    wb = contenu.json()
    df = pd.DataFrame(wb)
    return(df)

#régression linéaire
def regression(x, y):
    x_reg = sm.add_constant(x)
    y_reg = y.values.ravel()
    return(sm.OLS(y_reg, x_reg).fit())

#aggrégation d'une colonne par mois sur une année 
def aggreg_mensuel(df, data, annee):
    df_annulation_annuel = df.loc[(df['annee'] == annee),[data,'mois']]
    A = []
    for i in range(12):
        df = df_annulation_annuel.loc[(df_annulation_annuel['mois'] == i+1),[data]]
        x = np.mean(df[data])
        A.append(x)
    return(A)

#aggrégation d'une colonne par mois sur l'entièreté de la période
def aggreg_totale(df, data):
    A = aggreg_mensuel(df, data, 2018) + aggreg_mensuel(df, data, 2019) + aggreg_mensuel(df, data, 2020) + aggreg_mensuel(df, data, 2021) + aggreg_mensuel(df, data, 2022)
    return(A)

#passage des pourcentages aux niveaux
def niveau(df, nb_retards, causes):
    for cause in causes :
        df[cause] = df['prct_'+cause]/100*nb_retards
    return(df)

#visualisation de l'erreur dans le cadre de la régression
def visu_erreur(yPred, yTest):
    tempdf = pd.DataFrame({"prediction": yPred, "observed": yTest,
                       "epsilon": yTest - yPred})
    fig = plt.figure()
    g = sns.scatterplot(data = tempdf, x = "observed", y = "epsilon")
    g.axhline(0, color = "red")

def prediction(x, y, afficher = True):
    #séparation des données en 2 échantillon 
    X_train, X_test, y_train, y_test = train_test_split(x,y, test_size=0.2)
    
    #régression et prédiction
    ols = LinearRegression().fit(X_train, y_train)
    y_pred = ols.predict(X_test)
    
    #calcul des métriques
    rmse = sklearn.metrics.mean_squared_error(y_test, y_pred, squared = False)
    rsq = sklearn.metrics.r2_score(y_test, y_pred) 
    
    #nuage de points des valeurs observées
    tempdf = pd.DataFrame({"prediction": y_pred, "observed": y_test,
                           "error": y_test - y_pred})
    if afficher == True : 
        print("intercept : ",ols.intercept_)
        print("coeffs : ", ols.coef_)
        print("rsq : ", rsq)
        print("rmse : ", rmse)

        fig = plt.figure()
        g = sns.scatterplot(data = tempdf, x = "observed", y = "error")
        g.axhline(0, color = "red")
    
    return([X_train, y_train])