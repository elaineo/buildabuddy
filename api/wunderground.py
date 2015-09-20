"""
Weather for San Francisco
"""
import json
# tide

def astronomy():
    url = 'http://api.wunderground.com/api/58f24c82326936ee/astronomy/q/CA/San_Francisco.json'
    r = requests.get(url)
    return json.loads(r.content)


def conditions():
    url = 'http://api.wunderground.com/api/58f24c82326936ee/conditions/q/CA/San_Francisco.json'
    r = requests.get(url)
    return json.loads(r.content)


def tide():
    url = 'http://api.wunderground.com/api/58f24c82326936ee/tide/q/CA/San_Francisco.json'
    r = requests.get(url)
    return json.loads(r.content)


def forecast():
    url = 'http://api.wunderground.com/api/58f24c82326936ee/forecast/q/CA/San_Francisco.json'
    r = requests.get(url)
    return json.loads(r.content)


def yesterday():
    url = 'http://api.wunderground.com/api/58f24c82326936ee/forecast/q/CA/San_Francisco.json'
    r = requests.get(url)
    return json.loads(r.content)
