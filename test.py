import pytest

from fastapi.testclient import TestClient
from main import app, get_exchange_rate, get_utc_time

client = TestClient(app)

report = {
    "pay_by_link": [{
            "created_at": "2021-05-13T01:01:43-08:00",
            "currency": "EUR",
            "amount": 3000,
            "description": "Abonament na siłownię",
            "bank": "mbank"
        }],
    "dp": [{
            "created_at": "2021-05-14T08:27:09Z",
            "currency": "USD",
            "amount": 599,
            "description": "FastFood",
            "iban": "DE91100000000123456789"
        }],
    "card": [{
            "created_at": "2021-05-13T09:00:05+02:00",
            "currency": "PLN",
            "amount": 2450,
            "description": "REF123457",
            "cardholder_name": "John",
            "cardholder_surname": "Doe",
            "card_number": "2222222222222222"
        }, {
            "created_at": "2021-05-14T18:32:26Z",
            "currency": "GBP",
            "amount": 1000,
            "description": "REF123456",
            "cardholder_name": "John",
            "cardholder_surname": "Doe",
            "card_number": "1111111111111111"
        }]}
report_invalid_currency = {
    "pay_by_link": [{
            "customer_id": 7887777,
            "created_at": "",
            "currency": "re",
            "amount": 3000,
            "description": "Abonament na siłownię",
            "bank": "mbank"
        }],
    "dp": [{
            "customer_id": 7887777,
            "created_at": "2021-05-14T08:27:09Z",
            "currency": "re",
            "amount": 599,
            "description": "FastFood",
            "iban": "DE91100000000123456789"
        }],
    "card": [{
            "customer_id": 7887777,
            "created_at": "2021-05-13T09:00:05+02:00",
            "currency": "re",
            "amount": 2450,
            "description": "REF123457",
            "cardholder_name": "John",
            "cardholder_surname": "Doe",
            "card_number": "2222222222222222"
        }, {
            "customer_id": 7887777,
            "created_at": "2021-05-14T18:32:26Z",
            "currency": "re",
            "amount": 1000,
            "description": "REF123456",
            "cardholder_name": "John",
            "cardholder_surname": "Doe",
            "card_number": "1111111111111111"
        }]}
report_id_test1 = {
    "pay_by_link": [{
            "customer_id": 7887777,
            "created_at": "2021-05-13T01:01:43-08:00",
            "currency": "EUR",
            "amount": 3000,
            "description": "Abonament na siłownię",
            "bank": "mbank"
        }],
    "dp": [{
            "customer_id": 7887777,
            "created_at": "2021-05-14T08:27:09Z",
            "currency": "USD",
            "amount": 599,
            "description": "FastFood",
            "iban": "DE91100000000123456789"
        }],
    "card": [{
            "customer_id": 7887777,
            "created_at": "2021-05-13T09:00:05+02:00",
            "currency": "PLN",
            "amount": 2450,
            "description": "REF123457",
            "cardholder_name": "John",
            "cardholder_surname": "Doe",
            "card_number": "2222222222222222"
        }, {
            "customer_id": 7887777,
            "created_at": "2021-05-14T18:32:26Z",
            "currency": "GBP",
            "amount": 1000,
            "description": "REF123456",
            "cardholder_name": "John",
            "cardholder_surname": "Doe",
            "card_number": "1111111111111111"
        }]}
report_id_test2 = {
    "pay_by_link": [{
            "customer_id": 456666666664654564,
            "created_at": "2021-05-13T01:01:43-08:00",
            "currency": "EUR",
            "amount": 3000,
            "description": "Abonament na siłownię",
            "bank": "mbank"
        }],
    "dp": [{
            "customer_id": 456666666664654564,
            "created_at": "2021-05-14T08:27:09Z",
            "currency": "USD",
            "amount": 599,
            "description": "FastFood",
            "iban": "DE91100000000123456789"
        }],
    "card": [{
            "customer_id": 456666666664654564,
            "created_at": "2021-05-13T09:00:05+02:00",
            "currency": "PLN",
            "amount": 2450,
            "description": "REF123457",
            "cardholder_name": "John",
            "cardholder_surname": "Doe",
            "card_number": "2222222222222222"
        }, {
            "customer_id": 456666666664654564,
            "created_at": "2021-05-14T18:32:26Z",
            "currency": "GBP",
            "amount": 1000,
            "description": "REF123456",
            "cardholder_name": "John",
            "cardholder_surname": "Doe",
            "card_number": "1111111111111111"
        }]}
report_id_test2_1 = {
    "pay_by_link": [{
            "customer_id": 456666666664654564,
            "created_at": "2021-05-13T01:01:43-08:00",
            "currency": "Gbp",
            "amount": 3000,
            "description": "Abonament na siłownię",
            "bank": "mbank"
        }],
    "dp": [{
            "customer_id": 456666666664654564,
            "created_at": "2021-05-14T08:27:09Z",
            "currency": "Eur",
            "amount": 5939,
            "description": "FastFood",
            "iban": "DE91100000000123456789"
        }],
    "card": [{
            "customer_id": 456666666664654564,
            "created_at": "2021-05-13T09:00:05+02:00",
            "currency": "usd",
            "amount": 24510,
            "description": "REF123457",
            "cardholder_name": "John",
            "cardholder_surname": "Doe",
            "card_number": "2222222222222222"
        }, {
            "customer_id": 456666666664654564,
            "created_at": "2021-05-14T18:32:26Z",
            "currency": "GBP",
            "amount": 10001,
            "description": "REF123456",
            "cardholder_name": "John",
            "cardholder_surname": "Doe",
            "card_number": "1111111111111111"
        }]}
report_id_test3 = {
    "pay_by_link": [{
            "customer_id": "string",
            "created_at": "2021-05-13T01:01:43-08:00",
            "currency": "EUR",
            "amount": 3000,
            "description": "Abonament na siłownię",
            "bank": "mbank"
        }],
    "dp": [{
            "customer_id": "string",
            "created_at": "2021-05-14T08:27:09Z",
            "currency": "USD",
            "amount": 599,
            "description": "FastFood",
            "iban": "DE91100000000123456789"
        }],
    "card": [{
            "customer_id": "string",
            "created_at": "2021-05-13T09:00:05+02:00",
            "currency": "PLN",
            "amount": 2450,
            "description": "REF123457",
            "cardholder_name": "John",
            "cardholder_surname": "Doe",
            "card_number": "2222222222222222"
        }, {
            "customer_id": "string",
            "created_at": "2021-05-14T18:32:26Z",
            "currency": "GBP",
            "amount": 1000,
            "description": "REF123456",
            "cardholder_name": "John",
            "cardholder_surname": "Doe",
            "card_number": "1111111111111111"
        }]}
response_body = [{
        "customer_id": 7887777,
        "date": "2021-05-13T07:00:05Z",
        "type": "card",
        "payment_mean": "John Doe 2222********2222",
        "description": "REF123457",
        "currency": "PLN",
        "amount": 2450,
        "amount_in_pln": 2450
    }, {
        "customer_id": 7887777,
        "date": "2021-05-13T09:01:43Z",
        "type": "pay_by_link",
        "payment_mean": "mbank",
        "description": "Abonament na siłownię",
        "currency": "EUR",
        "amount": 3000,
        "amount_in_pln": 13494
    }, {
        "customer_id": 7887777,
        "date": "2021-05-14T08:27:09Z",
        "type": "dp",
        "payment_mean": "DE91100000000123456789",
        "description": "FastFood",
        "currency": "USD",
        "amount": 599,
        "amount_in_pln": 2219
    }, {
        "customer_id": 7887777,
        "date": "2021-05-14T18:32:26Z",
        "type": "card",
        "payment_mean": "John Doe 1111********1111",
        "description": "REF123456",
        "currency": "GBP",
        "amount": 1000,
        "amount_in_pln": 5208
    }]
report_pbl0 = {
    "pay_by_link": [{
            "customer_id": 9999999999,
            "created_at": "2021-05-13T01:01:43-08:00",
            "currency": "EUR",
            "amount": 3000,
            "description": "Abonament na siłownię",
            "bank": "mbank"
        }]}
report_pbl1 = {
    "pay_by_link": [{
            "customer_id": "string",
            "created_at": "2021-05-13T01:01:43-08:00",
            "currency": "EUR",
            "amount": 3000,
            "description": "Abonament na siłownię",
            "bank": "mbank"
        }]}
report_pbl2 = {
    "pay_by_link": [{
            "customer_id": 9999999999,
            "created_at": "2021-05-13T",
            "currency": "EUR",
            "amount": 3000,
            "description": "Abonament na siłownię",
            "bank": "mbank"
        }]}
report_pbl3 = {
    "pay_by_link": [{
            "customer_id": 9999999999,
            "created_at": "2021-05-13T01:01:43-08:00",
            "currency": "string",
            "amount": 3000,
            "description": "Abonament na siłownię",
            "bank": "mbank"
        }]}
report_pbl4 = {
    "pay_by_link": [{
            "customer_id": 9999999999,
            "created_at": "2021-05-13T01:01:43-08:00",
            "currency": "EUR",
            "amount": "3000",
            "description": "Abonament na siłownię",
            "bank": "mbank"
        }]}
report_pbl5 = {
    "pay_by_link": [{
            "customer_id": 9999999999,
            "created_at": "2021-05-13T01:01:43-08:00",
            "currency": "EUR",
            "amount": "string",
            "description": "Abonament na siłownię",
            "bank": "mbank"
        }]}
report_pbl6 = {
    "pay_by_link": [{
            "customer_id": 9999999999,
            "created_at": "2021-05-13T01:01:43-08:00",
            "currency": "EUR",
            "amount": 3000,
            "description": None,
            "bank": "mbank"
        }]}
report_pbl7 = {
    "pay_by_link": [{
            "customer_id": 9999999999,
            "created_at": "2021-05-13T01:01:43-08:00",
            "currency": "EUR",
            "amount": 3000,
            "description": "Abonament na siłownię",
            "bank": None
        }]}
response_pbl1 = [{
        "date": "2021-05-13T09:01:43Z",
        "type": "pay_by_link",
        "payment_mean": "mbank",
        "description": "Abonament na siłownię",
        "currency": "EUR",
        "amount": 3000,
        "amount_in_pln": 13494
    }]
report_dp0 = {
    "dp": [{
        "customer_id": 9999999999,
        "created_at": "2021-05-14T08:27:09Z",
        "currency": "USD",
        "amount": 599,
        "description": "FastFood",
        "iban": "DE91100000000123456789"
    }]}
report_dp1 = {
    "dp": [{
        "customer_id": "string",
        "created_at": "2021-05-14T08:27:09Z",
        "currency": "USD",
        "amount": 599,
        "description": "FastFood",
        "iban": "DE91100000000123456789"
    }]}
report_dp2 = {
    "dp": [{
        "customer_id": 9999999999,
        "created_at": "2021-05-14T",
        "currency": "USD",
        "amount": 599,
        "description": "FastFood",
        "iban": "DE91100000000123456789"
    }]}
report_dp3 = {
    "dp": [{
        "customer_id": 9999999999,
        "created_at": "2021-05-14T08:27:09Z",
        "currency": "string",
        "amount": 599,
        "description": "FastFood",
        "iban": "DE91100000000123456789"
    }]}
report_dp4 = {
    "dp": [{
        "customer_id": 9999999999,
        "created_at": "2021-05-14T08:27:09Z",
        "currency": "USD",
        "amount": "599",
        "description": "FastFood",
        "iban": "DE91100000000123456789"
    }]}
report_dp5 = {
    "dp": [{
        "customer_id": 9999999999,
        "created_at": "2021-05-14T08:27:09Z",
        "currency": "USD",
        "amount": "string",
        "description": "FastFood",
        "iban": "DE91100000000123456789"
    }]}
report_dp6 = {
    "dp": [{
        "customer_id": 9999999999,
        "created_at": "2021-05-14T08:27:09Z",
        "currency": "USD",
        "amount": 599,
        "description": None,
        "iban": "DE91100000000123456789"
    }]}
report_dp7 = {
    "dp": [{
        "customer_id": 9999999999,
        "created_at": "2021-05-14T08:27:09Z",
        "currency": "USD",
        "amount": 599,
        "description": "FastFood",
        "iban": None
    }]}
response_dp1 = [{
        "date": "2021-05-14T08:27:09Z",
        "type": "dp",
        "payment_mean": "DE91100000000123456789",
        "description": "FastFood",
        "currency": "USD",
        "amount": 599,
        "amount_in_pln": 2219
    }]
report_card0 = {
    "card": [{
        "customer_id": 9999999999,
        "created_at": "2021-05-13T09:00:05+02:00",
        "currency": "PLN",
        "amount": 2450,
        "description": "REF123457",
        "cardholder_name": "John",
        "cardholder_surname": "Doe",
        "card_number": "2222222222222222"
    }]}
report_card1 = {
    "card": [{
        "customer_id": 9999999999,
        "created_at": "2021-05-13T",
        "currency": "PLN",
        "amount": 2450,
        "description": "REF123457",
        "cardholder_name": "Johną",
        "cardholder_surname": "Doe",
        "card_number": "2222222222222222"
    }]}
report_card2 = {
    "card": [{
        "customer_id": "string",
        "created_at": "2021-05-13T09:00:05+02:00",
        "currency": "PLN",
        "amount": 2450,
        "description": "REF123457",
        "cardholder_name": "John",
        "cardholder_surname": "Doe",
        "card_number": "2222222222222222"
    }]}
report_card3 = {
    "card": [{
        "customer_id": 9999999999,
        "created_at": "2021-05-13T09:00:05+02:00",
        "currency": "string",
        "amount": 2450,
        "description": "REF123457",
        "cardholder_name": "John",
        "cardholder_surname": "Doe",
        "card_number": "2222222222222222"
    }]}
report_card4 = {
    "card": [{
        "customer_id": 9999999999,
        "created_at": "2021-05-13T09:00:05+02:00",
        "currency": "PLN",
        "amount": "2450",
        "description": "REF123457",
        "cardholder_name": "John",
        "cardholder_surname": "Doe",
        "card_number": "2222222222222222"
    }]}
report_card5 = {
    "card": [{
        "customer_id": 9999999999,
        "created_at": "2021-05-13T09:00:05+02:00",
        "currency": "PLN",
        "amount": 2450,
        "description": None,
        "cardholder_name": "John",
        "cardholder_surname": "Doe",
        "card_number": "2222222222222222"
    }]}
report_card6 = {
    "card": [{
        "customer_id": 9999999999,
        "created_at": "2021-05-13T09:00:05+02:00",
        "currency": "PLN",
        "amount": 2450,
        "description": "REF123457",
        "cardholder_name": None,
        "cardholder_surname": "Doe",
        "card_number": "2222222222222222"
    }]}
report_card7 = {
    "card": [{
        "customer_id": 9999999999,
        "created_at": "2021-05-13T09:00:05+02:00",
        "currency": "PLN",
        "amount": 2450,
        "description": "REF123457",
        "cardholder_name": "John",
        "cardholder_surname": None,
        "card_number": "2222222222222222"
    }]}
report_card8 = {
    "card": [{
        "customer_id": 9999999999,
        "created_at": "2021-05-13T09:00:05+02:00",
        "currency": "PLN",
        "amount": 2450,
        "description": "REF123457",
        "cardholder_name": "John",
        "cardholder_surname": "Doe",
        "card_number": "2"
    }]}
report_card9 = {
    "card": [{
        "customer_id": 9999999999,
        "created_at": "2021-05-13T09:00:05+02:00",
        "currency": "PLN",
        "amount": 2450,
        "description": "REF123457",
        "cardholder_name": "John",
        "cardholder_surname": "Doe",
        "card_number": "22string222222"
    }]}
report_card10 = {
    "card": [{
        "customer_id": 9999999999,
        "created_at": "2021-05-13T09:00:05+02:00",
        "currency": "PLN",
        "amount": 2450,
        "description": "REF123457",
        "cardholder_name": "John",
        "cardholder_surname": "Doe",
        "card_number": None
    }]}
response_card1 = [{
        "date": "2021-05-13T07:00:05Z",
        "type": "card",
        "payment_mean": "John Doe 2222********2222",
        "description": "REF123457",
        "currency": "PLN",
        "amount": 2450,
        "amount_in_pln": 2450
  }]


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
    # testowanie pobierania kursu waluty z danej datu w formacie UTC
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


@pytest.mark.parametrize(
    ["report_test", 'value'],
    [
        [report_pbl0, 200],  # prawidłowy
        [report_pbl1, 400],  # błędny id
        [report_pbl2, 400],  # błędny created_at (data)
        [report_pbl3, 400],  # błędny currency (waluta)
        [report_pbl4, 200],  # poprawny amount (kwota), można przekonwetować str do in
        [report_pbl5, 400],  # błędny amount (kwota), nie można przekonwetować str do in
        [report_pbl6, 400],  # błędne description
        [report_pbl7, 400],  # błędny bank
        [report_dp0, 200],  # prawidłowy
        [report_dp1, 400],  # błędny id
        [report_dp2, 400],  # błędny created_at (data)
        [report_dp3, 400],  # błędny currency (waluta)
        [report_dp4, 200],  # poprawny amount (kwota), można przekonwetować str do in
        [report_dp5, 400],  # błędny amount (kwota), nie można przekonwetować str do in
        [report_dp6, 400],  # błędne description
        [report_dp7, 400],  # błędny iban
        [report_card0, 200],  # prawidłowy
        [report_card1, 400],  # błędny id
        [report_card2, 400],  # błędny created_at (data)
        [report_card3, 400],  # błędny currency (waluta)
        [report_card4, 200],  # poprawny amount (kwota), można przekonwetować str do in
        [report_card5, 400],  # błędny amount (kwota), nie można przekonwetować str do in
        [report_card6, 400],  # błędne description
        [report_card7, 400],  # błędny cardholder_name
        [report_card8, 400],  # błędny cardholder_surname
        [report_card9, 400],  # błędny card_number
        [report_card10, 400]  # błędny card_number
    ]
)
def test_pay_by_link_requester(report_test, value):
    response = client.post("/report", json=report_test)
    assert response.status_code == value

    # testowanie poprawnego zapytania
    response = client.post("/report", json=report)
    assert response.status_code == 200

    # testowanie poprawnego zapytania zawierajacego id
    response = client.post("/report", json=report_id_test1)
    assert response.status_code == 200

    response = client.post("/report", json=report_pbl0)
    assert response.status_code == 200 and response.json() == response_pbl1

    response = client.post("/report", json=report_dp0)
    assert response.status_code == 200 and response.json() == response_dp1

    response = client.post("/report", json=report_card0)
    assert response.status_code == 200 and response.json() == response_card1


@pytest.mark.parametrize(
    ["report_test", 'value'],
    [
        [report_pbl0, 200],  # prawidłowy
        [report_pbl1, 400],  # błędny id
        [report_pbl2, 400],  # błędny created_at (data)
        [report_pbl3, 400],  # błędny currency (waluta)
        [report_pbl4, 200],  # poprawny amount (kwota), można przekonwetować str do in
        [report_pbl5, 400],  # błędny amount (kwota), nie można przekonwetować str do in
        [report_pbl6, 400],  # błędne description
        [report_pbl7, 400],  # błędny bank
        [report_dp0, 200],  # prawidłowy
        [report_dp1, 400],  # błędny id
        [report_dp2, 400],  # błędny created_at (data)
        [report_dp3, 400],  # błędny currency (waluta)
        [report_dp4, 200],  # poprawny amount (kwota), można przekonwetować str do in
        [report_dp5, 400],  # błędny amount (kwota), nie można przekonwetować str do in
        [report_dp6, 400],  # błędne description
        [report_dp7, 400],  # błędny iban
        [report_card0, 200],  # prawidłowy
        [report_card1, 400],  # błędny id
        [report_card2, 400],  # błędny created_at (data)
        [report_card3, 400],  # błędny currency (waluta)
        [report_card4, 200],  # poprawny amount (kwota), można przekonwetować str do in
        [report_card5, 400],  # błędny amount (kwota), nie można przekonwetować str do in
        [report_card6, 400],  # błędne description
        [report_card7, 400],  # błędny cardholder_name
        [report_card8, 400],  # błędny cardholder_surname
        [report_card9, 400],  # błędny card_number
        [report_card10, 400]  # błędny card_number
    ]
)
def test_report_pay_id(report_test, value):
    # testowanie pojednyczych wariantów
    response = client.post("/report", json=report_test)
    assert response.status_code == value

    # testowanie poprawnego zapytania
    response = client.post("/customer-report", json=report_id_test1)
    assert response.status_code == 200
    assert response.json() == response_body

    # testowanie błędnego zapytania - id jest str
    response = client.post("/customer-report", json=report_id_test3)
    assert response.status_code == 400

    # testowanie błędnego zapytania - zła waluta
    response = client.post("/customer-report", json=report_invalid_currency)
    assert response.status_code == 400


def test_customer_report_id():
    # testowanie id przypisanego w def test_report_pay_id
    response = client.get("/customer-report/7887777")
    assert response.status_code == 200
    assert response.json() == response_body

    # testowanie id niewystępującego w bazie
    response = client.get("/customer-report/456666666664654564")
    assert response.status_code == 400

    client.post("/customer-report", json=report_id_test2)
    response3 = client.get("/customer-report/456666666664654564")
    assert response3.status_code == 200

    # testowanie aktualizacji PaymentInfo
    client.post("/customer-report", json=report_id_test2_1)
    response4 = client.get("/customer-report/456666666664654564")
    assert response4 != response3
