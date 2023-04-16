
BOT_NAME = 'shop_parser'

SPIDER_MODULES = ['shop_parser.spiders']
NEWSPIDER_MODULE = 'shop_parser.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

SCRAPEOPS_API_KEY = ''
HTTPERROR_ALLOWED_CODES = [404]
HTTPERROR_ALLOWED_CODES = [405] 
HTTPERROR_ALLOWED_CODES = [401]

SCRAPEOPS_PROXY_ENABLED = True
# SCRAPEOPS_PROXY_SETTINGS = {'country': 'us'}

# Add In The ScrapeOps Monitoring Extension
EXTENSIONS = {
'scrapeops_scrapy.extension.ScrapeOpsMonitor': 500, 
}

LOG_LEVEL = 'INFO'

DOWNLOADER_MIDDLEWARES = {

    ## ScrapeOps Monitor
    'scrapeops_scrapy.middleware.retry.RetryMiddleware': 550,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    
    ## Proxy Middleware
    'scrapeops_scrapy_proxy_sdk.scrapeops_scrapy_proxy_sdk.ScrapeOpsScrapyProxySdk': 725,
}

# Max Concurrency On ScrapeOps Proxy Free Plan is 1 thread
CONCURRENT_REQUESTS = 1