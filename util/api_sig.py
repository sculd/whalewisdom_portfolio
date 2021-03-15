import base64, hashlib, hmac, json, os, time
from urllib.parse import quote_plus

_BASE_URL = 'https://whalewisdom.com/shell/command.json?'
_API_SECRET_KEY = os.getenv('WHALE_WISDOM_API_SECRET_KEY')
_API_SHARED_KEY = os.getenv('WHALE_WISDOM_API_SHARED_KEY')

def get_request_url(dict_args):
    json_args = json.dumps(dict_args)
    timenow = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    raw_args=json_args+'\n'+timenow

    hmac_hash = hmac.new(_API_SECRET_KEY.encode(),raw_args.encode(), hashlib.sha1).digest()
    sig = base64.b64encode(hmac_hash).rstrip()

    formatted_args = quote_plus(json_args)
    url_args = 'args=' + formatted_args
    url_end = '&api_shared_key=' + _API_SHARED_KEY + '&api_sig=' + sig.decode() + '&timestamp=' + timenow
    api_url = _BASE_URL + url_args + url_end
    return api_url
