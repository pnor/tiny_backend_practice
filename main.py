#!/usr/bin/env python3

from typing import List
from fastapi import FastAPI, HTTPException
from sqlalchemy import Engine
import sqlalchemy
from receipt_tracking.models import *
import receipt_tracking.database
import pdb

app = FastAPI()


class GlobalState:
    engine: Engine

    def __init__(self):
        self.engine = sqlalchemy.create_engine("sqlite://", echo=True)
        Base.metadata.create_all(self.engine)


# Datbase prep
state = GlobalState()
# db_engine = receipt_tracking.database.init_database("sqlite://")


@app.get("/")
def read_root():
    return {"hi": "world"}


# DONE [get] Get customer info
@app.get("/customers")
def get_customers() -> List[Customer]:
    return receipt_tracking.database.get_customers(state.engine)


# DONE [get] Get good info
@app.get("/goods")
def get_goods() -> List[Good]:
    return receipt_tracking.database.get_goods(state.engine)


# DONE [get] Get receipt trail for customer (all things customer bought)
@app.get("/receipt")
def get_receipts(customer_id: CustomerID) -> List[Receipt]:
    return receipt_tracking.database.get_recipts_for_customer(
        db_engine, customerId=customer_id
    )


# DONE [post] Create a customer
@app.post("/create_customer", status_code=201)
def create_customer(customer: Customer):
    result = receipt_tracking.database.create_customer(db_engine, customer=customer)
    if result:
        return {"success": True}
    else:
        raise HTTPException(status_code=400, detail="Unable to create customer")


# DONE [post] Create a Good
@app.post("/create_good", status_code=201)
def create_good(good: Good):
    result = receipt_tracking.database.create_good(db_engine, good=good)
    if result:
        return {"success": True}
    else:
        raise HTTPException(status_code=400, detail="Unable to create good")


# TODO [post] Say a customer bought a good
