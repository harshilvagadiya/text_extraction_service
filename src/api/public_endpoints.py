import fastapi
from fastapi import APIRouter, Depends

from src.api.routes.authentication import router as authentication_router
from src.api.routes.text_extraction import router as text_extraction_router

router = fastapi.APIRouter()

router.include_router(authentication_router)
router.include_router(text_extraction_router)
