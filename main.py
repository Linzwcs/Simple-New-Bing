from QuestionPreProcess import QuestionParser
from NewsSearch import SinaWebNewsSearcher
from GPTInterface import TemplatedChatGpt
from SimpleNewBing import SimpleNewBing


if __name__ == "__main__":
    news_searcher = SinaWebNewsSearcher()
    question_parser = QuestionParser()
    templated_gpt = TemplatedChatGpt()
    new_bing = SimpleNewBing(news_searcher, question_parser, templated_gpt)

    new_bing.create_dialogue()
