import requests

#good link http://docs.python-requests.org/en/master/user/quickstart/

hostname = "http://localhost:4000"

def get_key_value(key):
  params ={"key":key}
  url = hostname + '/get'
  r = requests.get(url, params)
  return r.text

def set_key_value(key, value):
  url = hostname + "/set"
  params = {key:value}
  r = requests.get(url, params)

