#!/usr/bin/env python3

# from sqlalchemy import Decla
from typing import List
import sqlalchemy
from sqlalchemy.orm import Session

from receipt_tracking.models import (
    Base,
    Customer,
    DBCustomer,
    CustomerID,
    DBGood,
    DBReceipt,
    Good,
    Receipt,
)

# === Helper; convert to DB classes ===========


def customer_to_db_customer(customer: Customer) -> DBCustomer:
    return DBCustomer(name=customer.name)


def db_customer_to_customer(db_customer: DBCustomer) -> Customer:
    return Customer(name=db_customer.name)


def good_to_db_good(good: Good) -> DBGood:
    return DBGood(name=good.name)


def db_good_to_good(db_good: DBGood) -> Good:
    return Good(name=db_good.name)


def receipt_to_db_receipt(receipt: Receipt) -> DBReceipt:
    return DBReceipt(
        customer_id=receipt.customer_id,
        good_id=receipt.good_id,
        time_purchased=receipt.time_purchased,
    )


def db_receipt_to_receipt(db_receipt: DBReceipt) -> Receipt:
    return Receipt(
        customer_id=db_receipt.customer_id,
        good_id=db_receipt.good_id,
        time_purchased=db_receipt.time_pruchased,
    )


# === Public API ========================


def init_database(database_string: str) -> sqlalchemy.Engine:
    engine = sqlalchemy.create_engine(database_string, echo=True)
    Base.metadata.create_all(engine)
    return engine


# --- Get ------


def get_customers(engine: sqlalchemy.Engine) -> List[Customer]:
    with Session(engine) as session:
        db_customers = session.query(DBCustomer).all()
        customers = [db_customer_to_customer(c) for c in db_customers]
    return customers


def get_goods(engine: sqlalchemy.Engine) -> List[Good]:
    with Session(engine) as session:
        db_goods = session.query(DBGood).all()
        goods = [db_good_to_good(g) for g in db_goods]
    return goods


def get_recipts_for_customer(
    engine: sqlalchemy.Engine, customerId: CustomerID
) -> List[Receipt]:
    results = []
    with Session(engine) as session:
        stmt = sqlalchemy.select(DBReceipt).where(
            DBReceipt.customer_id == customerId.id
        )

        for db_receipt in session.scalars(stmt):
            results += [db_receipt_to_receipt(db_receipt)]

    return results


# --- Create ------


def create_customer(engine: sqlalchemy.Engine, customer: Customer) -> bool:
    with Session(engine) as session:
        session.add(customer_to_db_customer(customer=customer))
        session.commit()
    return True


def create_good(engine: sqlalchemy.Engine, good: Good) -> bool:
    with Session(engine) as session:
        session.add(good_to_db_good(good=good))
        session.commit()
    return True
