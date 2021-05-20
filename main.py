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


app = FastAPI()


app.id_payment_info = {}
app.Acce_Char = string.ascii_letters + "ńŃśŚćĆóÓżŻźŹęĘąĄłŁ '-"
app.all_response = []
app.customer_id = None
app.Date_Format = "%Y-%m-%dT%H:%M:%S%z"


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


class PayByLink(BaseModel):
    customer_id: Optional[PositiveInt] = None
    created_at: str
    currency: str  # Literal['EUR', 'USD', 'GBP', 'PLN']
    amount: NonNegativeInt
    description: str
    bank: str


class Dp(BaseModel):
    customer_id: Optional[PositiveInt] = None
    created_at: str
    currency: str  # Literal['EUR', 'USD', 'GBP', 'PLN']
    amount: NonNegativeInt
    description: str
    iban: constr(max_length=22, min_length=22)


class Card(BaseModel):
    customer_id: Optional[PositiveInt] = None
    created_at: str
    currency: str  # Literal['EUR', 'USD', 'GBP', 'PLN']
    amount: NonNegativeInt
    description: str
    cardholder_name: str
    cardholder_surname: str
    card_number: constr(max_length=16, min_length=16)


class RequestReport(BaseModel):
    pay_by_link: Optional[List[PayByLink]]
    dp: Optional[List[Dp]]
    card: Optional[List[Card]]


def pay_by_link_requester(pbl_array, raport=False):
    if pbl_array is None:
        return
    for i in range(len(pbl_array)):
        pbl = pbl_array[i]
        if pbl.currency.upper() not in ['EUR', 'USD', 'GBP', 'PLN']:
            raise HTTPException(status_code=400)

        utc_date = get_utc_time(pbl.created_at, app.Date_Format)
        exchange_rate = get_exchange_rate(pbl.currency, utc_date)
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


def dp_requester(dp_array, raport=False):
    if dp_array is None:
        return
    for i in range(len(dp_array)):
        dp = dp_array[i]
        if dp.currency.upper() not in ['EUR', 'USD', 'GBP', 'PLN']:
            raise HTTPException(status_code=400)

        utc_date = get_utc_time(dp.created_at, app.Date_Format)
        exchange_rate = get_exchange_rate(dp.currency, utc_date)
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


def card_requester(card_array, raport=False):
    if card_array is None:
        return
    for i in range(len(card_array)):
        card = card_array[i]

        for name in [card.cardholder_name, card.cardholder_surname]:
            for test in name:
                if test not in app.Acce_Char:
                    raise HTTPException(status_code=400)

        if card.currency.upper() not in ['EUR', 'USD', 'GBP', 'PLN']:
            raise HTTPException(status_code=400)

        utc_date = get_utc_time(card.created_at, app.Date_Format)
        exchange_rate = get_exchange_rate(card.currency, utc_date)
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


def get_date(dictionary):
    return dictionary.get("date")


def get_utc_time(created_at, fmt):
    try:
        iso_time = datetime.strptime(str(created_at), fmt)
        date_utc = iso_time.astimezone(timezone('UTC'))
        return date_utc.strftime(app.Date_Format).replace("+0000", "Z")
    except:
        raise HTTPException(status_code=400)


@app.post("/report")
async def report_post_func(report: RequestReport):
    app.last_payment_info = []
    pay_by_link_requester(report.pay_by_link)
    dp_requester(report.dp)
    card_requester(report.card)
    app.last_payment_info.sort(key=get_date)
    return app.last_payment_info


@app.post("/customer-report")
async def report_pay_id(report: RequestReport):
    app.last_payment_info = []
    app.customer_id = None
    pay_by_link_requester(report.pay_by_link, True)
    dp_requester(report.dp, True)
    card_requester(report.card, True)
    app.last_payment_info.sort(key=get_date)

    app.customer_id = try_id(report.pay_by_link, report.dp, report.card)

    app.id_payment_info[app.customer_id] = app.last_payment_info
    return app.last_payment_info


@app.get("/customer-report/{customer_id}")
def customer_report_id(customer_id: int):
    try:
        return app.id_payment_info[customer_id]
    except:
        raise HTTPException(status_code=400)
