import openai
import requests


openai.api_key = "sk-SDNaZXJ4pocvDCXK9H99U6S7GUvMCsUGNQehQvQwu9znKkRP"
messages = []
system_message = input("What type of chatbot you want me to be?")
messages.append({"role": "system", "content": system_message})
print(messages)
print(
    "Alright! I am ready to be your friendly chatbot"
    + "\n"
    + "You can now type your messages."
)
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {
            "role": "assistant",
            "content": "The Los Angeles Dodgers won the World Series in 2020.",
        },
        {"role": "user", "content": "Where was it played?"},
    ],
)
reply = response["choices"][0]["message"]
