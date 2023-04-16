import scrapy
import pandas as pd
from urllib.parse import urlencode


API_KEY = ''

def get_proxy_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url
items = []
class AmazonSearchSpider(scrapy.Spider):
    name = "amazon_search" 
    def start_requests(self):
        keyword_list = ["iphone"]
        for keyword in keyword_list:
            amazon_search_url = f'https://www.amazon.com/s?k={keyword}&page=1'
            yield scrapy.Request(url=get_proxy_url(amazon_search_url), callback=self.parse_search_results, meta={'keyword': keyword, 'page': 1})
    def parse_search_results(self, response):
        page = response.meta['page']
        keyword = response.meta['keyword'] 
        search_products = response.css("div.s-result-item[data-component-type=s-search-result]")
        for product in search_products:
            relative_url = product.css("h2>a::attr(href)").get()
            asin = relative_url.split('/')[3] if len(relative_url.split('/')) >= 4 else None
            rating_count = product.css("span[aria-label~=stars] + span::attr(aria-label)").get()
            if(rating_count == None):
                rating_count = None
            else:
                people_rate = ''.join(people_rate.split(','))
            item =  {
                    "keyword": keyword,
                    "asin": asin,
                    "title": product.css("h2>a>span::text").get(),
                    "price": product.css(".a-price[data-a-size=xl] .a-offscreen::text").get(),
                    "real_price": product.css(".a-price[data-a-size=b] .a-offscreen::text").get(),
                    "rating": (product.css("span[aria-label~=stars]::attr(aria-label)").re(r"(\d+\.*\d*) out") or [None])[0],
                    "rating_count": rating_count,
                }
            items.append(item)
        if page == 1:
            available_pages = response.xpath(
                '//*[contains(@class, "s-pagination-item")][not(has-class("s-pagination-separator"))]/text()'
            ).getall()

            last_page = available_pages[-1]
            for page_num in range(2, int(last_page)):
                amazon_search_url = f'https://www.amazon.com/s?k={keyword}&page={page_num}'
                yield scrapy.Request(get_proxy_url(amazon_search_url), callback=self.parse_search_results, meta={'keyword': keyword, 'page': page_num})
        
    def closed(self, response):
        df = pd.DataFrame.from_dict(items, orient='columns')
        sorted_df = df.sort_index(ascending=True) 
        sorted_df.to_csv("products.csv")
    
        
