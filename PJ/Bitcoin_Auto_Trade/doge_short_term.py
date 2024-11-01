import os
from dotenv import load_dotenv
import pyupbit
import pandas as pd
import json
from openai import OpenAI
import ta
from ta.utils import dropna
import time
import requests

load_dotenv()

def add_indicators(df):
    # 볼린저 밴드: 윈도우 14, 표준편차 1.5로 설정
    indicator_bb = ta.volatility.BollingerBands(close=df['close'], window=14, window_dev=1.5)
    df['bb_bbm'] = indicator_bb.bollinger_mavg()
    df['bb_bbh'] = indicator_bb.bollinger_hband()
    df['bb_bbl'] = indicator_bb.bollinger_lband()
    
    # RSI: 기간 7로 설정하여 빠른 민감도 조정
    df['rsi'] = ta.momentum.RSIIndicator(close=df['close'], window=7).rsi()
    
    # MACD: 30분 봉에 맞춘 설정 (긴 주기: 26, 짧은 주기: 12, 시그널 주기: 9)
    macd = ta.trend.MACD(close=df['close'], window_slow=26, window_fast=12, window_sign=9)
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    df['macd_diff'] = macd.macd_diff()
    
    # 이동평균선: EMA(7), SMA(20)로 설정
    df['sma_20'] = ta.trend.SMAIndicator(close=df['close'], window=20).sma_indicator()
    df['ema_7'] = ta.trend.EMAIndicator(close=df['close'], window=7).ema_indicator()
    
    return df

def get_fear_and_greed_index():
    url = "https://api.alternative.me/fng/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['data'][0]
    else:
        print(f"Failed to fetch Fear and Greed Index. Status code: {response.status_code}")
        return None

def get_sol_news():
    serpapi_key = os.getenv("SERPAPI_API_KEY")
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_news",
        "q": "SOL",
        "api_key": serpapi_key
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        news_results = data.get("news_results", [])
        headlines = []
        for item in news_results:
            headlines.append({
                "title": item.get("title", ""),
                "date": item.get("date", "")
            })
        
        return headlines[:5]  # 최신 5개의 뉴스 헤드라인만 반환
    except requests.RequestException as e:
        print(f"Error fetching news: {e}")
        return []

def ai_trading():
    # Upbit 객체 생성
    access = os.getenv("UPBIT_ACCESS_KEY")
    secret = os.getenv("UPBIT_SECRET_KEY")
    upbit = pyupbit.Upbit(access, secret)

    # 1. 현재 투자 상태 조회
    all_balances = upbit.get_balances()
    filtered_balances = [balance for balance in all_balances if balance['currency'] in ['SOL', 'KRW']]
    
    # 2. 오더북(호가 데이터) 조회
    orderbook = pyupbit.get_orderbook("KRW-SOL")
    
    # 3. 차트 데이터 조회 및 보조지표 추가
    df_30min = pyupbit.get_ohlcv("KRW-SOL", interval="minute30", count=30)
    df_30min = dropna(df_30min)
    df_30min = add_indicators(df_30min)
    
    df_hourly = pyupbit.get_ohlcv("KRW-SOL", interval="minute60", count=24)
    df_hourly = dropna(df_hourly)
    df_hourly = add_indicators(df_hourly)

    # 4. 공포 탐욕 지수 가져오기
    fear_greed_index = get_fear_and_greed_index()

    # 5. 뉴스 헤드라인 가져오기
    news_headlines = get_sol_news()

    # AI에게 데이터 제공하고 판단 받기
    client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))

    response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
        "role": "system",
        "content": """You are an expert in SOL investing. Analyze the provided data including technical indicators, market data, recent news headlines, and the Fear and Greed Index. Tell me whether to buy, sell, or hold at the moment. Consider the following in your analysis:
        - Technical indicators and market data
        - Recent news headlines and their potential impact on SOL price
        - The Fear and Greed Index and its implications
        - Overall market sentiment
        
        Response in json format.

        Response Example:
        {"decision": "buy", "reason": "some technical, fundamental, and sentiment-based reason"}
        {"decision": "sell", "reason": "some technical, fundamental, and sentiment-based reason"}
        {"decision": "hold", "reason": "some technical, fundamental, and sentiment-based reason"}"""
        },
        {
        "role": "user",
        "content": f"""Current investment status: {json.dumps(filtered_balances)}
Orderbook: {json.dumps(orderbook)}
30-Minute OHLCV with indicators (30 periods): {df_30min.to_json()}
Hourly OHLCV with indicators (24 hours): {df_hourly.to_json()}
Recent news headlines: {json.dumps(news_headlines)}
Fear and Greed Index: {json.dumps(fear_greed_index)}"""
        }
    ],
    response_format={
        "type": "json_object"
    }
    )
    result = response.choices[0].message.content

    # AI의 판단에 따라 실제로 자동매매 진행하기
    result = json.loads(result)

    print("### AI Decision: ", result["decision"].upper(), "###")
    print(f"### Reason: {result['reason']} ###")

    if result["decision"] == "buy":
        my_krw = upbit.get_balance("KRW")
        if my_krw * 0.9995 > 5000:
            print("### Buy Order Executed ###")
            print(upbit.buy_market_order("KRW-SOL", my_krw * 0.9995))
        else:
            print("### Buy Order Failed: Insufficient KRW (less than 5000 KRW) ###")
    elif result["decision"] == "sell":
        my_SOL = upbit.get_balance("KRW-SOL")
        current_price = pyupbit.get_orderbook(ticker="KRW-SOL")['orderbook_units'][0]["ask_price"]
        if my_SOL * current_price > 5000:
            print("### Sell Order Executed ###")
            print(upbit.sell_market_order("KRW-SOL", my_SOL))
        else:
            print("### Sell Order Failed: Insufficient SOL (less than 5000 KRW worth) ###")
    elif result["decision"] == "hold":
        print("### Hold Position ###")

# Main loop
while True:
    try:
        ai_trading()
        time.sleep(1800)  # 30분마다 실행 (API 사용량 제한 고려)
    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(300)  # 오류 발생 시 5분 후 재시도
