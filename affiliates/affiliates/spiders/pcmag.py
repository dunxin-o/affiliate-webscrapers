from affiliates.affiliates.BaseSpider import BaseSpider
from scrapy.loader import ItemLoader
from ..items import ContentItem


class pcmagSpider(BaseSpider):
    name = 'pcmag'
    urls = []
    rules = [
        ('news', 'parse_news'),
        ('encyclopedia', 'parse_encyclopedia'),
    ]

    def parse_encyclopedia(self, response):
        l = ItemLoader(ContentItem(), response=response)
        l.add_value('url', response.url)
        l.add_css('content', 'div.encyclopedia-definition *::text')
        l.add_value('links', map(lambda x: x.url, self.get_links(response)))
        yield l.load_item()

    def parse_news(self, response):
        l = ItemLoader(ContentItem(), response=response)
        l.add_value('url', response.url)
        l.add_css('content', '#article *::text')
        l.add_value('links', map(lambda x: x.url, self.get_links(response)))
        yield l.load_item()


# class pcmagSpider(scrapy.spiders.SitemapSpider):
#     name = 'pcmag'
#     sitemap_urls = [
#         'https://www.pcmag.com/robots.txt'
#     ]
#     sitemap_rules = [
#         ('encyclopedia', 'parse_encyclopedia'),
#         ('news', 'parse_news'),
#     ]
#
#     def sitemap_filter(self, entries):
#         for entry in entries:
#             dt = parser.parse(entry['lastmod'])
#             if (datetime.now(tz=timezone.utc) - dt).days < 365:
#                 yield entry
#
#     def parse_encyclopedia(self, response):
#         l = ItemLoader(ContentItem(), response=response)
#         l.add_value('url', response.url)
#         l.add_css('content', 'div.encyclopedia-definition *::text')
#         l.add_css('links', 'a::attr(href)')
#         yield l.load_item()
#
#     def parse_news(self, response):
#         l = ItemLoader(ContentItem(), response=response)
#         l.add_value('url', response.url)
#         l.add_css('content', 'article::#article *::text')
#         l.add_css('links', 'a::attr(href)')
#         yield l.load_item()