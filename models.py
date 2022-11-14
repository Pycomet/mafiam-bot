from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase

from datetime import date


@dataclass
class User:
    "User Class Repr"
    id: int = 0
    language: str = "ja"


# To camel case in Json for exports
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Account:
    "Account Model For Registering Users"
    nickname: str
    user_id: int
    sex: str = ""
    lang: str = "en"
    secret_question: str = ""
    secret_answer: str = ""
    account_type: str = ""
    code: str = ""
    active: bool = False


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Referral:
    "Referral Model To Database"
    user_id: int
    ref_code: str
    ref_user_id: int
    status: str = "A"


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Room:
    "Room Criteria Model In Database"
    owner_id: int
    group_id: int
    name: str
    display_image: str = ""
    description: str = ""
    access_code: str = ""


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ProductItem:
    "Product Items Identifiable to Their Respective Rooms"

    room_id: int
    item_id: str
    cost: int = 0
    discount: int = 0
    quantity_available: int = 0
    created_date: str = ""
