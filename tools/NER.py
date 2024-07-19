from flair.data import Sentence
from flair.models import SequenceTagger


class NerExtractor:
  def __init__(self):
    self.tagger = SequenceTagger.load("PooryaPiroozfar/Flair-Persian-NER")
  
  def extract_entities(self, text):
    sentence = Sentence(text)

    self.tagger.predict(sentence)

    persons, dates = [], []

    for entity in sentence.get_spans('ner'):
        if entity.tag == 'PER':
            persons.append(entity.text)
        elif entity.tag == 'DAT':
            dates.append(entity.text)

    return persons, dates