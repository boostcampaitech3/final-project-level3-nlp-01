import copy

from pymongo import MongoClient
from typing import List, Dict
from collections import deque
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from app.__main__ import URL, PORT, DB_NAME

class DiaryContentInput(BaseModel):
    record_time: str = Field(..., description="일기가 적힌 날짜")
    diary_content: str = Field(..., description="일기 내용")
    feelings: List[str] = Field(..., description="일기에 담긴 감정들")
    recommended_content: Dict[str, List] = Field(..., description="감정에 맞추어 추천받은 콘텐츠들")

class SelectionInput(BaseModel):
    record_time: str = Field(..., description="콘텐츠가 선택된 날짜")
    selected_content: Dict[str, List[Dict[str, str]]] = Field(..., description="선택된 콘텐츠들")

def get_databse_deque(collection):
    database = deque()
    for i in collection.find():
        data_dict= {key : value for key, value in i.items() if key!='_id' }
        database.append(data_dict)
    return database

router = APIRouter(prefix='/history')

@router.on_event("startup")
def startup_event():
    from os.path import join
    
    global diary_history_database, selection_history_database, remote_selection_database, remote_diary_database
    client = MongoClient(host=URL, port=PORT)
    
    remote_selection_database = client[DB_NAME]['selection_history']
    selection_history_database = get_databse_deque(remote_selection_database)

    remote_diary_database = client[DB_NAME]['diary_history']
    diary_history_database = get_databse_deque(remote_diary_database)

@router.get("/diary")
def view_diary_history_database():
    """diary_history를 조회한다.

    Returns:
        Deque: 지금까지의 history{일기 기록, 시간, 감정, 추천컨텐츠}의 deque를 리턴함.
    """
    return diary_history_database

@router.get("/selection")
def view_selection_history_database():
    """사용자가 선택한 항목의 history를 조회한다. 제작중입니다.
    """
    return selection_history_database

@router.post("/diary/insert")
def insert_diary_record(insert_form: DiaryContentInput):
    """ 일기 기록 1개 {일기 기록, 시간, 감정, 추천컨텐츠}를 diary history에 넣는다.

    Args:
        insert_form (DiaryContentInput): 일기 기록 1개 {일기 기록, 시간, 감정, 추천컨텐츠}

    Returns:
        정상 동작 시 Response 201 반환
    """
    diary_record = insert_form.dict()
    remote_diary_record = copy.deepcopy(diary_record)
    try:
        diary_history_database.append(diary_record)
    except:
        return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE, content={"msg" : "Cannot append to local diary database"})
    try:
        remote_diary_database.insert_one(remote_diary_record)
    except:
        JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"msg" : "Cannot dump history database!"})
    
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"msg" : "Diary History Database Updated!"})

@router.post("/selection/insert")
def insert_selection_record(insert_form: SelectionInput):
    """ 선택 기록 1개 {시간, 선택된 컨텐츠}를 selection history에 넣는다.

    Args:
        insert_form (SelectionInput): 선택 기록 1개 {시간, 선택된 컨텐츠}

    Returns:
        정상 동작 시 Response 201 반환
    """
    selection_record = insert_form.dict()
    remote_selection_record = copy.deepcopy(selection_record)
    try:
        selection_history_database.append(selection_record)
    except:
        return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE, content={"msg" : "Cannot append to local selection database"})
                            
    try:
        remote_selection_database.insert_one(remote_selection_record)
    except:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"msg" : "Cannot dump selection database!"})
    
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"msg" : "Selection History Database Updated!"})