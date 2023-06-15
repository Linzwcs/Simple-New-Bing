import requests
from bs4 import BeautifulSoup
import json
from config import HEADERS


class SinaWebNews:
    def __init__(self):
        self.search_url_template = "https://s.weibo.com/weibo?q={}&category=4"

    # pass a keywords list
    def search(self, query_words, page_nums=1):
        news_texts = []
        for i in range(1, page_nums + 1):
            response = requests.get(
                url=self.search_url_template.format(" ".join(query_words))
                + f"&page{i}",
                headers=HEADERS,
            )
            news_texts = []
            soup = BeautifulSoup(response.text, "html.parser")
            news_node_lists = soup.find_all(
                "p", {"class": "txt", "node-type": "feed_list_content_full"}
            )
            news_texts += [node.get_text().strip() for node in news_node_lists]
        return news_texts
