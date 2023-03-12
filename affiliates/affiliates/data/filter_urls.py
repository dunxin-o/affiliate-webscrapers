import json
import collections
import pandas as pd
from urllib.parse import urlparse

'''
This section is meant to discover the paths in which to scrape
We want to choose:
- As relevant as possible articles
- Url paths with large enough of these articles to build a parser for
'''


with open('affiliates/affiliates/data/pages.json', 'r') as f:
    data = json.load(f)
    f.close()
pd.options.display.max_colwidth = 200
df = pd.DataFrame(data)
df['netloc'] = df['url'].apply(lambda x: urlparse(x).netloc)
df['path'] = df['url'].apply(lambda x: urlparse(x).path)
def get_path_level(path, level):
    try:
        return path.split('/')[level]
    except IndexError:
        return ''
df['path1'] = df['path'].apply(lambda x: get_path_level(x, 1))
df['path2'] = df['path'].apply(lambda x: get_path_level(x, 2))

# Deduplicate URLs
df = df.drop_duplicates(subset='url')
# Drop URLs with no path
## No point scraping the domain home page
df = df[df['path']!='']
df[['netloc', 'path1', 'path2']].value_counts().to_clipboard()
import re
# Remove paths with [a-zA-Z]{2}-[a-zA-Z]{2}
# This is to remove country-language specific websites (generally denotes non-english pages)
bool_filter = list(map(lambda x: False if re.search('\/[a-z]{2}-[a-z]{2}\/', x) else True, df['path']))
df = df[bool_filter]
# Find urls with vpn string
bool_filter = list(map(lambda x: True if re.search('vpn', x) else False, df['url']))
urls_w_vpn_string = df[bool_filter]
# Find urls with stream string
bool_filter = list(map(lambda x: True if re.search('stream', x) else False, df['url']))
urls_w_stream_string = df[bool_filter]
# Find urls with sports string
bool_filter = list(map(lambda x: True if re.search('sport', x) else False, df['url']))
urls_w_sport_string = df[bool_filter]

# Urls to scrape
urls = pd.concat([urls_w_vpn_string, urls_w_stream_string, urls_w_sport_string], axis=0)
urls = urls.drop_duplicates()
urls.to_csv('affiliates/affiliates/data/urls_to_scrape.csv', index=False)

urls[['netloc', 'path1']].value_counts().to_clipboard()
pattern = re.compile('cnet.com/tech')
print(
    urls[urls['url'].apply(lambda x: True if re.search(pattern, x) else False)].head()['url']
)
