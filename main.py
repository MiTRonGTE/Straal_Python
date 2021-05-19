# coding: utf-8


from datetime import datetime
from typing import Optional, List, Literal
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, constr, NonNegativeInt, PositiveInt
from pytz import timezone
import json
import urllib.request
import sqlite3


# uvicorn main:app

app = FastAPI()

app.id_payment_info = {}

app.all_response = []
app.customer_id = None
app.date_format = "%Y-%m-%dT%H:%M:%S%z"


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(exc):
    return PlainTextResponse(str(exc), status_code=400)


class PayByLink(BaseModel):
    customer_id: Optional[PositiveInt] = None
    created_at: str
    currency: Literal['EUR', 'USD', 'GBP', 'PLN']
    amount: NonNegativeInt
    description: str
    bank: str


class Dp(BaseModel):
    customer_id: Optional[PositiveInt] = None
    created_at: str
    currency: Literal['EUR', 'USD', 'GBP', 'PLN']
    amount: NonNegativeInt
    description: str
    iban: constr(max_length=22, min_length=22)


class Card(BaseModel):
    customer_id: Optional[PositiveInt] = None
    created_at: str
    currency: Literal['EUR', 'USD', 'GBP', 'PLN']
    amount: NonNegativeInt
    description: str
    cardholder_name: str
    cardholder_surname: str
    card_number: constr(max_length=16, min_length=16)


class RequestReport(BaseModel):
    pay_by_link: Optional[List[PayByLink]]
    dp: Optional[List[Dp]]
    card: Optional[List[Card]]


def get_exchange_rate(currency, iso_date):
    try:
        if currency.upper() != "PLN":
            short_date = iso_date[:10]

            with urllib.request.urlopen(
                    f"http://api.nbp.pl/api/exchangerates/rates/c/{currency}/{short_date}/?format=json") as url:
                exchange_rate = json.loads(url.read().decode())
                exchange_rate = exchange_rate.get("rates")[0].get("bid")
                return exchange_rate
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
        return date_utc.strftime(app.date_format).replace("+0000", "Z")
    except:
        raise HTTPException(status_code=400)


def pay_by_link_requester(pbl):

    for i in range(len(pbl)):
        exchange_rate = get_exchange_rate(pbl[i].currency, pbl[i].created_at)
        utc_date = get_utc_time(pbl[i].created_at, app.date_format)
        try:
            if pbl[i].customer_id:
                app.customer_id = pbl[i].customer_id
                app.last_payment_info.append({
                    "customer_id": pbl[i].customer_id,
                    "date": utc_date,
                    "type": "pay_by_link",
                    "payment_mean": pbl[i].bank,
                    "description": pbl[i].description,
                    "currency": pbl[i].currency.upper(),
                    "amount": pbl[i].amount,
                    "amount_in_pln": (int(pbl[i].amount) * exchange_rate)//1,
                })
            else:
                app.last_payment_info.append({
                    "date": utc_date,
                    "type": "pay_by_link",
                    "payment_mean": pbl[i].bank,
                    "description": pbl[i].description,
                    "currency": pbl[i].currency.upper(),
                    "amount": pbl[i].amount,
                    "amount_in_pln": (int(pbl[i].amount) * exchange_rate)//1,
                })
        except:
            raise HTTPException(status_code=400)


def dp_requester(dp):
    for i in range(len(dp)):
        exchange_rate = get_exchange_rate(dp[i].currency, dp[i].created_at)
        utc_date = get_utc_time(dp[i].created_at, app.date_format)
        try:
            if dp[i].customer_id:
                app.last_payment_info.append({
                    "customer_id": dp[i].customer_id,
                    "date": utc_date,
                    "type": "dp",
                    "payment_mean": dp[i].iban,
                    "description": dp[i].description,
                    "currency": dp[i].currency.upper(),
                    "amount": dp[i].amount,
                    "amount_in_pln": (int(dp[i].amount)*exchange_rate)//1,
                })
            else:
                app.last_payment_info.append({
                    "date": utc_date,
                    "type": "dp",
                    "payment_mean": dp[i].iban,
                    "description": dp[i].description,
                    "currency": dp[i].currency.upper(),
                    "amount": dp[i].amount,
                    "amount_in_pln": (int(dp[i].amount) * exchange_rate)//1,
                })
        except:
            raise HTTPException(status_code=400)


def card_requester(card):
    for i in range(len(card)):
        exchange_rate = get_exchange_rate(card[i].currency, card[i].created_at)
        utc_date = get_utc_time(card[i].created_at, app.date_format)
        try:
            int(card[i].card_number)
            if card[i].customer_id:
                app.customer_id = card[i].customer_id
                app.last_payment_info.append({
                    "customer_id": card[i].customer_id,
                    "date": utc_date,
                    "type": "card",
                    "payment_mean": f"{card[i].cardholder_name.title()} {card[i].cardholder_surname.title()}"
                                    f" {card[i].card_number[:4] + 8 * '*' + card[i].card_number[-4:]}",
                    "description": card[i].description,
                    "currency": card[i].currency.upper(),
                    "amount": card[i].amount,
                    "amount_in_pln": (int(card[i].amount) * exchange_rate) // 1,
                })
            else:
                app.last_payment_info.append({
                    "date": utc_date,
                    "type": "card",
                    "payment_mean": f"{card[i].cardholder_name.title()} {card[i].cardholder_surname.title()}"
                                    f" {card[i].card_number[:4] + 8 * '*' + card[i].card_number[-4:]}",
                    "description": card[i].description,
                    "currency": card[i].currency.upper(),
                    "amount": card[i].amount,
                    "amount_in_pln": (int(card[i].amount) * exchange_rate) // 1,
                })
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


def try_id(pbl, dp, card):
    if pbl[0].customer_id :
        id_customer = pbl[0].customer_id
    elif dp[0].customer_id:
        id_customer = dp[0].customer_id
    elif card[0].customer_id:
        id_customer = card[0].customer_id
    else:
        raise HTTPException(status_code=400)

    for i in range(len(pbl)) :
        if id_customer != pbl[i].customer_id:
            raise HTTPException(status_code=400)
    for i in range(len(dp)):
        if id_customer != dp[i].customer_id:
            raise HTTPException(status_code=400)
    for i in range(len(card)) :
        if id_customer != card[i].customer_id:
            raise HTTPException(status_code=400)
    return id_customer


@app.post("/customer-report")
async def report_pay_id(report: RequestReport):
    app.last_payment_info = []
    app.customer_id = None
    pay_by_link_requester(report.pay_by_link)
    dp_requester(report.dp)
    card_requester(report.card)
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
