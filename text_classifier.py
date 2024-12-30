from transformers import AutoModelForSequenceClassification, AutoTokenizer


class SequenceClassificationLoader:

    model_name : str
    num_labels : int
    id2labels : dict
    labels2id : dict
    model : AutoModelForSequenceClassification
    tokenizer : AutoTokenizer

    def __init__(self, model_name: str, num_labels:int, id2labels:dict, labels2id:dict ):
        self.model_name = model_name
        self.num_labels = num_labels
        self.id2labels = id2labels
        self.labels2id = labels2id

    
    def load(self):
        try:

            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name,
                                                                            num_labels = self.num_labels,
                                                                            id2label = self.id2labels,
                                                                            label2id = self.labels2id)
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name) 

            for param in self.model.parameters():
                param.requires_grad = True           
            
        except Exception as e:
            raise print("Model cloudn't be loaded: \n####\n", e)


    def tokenize(self, text: str):

        encoded_input = self.tokenizer(text, padding="max_length", truncation=True,  return_tensors='pt')

        return encoded_input

    def model_response(self, encoded_input):

        return self.model(**encoded_input)