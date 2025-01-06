from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

class SequenceClassificationLoader:

    model_name : str
    tokenizer_name : str
    num_labels : int
    id2labels : dict
    labels2id : dict
    model : AutoModelForSequenceClassification
    tokenizer : AutoTokenizer

    def __init__(self, model_name: str, tokenizer_name:str, num_labels:int, id2labels:dict, labels2id:dict ):
        self.model_name = model_name
        self.tokenizer_name = tokenizer_name
        self.num_labels = num_labels
        self.id2labels = id2labels
        self.labels2id = labels2id

    
    def load(self):
        """ 
        Loads the defined model and tokenier from the given path. It is reommended to do finetuning and rather
        load the finetuned model than the pretrained model from hugging face.
        """
        try:

            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name,
                                                                            num_labels = self.num_labels,
                                                                            id2label = self.id2labels,
                                                                            label2id = self.labels2id)
            self.tokenizer = AutoTokenizer.from_pretrained(self.tokenizer_name) 

            for param in self.model.parameters():
                param.requires_grad = True           
            
        except Exception as e:
            raise print("Model cloudn't be loaded: \n####\n", e)


    def tokenize(self, text: str):
        """Tokenization of the given text using the loaded tekonizer. This can be used to generate the model response."""

        encoded_input = self.tokenizer(text, padding="max_length", truncation=True,  return_tensors='pt')

        return encoded_input

    def model_response(self, encoded_input):
        """Generation of the model response using the encoded input."""

        return self.model(**encoded_input)
    
    def predict_label(self, text :str) ->str:
        """Predicts the class using the given labels."""
        encoded_input = self.tokenize(text = text)            
        model_output = self.model_response(encoded_input=encoded_input)
        # Make prediction
        with torch.no_grad():
            logits = model_output.logits
            predicted_class =  logits.argmax().item()

        return self.model.config.id2label[predicted_class]
        

