from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.model.utils import do_inference

class InferenceInput(BaseModel):
    diary_content: str

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

@router.post("/input", response_model=List[str])
def get_inference(content: InferenceInput):
    diary_content = content.diary_content
    output = do_inference(text=diary_content, threshold=0.2, pipe=pipe)
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
    
    return feelings