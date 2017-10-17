import requests

chart = "total-bitcoins"
BASE_URI = "https://api.blockchain.info"

def _handle_response(response):
    raise NotImplemented

def get_chart(chart, timespan=None, rollingAverage=None, start=None, sampled=None):

    params = {}
    if timespan:
        params['timespan'] = timespan

    if rollingAverage:
        params['rollingAverage'] = rollingAverage

    if start:
        params['start'] = start

    if sampled:
        params['include_breaks'] = sampled

    url = "https://api.blockchain.info/charts/" + chart
    response = requests.get(url, params=params)
    return _handle_response(response)

def get_ticker():
    url = BASE_URI+"/ticker"
    response = requests.get(url)
    return _handle_response(response)

def get_stats():
    url = BASE_URI+"/stats"
    response = requests.get(url)
    return _handle_response(response)

def get_pools():
    url = BASE_URI+"/pools"
    response = requests.get(url)
    return _handle_response(response)
