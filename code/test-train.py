import os, json
import pandas as pd
from transformers import (
    AutoConfig,
    AutoModelForSequenceClassification,
    AutoTokenizer,
    # DataCollatorWithPadding,
    # EvalPrediction,
    # HfArgumentParser,
    Trainer,
    TrainingArguments,
    set_seed,
)
from datasets import Dataset, DatasetDict, load_from_disk
import torch
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score




def main():
    config = AutoConfig.from_pretrained(
        "klue/roberta-large",
        num_labels=31)
    tokenizer = AutoTokenizer.from_pretrained("klue/roberta-large", use_fast=True)
    model = AutoModelForSequenceClassification.from_pretrained(
        "klue/roberta-large", 
        config=config, 
        )

    # print(
    #     config,
    #     tokenizer,
    #     model
    # )

    train_data_path = "../data/aihub_kr_hair/drop_dup/training"
    valid_data_path = "../data/aihub_kr_hair/drop_dup/validation"
    # print(os.listdir(train_data_path))
    train_dataset = load_from_disk(train_data_path)
    validation_dataset = load_from_disk(valid_data_path)

    print(train_dataset)
    print(validation_dataset)

    def label_to_num(label):
        labels = {
            '가르마': 0,
            '기타남자스타일': 1,
            '기타레이어드': 2,
            '기타여자스타일': 3,
            '남자일반숏': 4,
            '댄디': 5,
            '루프': 6,
            '리젠트': 7,
            '리프': 8,
            '미스티': 9,
            '바디': 10,
            '베이비': 11,
            '보니': 12,
            '보브': 13,
            '빌드': 14,
            '소프트투블럭댄디': 15,
            '숏단발': 16,
            '쉐도우': 17,
            '쉼표': 18,
            '스핀스왈로': 19,
            '시스루댄디': 20,
            '애즈': 21,
            '에어': 22,
            '여자일반숏': 23,
            '원랭스': 24,
            '원블럭댄디': 25,
            '테슬': 26,
            '포마드': 27,
            '플리츠': 28,
            '허쉬': 29,
            '히피': 30
        }

        return labels[label]

    def pre_processing_dataset(example):
        input_str = f"""
        머리 길이는 {example['basestyle-type']}, 곱슬기는 {example['curl']}, 앞머리는 {example['bang']}, 옆머리는 {example['side']}, 가르마는 {example['partition']}, 성별은 {example['sex']}, 모발 굵기는 {example['hair-width']}
        """
        inputs = tokenizer(
            input_str,
            padding='max_length')
        inputs['labels'] = label_to_num(example['basestyle'])

        return inputs

    print("Start Preprocessing training dataset ...")
    train_dataset = train_dataset.map(pre_processing_dataset)
    print("Start Preprocessing validation dataset ...")
    validation_dataset = validation_dataset.map(pre_processing_dataset)

    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    print(device)
    model.to(device)

    def compute_metrics(pred):
        labels = pred.label_ids
        preds = pred.predictions.argmax(-1)

        f1 = f1_score(labels, preds, average="macro", labels=range(31)) * 100.0
        acc = accuracy_score(labels, preds)

        return {'macro f1': f1, 'accuracy': acc}

    training_args = TrainingArguments(
        output_dir='./results',          # output directory
        save_total_limit=5,              # number of total save model.
        save_steps=500,                 # model saving step.
        num_train_epochs=10,              # total number of training epochs
        learning_rate=1e-5,               # learning_rate
        per_device_train_batch_size=8,  # batch size per device during training
        per_device_eval_batch_size=8,   # batch size for evaluation
        warmup_ratio=0.1,                # number of warmup steps for learning rate scheduler
        # weight_decay=0.01,               # strength of weight decay
        logging_dir='./logs',            # directory for storing logs
        logging_steps=100,              # log saving step.
        evaluation_strategy='steps', # evaluation strategy to adopt during training
                                    # `no`: No evaluation during training.
                                    # `steps`: Evaluate every `eval_steps`.
                                    # `epoch`: Evaluate every end of epoch.
        eval_steps = 500,            # evaluation step.
        load_best_model_at_end = True 
    )

    trainer = Trainer(
        model=model,                         # the instantiated 🤗 Transformers model to be trained
        args=training_args,                  # training arguments, defined above
        train_dataset=train_dataset,         # training dataset
        eval_dataset=validation_dataset,             # evaluation dataset
        compute_metrics=compute_metrics         # define metrics function
    )

    # train model
    print("Start Training ...")
    trainer.train()
    model.save_pretrained('./best_model')


    # dict0 = train_dataset[0:10]
    # print(dict0)
    # print()
    # input0 = f"""
    # 머리 길이는 {dict0['basestyle-type']}, 곱슬기는 {dict0['curl']}, 앞머리는 {dict0['bang']}, 옆머리는 {dict0['side']},
    # 가르마는 {dict0['partition']}, 성별은 {dict0['sex']}, 모발 굵기는 {dict0['hair-width']}
    # """
    # print(input0)
    # print()

    # inputs = tokenizer(input0, return_tensors="pt")
    # print(inputs)

    # with torch.no_grad():
    #     logits = model(**inputs).logits

    # predicted_class_id = logits.argmax().item()
    # print(model.config.id2label[predicted_class_id])


    

if __name__ == "__main__":
    main()