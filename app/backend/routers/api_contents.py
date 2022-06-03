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

class BookOutput(BaseModel):
    title: str = Field(..., description="책 제목")
    author: str = Field(..., description="저자")
    hyperlink: str = Field(..., description="yes24 사이트 주소")
    image: str = Field(..., description="책 이미지 주소")
    preview: str = Field(..., description="책 소개의 처음 일부분 미리보기")

class MovieOutput(BaseModel):
    title: str = Field(..., description="영화 제목")
    hyperlink: str = Field(..., description="네이버 영화 사이트 주소")
    image: str = Field(..., description="영화 이미지 주소")
    preview: str = Field(..., description="영화 소개의 처음 일부분 미리보기")

class PlayOutput(BaseModel):
    title: str = Field(..., description="연극 제목")
    hyperlink: str = Field(..., description="연극 사이트 주소")
    image: str = Field(..., description="연극 이미지 주소")
    preview: str = Field(..., description="연극 소개의 처음 일부분 미리보기")

router = APIRouter(prefix="/contents")

@router.on_event("startup")
def startup_event():
    import pickle
    from os.path import join
    from app.backend.main import top_dir
    
    global songs_database, books_database, movies_database, plays_database,\
           playlist, booklist, movielist, theaterlist
    playlist = []
    booklist = []
    movielist = []
    theaterlist = []
    
    songs_database_dir = join(top_dir, "app/database/songs_database.pkl")
    with open(songs_database_dir, 'rb') as f:
        songs_database = pickle.load(f)
    
    books_database_dir = join(top_dir, "app/database/books_database.pkl")
    with open(books_database_dir, 'rb') as f:
        books_database = pickle.load(f)
    
    movies_database_dir = join(top_dir, "app/database/movies_database.pkl")
    with open(movies_database_dir, 'rb') as f:
        movies_database = pickle.load(f)
    
    plays_database_dir = join(top_dir, "app/database/plays_database.pkl")
    with open(plays_database_dir, 'rb') as f:
        plays_database = pickle.load(f)

@router.post("/recommend", response_model=DiaryContentInput)
def recommend_contents(diary_and_feelings: DiaryAndFeelings):
    """ {날짜, 일기 내용, 감정}을 입력 시 {날짜, 일기 내용, 감정, 추천컨텐츠}로 반환해준다.

    Args:
        diary_and_feelings (DiaryAndFeelings): {날짜, 일기 내용, 감정}

    Returns:
        올바르게 동작 시 Response 200 리턴함.
    """
    recommended_content = {}
    diary_and_feelings = diary_and_feelings.dict()
    feelings = diary_and_feelings['now_feelings']
    
    # 노래 리스트 가져오기
    songs_response = requests.post("http://localhost:8000/contents/songs/search", json={"feelings" : feelings})
    if songs_response.status_code != 200:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"msg" : "Cannot search songs"})
    songs_content = eval(songs_response.content.decode("UTF-8"))
    recommended_content["songs"] = songs_content
    
    # 책 리스트 가져오기
    books_response = requests.post("http://localhost:8000/contents/books/search", json={"feelings" : feelings})
    if books_response.status_code != 200:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"msg" : "Cannot search books"})
    books_content = eval(books_response.content.decode("UTF-8"))
    recommended_content["books"] = books_content
    
    # 영화 리스트 가져오기
    movies_response = requests.post("http://localhost:8000/contents/movies/search", json={"feelings" : feelings})
    if movies_response.status_code != 200:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"msg" : "Cannot search movies"})
    movies_content = eval(movies_response.content.decode("UTF-8"))
    recommended_content["movies"] = movies_content
    
    # 연극 리스트 가져오기
    plays_response = requests.post("http://localhost:8000/contents/plays/search", json={"feelings" : feelings})
    if plays_response.status_code != 200:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"msg" : "Cannot search plays"})
    plays_content = eval(plays_response.content.decode("UTF-8"))
    recommended_content["plays"] = plays_content
    
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
        feelings (FeelingInput): 감정 리스트(ex : ['기쁨', '고마움', '행복'])

    Returns:
        List[List[SongOutput]]: 노래 리스트. 이중 리스트로 되어있는데,
        바깥 쪽의 원소는 각각의 감정 1개의 노래 목록이며,
        안쪽의 원소는 각각 노래 1개의 정보이다.
    """
    feelings = feelings.feelings
    global songs_database, playlist
    playlist = [songs_database[feeling] for feeling in feelings]
    
    return playlist

@router.get('/books')
def view_booklist():
    if booklist:
        return booklist
    else:
        raise HTTPException(status_code=404, detail="아직 오늘의 일기를 받지 못했습니다.")

@router.post("/books/search", response_model=List[List[BookOutput]])
def search_booklist(feelings: FeelingInput):
    """현재의 감정 리스트를 입력으로 넣고, Top-3개의 감정에 해당하는 책 리스트를 쭉 불러옵니다.

    Args:
        feelings (FeelingInput): 감정 리스트(ex : ['기쁨', '고마움', '행복'])

    Returns:
        List[List[BookOutput]]: 책 리스트. 이중 리스트로 되어있는데,
        바깥 쪽의 원소는 각각의 감정 1개의 책 목록이며,
        안쪽의 원소는 각각 책 1개의 정보이다.
    """
    feelings = feelings.feelings
    global books_database, booklist
    booklist = [books_database[feeling] for feeling in feelings]
    
    return booklist

@router.get('/movies')
def view_movielist():
    if movielist:
        return movielist
    else:
        raise HTTPException(status_code=404, detail="아직 오늘의 일기를 받지 못했습니다.")

@router.post("/movies/search", response_model=List[List[MovieOutput]])
def search_movielist(feelings: FeelingInput):
    """현재의 감정 리스트를 입력으로 넣고, Top-3개의 감정에 해당하는 영화 리스트를 쭉 불러옵니다.

    Args:
        feelings (FeelingInput): 감정 리스트(ex : ['기쁨', '고마움', '행복'])

    Returns:
        List[List[MovieOutput]]: 영화 리스트. 이중 리스트로 되어있는데,
        바깥 쪽의 원소는 각각의 감정 1개의 영화 목록이며,
        안쪽의 원소는 각각 영화 1개의 정보이다.
    """
    feelings = feelings.feelings
    global movies_database, movielist
    movielist = [movies_database[feeling] for feeling in feelings]
    
    return movielist

@router.get('/plays')
def view_theaterlist():
    if theaterlist:
        return theaterlist
    else:
        raise HTTPException(status_code=404, detail="아직 오늘의 일기를 받지 못했습니다.")

@router.post("/plays/search", response_model=List[List[PlayOutput]])
def search_theaterlist(feelings: FeelingInput):
    """현재의 감정 리스트를 입력으로 넣고, Top-3개의 감정에 해당하는 연극 리스트를 쭉 불러옵니다.

    Args:
        feelings (FeelingInput): 감정 리스트(ex : ['기쁨', '고마움', '행복'])

    Returns:
        List[List[PlayOutput]]: 연극 리스트. 이중 리스트로 되어있는데,
        바깥 쪽의 원소는 각각의 감정 1개의 연극 목록이며,
        안쪽의 원소는 각각 연극 1개의 정보이다.
    """
    feelings = feelings.feelings
    global plays_database, theaterlist
    theaterlist = [plays_database[feeling] for feeling in feelings]
    
    return theaterlist