import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, Request
from starlette.middleware.cors import CORSMiddleware

from auth.jwt_auth import get_authenticated_user
from tasks.routes import router as tasks_routes
from users.models import UserModel
from users.routes import router as users_routes

tags_metadata = [
    {
        "name": "tasks",
        "description": "here is tasks information.",
    },
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App Start...")
    yield
    print("App Finish...")


app = FastAPI(
    title="ChimichangApp",
    description="description",
    summary="Deadpool's favorite app. Nuff said.",
    version="0.0.1",
    contact={
        "name": "Mohammad Shekari Badi",
        "url": "https://badiDesign.ir/",
        "email": "m.shekari79b5@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "identifier": "MIT",
    },

    lifespan=lifespan,
    openapi_tags=tags_metadata
)
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks_routes, prefix="/api/v1/todo")
app.include_router(users_routes, prefix="/api/v1/user")


@app.get("/public")
def public_route():
    return {"message": "This is a public route."}


@app.get("/private")
def private_route(current_user: UserModel = Depends(get_authenticated_user)):
    return {"message": f"Hello {current_user.username}, this is a private route."}


@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    print("before")
    response = await call_next(request)
    print("next")
    process_time = time.perf_counter() - start_time
    response.headers['X-Process-Time'] = str(process_time)
    return response
