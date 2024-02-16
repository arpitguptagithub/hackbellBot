from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from playwright.async_api import async_playwright
import scrapy
import os
from DaCrBot.items import SiteDataItem



CHECK_STRING = "binary"

class LinkItem(scrapy.Item):
    url = scrapy.Field()


class SiteCrawlerSpider(CrawlSpider):
    name = "site_crawler"
    allowed_domains = ["www.geeksforgeeks.org"]
    start_urls = ["https://www.geeksforgeeks.org/binary-search/"]


    # Initialise serial number
    serial_number = 0

    # Rules to set for the crawler bot
    rules = (
        Rule(LinkExtractor(allow='/'), callback='parse', follow=True),
    )

    async def parse(self, response):
        data_item = SiteDataItem()

        data = response
        
        if CHECK_STRING in data.text:
            self.serial_number += 1
            data_item['serial_number'] = self.serial_number
            data_item['url'] = response.url

            async with async_playwright() as playwright:
                browser = await playwright.chromium.launch()
                page = await browser.new_page()
                await page.goto(response.url)
                if os.path.isdir('images') : 
                    pass
                else :
                    os.makedirs('images')
                screen_shot_path = os.path.join('images', f"{self.serial_number}")
                await page.screenshot(path=f"{screen_shot_path}.png", full_page=True)
                await browser.close()
            
            yield data_item

        # yield scrapy.Request(item["url"], meta=dict(
        #     playwright=True,
        #     playwright_include_page=True,
        #     errback=self.errback,
        # ))

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()