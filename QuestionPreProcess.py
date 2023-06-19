import spacy
from abc import abstractmethod, ABCMeta


class QuestionParser(metaclass=ABCMeta):
    @abstractmethod
    def parse_question(self, question):
        pass


class SpacyQuestionParser(QuestionParser):
    def __init__(self, lang="en"):
        if lang == "en":
            model_name = "en_core_web_trf"
        elif lang == "zh":
            model_name = "en_core_web_trf"
        self.nlp = spacy.load(model_name)

    def parse_question(self, question):
        doc = self.nlp(question)
        key_words = []
        for ent in doc.ents:
            key_words.append(ent.text)
            print(ent.text)
        if key_words == []:
            key_words.append(question)
        return key_words


class BertBilstmQuestionParser(QuestionParser):
    def __init__(self):
        assert None

    def parse_question(self, question):
        assert None
