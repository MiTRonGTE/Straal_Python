from typing import Optional, List  # Literal
from pydantic import BaseModel, constr, NonNegativeInt, PositiveInt

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