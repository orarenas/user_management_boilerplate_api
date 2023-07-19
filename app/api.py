from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from app.models import ErrorModel

from app.user.views import user_router
from app.access_control.views import access_control_router
from app.auth.views import auth_router

api_router = APIRouter(default_response_class=ORJSONResponse)

api_router.include_router(
    user_router,
    prefix="/users",
    tags=["users"],
    responses={401: {"model": ErrorModel}, 403: {"model":ErrorModel}}
)

api_router.include_router(
    access_control_router,
    prefix="/access-control",
    tags=["access-control"],
    responses={401: {"model": ErrorModel}, 403: {"model": ErrorModel}}
)

api_router.include_router(
    auth_router,
    prefix="",
    tags=["login"],
    responses={401: {"model": ErrorModel}, 403: {"model": ErrorModel}}
)