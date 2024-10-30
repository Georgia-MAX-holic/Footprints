import pyupbit

# 원하는 암호화폐 티커 지정
ticker = "KRW-BTC"  # BTC/원화 시장 데이터 예시

# 1. 현재 투자 상태 조회 (잔고)
def get_investment_status():
    access = "YOUR_ACCESS_KEY"  # 본인의 API Key로 변경
    secret = "YOUR_SECRET_KEY"  # 본인의 Secret Key로 변경
    upbit = pyupbit.Upbit(access, secret)
    balance = upbit.get_balances()  # 모든 자산 조회
    return balance

# 2. 오더북 데이터 조회 (호가 데이터)
def get_orderbook_data(ticker):
    orderbook = pyupbit.get_orderbook(ticker=ticker)
    return orderbook

# 3. 차트 데이터 조회 - 30일 일봉 ohlcv
def get_daily_chart_data(ticker):
    daily_ohlcv = pyupbit.get_ohlcv(ticker, interval="day", count=30)
    return daily_ohlcv

# 4. 차트 데이터 조회 - 24시간 시간 봉 ohlcv
def get_hourly_chart_data(ticker):
    hourly_ohlcv = pyupbit.get_ohlcv(ticker, interval="minute60", count=24)
    return hourly_ohlcv

# 결과 출력
if __name__ == "__main__":
    # 1. 현재 투자 상태 출력
    print("현재 투자 상태:")
    investment_status = get_investment_status()
    print(investment_status)

    # 2. 오더북 데이터 출력
    print("\n오더북 데이터:")
    orderbook_data = get_orderbook_data(ticker)
    print(orderbook_data)

    # 3. 30일 일봉 데이터 출력
    print("\n30일 일봉 데이터 (OHLCV):")
    daily_chart_data = get_daily_chart_data(ticker)
    print(daily_chart_data)

    # 4. 24시간 시간 봉 데이터 출력
    print("\n24시간 시간 봉 데이터 (OHLCV):")
    hourly_chart_data = get_hourly_chart_data(ticker)
    print(hourly_chart_data)