from datasets import load_dataset
import numpy as np


class DatasetLoader:
    dataset_name : str  
    dataset : dict  

    def __init__(self, dataset_name):
        self.dataset_name = dataset_name

    def id2labels_relation(self, labels: list)-> tuple[dict,dict]:
        """
        Creates id2labels dict which is used in the classification model.
        
        Input:
            - labels : list of string names 

        returns
            - id2labels, labels2id dicts
        
        """
        labels2id = {}
        id2labels = {}
        if len(self.dataset.keys())>0:
            label_ids = np.unique(self.dataset["train"]["label"]).tolist()
            assert len(label_ids) == len(labels)
            id2labels = { id : label for id, label in zip(label_ids, labels )}
            labels2id = { label : id for id, label in zip(label_ids, labels )}
        

        return id2labels, labels2id 


    def load(self):
        """Loads the wanted dataset from hugging face."""
        ds = {}
        try:
            splits = ["train", "test"]
            ds = {split: ds for split, ds in zip(splits, load_dataset("ag_news", split=splits))}    

        except Exception as e:
            raise print("Dataset couldn't be loaded: \n #### \n", e)

        self.dataset = ds
        
    def get_dataset(self) -> dict:
        return self.dataset