import csv
import portfolio.reconstruct_filer, portfolio.whale_index

_FILER_ID_SCION = '328297'

def print_hi():
    holdings = portfolio.reconstruct_filer.build_portfolio(_FILER_ID_SCION, 30000)

    import pprint
    pprint.pprint(holdings)

    print(sum([h['current_percent_of_portfolio'] for h in holdings]))
    print(round(sum([h['avg_price'] * h['number_of_stocks'] for h in holdings]), 2))

    holdings = portfolio.whale_index.build_portfolio(30000)

    import pprint
    pprint.pprint(holdings)

    print(round(sum([h['avg_price'] * h['number_of_stocks'] for h in holdings]), 2))

    import market.polygon.daily_price
    print(market.polygon.daily_price.get_close('AAPL'))

if __name__ == '__main__':
    print_hi()
