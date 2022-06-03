import torch.nn as nn

from transformers import Trainer

class SongTrainer(Trainer):
    def compute_loss(self, model, inputs):
        labels = inputs.pop("labels")
        labels = labels.float()
        outputs = model(**inputs)
        logits = outputs[0]
        loss = nn.BCEWithLogitsLoss()(logits, labels)
        return loss