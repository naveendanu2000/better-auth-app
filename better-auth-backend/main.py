from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting app!")

    yield
    print("Closing app!")


app = FastAPI(lifespan=lifespan)


@app.get("/")
def home():
    return "Welcome to better auth implementation project"


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000)
