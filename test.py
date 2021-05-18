from datetime import datetime
from pytz import timezone

fmt = "%Y-%m-%dT%H:%M:%S%z"

# Current time in UTC
nowtime = datetime.strptime("2021-05-13T01:01:43-08:00", "%Y-%m-%dT%H:%M:%S%z")
print(nowtime.strftime(fmt))

nowtime1 = datetime.strptime("2025-05-13T01:01:43-08:00", "%Y-%m-%dT%H:%M:%S%z")
print(nowtime.strftime(fmt))

now_utc = nowtime.astimezone(timezone('UTC'))
now_utc1 = nowtime1.astimezone(timezone('UTC'))
print(now_utc.strftime(fmt).replace("+0000","Z"))
print(now_utc1.strftime(fmt).replace("+0000","Z"))

if now_utc > now_utc1:
    print("wiekszy")
else:
    print("mniejszy")

# import urllib.request, json
#
# with urllib.request.urlopen("http://api.nbp.pl/api/exchangerates/rates/a/GBP/2021-05-13/?format=json") as url:
#     exchange_rate = json.loads(url.read().decode())
#     print(exchange_rate.get("rates")[0].get("mid"))