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

    # Initialise serial number and iteration counter
    serial_number = 0
    max_iterations = 100  # Maximum allowed iterations

    # Flag to track completion of ongoing tasks
    ongoing_tasks = 0

    # Flag to track if the maximum limit has been reached
    max_limit_reached = False


    # Rules to set for the crawler bot
    rules = (
        Rule(LinkExtractor(allow='/'), callback='parse', follow=True),
    )

    async def parse(self, response):
        if self.max_limit_reached:
            return

        data_item = SiteDataItem()

        data = response

        if CHECK_STRING in data.text:
            self.serial_number += 1
            data_item['serial_number'] = self.serial_number
            data_item['url'] = response.url

            self.ongoing_tasks += 1

            async with async_playwright() as playwright:
                browser = await playwright.chromium.launch()
                page = await browser.new_page()
                await page.goto(response.url)
                if os.path.isdir('images'):
                    pass
                else:
                    os.makedirs('images')
                screen_shot_path = os.path.join(
                    'images', f"{self.serial_number}")
                await page.screenshot(path=f"{screen_shot_path}.png", full_page=True)
                await browser.close()

            self.ongoing_tasks -= 1
            yield data_item

            # Check if maximum iterations reached
            if self.serial_number >= self.max_iterations and self.ongoing_tasks == 0:
                self.crawler.engine.close_spider(
                    self, 'Reached maximum iterations')
            elif self.serial_number == self.max_iterations:
                self.max_limit_reached = True

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
