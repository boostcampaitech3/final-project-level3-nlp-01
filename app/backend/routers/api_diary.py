import datetime

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List
from app.model.utils import do_inference

class InferenceInput(BaseModel):
    diary_content: str = Field(..., description="일기 내용")

class DiaryAndFeelings(BaseModel):
    record_time: str = Field(..., description="일기가 적힌 날짜")
    diary_content: str = Field(..., description="일기 내용")
    now_feelings: List[str] = Field(..., description="일기에 담긴 감정들")

router = APIRouter(prefix="/diary")

@router.on_event("startup")
def startup_event():
    from os.path import join
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    from app.model.pipeline import SongPipeline
    from app.backend.main import top_dir
    
    model_dir = join(top_dir, "app/saved_model")    
    model = AutoModelForSequenceClassification.from_pretrained(model_dir)
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    
    global pipe
    
    pipe = SongPipeline(
            model=model,
            tokenizer=tokenizer,
            device=0, # gpu number, -1 if cpu used
            return_all_scores=True,
            function_to_apply='sigmoid'
        )

@router.post("/input", response_model=DiaryAndFeelings)
def get_inference(content: InferenceInput):
    diary_content = content.diary_content
    output = do_inference(text=diary_content, threshold=0.2, pipe=pipe)
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cnt = 0
    feelings = []
    
    for out in output:
        feeling, _ = out
        if feeling == '없음':
            continue
        cnt += 1
        feelings.append(feeling)
        if cnt == 3:
            break
    outs = DiaryAndFeelings(record_time=now_time, diary_content=diary_content, now_feelings=feelings)
    outs = outs.dict()
    
    return outs