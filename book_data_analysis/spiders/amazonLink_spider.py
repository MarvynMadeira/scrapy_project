import scrapy
from datetime import datetime
from book_data_analysis.items import ProductDataItem

#implementar proxies ou um user agent aleatório


class AmazonCollector(scrapy.Spider):
    name = 'amazonLink_spider'
    allowed_domains = ['amazon.com.br', 'amazon.com']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }

    def __init__(self, url=None, *args, **kwargs):
        super(AmazonCollector, self).__init__(*args, **kwargs)
        self.start_urls = [url]

    async def start(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_item, headers=self.headers)

    def getTitle(self, response):
        title = response.xpath('//*[@id="productTitle"]/text()').get().strip()

        return title

    def getCode(self, response):
        if response.xpath('//a[contains(text(), "Kindle")]'):
            code = response.xpath('//*[@id="detailBullets_feature_div"]/ul/li[1]/span/span[2]/text()').get()
        else:
            code = response.xpath('//*[@id="detailBullets_feature_div"]/ul/li[6]/span/span[2]/text()').get()

        return code

    def getCurrency(self, response):
        currency_none = response.xpath('//*[@id="priceBlock-outsideOfForm_feature_div"]/div/div[1]/span[3]/span[2]/span[1]/text()').get()

        if currency_none is not None:
            return currency_none

        currency = response.xpath('//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[3]/span[2]/span[1]/text()').get()

        if currency is not None:
            return currency

        currency = response.xpath('//*[@id="KindleALCLegacy_feature_div"]/div/div[1]/div[1]/div[1]/span[3]/span[2]/span[1]/text()').get()
        return currency

    def getPrice(self, response):
        price_none = response.xpath('//*[@id="priceBlock-outsideOfForm_feature_div"]/div/div[1]/span[3]/span[2]/span[3]/text()').get()

        if price_none is not None:
            return '0'


        price = response.xpath('//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[3]/span[2]/span[2]/text()').get()

        if price is not None:
            return price

        price = response.xpath('//*[@id="KindleALCLegacy_feature_div"]/div/div[1]/div[1]/div[1]/span[3]/span[2]/span[2]/text()').get()
        return price

    def getCent(self, response):
        if self.getPrice(response) == '0':
            return '00'

        cent = response.xpath('//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[3]/span[2]/span[3]/text()').get()

        if cent is not None:
            return cent

        cent = response.xpath('//*[@id="KindleALCLegacy_feature_div"]/div/div[1]/div[1]/div[1]/span[3]/span[2]/span[3]/text()').get()
        return cent

    def priceConvert(self, response):
        price = self.getPrice(response)
        cent = self.getCent(response)

        string = f'{price},{cent}'
        inFloat = float(string.replace(',', '.'))
        inInt = int(inFloat * 100)

        return inInt

    def parse_item(self, response):
        info = response.xpath('//*[@id="bylineInfo"]/span/a/text()').get()

        if info is None:
            self.logger.warning(f"livro não encontrado!!! Por favor, insira uma url de livros...")
            return

        item = ProductDataItem()
        self.logger.info("Extraindo dados do produto")
        item['title'] = self.getTitle(response)
        item['code'] = self.getCode(response)
        item['url'] = response.url
        item['currency'] = self.getCurrency(response)
        item['present_price'] = self.priceConvert(response)
        item['created_at'] = datetime.now()
        print("Item emitido:", item)

        return item


