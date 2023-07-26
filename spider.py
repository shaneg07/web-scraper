import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import json
import math

# FIRST I WANT TO ITERATE THROUGH EVERY CATEGORY 
# THEN I WANT TO GET THE NUMBER OF PAGES IN EACH CATEGORY
# PERHAPS I SHOULD START BY GETTING ALL THE URLS APPENED AT ONCE, BECAUSE 
# CREATE A SEPARATE LIST CONTAINING LINKS OF ALL CATEGORIES - PAGE 1

 #https://www.e.leclerc/api/rest/live-api/product-search?language=fr-FR&size=90&sorts=%5B%5D&page=1&categories=%7B%22code%22:%5B%22NAVIGATION_bon-plan-sport-et-loisir%22%5D%7D

class LsportsSpider(scrapy.Spider):
    name = 'lsports'
    start_urls = ["https://www.e.leclerc/api/rest/live-api/categories-tree-by-code/NAVIGATION_sport-loisirs?pageType=NAVIGATION&maxDepth=undefined"]

    new_start = []

    cnam = ""
    headers = {
        "accept" : "application/json",
        "accept-encoding" : "gzip, deflate, br",
        "accept-language" : "en-US,en;q=0.9",
        "referer" : "https://www.e.leclerc/cat/sport-loisirs",
        "sec-fetch-dest" : "empty",
        "sec-fetch-mode" : "cors",
        "sec-fetch-site" : "same-origin",
        "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "X-Requested-With" : "Fetch",
    }
    catname = []

    def parse(self, response):
        url = "https://www.e.leclerc/api/rest/live-api/categories-tree-by-code/NAVIGATION_sport-loisirs?pageType=NAVIGATION&maxDepth=undefined"

        yield scrapy.Request(url, callback=self.parse_page, headers=self.headers)
    
  
    def parse_page(self, response):

        new_url1 = "https://www.e.leclerc/api/rest/live-api/product-search?language=fr-FR&size=30&sorts=%5B%5D&page="
        new_url2 = "&categories=%7B%22code%22:%5B%22"
        new_url3 = "%22%5D%7D"
        

        raw_data = response.body
        data = json.loads(raw_data)
        x = len(data["children"]) 

        for i in range(0,1):

            self.cnam = data["children"][i]['code']
            pagenum = math.ceil((data["children"][i]['nbProducts'] / 30)) + 1

            for z in range(1,pagenum):

                total_url = new_url1+str(z)+new_url2+str(data["children"][i]['code'])+new_url3
                yield scrapy.Request(total_url, callback=self.parse_page_new, headers=self.headers)
    

    def parse_page_new(self, response):

        new_raw = response.body
        data1 = json.loads(new_raw)

        y = len(data1["items"])
        for varx in range(y):
            yield {
                'name' : data1["items"][varx]['label']
            }