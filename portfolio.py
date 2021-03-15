import requests, numpy as np
import api_sig

def build_portfolio(filer_id, budget):
    url = api_sig.get_request_url(
        {"command":"holdings", "filer_ids":[str(filer_id)]})
    r = requests.get(url)

    results = r.json()['results']
    records = [] if not results else results[0]['records']
    holdings = [] if not records else records[0]['holdings']

    columns = ['avg_price', 'stock_ticker', 'stock_name', 'security_type', 'current_percent_of_portfolio']
    holdings = [{c: h[c] for c in columns} for h in holdings]
    holdings = [h for h in holdings if h['avg_price']]
    holdings = [h for h in holdings if h['current_percent_of_portfolio']]
    holdings.sort(key=lambda h: h['current_percent_of_portfolio'], reverse=True)

    sum_percent = sum([h['current_percent_of_portfolio'] for h in holdings])
    portfolio = [h for h in holdings]
    for h in portfolio:
        h['rescaled_percent_of_portfolio'] = round(h['current_percent_of_portfolio'] / sum_percent * 100, 3)
        h['number_of_stocks'] = int(np.floor(budget * h['rescaled_percent_of_portfolio'] / 100.0 / h['avg_price']))
        h['dollor_invested'] = round(h['avg_price'] * h['number_of_stocks'], 2)

    return portfolio
