from numpy import record
import requests

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List
from app.backend.routers.api_diary import DiaryAndFeelings
from app.backend.routers.api_history import DiaryContentInput

class FeelingInput(BaseModel):
    feelings: List[str] = Field(..., description="일기에 담긴 감정들")

class SongOutput(BaseModel):
    title: str = Field(..., description="노래 제목")
    singer: str = Field(..., description="가수")
    hyperlink: str = Field(..., description="멜론 사이트 주소")
    preview: str = Field(..., description="가사의 처음 일부분 미리보기")

router = APIRouter(prefix="/contents")

@router.on_event("startup")
def startup_event():
    import pickle
    from os.path import join
    from app.backend.main import top_dir
    
    global songs_database, playlist
    playlist = []
    songs_database_dir = join(top_dir, "app/database/songs_database.pkl")
    with open(songs_database_dir, 'rb') as f:
        songs_database = pickle.load(f)

@router.post("/recommend", response_model=DiaryContentInput)
def recommend_contents(diary_and_feelings: DiaryAndFeelings):
    recommended_content = {}
    diary_and_feelings = diary_and_feelings.dict()
    feelings = diary_and_feelings['now_feelings']
    songs_response = requests.post("http://localhost:8000/contents/songs/search", json={"feelings" : feelings})
    if songs_response.status_code != 200:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"msg" : "Cannot search songs"})
    songs_content = eval(songs_response.content.decode("UTF-8"))
    recommended_content["songs"] = songs_content
    output_contents = DiaryContentInput(record_time=diary_and_feelings['record_time'],
                                        diary_content=diary_and_feelings['diary_content'],
                                        feelings=feelings,
                                        recommended_content=recommended_content)
    
    history_response = requests.post("http://localhost:8000/history/diary/insert", json=output_contents.dict())
    if history_response.status_code != 201:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"msg" : "Something incorrect in diary_history insertion"})
    
    return JSONResponse(status_code=status.HTTP_200_OK, content={"msg" : "Recommend contents done!"})

@router.get('/songs')
def view_playlist():
    if playlist:
        return playlist
    else:
        raise HTTPException(status_code=404, detail="아직 오늘의 일기를 받지 못했습니다.")

@router.post("/songs/search", response_model=List[List[SongOutput]])
def search_playlist(feelings: FeelingInput):
    """현재의 감정 리스트를 입력으로 넣고, Top-3개의 감정에 해당하는 노래 리스트를 쭉 불러옵니다.

    Args:
        feelings (SongInput): 감정 리스트(ex : ['기쁨', '고마움', '행복'])

    Returns:
        List[List[SongOutput]]: 노래 리스트. 이중 리스트로 되어있는데,
        바깥 쪽의 원소는 각각의 감정 1개의 노래 목록이며,
        안쪽의 원소는 각각 노래 1개의 정보이다.
    """
    feelings = feelings.feelings
    global songs_database, playlist
    playlist = [songs_database[feeling] for feeling in feelings]
    
    return playlist