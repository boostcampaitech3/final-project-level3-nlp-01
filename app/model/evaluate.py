import pandas as pd
import torch

from transformers import AutoModelForSequenceClassification, AutoTokenizer
from pipeline import SongPipeline
from sklearn.metrics import f1_score
from sklearn.preprocessing import MultiLabelBinarizer

mlb = MultiLabelBinarizer()
mlb.fit([[i for i in range(44)]])

device = 0 if torch.cuda.is_available() else -1

model_dir = '/opt/ml/final_project/develop/app/saved_model'
model = AutoModelForSequenceClassification.from_pretrained(model_dir)
tokenizer = AutoTokenizer.from_pretrained(model_dir)

df = pd.read_csv('/opt/ml/final_project/develop/data/Lyrics_Top100_annotation_completed.csv')
texts = df['lyric'].tolist()
labels = list(map(eval, df['labels'].tolist()))

pipe = SongPipeline(
            model=model,
            tokenizer=tokenizer,
            device=device,
            return_all_scores=True,
            function_to_apply='sigmoid'
        )

outs = pipe(texts, stride=128, return_overflowing_tokens=True, padding=True, truncation=True)

threshold = 0.2
predicted_labels = []
for out in outs:
    predicted_label = []
    for idx, feeling in enumerate(out):
        if feeling["score"] > threshold:
            predicted_label.append(idx)
    predicted_labels.append(predicted_label)
    
labels = mlb.transform(labels)
predicted_labels = mlb.transform(predicted_labels)
score = f1_score(labels, predicted_labels, average='weighted', zero_division=0)

print(f"f1 score : {score}")