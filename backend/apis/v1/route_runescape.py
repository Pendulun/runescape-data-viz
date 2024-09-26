from fastapi import APIRouter
import requests

router = APIRouter()

@router.get("/info")
def api_info():
    runescape_info = requests.get("https://secure.runescape.com/m=itemdb_rs/api/info.json")
    data = runescape_info.json()
    return data