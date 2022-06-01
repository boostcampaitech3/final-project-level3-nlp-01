import requests

from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.on_event("startup")
def startup_event():
    import os
    import pickle
    from os.path import abspath, join
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    
    global model, tokenizer, songs_database, user_feeling
    user_feeling = []
    
    here_dir = os.path.abspath(__file__)
    top_dir = abspath(join(here_dir, os.pardir, os.pardir, os.pardir))
    database_dir = join(top_dir, "data/songs_database.pkl")
    model_dir = join(top_dir, "app/saved_model")
    
    with open(database_dir, 'rb') as f:
        songs_database = pickle.load(f)
    
    model = AutoModelForSequenceClassification.from_pretrained(model_dir)
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    
    from app.backend.routers import api_diary, api_song_playlist
    app.include_router(api_diary.router)
    app.include_router(api_song_playlist.router)

@app.get('/')
def hello():
    return "Model and Tokenizer Loaded!"

@app.get('/example')
def do_example():
    params = {"diary_content" : "나는 지금 매우매우 슬프다고요ㅠㅠㅠ"}
    output = requests.post("http://localhost:8000/diary/input", json=params)
    global user_feeling
    
    user_feeling = eval(output.content)
    return user_feeling

@app.get('/feeling')
def now_feeling():
    return user_feeling

@app.get('/song_playlist')
def view_playlist():
    if user_feeling:
        result = requests.post("http://localhost:8000/song_playlist/search", json={"now_feelings" : user_feeling})
        return result.content
    else:
        raise HTTPException(status_code=404, detail="아직 오늘의 일기를 받지 못했습니다.")