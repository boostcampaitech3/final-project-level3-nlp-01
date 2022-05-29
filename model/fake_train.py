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

# 현재, 데이터셋이 없는 관계로, 임의로 label을 생성하여 데이터셋으로 만들어봄.
df = pd.read_csv('../data/Lyrics_top100.csv')
fake_labels = [list(set(np.random.choice(44, 10))) for _ in range(100)]
df['labels'] = fake_labels
texts = df['lyric']
labels = df['labels']
# KcELECTRA Github에서 제공한 preprocessing 함수
cleaned_text = [clean(text) for text in texts]

train_dataset = SongDataset(cleaned_text, labels, tokenizer)
trainer = SongTrainer(model=model,
                      args=training_args,
                      train_dataset=train_dataset)

trainer.train()