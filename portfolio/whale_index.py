import csv, numpy as np
import market.polygon.daily_price
import portfolio.util as portfolio_util

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
            portfolio_util.AVERAGE_PRICE: close_price,
            portfolio_util.PERCENT_OF_PORTFOLIO: 0,
            portfolio_util.NUMBER_OF_STOCKS: 0,
            portfolio_util.DOLLAR_INVESTED: 0,
            portfolio_util.STOCK_NAME: row[0],
            portfolio_util.STOCK_TICKER: symbol,
        })

    for h in portfolio:
        close_price = h[portfolio_util.AVERAGE_PRICE]
        percent = round(100.0 / len(rows), 2)
        number_of_stocks = int(np.floor(budget * percent / 100.0 / close_price))
        h[portfolio_util.PERCENT_OF_PORTFOLIO] = percent
        h[portfolio_util.NUMBER_OF_STOCKS] = number_of_stocks
        h[portfolio_util.DOLLAR_INVESTED] = round(close_price * number_of_stocks, 2)

    return portfolio
