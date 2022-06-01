from fastapi import APIRouter
from pydantic import BaseModel
from app.model.utils import do_inference

class InferenceInput(BaseModel):
    diary_content: str

router = APIRouter(prefix="/diary")

@router.on_event("startup")
def startup_event():
    from app.model.pipeline import SongPipeline
    from app.backend.main import model, tokenizer
    
    global pipe
    
    pipe = SongPipeline(
            model=model,
            tokenizer=tokenizer,
            device=0, # gpu number, -1 if cpu used
            return_all_scores=True,
            function_to_apply='sigmoid'
        )

@router.post("/input")
def get_inference(content: InferenceInput):
    diary_content = content.diary_content
    output = do_inference(text=diary_content, threshold=0.2, pipe=pipe)
    
    return output
