import pandas as pd
import re
from urllib.parse import urlparse
from scrapy.crawler import CrawlerProcess
from affiliates.affiliates.spiders import \
    (
        cnet,
        pcmag,
        techradar,
        tomsguide,
        vpnmentor
     )

process = CrawlerProcess(
    settings={
        "FEEDS": {
            "contents.json": {"format": "jsonlines"},
        },
        "CONCURRENT_REQUESTS": 32,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 4,
    }
)


def get_hostname(url):
    pattern = re.compile('\.([a-z0-9]*)\.')
    hostname = re.search(
            pattern,
            urlparse(url).netloc
        )[1]
    return hostname


df = pd.read_csv('affiliates/affiliates/data/urls_to_scrape.csv')
df['hostname'] = df['url'].apply(lambda x: get_hostname(x))

spiders = [
    cnet.cnetSpider,
    pcmag.pcmagSpider,
    techradar.techradarSpider,
    tomsguide.tomsguideSpider,
    vpnmentor.vpnmentorSpider,
]

for spider in spiders:
    urls = list(df[df['hostname']==spider.name]['url'])
    # urls = urls[:min(20, len(urls))]
    process.crawl(spider, urls=urls)

process.start()
