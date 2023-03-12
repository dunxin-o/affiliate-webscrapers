import scrapy
from datetime import datetime, timezone
from dateutil import parser
import logging
import re
from scrapy.http import Request, XmlResponse
from scrapy.utils.gz import gunzip, gzip_magic_number
from scrapy.utils.sitemap import Sitemap, sitemap_urls_from_robots
from ..items import PageItem

def regex(x):
    if isinstance(x, str):
        return re.compile(x)
    return x


def iterloc(it, alt=False):
    for d in it:
        yield d["loc"]

        # Also consider alternate URLs (xhtml:link rel="alternate")
        if alt and "alternate" in d:
            yield from d["alternate"]

class getSitemaps(scrapy.spiders.SitemapSpider):

    name = 'getSitemaps'
    sitemap_urls = [
        'https://www.vpnmentor.com/robots.txt',
        'https://www.techradar.com/robots.txt',
        'https://www.top10vpn.com/robots.txt',
        'https://www.cnet.com/robots.txt',
        'https://www.tomsguide.com/robots.txt',
        'https://www.pcmag.com/robots.txt',
        'https://www.zdnet.com/robots.txt',
        'https://www.wired.com/robots.txt',
    ]


    def sitemap_filter(self, entries):
        for entry in entries:
            try:
                dt = parser.parse(entry['lastmod'])
            # If no lastmod, then allow entry
            except KeyError:
                yield entry
            else:
                try:
                    if (datetime.now(tz=timezone.utc) - dt).days < 365:
                        yield entry
                except TypeError:
                    dt = dt.replace(tzinfo=timezone.utc)
                    if (datetime.now(tz=timezone.utc) - dt).days < 365:
                        yield entry

    def _parse_sitemap(self, response):
        if response.url.endswith("/robots.txt"):
            for url in sitemap_urls_from_robots(response.text, base_url=response.url):
                yield Request(url, callback=self._parse_sitemap)
        else:
            body = self._get_sitemap_body(response)
            if body is None:
                logger.warning(
                    "Ignoring invalid sitemap: %(response)s",
                    {"response": response},
                    extra={"spider": self},
                )
                return

            s = Sitemap(body)
            it = self.sitemap_filter(s)

            if s.type == "sitemapindex":
                for loc in iterloc(it, self.sitemap_alternate_links):
                    if any(x.search(loc) for x in self._follow):
                        yield Request(loc, callback=self._parse_sitemap)
            elif s.type == "urlset":
                for loc in iterloc(it, self.sitemap_alternate_links):
                    for r, c in self._cbs:
                        if r.search(loc):
                            item = PageItem()
                            item['url'] = loc
                            yield item
                            break