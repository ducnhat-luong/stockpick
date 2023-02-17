import pandas as pd
from ultilities import *
from config import emaxiss
import matplotlib.pyplot as plt


geoAvgReturn, sharpeRatio = calRisk(emaxiss, period='annualy')
print(geoAvgReturn, sharpeRatio)
# riskyAssetAllocation(geoAvgReturn, SDofExcessReturn)

# data1 = sp500[sp500.index.is_month_end]
# data1['HPR'] = (data1.loc[:, 'Close'].pct_change())*100
# data2 = amazon[amazon.index.is_month_end]
# data2['HPR'] = (data2.loc[:, 'Close'].pct_change())*100
# data1 = data1.iloc[1:] 
# data2 = data2.iloc[1:] 
# x = data1['HPR']
# y = data2['HPR']

# #use green as color for individual points
# plt.plot(x, y, 'o', color='green')

# #obtain m (slope) and b(intercept) of linear regression line
# m, b = np.polyfit(x, y, 1)
# print(m)





from IPython.display import display
# display(df)