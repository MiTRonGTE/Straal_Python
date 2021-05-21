# descriptions 

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

'http://127.0.0.1:8000/'

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

### Input

```python
{
  pay_by_link: [{
    "customer_id": Optional[PositiveInt],
    "created_at": string(date-time)
    "currenc"y: string
    "amount": NonNegativeInt
    "description": string
    "bank": string
  }],
  dp: [{
    "customer_id": Optional[PositiveInt],
    "created_at": string(date-time)
    "currency": string
    "amount": NonNegativeInt
    "description": string
    "iban": constr(max_length=22, min_length=22)
  }],
    card: [{
    "customer_id": Optional[PositiveInt],
    "created_at": string(date-time)
    ""currency": string
    "amount": NonNegativeInt
    "description": string
    "cardholder_name": string
    "cardholder_surname"": string
    "card_number": constr(max_length=16, min_length=16)
  }]
  }
```

### Output

```python
[
  {
    "customer_id": Optional[PositiveInt],
    "date": string(date-time)
    "type": card
    "payment_mean": ‘cardholder_name cardholder_surname masked_card_number’ e.g ‘Jan Nowak 1111********1111’
    "description": string
    "currency": string  # [“EUR”,”USD”, “GBP”, “PLN”]
    "amount": int
    "amount_in_pl"n: int
  },
  {
    "customer_id": Optional[PositiveInt],
    "date": string(date-time)
    "type": pay_by_link
    "payment_mean": string
    "description": string
    "currency": string  # [“EUR”,”USD”, “GBP”, “PLN”]
    "amount": int
    "amount_in_pln": int
  },
  {
    "customer_id": Optional[PositiveInt],
    "date": string(date-time)
    "type": dp
    "payment_mean": string
    "description": string
    "currency": string  # [“EUR”,”USD”, “GBP”, “PLN”]
    "amount": int
    "amount_in_pln": int
  }
]
'''
