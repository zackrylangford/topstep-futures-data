import yfinance as yf
from datetime import datetime
import boto3
import json

# DynamoDB setup
dynamodb = boto3.resource('dynamodb')
table_name = 'futures-data'
table = dynamodb.Table(table_name)

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
            'high': current_day_data['High'],
            'low': current_day_data['Low'],
            'close': current_day_data['Close']
        }
    else:
        return {
            'symbol': symbol,
            'message': "Data for today is not available yet."
        }

def camarilla_pivot_points(high, low, close):
    pivot_point = (high + low + close) / 3

    r4 = (high - low) * 1.1 / 2 + close
    r3 = (high - low) * 1.1 / 4 + close
    r2 = (high - low) * 1.1 / 6 + close
    r1 = (high - low) * 1.1 / 12 + close

    s1 = close - (high - low) * 1.1 / 12
    s2 = close - (high - low) * 1.1 / 6
    s3 = close - (high - low) * 1.1 / 4
    s4 = close - (high - low) * 1.1 / 2

    breakout_target = close + (high - low) * 1.1
    breakdown_target = close - (high - low) * 1.1

    return {
        "breakout_target": breakout_target,
        "resistance_4": r4,
        "resistance_3": r3,
        "resistance_2": r2,
        "resistance_1": r1,
        "pivot_point": pivot_point,
        "support_1": s1,
        "support_2": s2,
        "support_3": s3,
        "support_4": s4,
        "breakdown_target": breakdown_target
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

def lambda_handler(event, context):
    results = []

    for ticker in tickers:
        result = get_current_day_data(ticker)
        if 'message' not in result:
            pivot_points = camarilla_pivot_points(result['high'], result['low'], result['close'])
            result.update(pivot_points)
        results.append(result)

    # Write to DynamoDB
    for res in results:
        if 'message' not in res:
            table.put_item(Item=res)

    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }
