from fastapi import FastAPI
from api import payments

app = FastAPI()

app.include_router(payments.router)