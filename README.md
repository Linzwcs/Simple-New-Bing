# Simple-New-Bing

## Description

Simple-New-Bing is a low profile version of New Bing. It imitates the New Bing to answer user's question by combing news on the Internet.

### implemented functions

1. I complete two crawlers myself, and news sources are from Sina News and Global Time.
2. Simple New Bing supports language including English and Chinese.
3. The project supports to use LLaMA deployed on your PC to replace Chatgpt.
4. Simple New Bing can also handle user's input by using NER model, and then get the sequence of entities. The project use these extracted entities as keywords to search news. Regarding the NER model, you have two options: 1. you can use spacy, which is a open-source NLP library containing the NER pipline. 2. in this repository, I have completed a Bert-Bilstm model. You can use it to sovle the NER problem.

## Usage

### Environment

first，you need to use conda to create new virtual environment. For instance:

```
conda create -n openai python=3.11
```

then, run the following command to import the environment:

```
conda activate openai

pip install -r requirements.txt
```

if you want use NER model in spacy, please download related model files, for example:

```
python -m spacy download en_core_web_sm
```

For more information please visit [spacy.io](https://spacy.io/models).

The porject supports LLaMA, and to replace Chatgpt by LLaMA, you should first deploy it locally. please visit [Chinese-LLaMA-Alpaca](https://github.com/ymcui/Chinese-LLaMA-Alpaca), [llama.cpp](https://github.com/ggerganov/llama.cpp).

### Run

#### Ask question

```
python main.py

[-h]  show this help message and exit
[-L LANGUAGE]  choose the language. Currently support en,zh
[-G GPT_MODEL] choose your LLM. Currently support chatgpt,llama
[-N NER_MODEL]  choose your NER model. Currently support spacy, bert_bilstm
[--show_news SHOW_NEWS] whether to display news
[--show_templated_question SHOW_TEMPLATED_QUESTION] whether to display templated question

```

#### train Bert-Bilstm

you can run the following cammand to train your Bert-Bilstm model.

```
python train.py
```

Or you can run the `train.ipynb`.

## Example

### ChatGPT

![](./imgs/example.png)

### LLaMA

![](./imgs/llama.jpg)
![](./imgs/llama.png)
