import requests, numpy as np
from util import api_sig
import portfolio.util as portfolio_util

def build_portfolio(filer_id, budget):
    url = api_sig.get_request_url(
        {"command":"holdings", "filer_ids":[str(filer_id)]})
    r = requests.get(url)

    results = r.json()['results']
    records = [] if not results else results[0]['records']
    holdings = [] if not records else records[0]['holdings']

    columns = [portfolio_util.AVERAGE_PRICE, portfolio_util.STOCK_TICKER, portfolio_util.STOCK_NAME, 'security_type', portfolio_util.PERCENT_OF_PORTFOLIO]
    holdings = [{c: h[c] for c in columns} for h in holdings]
    holdings = [h for h in holdings if h[portfolio_util.AVERAGE_PRICE]]
    holdings = [h for h in holdings if h[portfolio_util.PERCENT_OF_PORTFOLIO]]
    holdings.sort(key=lambda h: h[portfolio_util.PERCENT_OF_PORTFOLIO], reverse=True)

    sum_percent = sum([h[portfolio_util.PERCENT_OF_PORTFOLIO] for h in holdings])
    portfolio = [h for h in holdings]
    for h in portfolio:
        h['rescaled_percent_of_portfolio'] = round(h['current_percent_of_portfolio'] / sum_percent * 100, 3)
        h[portfolio_util.NUMBER_OF_STOCKS] = int(np.floor(budget * h['rescaled_percent_of_portfolio'] / 100.0 / h[portfolio_util.AVERAGE_PRICE]))
        h[portfolio_util.DOLLAR_INVESTED] = round(h[portfolio_util.AVERAGE_PRICE] * h[portfolio_util.NUMBER_OF_STOCKS], 2)

    return portfolio
