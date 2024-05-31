import yfinance as yf
from datetime import datetime

def get_current_day_data(symbol):
    # Download today's data
    data = yf.download(symbol, period='1d', interval='1d')
    
    # Get today's date
    today_str = datetime.now().strftime('%Y-%m-%d')
    
    if today_str in data.index:
        current_day_data = data.loc[today_str]
        return {
            'symbol': symbol,
            'open': current_day_data['Open'],
            'close': current_day_data['Close'],
            'low': current_day_data['Low']
        }
    else:
        return {
            'symbol': symbol,
            'message': "Data for today is not available yet."
        }

tickers = [
    'ES=F', 'NQ=F', 'RTY=F', 'NKD=F',
    '6A=F', '6B=F', '6C=F', '6E=F', '6J=F', '6S=F', 'E7=F', '6M=F', '6N=F',
    'HE=F', 'LE=F',
    'CL=F', 'QM=F', 'NG=F', 'QG=F', 'RB=F', 'HO=F', 'PL=F',
    'ZC=F', 'ZW=F', 'ZS=F', 'ZM=F', 'ZL=F',
    'YM=F',
    'ZT=F', 'ZF=F', 'ZN=F', 'TN=F', 'ZB=F', 'UB=F',
    'GC=F', 'SI=F', 'HG=F'
]

results = []

for ticker in tickers:
    result = get_current_day_data(ticker)
    results.append(result)

for res in results:
    print(res)
