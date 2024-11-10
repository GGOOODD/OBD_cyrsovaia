from fastapi import APIRouter

from api.auth import router as auth_router
from api.classifier import router as classifier_router

router = APIRouter(prefix="/api")

router.include_router(auth_router)
router.include_router(classifier_router)
