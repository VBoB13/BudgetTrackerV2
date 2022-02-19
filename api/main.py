import uvicorn
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth

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

@app.get("/")
async def read_root():
    return {"Hi": "Babe <3"}



if __name__ == "__main__":
    # Keyword argument [ reload = True ] ONLY IN DEBUGGING
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)