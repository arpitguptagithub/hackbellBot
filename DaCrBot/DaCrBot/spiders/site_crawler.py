from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from playwright.async_api import async_playwright


class LinkItem(scrapy.Item):
    url = scrapy.Field()


class SiteCrawlerSpider(CrawlSpider):
    name = "site_crawler"
    allowed_domains = ["www.port-folio-phi-peach.vercel.app/"]
    start_urls = ["https://port-folio-phi-peach.vercel.app/"]


    # Rules to set for the crawler bot
    rules = (
        Rule(LinkExtractor(allow='/'), callback='parse', follow=True),
    )

    async def parse(self, response):
        data = response
        if "binary" in response.text:
            print("******************************************************************************************************************************************************************************************************")
            print("Found Binary")
            print("******************************************************************************************************************************************************************************************************")
        item = LinkItem()
        item['url'] = response.url
        yield item

        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch()
            page = await browser.new_page()
            await page.goto(item['url'])
            await page.screenshot(path=f"screenshot_{item['url'].replace('/', '_').replace(':', '_')}.png")
            await browser.close()

        yield scrapy.Request(item["url"], meta=dict(
            playwright=True,
            playwright_include_page=True,
            errback=self.errback,
        ))

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()