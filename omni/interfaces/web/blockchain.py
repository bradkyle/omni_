from omni.interfaces.util import invoke

chart = "total-bitcoins"
BASE_URI = "https://api.blockchain.info"

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
    return invoke("GET", url, params=params)

def get_ticker():
    url = BASE_URI+"/ticker"
    return invoke("GET", url)

def get_stats():
    url = BASE_URI+"/stats"
    return invoke("GET", url)

def get_pools():
    url = BASE_URI+"/pools"
    return invoke("GET", url)
