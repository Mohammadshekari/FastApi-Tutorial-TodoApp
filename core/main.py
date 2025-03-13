import datetime
import time
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI, Depends, Request, status, BackgroundTasks
from fastapi.exceptions import RequestValidationError
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from fastapi_cache.decorator import cache
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from auth.jwt_auth import get_authenticated_user
from core.config import settings
from core.email_utils import send_email
from tasks.routes import router as tasks_routes
from users.models import UserModel
from users.routes import router as users_routes

scheduler = AsyncIOScheduler()

tags_metadata = [
    {
        "name": "tasks",
        "description": "here is tasks information.",
    },
]


def my_task():
    print('Task Executed at ', datetime.datetime.now().isoformat())


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App Start...")
    scheduler.add_job(my_task, IntervalTrigger(seconds=10))
    scheduler.start()
    yield
    scheduler.shutdown()
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


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    error_message = {
        'ok': False,
        'status_code': exc.status_code,
        'detail': str(exc.detail)
    }
    return JSONResponse(status_code=exc.status_code, content=error_message)


@app.exception_handler(RequestValidationError)
async def http_validation_exception_handler(request, exc):
    error_message = {
        'ok': False,
        'status_code': status.HTTP_422_UNPROCESSABLE_ENTITY,
        'detail': 'invalid form data',
        'content': exc.errors(),
    }
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=error_message)


import random

task_counter = 1


def do_task(task_id):
    print("Start Task #", task_id)
    time.sleep(random.randint(3, 10))
    print("Task Done #", task_id)


@app.get("/init_task")
def init_task(background_tasks: BackgroundTasks):
    global task_counter
    task_counter += 1
    background_tasks.add_task(do_task, task_id=task_counter)
    return {"message": f"Task Done"}


redis = aioredis.from_url(settings.REDIS_URL)
cache_backend = RedisBackend(redis)
FastAPICache.init(cache_backend, prefix="fastapi-cache")


@app.get("/cache_last_datetime_with_decorator")
@cache(expire=10)
def cache_last_datetime_with_decorator():
    time.sleep(3)
    return {"last_action": datetime.datetime.now().isoformat()}


@app.get("/cache_last_datetime_without_decorator")
async def cache_last_datetime_without_decorator():
    cache_key = 'last_datetime'
    cache_data = await cache_backend.get(cache_key)
    if cache_data:
        return {"last_action": cache_data}
    else:
        time.sleep(3)
        current_datetime = datetime.datetime.now().isoformat()
        await cache_backend.set(cache_key, current_datetime.encode('utf-8'), 10)
        return {"last_action": current_datetime}


# Endpoint to send email
@app.get("/test-send-mail", status_code=200)
async def test_send_mail():
    await send_email(
        subject="Test Email from FastAPI",
        recipients=["recipient@example.com"],
        body="This is a test email sent using the email_util function."
    )
    return JSONResponse(content={"detail": "Email has been sent"})
