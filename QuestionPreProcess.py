import spacy


class QuestionParser:
    def __init__(self, model_name="zh_core_web_trf"):
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
