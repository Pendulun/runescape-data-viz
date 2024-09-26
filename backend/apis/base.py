from fastapi import APIRouter

from apis.v1 import route_runescape

api_router = APIRouter()
api_router.include_router(route_runescape.router, prefix="", tags=["runescape"])