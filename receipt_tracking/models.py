#!/usr/bin/env python3

import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey


# ===== Models for API ===============
class Customer(BaseModel):
    name: str


class Good(BaseModel):
    name: str


class Receipt(BaseModel):
    customer_id: int
    good_id: int
    time_purchased: datetime.datetime


class CustomerID(BaseModel):
    id: int


# ===== Models for Database
class Base(DeclarativeBase):
    pass


class DBCustomer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]


class DBGood(Base):
    __tablename__ = "goods"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]


class DBReceipt(Base):
    __tablename__ = "receipts"

    id: Mapped[int] = mapped_column(primary_key=True)

    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    # buyer TODO ?
    good_id: Mapped[int] = mapped_column(ForeignKey("goods.id"))
    # good TODO ?
    time_pruchased: Mapped[datetime.datetime]
