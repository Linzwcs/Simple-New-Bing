import requests
from bs4 import BeautifulSoup
from config import HEADERS
from abc import abstractmethod, ABCMeta


class NewsSearcher(metaclass=ABCMeta):
    @abstractmethod
    def search(self, query_words, page_nums=1):
        pass


class SinaWebNewsSearcher(NewsSearcher):
    def __init__(self):
        # self.search_url_template = "https://s.weibo.com/weibo?q={}&category=4"

        self.search_url_template = "https://s.weibo.com/weibo?q={}"

    # pass a keywords list
    def search(self, query_words, page_nums=1):
        news_texts = []
        for i in range(1, page_nums + 1):
            # print(self.search_url_template.format(" ".join(query_words)))
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
            news_node_lists += soup.find_all(
                "p", {"class": "txt", "node-type": "feed_list_content"}
            )
            news_texts += [node.get_text().strip() for node in news_node_lists]

        return news_texts
