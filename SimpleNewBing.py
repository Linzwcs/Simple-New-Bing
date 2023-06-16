from QuestionPreProcess import QuestionParser
from NewsSearch import SinaWebNewsSearcher
from GPTInterface import TemplatedChatGpt


class SimpleNewBing:
    def __init__(self, news_searcher, question_parser, templated_gpt, news_sorter=None):
        self.news_searcher = news_searcher
        self.question_parser = question_parser
        self.templated_gpt = templated_gpt
        self.news_sorter = news_sorter

    def create_dialogue(self):
        while True:
            question = input("hello, can I help you\n")
            # keywords = self.question_parser.parse_question(question)
            # news_list = self.news_searcher.search(keywords)
            news_list = self.news_searcher.search([question])
            if self.news_sorter is not None:
                news_list = self.news_sorter(news_list)

            ###########################
            print("-" * 5 + "here are some related news" + "-" * 5)
            for new in news_list:
                print(new + "\n\n")
            print("-" * 5 + "--------------------------" + "-" * 5)

            ##########################

            print("please waiting...\n  ")
            gpt_answer = self.templated_gpt.ask_question(news_list[0], question)
            print(gpt_answer["content"])

            continue_choice = input("continue? yes[y]/no[n]\n")
            if continue_choice == "y":
                continue
            else:
                break
        return
