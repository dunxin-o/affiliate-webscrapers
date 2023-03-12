import scrapy
import re
import unicodedata
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor


def regex(x):
    if isinstance(x, str):
        return re.compile(x)
    return x


class BaseSpider(scrapy.spiders.Spider):
    name = 'base'
    urls = []
    rules = ["", "parse"]
    get_links = LinkExtractor().extract_links


    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._cbs = []
        for r, c in self.rules:
            if isinstance(c, str):
                c = getattr(self, c)
            self._cbs.append((regex(r), c))

    def start_requests(self):
        for url in self.urls:
            for r, c in self._cbs:
                if r.search(url):
                    print(url)
                    yield Request(url, callback=c)