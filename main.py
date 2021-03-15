import portfolio

_FILER_ID_SCION = '328297'

def print_hi():
    holdings = portfolio.build_portfolio(_FILER_ID_SCION, 30000)

    import pprint
    pprint.pprint(holdings)

    print(sum([h['current_percent_of_portfolio'] for h in holdings]))
    print(round(sum([h['avg_price'] * h['number_of_stocks'] for h in holdings]), 2))

if __name__ == '__main__':
    print_hi()
