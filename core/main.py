from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends

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

app.include_router(tasks_routes, prefix="/api/v1/todo")
app.include_router(users_routes, prefix="/api/v1/user")


@app.get("/public")
def public_route():
    return {"message": "This is a public route."}


@app.get("/private")
def private_route(current_user: UserModel = Depends(get_authenticated_user)):
    return {"message": f"Hello {current_user.username}, this is a private route."}
