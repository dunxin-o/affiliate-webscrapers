import scrapy
from datetime import datetime, timezone
from dateutil import parser
from scrapy.loader import ItemLoader
from ..items import ContentItem

class top10vpnSpider(scrapy.spiders.SitemapSpider):
    name = 'top10vpn'
    sitemap_urls = [
        'https://www.top10vpn.com/robots.txt'
    ]
    sitemap_rules = [
        ('guides', 'parse_guides'),
    ]

    def sitemap_filter(self, entries):
        for entry in entries:
            dt = parser.parse(entry['lastmod'])
            if (datetime.now(tz=timezone.utc) - dt).days < 365:
                yield entry

    def parse_guides(self, response):
        yield l.load_item()
