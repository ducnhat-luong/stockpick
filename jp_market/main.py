import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import datetime as dt
import pandas_datareader.data as web

MOS = 0.95
MARR = 0.15

def get_profit_n_loss(year):
    df = pd.read_csv('fy-profit-and-loss-20{}.csv'.format(year), skiprows=1)
    return df


def check_akaji(data):
    data.columns = data.iloc[1]
    data = data[1:-1] 
    eps_hist = data[-1*N_YEARS:]['EPS'].astype(float).to_numpy()
    return ((np.min(eps_hist))<0)

def get_eps_rate(code):
    eps_list = []
    for data in profit_data:
        val = data.loc[data['コード']==code, 'EPS'].values[0]
        eps_list.append(val)
    eps_list = np.array(eps_list).astype(float)

    i = -10
    ma_eps = []
    while i <= -1:
        window = eps_list[i - WINDOW : i+1]
        window_average = sum(window) / (WINDOW+1)
        ma_eps.append(window_average)
        i += 1
    eps_growth = (ma_eps[-1]/ma_eps[-1*N_YEARS])**(1/N_YEARS) - 1
    avg_eps = np.mean(eps_list)
    return eps_growth, avg_eps

def get_sale_rate(code):
    sale_hist = []
    for data in profit_data:
        val = data.loc[data['コード']==code, '売上高'].values[0]
        sale_hist.append(float(val))
    sale_growth = (sale_hist[-1]/sale_hist[0])**(1/N_YEARS) - 1
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

def get_average_per(code):
    per_url = 'https://irbank.net/{}/per'.format(code)
    per_page = requests.get(per_url)
    # parser-lxml = Change html to Python friendly format
    soup = BeautifulSoup(per_page.text, 'lxml')
    table = soup.find('div', id='g_1')
    per_hist = []
    for i in table.find_all('span'):
        per = i.text
        if per != "":
            per_hist.append(per.replace('倍', ''))
    per_hist = per_hist[-1*N_YEARS:]        
    per_hist = np.array(per_hist).astype(float)
    return np.mean(per_hist)

def get_sticker_price(avg_eps, est_growth_rate, avg_per):
    future_eps = avg_eps*((1+est_growth_rate)**N_YEARS)
    print(est_growth_rate)
    future_price = avg_per*future_eps
    sticker_price = MOS*future_price/((1+MARR)**10)
    return sticker_price

def get_current_price(ticker):
    price = np.inf
    try:
        ticker_symbol_dr = str(ticker) + ".JP"
        start='2022-12-20'
        end = dt.date.today()
        df = web.DataReader(ticker_symbol_dr, data_source='stooq', start=start,end=end)
        price = df["Close"].iloc[-1].astype(float)
    except Exception as e:
        print(str(e))
    return price


def roe_filter(data):
    df = data.copy()
    df['ROE'] = df['ROE'].replace(['-'], '0')
    df['ROE'] = pd.to_numeric(df['ROE'], downcast='float')
    df = df[df['ROE'] > 10]
    return df['コード'].tolist()

def roa_filter(data):
    df = data.copy()
    df['ROA'] = df['ROA'].replace(['-'], '0')
    df['ROA'] = pd.to_numeric(df['ROA'], downcast='float')
    df = df[df['ROA'] > 4]
    return df['コード'].tolist()

def eps_filter(code_list):
    bad_codes = []
    for code in code_list:
        for data in profit_data:
            try:
                val = data.loc[data['コード']==code, 'EPS'].values[0]
                if val == '-' or float(val) < 0:
                    bad_codes.append(code)
                    break
            except Exception as e:
                bad_codes.append(code)
                break 
    return bad_codes

# profit_data = []
# YEAR = 21
# WINDOW = 2
# N_YEARS = 10
# years = np.arange(YEAR-N_YEARS-WINDOW, YEAR) + 1

# for year in years:
#     data = get_profit_n_loss(year)
#     profit_data.append(data)

# good_roe_codes = roe_filter(profit_data[-1])
# good_roa_codes = roa_filter(profit_data[-1])

# good_codes = np.intersect1d(np.array(good_roa_codes), np.array(good_roe_codes))
# best_codes = np.setdiff1d(good_codes, eps_filter(good_codes))

# for code in best_codes:
#     print(code)
#     eps_rate, avg_eps = get_eps_rate(code)
# # #     # average_ROE = get_roe_rate(tables["業績"])
# #     # sale_rate = get_sale_rate(code)
# # #     bvps_rate = get_bvps_rate(tables["財務"])
# # #     cash_rate = get_cash_rate(tables["CF"])
#     est_growth_rate = eps_rate
# # #     est_growth_rate = np.mean(np.array([eps_rate, sale_rate, bvps_rate, cash_rate]))
#     try:
#         avg_per = get_average_per(code)
#     except ValueError as e:
#         continue
#     current_price = get_current_price(code)
#     sticker_price = get_sticker_price(avg_eps, est_growth_rate, avg_per)

#     print(round(current_price,2), round(sticker_price,2) )
#     if current_price < sticker_price:
#         print("I FOUND A PROMISSING STOCK: " + str(code))
#         print(current_price/sticker_price)
#         print(sticker_price, eps_rate, avg_eps)


eps_hist = [1,2,3,4,5,6,7,8,9,10,11,12]
moving_averages = []
window_size = 3
i = 0
# Loop through the array to consider
# every window of size 3
while i < len(eps_hist) - window_size + 1:
    window = eps_hist[i : i + window_size]
    window_average = round(sum(window) / window_size, 2)
    moving_averages.append(window_average)
    i += 1
print(moving_averages)