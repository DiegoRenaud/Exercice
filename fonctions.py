import requests
import pandas as pd
import statsmodels.api as sm
from sklearn.model_selection import train_test_split

#importation des donnees
def importer(url):
    contenu = requests.get(url)
    wb = contenu.json()
    df = pd.DataFrame(wb)
    return(df)

def regression(x, y):
    x_reg = sm.add_constant(x)
    y_reg = y.values.ravel()
    xTrain, xTest, yTrain, yTest = train_test_split(x_reg, y_reg, test_size=0.2)
    return([sm.OLS(yTrain, xTrain).fit(), xTrain, xTest, yTrain, yTest])

def niveau(df, nb_retards, causes):
    for cause in causes[:-1] :
        df[cause] = df['prct_'+cause]/100*nb_retards
    return(df)