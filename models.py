from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

from db import Base


class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True)
    email = Column(String(255), unique=True)
    password = Column(Text, nullable=True)
    is_active = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)

    order = relationship('Order', back_populates='user')  # back = esme tablename

    def __str__(self):
        return f'User {self.username}'


class Order(Base):

    ORDER_STATUS = [
        ('PENDING', 'pending'),
        ('IN-TRANSIT', 'in-transit'),
        ('DELIVERED', 'delivered')
    ]
    PIZZA_SIZE = [
        ('SMALL', 'small'),
        ('MEDIUM', 'medium'),
        ('LARGE', 'large'),
        ('EXTRA-LARGE', 'extra-large')
    ]

    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=True)
    order_status = Column(ChoiceType(ORDER_STATUS), default='PENDING')
    pizza_size = Column(ChoiceType(PIZZA_SIZE), default='MEDIUM')
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship('User', back_populates='order')  # khode motaghayer ham byd esme class bashe

    def __repr__(self):
        return f'Order {self.id}'
