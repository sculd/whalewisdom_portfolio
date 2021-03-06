import market.tdameritrade.common
from market.dry_run.short.enter import ShortDryRun
import tda.orders.equities
from tda.orders.common import Duration, Session
import os, threading, datetime
import util.logging

_ACCOUNT_NUMBER = os.getenv('TD_ACCOUNT_ID')
_INSTRUCTION_SELL_SHORT = 'SELL_SHORT'

class Short:
    def __init__(self, market_price):
        self.market_price = market_price
        self.client = market.tdameritrade.common.get_client()

    def _short(self, enter_plan):
        symbol, price, quantity = enter_plan.plan(self.market_price)
        util.logging.info('shorting {symbol}, quantity: {quantity}, target price: {target_price}, price: {price}'.format(symbol=enter_plan.symbol, quantity=quantity, target_price = enter_plan.target_price, price=price))

        if price < 5:
            util.logging.warning('shorting {symbol} under $5 is not allowed, quantity: {quantity}, target price: {target_price}, price: {price}'.format(symbol=enter_plan.symbol, quantity=quantity, target_price = enter_plan.target_price, price=price))
            return None

        try:
            order_spec = tda.orders.equities.equity_sell_market(symbol, quantity). \
                set_duration(Duration.GOOD_TILL_CANCEL). \
                set_session(Session.SEAMLESS). \
                build()

            for leg in order_spec['orderLegCollection']:
                leg['instruction'] = _INSTRUCTION_SELL_SHORT

            response = self.client.place_order(_ACCOUNT_NUMBER, order_spec)
            if not response or not response.ok:
                return {}

            js = response.json()
            util.logging.info('submitted a short enter order for {symbol}, response: {response}'.format(symbol=symbol, response=js))
            return js
        except Exception as ex:
            util.logging.error(str(ex))
            return {}

    def _short_thread(self, enter_plan):
        threading.Thread(target=self._short, args=(enter_plan,)).start()

    def enter(self, enter_plan):
        '''

        :param enter_plan: map of symbol to quantity
        :return:
        '''
        self._short_thread(enter_plan)


_buy = None
def get_short(market_price, dry_run):
    global _buy
    if _buy is not None:
        return _buy

    if dry_run:
        res = ShortDryRun(market_price)
    else:
        res = Short(market_price)
    _buy = res
    return res
