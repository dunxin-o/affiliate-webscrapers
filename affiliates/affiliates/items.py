# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import re
import unicodedata
from itemloaders.processors import Join, MapCompose, TakeFirst
from functools import partial

normalize_content = partial(
    unicodedata.normalize, 'NFKD'
)

def remove_special_chars(s):
    pattern = re.compile('(\\[a-zA-Z0-9]*|\n)')
    return re.sub(pattern, '', s)

def remove_unicode_chars(s):
    s = s.encode('ascii', 'ignore')
    return s.decode()

class PageItem(scrapy.Item):
    url = scrapy.Field(
        output_processor=TakeFirst()
    )

class ContentItem(scrapy.Item):
    url = scrapy.Field(
        output_processor=TakeFirst()
    )
    content = scrapy.Field(
        input_processor=MapCompose(
            normalize_content,
            remove_special_chars,
            remove_unicode_chars
        ),
        output_processor=Join()
    )
    links = scrapy.Field()

