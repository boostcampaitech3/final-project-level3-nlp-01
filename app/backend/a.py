import uvicorn

from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def hello():
    return "Hello World!"

uvicorn.run(app, host="0.0.0.0", port=8000)