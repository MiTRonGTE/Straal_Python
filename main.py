# coding: utf-8

from fastapi import FastAPI, HTTPException, Request, Response,  status, Cookie, Depends
from pydantic import BaseModel, PositiveInt, constr, Field, NonNegativeInt, PydanticTypeError, validator
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse, ORJSONResponse
from datetime import timedelta, date, datetime
from pytz import timezone
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Optional, List, Literal
import hashlib
import string
import secrets
import random
import sqlite3
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import urllib.request
import json

# uvicorn main:app

app = FastAPI()

app.all_response = []
app.date_format = "%Y-%m-%dT%H:%M:%S%z"


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


class PayByLink(BaseModel):
    created_at: str
    currency: Literal['EUR','USD', 'GBP', 'PLN']
    amount: NonNegativeInt
    description: str
    bank: str


class Dp(BaseModel):
    created_at: str
    currency: Literal['EUR','USD', 'GBP', 'PLN']
    amount: NonNegativeInt
    description: str
    iban: constr(max_length=22, min_length=22)


class Card(BaseModel):
    created_at: str
    currency: Literal['EUR','USD', 'GBP', 'PLN']
    amount: NonNegativeInt
    description: str
    cardholder_name: str
    cardholder_surname: str
    card_number: constr(max_length=16, min_length=16)


class RequestReport(BaseModel):
    pay_by_link: Optional[List[PayByLink]]
    dp: Optional[List[Dp]]
    card: Optional[List[Card]]


def get_exchange_rate(currency, date):
    try:
        if currency.upper() != "PLN":
            short_date = date[:10]

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
        date = get_utc_time(pbl[i].created_at, app.date_format)

        app.last_payment_info.append({
            "date": date,
            "type": "pay_by_link",
            "payment_mean": pbl[i].bank,
            "description": pbl[i].description,
            "currency": pbl[i].currency.upper(),
            "amount": pbl[i].amount,
            "amount_in_pln": (int(pbl[i].amount) * exchange_rate)//1,
        })


def dp_requester(dp):
    for i in range(len(dp)):
        exchange_rate = get_exchange_rate(dp[i].currency, dp[i].created_at)
        date = get_utc_time(dp[i].created_at, app.date_format)

        app.last_payment_info.append({
            "date": date,
            "type": "dp",
            "payment_mean": dp[i].iban,
            "description": dp[i].description,
            "currency": dp[i].currency.upper(),
            "amount": dp[i].amount,
            "amount_in_pln": (int(dp[i].amount) * exchange_rate)//1,
        })


def card_requester(card):
    for i in range(len(card)):
        exchange_rate = get_exchange_rate(card[i].currency, card[i].created_at)
        date = get_utc_time(card[i].created_at, app.date_format)

        app.last_payment_info.append({
            "date": date,
            "type": "card",
            "payment_mean": f"{card[i].cardholder_name.title()} {card[i].cardholder_surname.title()} {card[i].card_number[:4] + 8*'*'+ card[i].card_number[-4:]}",
            "description": card[i].description,
            "currency": card[i].currency.upper(),
            "amount": card[i].amount,
            "amount_in_pln": (int(card[i].amount) * exchange_rate)//1,
        })


@app.post("/report")
async def report_post_func(rep: RequestReport):
    app.last_payment_info = []
    pay_by_link_requester(rep.pay_by_link)
    dp_requester(rep.dp)
    card_requester(rep.card)
    app.last_payment_info.sort(key=get_date)
    return app.last_payment_info


# sprawdzić czy w card number są tylko cyferki

