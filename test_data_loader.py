import pytest
from dataset_handler import DatasetLoader
import numpy as np



def test_data_loader():
    # dataset name which is used for text classification.
    dataset_name = "ag_news"

    labels = ["World", "Sports", "Business", "Science/Tech"]
    dataset_loader = DatasetLoader(dataset_name=dataset_name)       
    dataset_loader.load() 
    id2labels, labels2id =  dataset_loader.id2labels_relation(labels)
    data = dataset_loader.get_dataset()

    assert len(np.unique(data["train"]["label"]).tolist()) == len(labels)