from affiliates.BaseSpider import BaseSpider
from scrapy.loader import ItemLoader
from ..items import ContentItem


class tomsguideSpider(BaseSpider):
    name = 'tomsguide'
    urls = []
    rules = [
        ('news', 'parse_news'),
    ]

    def parse_news(self, response):
        l = ItemLoader(item=ContentItem(), response=response)
        l.add_value('url', response.url)
        l.add_css('content', '#article-body *::text')
        l.add_value('links', map(lambda x: x.url, self.get_links(response)))
        yield l.load_item()