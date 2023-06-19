from QuestionPreProcess import (
    SpacyQuestionParser,
    BertBilstmQuestionParser,
)
from NewsSearch import SinaWebNewsSearcher, GlobalTimesSearcher
from GPTInterface import TemplatedChatGpt, TemplatedLLaMA
from SimpleNewBing import SimpleNewBing
import argparse

parser = argparse.ArgumentParser(
    description="Simple New Bing is a toy project. The aim that I complete this project is to apply for Westlake University"
)
parser.add_argument(
    "-L",
    "--language",
    default="en",
    help="choose the language. Currently support en, zh",
)
parser.add_argument(
    "-G",
    "--gpt_model",
    default="chatgpt",
    help="choose your LLM. Currently support chatgpt, llama",
)
parser.add_argument(
    "-N",
    "--ner_model",
    default="spacy",
    help="choose your NER model. Currently support spacy, bert_bilstm",
)
parser.add_argument(
    "--show_news",
    default=True,
    help="whether to display news",
)
parser.add_argument(
    "--show_templated_question",
    default=True,
    help="whether to display templated question",
)
parser.add_argument(
    "-U",
    "--use_ner_model",
    default=False,
    help="whether to use NER model",
)


args = parser.parse_args()

print(f"choose language: {args.language}")
print(f"choose model: {args.gpt_model}")
print(f"show news: {args.show_news}")
print(f"choose model: {args.show_templated_question}")

if __name__ == "__main__":
    (
        language,
        gpt_model,
        show_news,
        show_templated_question,
        ner_model,
        use_ner_model,
    ) = (
        args.language,
        args.gpt_model,
        args.show_news,
        args.show_templated_question,
        args.ner_model,
        args.use_ner_model,
    )
    templated_gpt, news_searcher = None, None

    if language == "en":
        news_searcher = GlobalTimesSearcher()
    elif language == "zh":
        news_searcher = SinaWebNewsSearcher()

    if gpt_model == "chatgpt":
        templated_gpt = TemplatedChatGpt(
            lang=language, show_templated_question=show_templated_question
        )
    elif gpt_model == "llama":
        templated_gpt = TemplatedLLaMA(
            lang=language, show_templated_question=show_templated_question
        )

    if use_ner_model is False:
        question_parser = None
    elif ner_model == "bert_bilstm":
        assert language == "zh"
        question_parser = BertBilstmQuestionParser()
    elif ner_model == "spacy":
        question_parser = SpacyQuestionParser(lang=language)
    new_bing = SimpleNewBing(
        news_searcher, question_parser, templated_gpt, show_news=show_news
    )

    new_bing.create_dialogue()
