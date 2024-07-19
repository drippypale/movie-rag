import pandas as pd
from nltk import WordNetLemmatizer, tokenize, corpus
from hazm import Lemmatizer, WordTokenizer
from hazm.utils import stopwords_list
from tqdm import tqdm
from string import punctuation
from re import sub



class PreProcess:
    def __init__(self, language: str) -> None:
        self.language = language

        if self.language == "fa":
            self.stop_words = stopwords_list()
            self.lemmatizer = Lemmatizer()
            self.tokenizer = WordTokenizer()
            
        else:
            self.stop_words = corpus.stopwords.words('english')
            self.lemmatizer = WordNetLemmatizer()

    def process(self, sentence: str) -> str:
        if len(str(sentence)) < 10:
            return ""

        if self.language == "fa":
            tokenized = self.tokenizer.tokenize(sentence)
            punc_removed = list(map(lambda c: c if c not in punctuation else " ", tokenized))
        else:
            tokenized = tokenize.word_tokenize(sentence)
            punc_removed = list(map(lambda c: c.lower() if c not in punctuation else " ", tokenized))

        stops_removed = list(map(lambda w: w if w not in self.stop_words else " ", punc_removed))
        lemmatized = " ".join(list(map(lambda w: self.lemmatizer.lemmatize(w), stops_removed)))
        stripped = sub(r" +", " ", lemmatized)
        return stripped

    def get_and_save_processed(self, data: pd.DataFrame, name_att: str, designated_atts: list, file_name: str) -> pd.DataFrame:
        processed = []
        for index, row in tqdm(data.iterrows(), total=len(data)):
            series = []
            for attribute in designated_atts:
                series.append(self.process(row[attribute]))

            if sum([len(x) for x in series]) > 0:
                series.insert(0, row[name_att])
                processed.append(tuple(series))

        designated_atts.insert(0 ,name_att)
        processed_df = pd.DataFrame(processed, columns=designated_atts)
        processed_df.to_csv(file_name, index=False)
        return processed_df