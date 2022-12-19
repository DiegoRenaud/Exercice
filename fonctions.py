import requests
import folium
import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

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
    xTrain, xTest, yTrain, yTest = train_test_split(x_reg, y_reg, test_size=0.2)
    return([sm.OLS(yTrain, xTrain).fit(), xTrain, xTest, yTrain, yTest])

#passage des pourcentages aux niveaux
def niveau(df, nb_retards, causes):
    for cause in causes[:-1] :
        df[cause] = df['prct_'+cause]/100*nb_retards
    return(df)

#visualisation de l'erreur dans le cadre de la régression
def visu_erreur(yPred, yTest):
    tempdf = pd.DataFrame({"prediction": yPred, "observed": yTest,
                       "epsilon": yTest - yPred})
    fig = plt.figure()
    g = sns.scatterplot(data = tempdf, x = "observed", y = "epsilon")
    g.axhline(0, color = "red")