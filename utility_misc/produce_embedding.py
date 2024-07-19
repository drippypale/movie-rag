import numpy as np
from tqdm import tqdm
import pandas as pd
import pickle
import fasttext
import torch
from transformers import AutoTokenizer, AutoModel



class Embedding:
    def __init__(self, model_and_language: str) -> None:
        self.model_and_language = model_and_language
        match model_and_language:
            case "fast fa":
                self.model = ft = fasttext.load_model('cc.fa.300.bin')
            case "fast eng":
                self.model = fasttext.load_model('cc.en.300.bin')
            case "bert fa":
                self.tokenizer = AutoTokenizer.from_pretrained("HooshvareLab/bert-base-parsbert-uncased")
                self.model = AutoModel.from_pretrained("HooshvareLab/bert-base-parsbert-uncased")
            case "bert eng":
                self.tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
                self.model = AutoModel.from_pretrained('bert-base-uncased')

    
    def sentence_embedding(self, sentence):
        if "fast" in self.model_and_language:
            words = sentence.split()
            word_embeddings = [self.model.get_word_vector(w) for w in words if w in self.model]
            if len(word_embeddings) == 0:
                return np.zeros(self.model.get_dimension())
            else:
                return np.mean(word_embeddings, axis=0)
            
        else:
            inputs = self.tokenizer(sentence, return_tensors='pt', truncation=True, max_length=512, padding=True)
            input_ids = inputs['input_ids']
            attention_mask = inputs['attention_mask']

            with torch.no_grad():
                outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)

            cls_embedding = outputs.last_hidden_state[:, 0, :].squeeze().numpy()
            return cls_embedding


    def get_and_save_embedding(self, data: pd.DataFrame, name_att: str, designated_atts: list, file_name: str) -> pd.DataFrame:
        embeddings = []        
        for index, row in tqdm(data.iterrows(), total=len(data)):
            series = [row[name_att]]
            for attribute in designated_atts:
                series.append(self.sentence_embedding(row[attribute]))

            embeddings.append(tuple(series))

        designated_atts.insert(0 ,name_att)
        embeddings_df = pd.DataFrame(embeddings, columns=designated_atts)
        with open(file_name, 'wb') as f:
            pickle.dump(embeddings_df, f)
        return embeddings_df
