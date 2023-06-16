import openai
from config import (
    OPAI_API_KEY,
    TEMPLATE_FOR_CHATGPT,
    LLAMA_GPT_EXE_PATH,
    LLAMA_GPT_MODEL_PATH,
    LLAMA_ARGS,
)
from abc import abstractmethod, ABCMeta
import subprocess


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
    def __init__(self):
        self.llaMA_exe_path = LLAMA_GPT_EXE_PATH
        self.template_for_gpt = TEMPLATE_FOR_CHATGPT
        self.llaMA_model_path = LLAMA_GPT_MODEL_PATH
        self.prompt_arg = '--prompt "{}"'

    def ask_question(self, news, question):
        templated_question = self.template_for_gpt.format(news, question)
        "./main -m zh-models/7B/ggml-model-q4_0.bin --color -f prompts/alpaca.txt -ins -c 2048 --temp 0.2 -n 256 --repeat_penalty 1.1"
        prompt = self.prompt_arg.format(templated_question)
        print(
            "-" * 5
            + "templated question"
            + "-" * 5
            + f"\n{templated_question}"
            + "-" * 5
            + "--------------"
            + "-" * 5
        )
        process = subprocess.Popen(
            [self.llaMA_exe_path, "-m", self.llaMA_model_path, LLAMA_ARGS, prompt],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        output_data, error = process.communicate()
        output_data = output_data.decode()
        print("Output:", output_data)
