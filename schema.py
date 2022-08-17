from pydantic import BaseModel
from typing import Optional


class SignUp(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    is_active: Optional[bool]
    is_staff: Optional[bool]

    class Config:
        orm_mode = True


class Login(BaseModel):

    username: str
    password: str


class Settings(BaseModel):

    authjwt_secret_key: str = 'b9d37cc61d555db4cf0ba57cecf31bc59a2d237359455a56ce3268c3e8aaabe7'


class OrderModel(BaseModel):

    id: Optional[int]
    quantity: int = 0
    order_status: Optional[str] = 'PENDING'
    pizza_size: Optional[str] = 'MEDIUM'
    user_id: Optional[int]

    class Config:
        orm_mode = True


class OrderStatus(BaseModel):

    order_status: Optional[str] = 'PENDING'

    class Config:
        orm_mode = True
        schema_extra = {
            "example":
                {
                    'order_status': 'PENDING'
                }
        }
