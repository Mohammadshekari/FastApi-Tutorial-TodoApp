from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App Start...")
    yield
    print("App Finish...")


app = FastAPI(lifespan=lifespan)
