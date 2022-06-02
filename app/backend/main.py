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
    
    from app.backend.routers import api_diary, api_contents, api_history
    app.include_router(api_diary.router)
    app.include_router(api_contents.router)
    app.include_router(api_history.router)

@app.get('/')
def hello():
    return "Model and Tokenizer Loaded!"

@app.get("/example/{diary_content}")
def do_example(diary_content):
    params = {"diary_content" : diary_content}
    output = requests.post("http://localhost:8000/diary/input", json=params)
    output = eval(output.content.decode("UTF-8"))
    
    global user_feeling
    user_feeling = output['now_feelings']
    
    response = requests.post("http://localhost:8000/contents/recommend", json=output)
    if response.status_code != 200:
        return "Something is Wrong!!!"
    
    return "Well Done!"

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