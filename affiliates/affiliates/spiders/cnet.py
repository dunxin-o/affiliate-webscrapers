from affiliates.affiliates.BaseSpider import BaseSpider
from scrapy.loader import ItemLoader
from ..items import ContentItem


class cnetSpider(BaseSpider):
    name = 'cnet'
    urls = []
    rules = [
        ('tech', 'parse_tech')
    ]

    def parse_tech(self, response):
        l = ItemLoader(ContentItem(), response=response)
        l.add_value('url', response.url)
        l.add_css('content', '#article-body *::text')
        l.add_value('links', map(lambda x: x.url, self.get_links(response)))
        yield l.load_item()
