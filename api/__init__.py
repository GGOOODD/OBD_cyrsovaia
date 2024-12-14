from fastapi import APIRouter

from api.auth import router as auth_router
from api.classifier import router as classifier_router
from api.flight import router as flight_router
from api.user import router as user_router

router = APIRouter(prefix="/api")

router.include_router(auth_router)
router.include_router(classifier_router)
router.include_router(flight_router)
router.include_router(user_router)
