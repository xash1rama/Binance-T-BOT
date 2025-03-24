import numpy as np
from database import Information, session
from main import client

def calculate_rsi(prices):
    period = int(session.query(Information).filter(Information.name == "Period").first().data)
    deltas = np.diff(prices)
    gain = (deltas[deltas > 0]).sum() / period
    loss = (-deltas[deltas < 0]).sum() / period

    if loss == 0:
        return 100  # Если нет потерь, RSI равен 100

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def calculate_ra(prices):
    period = int(session.query(Information).filter(Information.name == "Period").first().data)
    return np.mean(prices[-period:])  # Среднее значение за последние `period` значений


def get_top_coins():
    limit = int(session.query(Information).filter(Information.name == "Лимит токенов").first().data)
    data = client.ticker_24hr_price_change()
    change = {}

    for el in data:
        # Проверяем, что символ заканчивается на USDT
        if el['symbol'].endswith('USDT'):
            change[el['symbol']] = float(el['priceChangePercent'])

    top_coins = sorted(change, key=change.get, reverse=True)[:limit]
    print(f"Топ {limit} монет: {top_coins}")
    return top_coins



def get_symbol_price(symbol):
    price = round(float(client.ticker_price(symbol)['price']), 5)
    print(f"Цена монеты {symbol}: {price}")
    return price


def get_close_data(symbol):
    time_frame = session.query(Information).filter(Information.name == "Time Frame").first().data
    klines = client.klines(symbol, time_frame, limit=1500)
    close = []
    for kline in klines:
        close.append(float(kline[4]))
    print(close)
    return close


def get_trade_volume(symbol):
    dep = session.query(Information).filter(Information.name == "Deposit").first().data
    volume = round(round(float(dep), 2)/get_symbol_price(symbol))
    print(f"Volume: {volume}")
    return volume


def open_market_order(symbol, volume):
    params = {
        'symbol': symbol,
        'side': 'BUY',
        'type': 'MARKET',
        'quantity': volume,
    }
    response = client.new_order(**params)
    print(response)

def open_stop_order(symbol, price, volume):
    params = {
        'symbol': symbol,
        'side': 'SELL',
        'type': 'TAKE_PROFIT_MARKET',
        'stopPrice': price,
        'quantity': volume,
    }
    response = client.new_order(**params)
    print(response)


def open_take_profit_order(symbol, price, volume):
    params = {
        'symbol': symbol,
        'side': 'SELL',
        'type': 'STOP_MARKET',
        'stopPrice': price,
        'quantity': volume,
    }
    response = client.new_order(**params)
    print(response)


def get_stop_lose_price(price):
    stop_lose = session.query(Information).filter(Information.name == "Stop lose").first().data
    stop_lose_price = round(price - (price * round(float(stop_lose),2)), 4)
    print(f"Stop-lose: {stop_lose_price}")
    return stop_lose_price


def get_take_profit_price(price):
    take_profite = session.query(Information).filter(Information.name == "Take profit").first().data

    take_profit_price = round((price * round(float(take_profite), 2) + price), 4)
    print(f"Take profit: {take_profit_price}")
    return take_profit_price