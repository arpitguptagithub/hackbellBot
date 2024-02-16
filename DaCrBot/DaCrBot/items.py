import scrapy



class SiteDataItem(scrapy.Item) :

    serial_number = scrapy.Field()
    url = scrapy.Field()