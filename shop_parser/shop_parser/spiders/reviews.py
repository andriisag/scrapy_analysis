import scrapy
from urllib.parse import urljoin
from urllib.parse import urlencode
import pandas as pd


API_KEY = ''

def get_proxy_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url


items = []
class AmazonReviewsSpider(scrapy.Spider):
    name = "amazon_reviews"

    def start_requests(self):
        asin_list = ['B09G9FPHY6']
        for asin in asin_list:
            amazon_reviews_url = f'https://www.amazon.com/product-reviews/{asin}/'
            yield scrapy.Request(url=get_proxy_url(amazon_reviews_url), callback=self.parse_reviews, meta={'asin': asin, 'retry_count': 0})


    def parse_reviews(self, response):
        asin = response.meta['asin']
        retry_count = response.meta['retry_count']

        next_page_relative_url = response.css(".a-pagination .a-last>a::attr(href)").get()
        if next_page_relative_url is not None:
            retry_count = 0
            next_page = urljoin('https://www.amazon.com/', next_page_relative_url)
            yield scrapy.Request(url=get_proxy_url(next_page), callback=self.parse_reviews, meta={'asin': asin, 'retry_count': retry_count})

        
        elif retry_count < 3:
            retry_count = retry_count+1
            yield scrapy.Request(url=get_proxy_url(response.url), callback=self.parse_reviews, dont_filter=True, meta={'asin': asin, 'retry_count': retry_count})


        
        review_elements = response.css("#cm_cr-review_list div.review")
        for review_element in review_elements:
            people_rate_get = review_element.css("span[data-hook=helpful-vote-statement] ::text").get()
            if(people_rate_get == None):
                people_rate = None
            elif(people_rate_get != None and people_rate_get.split()[0] == "One"):
                 people_rate = "1"
            else:
                people_rate = people_rate_get.split()[0] 
       
            
            item = {
                    "asin": asin,
                    "text": "".join(review_element.css("span[data-hook=review-body] ::text").getall()).strip(),
                    "title": review_element.css("*[data-hook=review-title]>span::text").get(),
                    "location_and_date": review_element.css("span[data-hook=review-date] ::text").get(),
                    "verified": bool(review_element.css("span[data-hook=avp-badge] ::text").get()),
                    "rating": review_element.css("*[data-hook*=review-star-rating] ::text").re(r"(\d+\.*\d*) out")[0],
                    "people_rate": people_rate
                    }
            items.append(item)


    def closed(self, response):
        df = pd.DataFrame.from_dict(items, orient='columns')
        sorted_df = df.sort_index(ascending=True) 
        sorted_df.to_csv("reviews.csv")
        
    
    
