from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from src.controllers.authController import router as AuthRouter
from src.connection.pool import create_pool, close_pool
from src.responses.register_exception_handler import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting app!")
    try:
        print("Connecting to DB!")
        await create_pool(app=app)
    except Exception as e:
        print(f"unable to connect to DB! {e}")

    try:
        yield
        print("Closing app!")
        try:
            print("Disconnecting from DB!")
            await close_pool(app=app)
        except Exception as e:
            print(f"Unable to disconnect from DB!{e}")
    except Exception as e:
        print(f"Unable to close app!{e}")


app = FastAPI(lifespan=lifespan)

register_exception_handlers(app=app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(AuthRouter)


@app.get("/")
def home():
    return "Welcome to better auth implementation project"


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000)
