import os, datetime
from polygon import RESTClient
import util.time

_POLYGON_API_KEY = os.environ['API_KEY_POLYGON']

_client = RESTClient(_POLYGON_API_KEY)

def get_close(symbol, current_epoch_seconds=None):
    print('getting the closing price for {s}'.format(s=symbol))
    current_epoch_seconds = current_epoch_seconds or int(datetime.datetime.now().timestamp())
    most_recent = datetime.datetime.fromtimestamp(current_epoch_seconds, util.time.get_us_east_timezone())

    ret = 0
    max_delta_days = 7
    delta_days = 0
    while True:
        try:
            dt = (most_recent - datetime.timedelta(days=delta_days)).date()
            resp = _client.stocks_equities_daily_open_close(symbol, str(dt))
            ret = resp.close
        except Exception as e:
            delta_days += 1
            if delta_days > max_delta_days:
                break
            continue
        break
    return ret
