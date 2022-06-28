from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
import logging
import uvicorn
import sys

from .routers import auth, categories, stores, transactions, subscriptions, stats, incomes

sys.dont_write_bytecode = True

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
    logging.error(f"{request}: {exc_str}")
    content = {'status_code': 10422, 'message': exc_str, 'data': None}
    return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


origins = [
    "http://localhost:3000",
    "localhost:3000",
    "127.0.0.1:3000",
    "192.168.1.110:3000",
    "192.168.1.105:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(incomes.router)
app.include_router(stats.router)
app.include_router(stores.router)
app.include_router(subscriptions.router)
app.include_router(transactions.router)


@app.get("/")
async def read_root():
    return {"Hi Babe!": "I wuuuve you <3"}


if __name__ == "__main__":
    # Keyword argument [ reload = True ] ONLY IN DEBUGGING
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
