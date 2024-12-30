
import torch
from fastapi import FastAPI
from text_classifier import SequenceClassificationLoader
from dataset_handler import DatasetLoader
import uvicorn

app = FastAPI()
# model name which is used for text classification. 
#model_name = "distilbert-base-uncased"
model_name = "C:/Users/mcab/Projects/llms/data/news_classifier_finetune/checkpoint-228/"

# dataset name which is used for text classification.
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


@app.get("/")
async def home():
  return {"message": "Machine Learning service", "Possible labels" : labels}

@app.get("/select data to classify")
async def data_in(input_text : str):
  try:
    

    #input_text = data["test"]["text"][sel_data]
    encoded_input = model_loader.tokenize(text = input_text)            
    model_output = model_loader.model_response(encoded_input=encoded_input)
    # Make prediction
    with torch.no_grad():
        logits = model_output.logits
        #probabilities = torch.nn.functional.softmax(logits, dim=1)
        #predicted_class = torch.argmax(probabilities)
        predicted_class =  logits.argmax().item()
        res = { "Request" : input_text, 
            "Classified Category" :  model_loader.model.config.id2label[predicted_class]} 
    return res
  except Exception as e:
    print("Something went wrong: ", e)


if  __name__ == "__main__":
    uvicorn.run(app="classifier_app:app", reload=True, port=6001 )