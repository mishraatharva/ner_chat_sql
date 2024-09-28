from transformers import AutoModelForTokenClassification
from transformers import BertTokenizerFast
from transformers import pipeline
import datasets
from sql_script import db_operations
from constants import *


class predict_save():
    def __init__(self,model_path,tokenizer_path) -> None:
        self.conll2003 = datasets.load_dataset("conll2003", trust_remote_code=True)
        self.ner_tokens = ['B-PER','B-ORG','B-LOC','I-PER','I-ORG','I-LOC']
        self.db = db_operations()
        self.ner = pipeline("ner", model=model_path, tokenizer=tokenizer_path)

    def create_data(self,ner_results,text):
        person = ""
        location = ""
        organization = ""
        start = 0 
        end = 0
        for i in range(len(ner_results[:100])):
            if ner_results[i]['entity'] in self.ner_tokens:
                if ner_results[i]['entity'] == "B-PER" or ner_results[i]['entity'] == "I-PER":
                    start = ner_results[i]['start']
                    end = ner_results[i]['end']
                    person = person + text[start:end]
                elif ner_results[i]['entity'] == 'B-ORG' or ner_results[i]['entity'] == "I-ORG":
                    start = ner_results[i]['start']
                    end = ner_results[i]['end']
                    organization = organization + text[start:end]
                else:
                    start = ner_results[i]['start']
                    end = ner_results[i]['end']
                    location = location + text[start:end]
        return (person,organization,location)
    

    def push_data(self):
        validation_data = self.conll2003['validation']
        for i in range(len(validation_data)):
            data = " ".join(validation_data[i]['tokens'])
            ner_data = self.ner(data)
            values = self.create_data(ner_data,data)
            self.db.insert_data(values)
    

if __name__ == "__main__":
    pbj = predict_save(MODEL_PATH,TOKENIZER_PATH)
    pbj.push_data()