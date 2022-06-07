import pandas as pd
import numpy as np

from utils import clean
from dataset import SongDataset
from trainer import SongTrainer
from arguments import *
from transformers import AutoTokenizer, AutoModelForSequenceClassification, HfArgumentParser, TrainingArguments

parser = HfArgumentParser((ModelArguments, DataTrainingArguments, TrainingArguments))
model_args, data_args, training_args = parser.parse_json_file('./args.json')

model_name = "searle-j/kote_for_easygoing_people"
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

df = pd.read_csv('../data/Lyrics_Top100_annotation_completed.csv')
texts = df['lyric']
labels = df['labels']
labels = labels.tolist()
# KcELECTRA Github에서 제공한 preprocessing 함수
cleaned_text = [clean(text) for text in texts]

train_dataset = SongDataset(cleaned_text, labels, tokenizer)
trainer = SongTrainer(model=model,
                      args=training_args,
                      train_dataset=train_dataset)

trainer.train()