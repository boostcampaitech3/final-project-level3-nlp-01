import pickle

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

class UserInput(BaseModel):
    user_id: str = Field(..., min_length=2, max_length=8, description="ID")
    user_password: str = Field(..., min_length=4, max_length=12, description="Password")

router = APIRouter(prefix='/user')

@router.on_event("startup")
def startup_event():
    from os.path import join
    from app.backend.main import top_dir
    
    global user_database, database_dir
    database_dir = join(top_dir, "app/database/user_database.pkl")
    with open(database_dir, 'rb') as f:
        user_database = pickle.load(f)

@router.get("/")
def view_user_database():
    return user_database

@router.post("/register")
def register_user(register_form: UserInput):
    user_id, user_password = register_form.user_id, register_form.user_password
    response = user_database[user_id]
    if response != 0:
        raise HTTPException(status_code=404, detail="이미 존재하는 사용자입니다.")
    user_database[user_id] = user_password
    with open(database_dir, 'wb') as f:
        pickle.dump(user_database, f)
    
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"msg" : "Created!"})