from QuestionPreProcess import QuestionParser
from NewsSearch import SinaWebNews

sina_web_news = SinaWebNews()


while True:
    question = input("请输入你的问题\n")

    keywords = parse_question(question)

    news = sina_web_news.search(keywords)
    for new in news:
        print(new)
