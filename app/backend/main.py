import requests

from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
def startup_event():
    import os
    from os.path import abspath, join
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    
    global model, tokenizer
    here_dir = os.path.abspath(__file__)
    model_dir = join(abspath(join(here_dir, os.pardir, os.pardir)), "saved_model")
    
    model = AutoModelForSequenceClassification.from_pretrained(model_dir)
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    
    from app.backend.routers import api_diary
    app.include_router(api_diary.router)

@app.get('/')
def hello():
    return "Model and Tokenizer Loaded!"

@app.get('/example')
def do_example():
    params = {"diary_content" : "나는 지금 매우매우 슬프다고요ㅠㅠㅠ"}
    output = requests.post("http://localhost:8000/diary/input", json=params)
    return output.content