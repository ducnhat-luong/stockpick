from config import *
import pandas as pd
import vnstock
import numpy as np

implicit_probability = 1/duration

hpr = []

def format_date(date):
    return date.strftime('%Y-%m-%d')


data =  vnstock.stock_historical_data(symbol=stock_name, 
        start_date=format_date(start_date), 
        end_date=format_date(today))

def get_exam_dates(data):
    index_list = []
    last_record_id = len(data.index)-1
    for step in range(duration):
        index = last_record_id - step*250
        index_list.insert(0,index)
    return index_list

history_idx = get_exam_dates(data)
df = pd.DataFrame(data, index=history_idx)
df['HPR'] = df.Close.pct_change()
df = df.iloc[1:]       #drop the first record seen there is no HPR
df['GrossReturn'] = df['HPR'] + 1

TBillRate = 0.08
df['ExcessReturns'] = df['HPR'] - TBillRate

riskPremium = df['ExcessReturns'].mean()
SDofExcessReturn = df['ExcessReturns'].std()

wealthIndex = 1
for index, row in df.iterrows():
    wealthIndex *= (1 + row["HPR"])
geo_avg_return = wealthIndex**(1/(duration-1)) - 1

expected_HPR = df["HPR"].mean()
std_deviation_HPR = df["HPR"].std()

sharpeRatio = riskPremium/SDofExcessReturn

print(sharpeRatio)

    
    

# for date in time_list:
#     query_phase = 'TradingDate==' +  date
#     capital_gain = data.query("TradingDate=='{}'".format(date))['Close']
#     hpr.insert(0,capital_gain)
#     print(date)
#     print(capital_gain)

