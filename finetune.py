from transformers import DataCollatorWithPadding, Trainer, TrainingArguments
import numpy as np
from text_classifier import SequenceClassificationLoader
from dataset_handler import DatasetLoader

def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return {"accuracy": (predictions == labels).mean()}



if __name__ == '__main__':
    # model name which is used for text classification. 
    model_name = "distilbert-base-uncased"
    dataset_name = "ag_news"

    labels = ["World", "Sports", "Business", "Science/Tech"]
    dataset_loader = DatasetLoader(dataset_name=dataset_name)       
    dataset_loader.load() 
    id2labels, labels2id =  dataset_loader.id2labels_relation(labels)
    data = dataset_loader.get_dataset()


    model_loader = SequenceClassificationLoader(model_name=model_name,
                                                num_labels=len(labels),
                                                id2labels=id2labels,
                                                labels2id=labels2id)    
    model_loader.load()

    train_data_len = len(data["train"]["text"])
    test_data_len = len(data["test"]["text"])

    tokenized_dataset = {}
    splits = ["train", "test"]
    num_batches = [600, min(200, test_data_len)]
    for split, num_batch in zip(splits, num_batches):
        try:
            small_dataset = data[split].shuffle(seed=42).select(range(num_batch))
            tokenized_dataset[split] = small_dataset.map(
                lambda x: model_loader.tokenizer(x["text"], truncation=True), batched=True
        )
            print("Subset of the dataset created successfully.")
        except Exception as e:
            print(f"An error occurred while creating a subset of the dataset: {e}")



    trainer = Trainer(
        model=model_loader.model,
        args=TrainingArguments(
            output_dir="./data/news_classifier_finetune",
            # Set the learning rate
            learning_rate=3e-5,
            # Set the per device train batch size and eval batch size
            per_device_train_batch_size=16,
            per_device_eval_batch_size=16,
            # Evaluate and save the model after each epoch
            evaluation_strategy="epoch",
            save_strategy="epoch",
            # Set the learning rate
            num_train_epochs=20,
            weight_decay=0.01,
            load_best_model_at_end=True,
        ),
        train_dataset=tokenized_dataset["train"],
        eval_dataset=tokenized_dataset["test"],
        tokenizer=model_loader.tokenizer,
        data_collator=DataCollatorWithPadding(tokenizer=model_loader.tokenizer),
        compute_metrics=compute_metrics,
    )

    trainer.train()

    model_loader.model.save_pretrained("./data/finetuned_classifier_model/")
