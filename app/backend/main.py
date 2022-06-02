import requests

from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.on_event("startup")
def startup_event():
    import os
    from os.path import abspath, join
    
    global user_feeling, top_dir
    user_feeling = []
    
    here_dir = os.path.abspath(__file__)
    top_dir = abspath(join(here_dir, os.pardir, os.pardir, os.pardir))
    
    from app.backend.routers import api_diary, api_song_playlist, api_user
    app.include_router(api_diary.router)
    app.include_router(api_song_playlist.router)
    app.include_router(api_user.router)

@app.get('/')
def hello():
    return "Model and Tokenizer Loaded!"

@app.get("/example/{diary_content}")
def do_example(diary_content):
    params = {"diary_content" : diary_content}
    output = requests.post("http://localhost:8000/diary/input", json=params)
    global user_feeling
    
    user_feeling = eval(output.content)
    return user_feeling

@app.get('/feeling')
def now_feeling():
    return user_feeling

@app.get('/post_example')
def post_playlist():
    if user_feeling:
        result = requests.post("http://localhost:8000/song_playlist/search", json={"now_feelings" : user_feeling})
        return result.content
    else:
        raise HTTPException(status_code=404, detail="아직 오늘의 일기를 받지 못했습니다.")