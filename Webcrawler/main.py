# Inspired by https://dev.to/fprime/how-to-create-a-web-crawler-from-scratch-in-python-2p46
# Honestly, this is a pretty definitive 'right' way of doing things

# Start by importing necessary libraries
import requests
import re
from urllib.parse import urlparse
import pandas as pd

# Build the crawler class object; useful for storage method for recursion
class PyCrawler(object):
    def __init__(self, starting_url):
        self.starting_url = starting_url
        self.visited = set()
        self.threshold = 25

    def get_html(self, url):
        try:
            html = requests.get(url)
        except Exception as e:
            print(e)
            return ""
        return html.content.decode('latin-1')

    def get_links(self, url):
        html = self.get_html(url)
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        links = re.findall('''<a\s+(?:[^>]*?\s+)?href="([^"]*)"''', html)
        for i, link in enumerate(links):
            if not urlparse(link).netloc:
                link_with_base = base + link
                links[i] = link_with_base

        return set(filter(lambda x: 'mailto' not in x, links))

    def extract_info(self, url):
        html = self.get_html(url)
        meta = re.findall("<meta .*?name=[\"'](.*?)['\"].*?content=[\"'](.*?)['\"].*?>", html)
        return dict(meta)

    def output_visited(self):
        result = pd.DataFrame()
        urls = list(self.visited)
        result['URL'] = urls
        result.to_csv('result.csv', encoding='utf-8-sig')

    def crawl(self, url,):
        print('Thresh = ', self.threshold)
        if self.threshold > 0:
            for link in self.get_links(url):
                if link in self.visited:
                    continue
                self.visited.add(link)
                info = self.extract_info(link)

                print(f"""Link: {link}    
    Description: {info.get('description')}    
    Keywords: {info.get('keywords')}    
                """)
                self.threshold -= 1
                self.crawl(link)
        else:
            self.output_visited()
            exit(0)

    def start(self):
        self.crawl(self.starting_url)


if __name__ == "__main__":
    crawler = PyCrawler("https://google.com")
    #crawler = PyCrawler("https://example.com")
    crawler.start()
