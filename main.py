# coding: utf-8
# uvicorn main:app
# pytest test.py

import string
from datetime import datetime
from typing import Optional, List  # Literal
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, constr, NonNegativeInt, PositiveInt
from pytz import timezone
import json
import urllib.request
from raport_basemodel import *  # modele porzyjmowanych danych


app = FastAPI()


id_payment_info = {}
Acce_Char = string.ascii_letters + "ńŃśŚćĆóÓżŻźŹęĘąĄłŁ '-"  # znazki dozwolone w imieniu i nazwisku
customer_id = None
Date_Format = "%Y-%m-%dT%H:%M:%S%z"  # format do jakiego ma być przekształcone created_at


# zamiana błędu nieprawidłowych danych z 422 do 400
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


# funkcja przekształcająca pay_by_link dla klijenta
def pay_by_link_requester(pbl_array, raport=False):
    # potwierdzenie czy został wysłany pbl
    if pbl_array is None:
        return

    # odczyt kojenych pbl z listy pbl_array
    for i in range(len(pbl_array)):
        pbl = pbl_array[i]

        # walidacja currency (waluta)
        if pbl.currency.upper() not in ['EUR', 'USD', 'GBP', 'PLN']:
            raise HTTPException(status_code=400)

        # przekonwertowanie daty do UTC i pobranie waluty z danygo dnia
        utc_date = get_utc_time(pbl.created_at, Date_Format)
        exchange_rate = get_exchange_rate(pbl.currency, utc_date)

        # składanie response_pbl
        try:
            converted_pbl = {}
            if pbl.customer_id and raport:
                converted_pbl["customer_id"] = pbl.customer_id

            converted_pbl.update({
                    "date": utc_date,
                    "type": "pay_by_link",
                    "payment_mean": pbl.bank,
                    "description": pbl.description,
                    "currency": pbl.currency.upper(),
                    "amount": pbl.amount,
                    "amount_in_pln": (int(pbl.amount) * exchange_rate)//1,
                })
            app.last_payment_info.append(converted_pbl)
        except:
            raise HTTPException(status_code=400)


# funkcja przekształcająca dp dla klijenta
def dp_requester(dp_array, raport=False):
    # potwierdzenie czy został wysłany dp
    if dp_array is None:
        return

    # odczyt kojenych dp z listy dp_array
    for i in range(len(dp_array)):
        dp = dp_array[i]

        # walidacja currency (waluta)
        if dp.currency.upper() not in ['EUR', 'USD', 'GBP', 'PLN']:
            raise HTTPException(status_code=400)

        # przekonwertowanie daty do UTC i pobranie waluty z danygo dnia
        utc_date = get_utc_time(dp.created_at, Date_Format)
        exchange_rate = get_exchange_rate(dp.currency, utc_date)

        # składanie response_dp
        try:
            converted_dp = {}
            if dp.customer_id and raport:
                converted_dp["customer_id"] = dp.customer_id
            converted_dp.update({
                "date": utc_date,
                "type": "dp",
                "payment_mean": dp.iban,
                "description": dp.description,
                "currency": dp.currency.upper(),
                "amount": dp.amount,
                "amount_in_pln": (int(dp.amount) * exchange_rate)//1,
            })
            app.last_payment_info.append(converted_dp)
        except:
            raise HTTPException(status_code=400)


# funkcja przekształcająca card dla klijenta
def card_requester(card_array, raport=False):
    # potwierdzenie czy został wysłany dp
    if card_array is None:
        return

    # odczyt kojenych card z listy card_array
    for i in range(len(card_array)):
        card = card_array[i]

        # walidacja cardholder_name i cardholder_surname czy nie zawierają niedozwolonych znaków
        for name in [card.cardholder_name, card.cardholder_surname]:
            for test in name:
                if test not in Acce_Char:
                    raise HTTPException(status_code=400)

        # walidacja currency (waluta)
        if card.currency.upper() not in ['EUR', 'USD', 'GBP', 'PLN']:
            raise HTTPException(status_code=400)

        # przekonwertowanie daty do UTC i pobranie waluty z danygo dnia
        utc_date = get_utc_time(card.created_at, Date_Format)
        exchange_rate = get_exchange_rate(card.currency, utc_date)

        # składanie response_card
        try:
            int(card.card_number)
            converted_card = {}
            if card.customer_id and raport:
                converted_card["customer_id"] = card.customer_id

            converted_card.update({
                "date": utc_date,
                "type": "card",
                "payment_mean": f"{card.cardholder_name.title()} {card.cardholder_surname.title()}"
                                f" {card.card_number[:4] + 8 * '*' + card.card_number[-4:]}",
                "description": card.description,
                "currency": card.currency.upper(),
                "amount": card.amount,
                "amount_in_pln": (int(card.amount) * exchange_rate) // 1,
            })

            app.last_payment_info.append(converted_card)
        except:
            raise HTTPException(status_code=400)


# potwierdzenie że wszystkie wysłane id klijenta są takie same a następnie zwrócenie id_customer
def try_id(pbl, dp, card):
    if pbl is None or dp is None or card is None:
        return
    if pbl[0].customer_id:
        id_customer = pbl[0].customer_id
    elif dp[0].customer_id:
        id_customer = dp[0].customer_id
    elif card[0].customer_id:
        id_customer = card[0].customer_id
    else:
        raise HTTPException(status_code=400)

    pbl_len = len(pbl)
    dp_len = len(dp)
    card_len = len(card)
    max_len = max(pbl_len, dp_len, card_len)

    for i in range(max_len):
        if i < pbl_len and pbl[i].customer_id != id_customer:
            raise HTTPException(status_code=400)
        if i < dp_len and dp[i].customer_id != id_customer:
            raise HTTPException(status_code=400)
        if i < card_len and card[i].customer_id != id_customer:
            raise HTTPException(status_code=400)

    return id_customer


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


# funkcja potrzebna do sortowania response'ów po dacie
def get_date(dictionary):
    return dictionary.get("date")


# funkcja zamieniająca date z formatu iso8061 do UTC
def get_utc_time(created_at, fmt):
    try:
        iso_time = datetime.strptime(str(created_at), fmt)
        date_utc = iso_time.astimezone(timezone('UTC'))
        return date_utc.strftime(Date_Format).replace("+0000", "Z")
    except:
        raise HTTPException(status_code=400)


# endpoint pobierajacy dane o płatnością i konwertuje je do raportu
@app.post("/report")
async def report_post_func(report: RequestReport):
    app.last_payment_info = []
    pay_by_link_requester(report.pay_by_link)
    dp_requester(report.dp)
    card_requester(report.card)
    app.last_payment_info.sort(key=get_date)
    return app.last_payment_info


# endpoint pobierajacy dane o płatnością i konwertuje je z dodatkowym przypisaniem id do raportu
@app.post("/customer-report")
async def report_pay_id(report: RequestReport):
    app.last_payment_info = []
    customer_id = None
    pay_by_link_requester(report.pay_by_link, True)
    dp_requester(report.dp, True)
    card_requester(report.card, True)
    app.last_payment_info.sort(key=get_date)

    customer_id = try_id(report.pay_by_link, report.dp, report.card)

    id_payment_info[customer_id] = app.last_payment_info
    return app.last_payment_info


# endpoint wyświetlający raport dla wskazanego id
@app.get("/customer-report/{customer_id}")
def customer_report_id(customer_id: int):
    try:
        return id_payment_info[customer_id]
    except:
        raise HTTPException(status_code=400)
