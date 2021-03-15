import csv, numpy as np
import market.polygon.daily_price

_FILE_NAME = 'data/whale_index_100.csv'

def build_portfolio(budget):
    portfolio = []

    rows = []
    with open(_FILE_NAME, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csv_reader:
            rows.append(row)

    for row in rows:
        symbol = row[1]
        close_price = market.polygon.daily_price.get_close(symbol)
        if close_price == 0:
            continue
        portfolio.append({
            'avg_price': close_price,
            'percent_of_portfolio': 0,
            'number_of_stocks': 0,
            'dollor_invested': 0,
            'stock_name': row[0],
            'stock_ticker': symbol,
        })

    for h in portfolio:
        close_price = h['avg_price']
        percent = round(100.0 / len(rows), 2)
        number_of_stocks = int(np.floor(budget * percent / 100.0 / close_price))
        h['percent_of_portfolio'] = percent
        h['number_of_stocks'] = number_of_stocks
        h['dollor_invested'] = round(close_price * number_of_stocks, 2)

    return portfolio
