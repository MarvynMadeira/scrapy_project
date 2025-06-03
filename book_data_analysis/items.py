import scrapy


class ProductDataItem(scrapy.Item):
    title = scrapy.Field()
    code = scrapy.Field()
    url = scrapy.Field()
    currency = scrapy.Field()
    present_price = scrapy.Field()
    created_at = scrapy.Field()
