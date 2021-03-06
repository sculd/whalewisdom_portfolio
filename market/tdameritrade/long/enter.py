import market.tdameritrade.common
from market.dry_run.long.enter import LongDryRun
import tda.orders.equities
from tda.orders.common import Duration, Session
import os, threading
import util.logging

_ACCOUNT_NUMBER = os.getenv('TD_ACCOUNT_ID')


class Long:
    def __init__(self, market_price):
        self.market_price = market_price
        self.client = market.tdameritrade.common.get_client()

    def _long(self, enter_plan):
        symbol, price, quantity = enter_plan.plan(self.market_price)
        util.logging.info('buying {symbol}, quantity: {quantity}, target price: {target_price}, price: {price}'.format(symbol=enter_plan.symbol, quantity=quantity, target_price = enter_plan.target_price, price=price))

        try:
            order_spec = tda.orders.equities.equity_buy_market(symbol, quantity). \
                set_duration(Duration.GOOD_TILL_CANCEL). \
                set_session(Session.SEAMLESS). \
                build()

            response = self.client.place_order(_ACCOUNT_NUMBER, order_spec)
            if not response or not response.ok:
                return {}

            js = response.json()
            return js
        except Exception as ex:
            util.logging.error(str(ex))
            return {}

    def _long_thread(self, enter_plan):
        threading.Thread(target=self._long, args=(enter_plan,)).start()

    def enter(self, enter_plan):
        '''

        :param enter_plan: map of symbol to quantity
        :return:
        '''
        self._long_thread(enter_plan)

_buy = None
def get_long(market_price, dry_run):
    global _buy
    if _buy is not None:
        return _buy

    if dry_run:
        res = LongDryRun(market_price)
    else:
        res = Long(market_price)
    _buy = res
    return res
