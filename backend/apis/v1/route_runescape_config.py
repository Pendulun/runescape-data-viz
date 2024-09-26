from core.config import runescapeRoutesFormats
from fastapi import APIRouter
import requests

router = APIRouter()


@router.get("/info")
def api_info():
    runescape_info = requests.get(runescapeRoutesFormats.INFO)
    data = runescape_info.json()
    return data
