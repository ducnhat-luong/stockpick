import datetime
import pandas as pd
import yfinance as yf
import pandas_datareader.data as web

start = datetime.datetime(2013, 6, 1)
# end = datetime.datetime(2018, 6, 1)
end = datetime.datetime.today()


risk_aversion = 3   # I have done the test on https://www.fidelity.co.uk/funds/risk-calculator-tool/

# inflation = {
#     "jp" : 0.038,
#     "us" : 0.0775,
#     "vn" : 0.043
# }

risk_free_rate = {
    "jp" : 0.00,
    "us" : 0.0475,
    "vn" : 0.08
}


# # ===========================================================
# # ======================== VN30 INDEX =======================
# csv_file = "VN30.csv"
# vn30 = pd.read_csv(csv_file)
# vn30['Date'] = pd.to_datetime(vn30['Date'])
# vn30 = vn30.set_index('Date') 
# vn30 = vn30.loc[str(start):str(end)]

# # ======================= SP500 INDEX =======================
# sp500 = yf.download("^GSPC", start, end)

# # ===================== NIKKEI225 INDEX =====================
# nikkei225 = yf.download("^N225", start, end)

# # ==================== eMAXISS SLIM SP500 ===================
csv_file = "https://toushin-lib.fwg.ne.jp/FdsWeb/FDST030000/csv-file-download?isinCd=JP90C000GKC6&associFundCd=03311187"
csv_file = "https://toushin-lib.fwg.ne.jp/FdsWeb/FDST030000/csv-file-download?isinCd=JP90C000ENC5&associFundCd=03319172"
csv_file = "https://toushin-lib.fwg.ne.jp/FdsWeb/FDST030000/csv-file-download?isinCd=JP90C000FLK9&associFundCd=6431217B"
csv_file = "https://toushin-lib.fwg.ne.jp/FdsWeb/FDST030000/csv-file-download?isinCd=JP90C000H1T1&associFundCd=0331418A"
emaxiss = pd.read_csv(csv_file, index_col=0, encoding='SHIFT-JIS')
emaxiss.index = pd.to_datetime(emaxiss.index, format='%Y年%m月%d日')
emaxiss.rename(columns = {"基準価額(円)": "Close"}, inplace = True)
emaxiss = emaxiss.loc[str(start):str(end)]

# # ========================= YEN/USD =========================
# yen = web.get_data_yahoo("JPY=X", start, end)


# # ========================== AMAZON =========================
# amazon = yf.download("AMZN", start, end)






# # import matplotlib.pyplot as plt
# import vnstock
# import cufflinks as cf
# from config import *
# import plotly.express as px

# cf.set_config_file(theme='pearl', world_readable=False)
# cf.set_config_file(offline=True)


# today = today.strftime('%Y-%m-%d')
# start_date = start_date.strftime('%Y-%m-%d')

# data =  vnstock.stock_historical_data(symbol=stock_name, start_date=start_date, end_date=today)



# fig = px.line(data, x='TradingDate', y="Close")
# fig.show()