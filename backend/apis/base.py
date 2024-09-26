from fastapi import APIRouter

from apis.v1 import route_runescape_config, route_runescape_catalogue

api_router = APIRouter()
api_router.include_router(route_runescape_config.router,
                          prefix="",
                          tags=["runescape api config"])
api_router.include_router(route_runescape_catalogue.router,
                          prefix="",
                          tags=["runescape api catalogue"])
