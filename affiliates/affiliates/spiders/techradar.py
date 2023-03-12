from affiliates.affiliates.BaseSpider import BaseSpider
from scrapy.loader import ItemLoader
from ..items import ContentItem


class techradarSpider(BaseSpider):
    name = 'techradar'
    urls = []
    rules = [
        ('vpn', 'parse_vpn'),
        ('reviews', 'parse_reviews'),
        ('how-to', 'parse_how_to'),
        ('news', 'parse_news'),
    ]

    def parse_reviews(self, response):
        l = ItemLoader(item=ContentItem(), response=response)
        l.add_value('url', response.url)
        l.add_css('content', '#article-body *::text')
        l.add_value('links', map(lambda x: x.url, self.get_links(response)))
        yield l.load_item()

    def parse_how_to(self, response):
        return self.parse_reviews(response)

    def parse_vpn(self, response):
        return self.parse_reviews(response)

    def parse_news(self, response):
        return self.parse_reviews(response)