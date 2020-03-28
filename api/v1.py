from fastapi import FastAPI
from api.routers import contacts


def create_api() -> FastAPI:
    api = FastAPI()

    # TODO inject config here
    api.include_router(
        contacts.router, prefix="/v1",
    )

    return api
