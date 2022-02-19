import uvicorn
import sys

from fastapi import FastAPI

from typing import Optional

sys.dont_write_bytecode = True

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hi": "Babe <3"}

if __name__ == "__main__":
    # Keyword argument [ reload = True ] ONLY IN DEBUGGING
    uvicorn.run("backend.app.api:app", host="0.0.0.0", port=8000, reload=True)