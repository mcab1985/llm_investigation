
from fastapi import FastAPI
from text_classifier import SequenceClassificationLoader
from dataset_handler import DatasetLoader
import uvicorn

app = FastAPI()
# model name which is used for text classification. 
tokenizer_name = "./data/tokenizer/"
model_name = "./data/finetuned_classifier_model/"

# dataset name which is used for text classification.
dataset_name = "ag_news"

labels = ["World", "Sports", "Business", "Science/Tech"]
dataset_loader = DatasetLoader(dataset_name=dataset_name)       
dataset_loader.load() 
id2labels, labels2id =  dataset_loader.id2labels_relation(labels)
data = dataset_loader.get_dataset()


model_loader = SequenceClassificationLoader(model_name=model_name,
                                            tokenizer_name=tokenizer_name,
                                            num_labels=len(labels),
                                            id2labels=id2labels,
                                            labels2id=labels2id)    
model_loader.load()


@app.get("/")
async def home():
  return {"message": "Machine Learning service", "Possible labels" : labels}

@app.get("/select data to classify/")
async def data_in(input_text : str):
  try:

    text_classification = model_loader.predict_label(text = input_text)
    res = { "Request" : input_text, 
            "Classified Category" : text_classification} 
    return res
  except Exception as e:
    print("Something went wrong: ", e)


if  __name__ == "__main__":
    uvicorn.run(app="classifier_app:app", reload=True, port=6001 )