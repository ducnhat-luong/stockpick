import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import datetime as dt
import pandas_datareader.data as web

MOS = 0.8
MARR = 0.14
NYEARS = 10

nikkei225 = pd.read_csv("nikkei225.csv")
symbol_list = nikkei225["Code"].to_numpy()
symbol_list = symbol_list[np.where(symbol_list>=9435)]

def seperate_tables_from_csv():
    finance_url = 'https://f.irbank.net/files/{}/fy-data-all.csv'.format(symbol)
    df = pd.read_csv(finance_url, header=None, names=range(10), on_bad_lines='skip')
    table_names = ["業績", "財務", "CF", "配当"]
    index_positions = []
    for table in table_names:
        index_positions.append(df[df[0]==table].index.tolist()[0]) #col_with_table_names

    ## Include end of table for last slice, omit for iteration below
    index_positions.append(df.index.tolist()[-1])

    tables = {}
    for position in index_positions[:-1]:
        table_no = index_positions.index(position)
        tables[table_names[table_no]]= df.loc[position+1:index_positions[table_no+1]-1]
    return tables


def check_akaji(data):
    data.columns = data.iloc[0]
    data = data[1:-1] 
    eps_hist = data[-1*NYEARS:]['EPS'].astype(float).to_numpy()
    return ((np.min(eps_hist))<0)

def get_eps_rate(data):
    data.columns = data.iloc[0]
    data = data[1:-1]       # -1 to eliminate the last row which is predicted EPS
    eps_hist = data[-1*(NYEARS+2):]['EPS'].astype(float).to_numpy()

    ma_eps = []
    window_size = 3
    i = 0
    while i < len(eps_hist) - window_size + 1:
        window = eps_hist[i : i + window_size]
        window_average = round(sum(window) / window_size, 2)
        ma_eps.append(window_average)
        i += 1
    
    eps_growth = (ma_eps[-1]/ma_eps[0])**(1/NYEARS) - 1
    avg_eps = np.mean(ma_eps)
    return eps_growth, avg_eps

def get_sale_rate(data):
    data.columns = data.iloc[0]
    data = data[1:-1]       # -1 to eliminate the last row which is predicted EPS
    sale_hist = data[-1*NYEARS:]['売上高'].astype(float).to_numpy()
    sale_growth = (sale_hist[-1]/sale_hist[0])**(1/NYEARS) - 1
    return sale_growth

# def get_roe_rate(data):
#     data.columns = data.iloc[0]
#     data = data[1:-1]       # -1 to eliminate the last row which is predicted EPS
#     avgROE = np.mean(data[-1*NYEARS:]['ROE'].astype(float).to_numpy())
#     return avgROE

def get_cash_rate(data):
    data.columns = data.iloc[0]
    data = data[1:]
    cash_hist = data[-1*NYEARS:]['現金同等物'].astype(float).to_numpy()
    cash_growth = (cash_hist[-1]/cash_hist[0])**(1/NYEARS) - 1
    return cash_growth

def get_bvps_rate(data):
    data.columns = data.iloc[0]
    data = data[1:]
    bvps_hist = data[-1*NYEARS:]['BPS'].astype(float).to_numpy()
    bvps_growth = (bvps_hist[-1]/bvps_hist[0])**(1/NYEARS) - 1
    return bvps_growth

def get_average_per():
    per_url = 'https://irbank.net/{}/per'.format(symbol)
    per_page = requests.get(per_url)
    # parser-lxml = Change html to Python friendly format
    soup = BeautifulSoup(per_page.text, 'lxml')
    table = soup.find('div', id='g_1')
    per_hist = []
    for i in table.find_all('span'):
        per = i.text
        if per != "":
            per_hist.append(per.replace('倍', ''))
    per_hist = per_hist[-1*NYEARS:]        
    per_hist = np.array(per_hist).astype(float)
    return np.mean(per_hist)

def get_sticker_price(avg_eps, est_growth_rate, avg_per):
    future_eps = avg_eps*((1+est_growth_rate)**NYEARS)
    future_price = avg_per*future_eps
    sticker_price = MOS*future_price/((1+MARR)**10)
    return sticker_price

def get_current_price(ticker):
    ticker_symbol_dr = str(ticker) + ".JP"
    start='2022-12-20'
    end = dt.date.today()
    df = web.DataReader(ticker_symbol_dr, data_source='stooq', start=start,end=end)
    return df["Close"].iloc[-1].astype(float)

for symbol in symbol_list:
    print(symbol)
    tables = seperate_tables_from_csv()

    if check_akaji(tables["業績"]):
        print("赤字")
        continue

    eps_rate, avg_eps = get_eps_rate(tables["業績"])
    # average_ROE = get_roe_rate(tables["業績"])
    sale_rate = get_sale_rate(tables["業績"])
    bvps_rate = get_bvps_rate(tables["財務"])
    cash_rate = get_cash_rate(tables["CF"])

    est_growth_rate = np.mean(np.array([eps_rate, bvps_rate]))
    try:
        avg_per = get_average_per()
    except ValueError as e:
        print(str(e))
        continue
    current_price = get_current_price(symbol)
    sticker_price = get_sticker_price(avg_eps, est_growth_rate, avg_per)

    if current_price < sticker_price:
        print("I FOUND A PROMISSING STOCK: " + str(symbol))
        print(current_price/sticker_price)
        print(sticker_price, eps_rate, avg_eps)