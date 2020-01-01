# Inspired by https://github.com/RainBoltz/DeepUrlCrawler/blob/master/main.py
# Tried to add a print function for the spider to save results.
import requests
import pandas as pd
from lxml import html
from urllib.parse import urljoin
# Import the necessary libraries. In this case, requests for URL's, pandas for data structuring

# Create the class, to serve as a crawler object
class DeepCrawler:
    def __init__(self, start_page):
        # store visited urls & keep track of what is next
        self.visited_url = {}
        self.queue_url = [start_page]

    def get_url_list(self, url):
        # output to screen for usability
        print('crawling: %s' % (url))

        # error handling
        try:
            # try to get an html response from requested target
            url = url.lower()
            response = requests.get(url, timeout=10.0)
            raw_html = response.text
            parsed_html = html.fromstring(raw_html)
        except:
            return

        url_title_item = parsed_html.xpath('//title')
        url_title = '(NO TITLE)'
        try:
            url_title = url_title_item[0].text
        except:
            url_title = '(ERROR TITLE)'
        # assuming success, add url to visited list
        self.visited_url[url] = url_title

        # for found links in the parsed html...
        for a in parsed_html.xpath('//a'):
            # get the url extension and store it temporarily
            raw_url = a.get('href')
            if raw_url is None:
                continue

            # join the new extension to the current branch of the search
            parsed_url = urljoin(url, raw_url)
            if parsed_url not in list(self.visited_url.keys()) and parsed_url not in self.queue_url:
                self.queue_url.append(parsed_url)

    # output final results as a csv
    def output_result(self):
        result = pd.DataFrame()
        urls = list(self.visited_url.keys())
        titles = list(self.visited_url.values())

        result['TITLE'] = titles
        result['URL'] = urls

        result.to_csv('result.csv', encoding='utf-8-sig')

    # the crawler's logic
    def start_crawling(self, threshold=-1):
        # check to see what level of recursion we are on
        while threshold is not 0:
            this_url = self.queue_url[0]
            self.get_url_list(this_url)

            if len(self.queue_url) == 1:
                break
            else:
                self.queue_url = self.queue_url[1:]

            threshold -= 1

        self.output_result()
        print('DONE!')


# the telemetry data for the crawler
myCrawler = DeepCrawler('https://cnn/')
myCrawler.start_crawling(threshold=25)