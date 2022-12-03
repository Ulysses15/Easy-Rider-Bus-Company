import requests


def check_success(url):
    r = requests.get(url)
    h = r.status_code
    if h >= 200 and h <= 399:
        return 'Success'
    if str(h)[0] == '4':
        return 'Fail'
