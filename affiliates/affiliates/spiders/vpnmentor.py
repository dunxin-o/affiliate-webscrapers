from affiliates.affiliates.BaseSpider import BaseSpider
from scrapy.loader import ItemLoader
from ..items import ContentItem


class vpnmentorSpider(BaseSpider):
    name = 'vpnmentor'
    urls = []
    rules = [
        ('bestvpns', 'parse_bestvpns'),
        ('blog', 'parse_blog'),
        ('reviews', 'parse_reviews'),
    ]

    def parse_blog(self, response):
        return self.parse_bestvpns(response)


    def parse_bestvpns(self, response):
        l = ItemLoader(item=ContentItem(), response=response)
        l.add_value('url', response.url)
        l.add_css('content', 'div.post-text *::text')
        l.add_value('links', map(lambda x: x.url, self.get_links(response)))
        yield l.load_item()


    def parse_reviews(self, response):
        l = ItemLoader(item=ContentItem(), response=response)
        l.add_value('url', response.url)
        l.add_value('content', 'div.text-block *::text')
        l.add_value('links', map(lambda x: x.url, self.get_links(response)))
        yield l.load_item()


# class vpnmentorSpider(scrapy.spiders.SitemapSpider):
#     name = 'vpnmentor'
#     sitemap_urls = [
#         'https://www.vpnmentor.com/robots.txt',
#     ]
#     sitemap_rules = [
#         ('bestvpns', 'parse_bestvpns'),
#         ('blog', 'parse_blog'),
#         ('reviews', 'parse_reviews'),
#     ]
#
#     def sitemap_filter(self, entries):
#         for entry in entries:
#             dt = parser.parse(entry['lastmod'])
#             if (datetime.now(tz=timezone.utc) - dt).days < 365:
#                 yield entry
#
#     def parse_blog(self, response):
#         return self.parse_bestvpns(response)
#
#     def parse_bestvpns(self, response):
#         l = ItemLoader(item=ContentItem(), response=response)
#         l.add_value('url', response.url)
#         l.add_css('content', 'div.post-text *::text')
#         l.add_css('links', 'a::attr(href)')
#         yield l.load_item()
#
#     def parse_reviews(self, response):
#         l = ItemLoader(item=ContentItem(), response=response)
#         l.add_value('url', response.url)
#         l.add_css('content', 'div.text-block *::text')
#         l.add_css('links', 'a::attr(href)')
#         yield l.load_item()