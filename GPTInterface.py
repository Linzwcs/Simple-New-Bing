import openai
from config import OPAI_API_KEY, TEMPLATE_FOR_CHATGPT
from abc import abstractmethod, ABCMeta

openai.api_key = OPAI_API_KEY


class TemplatedGpt(metaclass=ABCMeta):
    @abstractmethod
    def ask_question(self, news, question):
        pass


class TemplatedChatGpt(TemplatedGpt):
    def __init__(self) -> None:
        self.template_for_gpt = TEMPLATE_FOR_CHATGPT

    def ask_question(self, news, question):
        templated_question = self.template_for_gpt.format(news, question)
        print(
            "-" * 5
            + "templated question"
            + "-" * 5
            + f"\n{templated_question}"
            + "-" * 5
            + "--------------"
            + "-" * 5
        )
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": templated_question}],
        )
        reply = response["choices"][0]["message"]
        return reply


class TemplatedLLaMA(TemplatedGpt):
    def __init__(self) -> None:
        self.template_for_gpt = TEMPLATE_FOR_CHATGPT

    def ask_question(self, news, question):
        templated_question = self.template_for_gpt.format(news, question)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": templated_question}],
        )
        reply = response["choices"][0]["message"]
        return reply
