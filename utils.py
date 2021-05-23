from fastapi import HTTPException
from datetime import datetime
from pytz import timezone
import json
import urllib.request

def try_currency(currency):
    if currency.upper() not in ['EUR', 'USD', 'GBP', 'PLN']:
        raise HTTPException(status_code=400)


# funkcja zmieniająca date z formatu iso 8061 do UTC
def get_utc_time(created_at):
    try:
        iso_time = datetime.strptime(str(created_at), "%Y-%m-%dT%H:%M:%S%z")
        date_utc = iso_time.astimezone(timezone('UTC'))
        return date_utc.strftime("%Y-%m-%dT%H:%M:%S%z").replace("+0000", "Z")
    except:
        raise HTTPException(status_code=400)


# funkcja pobierająca pojedyńczą walute z danego dnia
# funkcja łączy się z http://api.nbp.pl/
def get_exchange_rate(currency, utc_date):
    try:
        if currency.upper() != "PLN":
            short_date = utc_date[:10]
            with urllib.request.urlopen(
                    f"http://api.nbp.pl/api/exchangerates/rates/c/{currency}/{short_date}/?format=json") as url:
                exchange_rate = json.loads(url.read().decode())
                exchange_rate = exchange_rate.get("rates")[0].get("bid")
                return float(exchange_rate)
        else:
            return 1
    except:
        raise HTTPException(status_code=400)


# funkcja potrzebna do sortowania response po dacie
def get_date(dictionary):
    return dictionary.get("date")
