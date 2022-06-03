import pickle

from typing import List, Dict
from collections import deque
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

class DiaryContentInput(BaseModel):
    record_time: str = Field(..., description="일기가 적힌 날짜")
    diary_content: str = Field(..., description="일기 내용")
    feelings: List[str] = Field(..., description="일기에 담긴 감정들")
    recommended_content: Dict[str, List] = Field(..., description="감정에 맞추어 추천받은 콘텐츠들")

class SelectionInput(BaseModel):
    record_time: str = Field(..., description="콘텐츠가 선택된 날짜")
    selected_content: Dict[str, str] = Field(..., description="선택된 콘텐츠들")

router = APIRouter(prefix='/history')

@router.on_event("startup")
def startup_event():
    from os.path import join
    from app.backend.main import top_dir
    
    global diary_history_database, selection_history_database, diary_history_database_dir, selection_history_database_dir
    diary_history_database_dir = join(top_dir, "app/database/diary_history_database.pkl")
    selection_history_database_dir = join(top_dir, "app/database/selection_history_database.pkl")
    with open(diary_history_database_dir, 'rb') as f:
        diary_history_database = pickle.load(f)
    with open(selection_history_database_dir, 'rb') as f:
        selection_history_database = pickle.load(f)

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
    try:
        diary_history_database.appendleft(diary_record)
    except:
        return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE, content={"msg" : "Cannot append to local diary database"})
                            
    try:
        with open(diary_history_database_dir, 'wb') as f:
            pickle.dump(diary_history_database, f)
    except:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"msg" : "Cannot dump history database!"})
    
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
    try:
        selection_history_database.appendleft(selection_record)
    except:
        return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE, content={"msg" : "Cannot append to local selection database"})
                            
    try:
        with open(selection_history_database_dir, 'wb') as f:
            pickle.dump(selection_history_database, f)
    except:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"msg" : "Cannot dump selection database!"})
    
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"msg" : "Selection History Database Updated!"})

@router.delete("/diary_records")
def clear_diary_db():
    """ diary_history_database를 clear합니다.
    """
    global diary_history_database
    diary_history_database = deque()
    with open(diary_history_database_dir, 'wb') as f:
            pickle.dump(diary_history_database, f)

@router.delete("/selection_records")
def clear_selection_db():
    """ selection_history_database를 clear합니다.
    """
    global selection_history_database
    selection_history_database = deque()
    with open(selection_history_database_dir, 'wb') as f:
            pickle.dump(selection_history_database, f)