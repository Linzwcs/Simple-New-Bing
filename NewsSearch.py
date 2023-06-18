import requests
from bs4 import BeautifulSoup
from config import HEADERS
from abc import abstractmethod, ABCMeta
import re


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
            soup = BeautifulSoup(response.text, "html.parser")
            news_node_lists = soup.find_all(
                "p", {"class": "txt", "node-type": "feed_list_content_full"}
            )
            news_node_lists += soup.find_all(
                "p", {"class": "txt", "node-type": "feed_list_content"}
            )
            news_texts += [node.get_text().strip() for node in news_node_lists]

        return news_texts


class GlobalTimesSearcher(NewsSearcher):
    def __init__(self):
        self.search_url = "https://search.globaltimes.cn/QuickSearchCtrl"
        self.pattern = r"https://www.globaltimes.cn/page/.*"

    # pass a keywords list
    def search(self, query_words, page_nums=1):
        news_texts = []
        for i in range(1, page_nums + 1):
            # print(self.search_url_template.format(" ".join(query_words)))
            response = requests.post(
                url=self.search_url,
                data={"page_no": f"{i}", "search_txt": " ".join(query_words)},
            )
            soup = BeautifulSoup(response.text, "html.parser")

            node_list = soup.find_all("a")
            hrefs = []
            for node in node_list:
                href = node.attrs["href"]
                if re.match(self.pattern, href):
                    # print(node.attrs["href"])
                    hrefs.append(href)
                else:
                    continue
            for href in hrefs:
                response = requests.get(url=href)
                soup = BeautifulSoup(response.text, "html.parser")
                node = soup.find("div", {"class": "article_right"})
                news_texts.append(node.get_text().strip())
        return news_texts
