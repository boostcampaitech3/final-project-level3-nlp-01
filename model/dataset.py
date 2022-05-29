import numpy as np

from torch.utils.data import Dataset
from utils import mlb

class SongDataset(Dataset):
    def __init__(self, text, labels, tokenizer):
        tokenized_text = tokenizer(text, return_tensors="pt", padding=True,
                                   truncation=True, max_length=512, add_special_tokens=True)
        self.dataset = tokenized_text # {'input_ids': ~, 'token_type_ids': ~, 'attention_mask': ~, 'entity_ids' : ~}
        labels = mlb.transform(labels)
        self.labels = labels # multi-label one-hot encoding

    def __getitem__(self, idx):
        item = {key: val[idx].clone().detach() for key, val in self.dataset.items()}
        item['labels'] = self.labels[idx]
        return item

    def __len__(self):
        return len(self.labels)