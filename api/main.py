import uvicorn
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, categories, stores, transactions, subscriptions, stats

sys.dont_write_bytecode = True

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
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
app.include_router(stores.router)
app.include_router(transactions.router)
app.include_router(subscriptions.router)
app.include_router(stats.router)


@app.get("/")
async def read_root():
    return {"Hi Babe!": "I wuuuve you <3"}


if __name__ == "__main__":
    # Keyword argument [ reload = True ] ONLY IN DEBUGGING
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
