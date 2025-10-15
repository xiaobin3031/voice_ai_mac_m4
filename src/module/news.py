""" 新闻模块 """

from src.module.base_module import BaseModule
import requests
from lxml import etree

news_url = "https://www.sina.com.cn/"

g_titles = None
g_sub_titles = None

class News(BaseModule):
    def __init__(self): pass

    def first(self, text):
        if g_titles is None:
            self.load_news()
        self.__play_news(g_titles['国内'])

    def again(self, text):
        pass

    def load_news(self):
        tree = self.__load_url(news_url)
        links = tree.xpath("//div[contains(@class, 'nav-mod-1')]/ul/li/a")
        titles = {}
        for link in links:
            title = link.xpath("b/text()")
            if title is None or len(title) == 0:
                title = link.xpath("text()")
                if title is None or len(title) == 0:
                    continue
            href = link.xpath('@href')
            titles[title[0]] = href[0]
        print('titles', titles)
        g_titles = titles

    def __play_news(self, url):
        """ 播放新闻"""
        tree = self.__load_url(url)

    def __load_url(self, url):
        response = requests.get(url)
        response.encoding = 'utf-8'
        return etree.HTML(response.text)