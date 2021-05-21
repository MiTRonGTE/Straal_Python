## Description 

This application is simple http service that prepares report of client's transactions based on given data.

## Functionality

* The application accepts a set of payment data from the customer. 
* The data will be converted and returned. 
* The report will be sorted by date.
* Data can be transferred to the customer ID. 
* You can get the latest report with the customer ID.

## Used technologies
* Python 3.8
* fastapi
* uvicorn
* pytest

## Run app

Download source and requiremets.txt and in the terminal type in the root directory:

* basic

`uvicorn main:app`

* auto-reload:

`uvicorn main:app --reload`

* port

http://127.0.0.1:8000/

* docs

http://127.0.0.1:8000/docs

## Cloud

Api is available on heroku cloud:

https://recruitment-task-straal.herokuapp.com/

API docs:

https://recruitment-task-straal.herokuapp.com/docs

## Pytest

* to run all tests type in terminal:  

`pytest test.py`

## Endpoints

- /report
- /customer-report
- /customer-report/[customer_id]

### Input

```python
{
  pay_by_link: [{
    "customer_id": Optional[PositiveInt],
    "created_at": string(date-time),
    "currency": string,
    "amount": NonNegativeInt,
    "description": string,
    "bank": string,
  }],
  dp: [{
    "customer_id": Optional[PositiveInt],
    "created_at": string(date-time),
    "currency": string,
    "amount": NonNegativeInt,
    "description": string,
    "iban": constr(max_length=22, min_length=22),
  }],
    card: [{
    "customer_id": Optional[PositiveInt],
    "created_at": string(date-time),
    "currency": string,
    "amount": NonNegativeInt,
    "description": string,
    "cardholder_name": string,
    "cardholder_surname": string,
    "card_number": constr(max_length=16, min_length=16),
  }]
  }
```

### Output

```python
[
  {
    "customer_id": Optional[PositiveInt],
    "date": string(date-time),
    "type": pay_by_link,
    "payment_mean": string,
    "description": string,
    "currency": string,  # [“EUR”,”USD”, “GBP”, “PLN”]
    "amount": int,
    "amount_in_pln": int,
  },
  {
    "customer_id": Optional[PositiveInt],
    "date": string(date-time),
    "type": dp,
    "payment_mean": string,
    "description": string,
    "currency": string,  # [“EUR”,”USD”, “GBP”, “PLN”]
    "amount": int,
    "amount_in_pln": int,
  },
  {
    "customer_id": Optional[PositiveInt],
    "date": string(date-time),
    "type": card,
    "payment_mean": ‘cardholder_name cardholder_surname masked_card_number’ e.g ‘Jan Nowak 1111********1111’,
    "description": string,
    "currency": string,  # [“EUR”,”USD”, “GBP”, “PLN”]
    "amount": int,
    "amount_in_pln": int,
  }
 ]
    
