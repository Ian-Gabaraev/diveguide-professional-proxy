import shelve
from urllib.parse import urljoin

import requests
import time
import settings


while True:
    try:
        api_url = settings.get_api_url()
        url = urljoin(api_url, settings.API_HEALTH_CHECK_ROUTE)
        response = requests.get(url)

        if response.status_code == 200:
            with shelve.open('cache') as db:
                db[settings.HEALTHY_CACHE_KEY] = 1
        else:
            with shelve.open('cache') as db:
                db[settings.HEALTHY_CACHE_KEY] = 0
    except requests.exceptions.RequestException as e:
        with shelve.open('cache') as db:
            db[settings.HEALTHY_CACHE_KEY] = 0

    time.sleep(10)
