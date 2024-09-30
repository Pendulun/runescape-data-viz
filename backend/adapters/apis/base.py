from fastapi import APIRouter

from adapters.apis.v1 import route_runescape_config, route_runescape_catalogue
from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory="templates")
api_router = APIRouter()
api_router.include_router(route_runescape_config.router,
                          prefix="/info",
                          tags=["runescape api config"])
api_router.include_router(route_runescape_catalogue.router,
                          prefix="/catalogue",
                          tags=["runescape api catalogue"])

@api_router.get("/")
async def root(request:Request):
    return templates.TemplateResponse("home.html", {"request": request})
