from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

class SongInput(BaseModel):
    now_feelings: List[str]

class SongOutput(BaseModel):
    title: str
    singer: str
    hyperlink: str
    preview: str

router = APIRouter(prefix="/song_playlist")

@router.on_event("startup")
def startup_event():
    import pickle
    from os.path import join
    from app.backend.main import top_dir
    
    global songs_database, playlist
    playlist = []
    database_dir = join(top_dir, "app/database/songs_database.pkl")
    with open(database_dir, 'rb') as f:
        songs_database = pickle.load(f)

@router.get('/')
def view_playlist():
    if playlist:
        return playlist
    else:
        raise HTTPException(status_code=404, detail="아직 오늘의 일기를 받지 못했습니다.")

@router.post("/search", response_model=List[List[SongOutput]])
def search_playlist(feelings: SongInput):
    """현재의 감정 리스트를 입력으로 넣고, Top-3개의 감정에 해당하는 노래 리스트를 쭉 불러옵니다.

    Args:
        feelings (SongInput): 감정 리스트(ex : ['기쁨', '고마움', '행복'])

    Returns:
        List[List[SongOutput]]: 노래 리스트. 이중 리스트로 되어있는데,
        바깥 쪽의 원소는 각각의 감정 1개의 노래 목록이며,
        안쪽의 원소는 각각 노래 1개의 정보이다.
    """
    feelings = feelings.now_feelings
    global songs_database, playlist
    playlist = [songs_database[feeling] for feeling in feelings]
    
    return playlist