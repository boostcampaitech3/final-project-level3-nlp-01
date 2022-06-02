from fastapi import APIRouter
from pydantic import BaseModel

class FeelingInput(BaseModel):
    now_feelings: list

router = APIRouter(prefix="/song_playlist")

@router.on_event("startup")
def startup_event():
    global songs_database
    from app.backend.main import songs_database

@router.post("/search")
def search_playlist(feelings: FeelingInput):
    feelings = feelings.now_feelings
    global songs_database
    playlist = [songs_database[feeling] for feeling in feelings]
    
    return playlist