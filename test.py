import pytest

from fastapi.testclient import TestClient
from main import app, get_exchange_rate, get_utc_time

client = TestClient(app)

report = {
    "pay_by_link": [
        {
            "created_at": "2021-05-13T01:01:43-08:00",
            "currency": "EUR",
            "amount": 3000,
            "description": "Abonament na siłownię",
            "bank": "mbank"
        }
    ],
    "dp": [
        {
            "created_at": "2021-05-14T08:27:09Z",
            "currency": "USD",
            "amount": 599,
            "description": "FastFood",
            "iban": "DE91100000000123456789"
        }
    ],
    "card": [
        {
            "created_at": "2021-05-13T09:00:05+02:00",
            "currency": "PLN",
            "amount": 2450,
            "description": "REF123457",
            "cardholder_name": "John",
            "cardholder_surname": "Doe",
            "card_number": "2222222222222222"
        },
        {
            "created_at": "2021-05-14T18:32:26Z",
            "currency": "GBP",
            "amount": 1000,
            "description": "REF123456",
            "cardholder_name": "John",
            "cardholder_surname": "Doe",
            "card_number": "1111111111111111"
        }
    ]
}

report_invalid_currency = {
    "pay_by_link": [
        {
            "customer_id": 1,
            "created_at": "",
            "currency": "re",
            "amount": 3000,
            "description": "Abonament na siłownię",
            "bank": "mbank"
        }
    ],
    "dp": [
        {
            "customer_id": 1,
            "created_at": "2021-05-14T08:27:09Z",
            "currency": "re",
            "amount": 599,
            "description": "FastFood",
            "iban": "DE91100000000123456789"
        }
    ],
    "card": [
        {
            "customer_id": 1,
            "created_at": "2021-05-13T09:00:05+02:00",
            "currency": "re",
            "amount": 2450,
            "description": "REF123457",
            "cardholder_name": "John",
            "cardholder_surname": "Doe",
            "card_number": "2222222222222222"
        },
        {
            "customer_id": 1,
            "created_at": "2021-05-14T18:32:26Z",
            "currency": "re",
            "amount": 1000,
            "description": "REF123456",
            "cardholder_name": "John",
            "cardholder_surname": "Doe",
            "card_number": "1111111111111111"
        }
    ]
}

report_id_test1 = {
    "pay_by_link": [
        {
            "customer_id": 1,
            "created_at": "2021-05-13T01:01:43-08:00",
            "currency": "EUR",
            "amount": 3000,
            "description": "Abonament na siłownię",
            "bank": "mbank"
        }
    ],
    "dp": [
        {
            "customer_id": 1,
            "created_at": "2021-05-14T08:27:09Z",
            "currency": "USD",
            "amount": 599,
            "description": "FastFood",
            "iban": "DE91100000000123456789"
        }
    ],
    "card": [
        {
            "customer_id": 1,
            "created_at": "2021-05-13T09:00:05+02:00",
            "currency": "PLN",
            "amount": 2450,
            "description": "REF123457",
            "cardholder_name": "John",
            "cardholder_surname": "Doe",
            "card_number": "2222222222222222"
        },
        {
            "customer_id": 1,
            "created_at": "2021-05-14T18:32:26Z",
            "currency": "GBP",
            "amount": 1000,
            "description": "REF123456",
            "cardholder_name": "John",
            "cardholder_surname": "Doe",
            "card_number": "1111111111111111"
        }
    ]
}

report_id_test2 = {
    "pay_by_link": [
        {
            "customer_id": 456666666664654564,
            "created_at": "2021-05-13T01:01:43-08:00",
            "currency": "EUR",
            "amount": 3000,
            "description": "Abonament na siłownię",
            "bank": "mbank"
        }
    ],
    "dp": [
        {
            "customer_id": 456666666664654564,
            "created_at": "2021-05-14T08:27:09Z",
            "currency": "USD",
            "amount": 599,
            "description": "FastFood",
            "iban": "DE91100000000123456789"
        }
    ],
    "card": [
        {
            "customer_id": 456666666664654564,
            "created_at": "2021-05-13T09:00:05+02:00",
            "currency": "PLN",
            "amount": 2450,
            "description": "REF123457",
            "cardholder_name": "John",
            "cardholder_surname": "Doe",
            "card_number": "2222222222222222"
        },
        {
            "customer_id": 456666666664654564,
            "created_at": "2021-05-14T18:32:26Z",
            "currency": "GBP",
            "amount": 1000,
            "description": "REF123456",
            "cardholder_name": "John",
            "cardholder_surname": "Doe",
            "card_number": "1111111111111111"
        }
    ]
}

report_id_test2_1 = {
    "pay_by_link": [
        {
            "customer_id": 456666666664654564,
            "created_at": "2021-05-13T01:01:43-08:00",
            "currency": "Gbp",
            "amount": 3000,
            "description": "Abonament na siłownię",
            "bank": "mbank"
        }
    ],
    "dp": [
        {
            "customer_id": 456666666664654564,
            "created_at": "2021-05-14T08:27:09Z",
            "currency": "Eur",
            "amount": 5939,
            "description": "FastFood",
            "iban": "DE91100000000123456789"
        }
    ],
    "card": [
        {
            "customer_id": 456666666664654564,
            "created_at": "2021-05-13T09:00:05+02:00",
            "currency": "usd",
            "amount": 24510,
            "description": "REF123457",
            "cardholder_name": "John",
            "cardholder_surname": "Doe",
            "card_number": "2222222222222222"
        },
        {
            "customer_id": 456666666664654564,
            "created_at": "2021-05-14T18:32:26Z",
            "currency": "GBP",
            "amount": 10001,
            "description": "REF123456",
            "cardholder_name": "John",
            "cardholder_surname": "Doe",
            "card_number": "1111111111111111"
        }
    ]
}

report_id_test3 = {
    "pay_by_link": [
        {
            "customer_id": "string",
            "created_at": "2021-05-13T01:01:43-08:00",
            "currency": "EUR",
            "amount": 3000,
            "description": "Abonament na siłownię",
            "bank": "mbank"
        }
    ],
    "dp": [
        {
            "customer_id": "string",
            "created_at": "2021-05-14T08:27:09Z",
            "currency": "USD",
            "amount": 599,
            "description": "FastFood",
            "iban": "DE91100000000123456789"
        }
    ],
    "card": [
        {
            "customer_id": "string",
            "created_at": "2021-05-13T09:00:05+02:00",
            "currency": "PLN",
            "amount": 2450,
            "description": "REF123457",
            "cardholder_name": "John",
            "cardholder_surname": "Doe",
            "card_number": "2222222222222222"
        },
        {
            "customer_id": "string",
            "created_at": "2021-05-14T18:32:26Z",
            "currency": "GBP",
            "amount": 1000,
            "description": "REF123456",
            "cardholder_name": "John",
            "cardholder_surname": "Doe",
            "card_number": "1111111111111111"
        }
    ]
}

response_body = [
    {
        "customer_id": 1,
        "date": "2021-05-13T07:00:05Z",
        "type": "card",
        "payment_mean": "John Doe 2222********2222",
        "description": "REF123457",
        "currency": "PLN",
        "amount": 2450,
        "amount_in_pln": 2450
    },
    {
        "customer_id": 1,
        "date": "2021-05-13T09:01:43Z",
        "type": "pay_by_link",
        "payment_mean": "mbank",
        "description": "Abonament na siłownię",
        "currency": "EUR",
        "amount": 3000,
        "amount_in_pln": 13494
    },
    {
        "customer_id": 1,
        "date": "2021-05-14T08:27:09Z",
        "type": "dp",
        "payment_mean": "DE91100000000123456789",
        "description": "FastFood",
        "currency": "USD",
        "amount": 599,
        "amount_in_pln": 2219
    },
    {
        "customer_id": 1,
        "date": "2021-05-14T18:32:26Z",
        "type": "card",
        "payment_mean": "John Doe 1111********1111",
        "description": "REF123456",
        "currency": "GBP",
        "amount": 1000,
        "amount_in_pln": 5208
    }
]


@pytest.mark.parametrize(
    ["currency", "iso_date", "value"],
    [
        ["PLN", "2021-05-13T09:00:05+02:00", 1],
        ["pln", "2023-08-12T01:01:43-09:00", 1],
        ["GBP", "2021-05-14T18:32:26Z", 5.2084],
        ["gBp", "2021-05-14T18:32:26Z", 5.2084],
        ["euR", "2021-05-13T01:01:43-08:00", 4.4981],
        ["uSD", "2021-05-14T08:27:09Z", 3.7055]
    ]
)
def test_get_exchange_rate(currency: str, iso_date: str, value: float):
    # testowanie pobierania kursu waluty z danego dnia
    # wykorzytywana jest przekształcona data do UTC
    assert float(value) == get_exchange_rate(currency, iso_date)


@pytest.mark.parametrize(
    ["created_at", 'date_utc'],
    [
        ["2021-05-14T18:32:26Z", "2021-05-14T18:32:26Z"],
        ["2021-05-13T09:00:05+02:00", "2021-05-13T07:00:05Z"]
    ]
)
def test_get_utc_time(created_at: str, date_utc: str):
    # testowanie przekształcania daty z iso8601 do UTC
    assert date_utc == get_utc_time(created_at, "%Y-%m-%dT%H:%M:%S%z")


def test_pay_by_link_requester():
    # testowanie poprawnego zapytania
    response = client.post("/report", json=report)
    assert response.status_code == 200

    # testowanie poprawnego zapytania zawierajacego id
    response = client.post("/report", json=report_id_test1)
    assert response.status_code == 200


def test_report_pay_id():
    # testowanie poprawnego zapytania
    response = client.post("/customer-report", json=report_id_test1)
    assert response.status_code == 200
    assert response.json() == response_body

    # testowanie niepoprawnego zapytania - id jest str
    response = client.post("/customer-report", json=report_id_test3)
    assert response.status_code == 400

    # testowanie niepoprawnego zapytania - zła waluta
    response = client.post("/customer-report", json=report_invalid_currency)
    assert response.status_code == 400


def test_customer_report_id():
    # testowanie id przypisanego w def test_report_pay_id
    response = client.get("/customer-report/1")
    assert response.status_code == 200
    assert response.json() == response_body

    # testowanie id niewystępującego w bazie
    response2 = client.get("/customer-report/456666666664654564")
    assert response2.status_code == 400

    client.post("/customer-report", json=report_id_test2)
    response3 = client.get("/customer-report/456666666664654564")
    assert response3.status_code == 200

    # testowanie aktualizacji PaymentInfo
    client.post("/customer-report", json=report_id_test2_1)
    response4 = client.get("/customer-report/456666666664654564")
    assert response4 != response3
