import pandas as pd
from config import risk_free_rate, risk_aversion
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import table


def reSample(data, period='annualy'):
    if (period == 'annualy'):
        resample_data = data['Close'].resample('Y',level=0).mean()
    elif (period == 'monthly'):
        resample_data = data['Close'].resample('M',level=0).mean()
    return pd.DataFrame(resample_data)

def calGeoAvgReturn(listHPR):
    wealthIndex = 1
    for hpr in listHPR:
        wealthIndex *= (1 + hpr)
    return wealthIndex**(1/len(listHPR)) - 1

def calRisk(data, period):
    data = reSample(data, period)

    data['HPR'] = data.loc[:, 'Close'].pct_change()
    data = data.iloc[1:]       #drop the first record seen there is no HPR
    listHPR = data['HPR'].to_numpy()

    data['GrossReturn'] = listHPR + 1
    data['ExcessReturns'] = listHPR - risk_free_rate["jp"]
    riskPremium = data['ExcessReturns'].mean()
    SDofExcessReturn = data['ExcessReturns'].std()
    exceptROR = listHPR.mean()
    geoAvgReturn = calGeoAvgReturn(listHPR)
    sharpeRatio = riskPremium/SDofExcessReturn
    return (geoAvgReturn, sharpeRatio)


def riskyAssetAllocation(riskAssetExptReturn, SDofExcessReturn):
    # y = np.arange(0, 1, 0.1)
    # rf = risk_free_rate["us"]
    # u = rf + y*(riskAssetExptReturn-rf) - 0.5*risk_aversion*(y*y*SDofExcessReturn**2)
    # plt.plot(y, u)
    # plt.show()
    best_position = (riskAssetExptReturn - risk_free_rate["us"])/(risk_aversion*(SDofExcessReturn**2))
    print("best position:", best_position)





def display_analysis():
    # grouping data and calculating average
    grouped_dataframe = iris_df.groupby('target').mean().round(1)
    grouped_dataframe['species_name'] = ['setosa', 'versicolor', 'virginica']

    # plotting data
    ax = plt.subplot(211)
    plt.title("Iris Dataset Average by Plant Type")
    plt.ylabel('Centimeters (cm)')

    ticks = [4, 8, 12, 16]
    a = [x - 1 for x in ticks]
    b = [x + 1 for x in ticks]

    plt.xticks([])

    plt.bar(a, grouped_dataframe.loc[0].values.tolist()[
            :-1], width=1, label='setosa')
    plt.bar(ticks, grouped_dataframe.loc[1].values.tolist()[
            :-1], width=1, label='versicolor')
    plt.bar(b, grouped_dataframe.loc[2].values.tolist()[
            :-1], width=1, label='virginica')

    plt.legend()
    plt.figure(figsize=(12, 8))
    table(ax, grouped_dataframe.drop(['species_name'], axis=1), loc='bottom')
