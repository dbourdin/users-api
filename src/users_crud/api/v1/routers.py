"""File that joins all the defined routers to be imported by the main API file."""

from fastapi import APIRouter

from users_crud.api.v1.endpoints import auth, users

router = APIRouter()
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(auth.router, prefix="/auth", tags=["auth"])
