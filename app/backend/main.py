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
    """Application이 load 되었는지 보여줍니다.

    Returns:
        str: "Model and Tokenizer Loaded!"
    """
    return "Model and Tokenizer Loaded!"

@app.get("/example/{diary_content}")
def do_example(diary_content):
    """일기 예시 내용을 넣어서, 감정을 얻어내고 컨텐츠 추출하고,
       history에 들어가는 것까지 한번에 진행됩니다.

    Args:
        diary_content (str): 일기 내용

    Returns:
        정상 동작 시 Response 200 반환
    """
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
    """가장 최근 일기의 감정을 조회해줍니다.

    Returns:
        List[str]: 감정 리스트
    """
    return user_feeling