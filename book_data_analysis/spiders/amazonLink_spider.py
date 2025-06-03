import scrapy
from datetime import datetime
from book_data_analysis.items import ProductDataItem


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

    async def getCurrency(self, response):
        currency = response.xpath('//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[3]/span[2]/span[1]/text()').get()

        if currency is not None:
            return currency

        currency = response.xpath('//*[@id="KindleALCLegacy_feature_div"]/div/div[1]/div[1]/div[1]/span[3]/span[2]/span[1]/text()').get()
        return currency

        ## fazer com todos que tem 2 xpath possíveis e com o price amanhã.


    async def parse_item(self, response):
        info = response.xpath('//*[@id="bylineInfo"]/span/a/text()').get()

        if info is None:
            self.logger.warning(f"livro não encontrado!!! Por favor, insira uma url de livros...")
            return

        item = ProductDataItem()
        self.logger.info("Extraindo dados do produto")
        item['title'] = response.xpath('//*[@id="productTitle"]/text()').get().strip()
        item['code'] = response.xpath('//*[@id="detailBullets_feature_div"]/ul/li[6]/span/span[2]/text()', '//*[@id="detailBullets_feature_div"]/ul/li[1]/span/span[2]/text()').get()
        item['url'] = response.url
        item['currency'] = self.getCurrency(response)
        valueItem = response.xpath('//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[3]/span[2]/span[2]/text()', '//*[@id="KindleALCLegacy_feature_div"]/div/div[1]/div[1]/div[1]/span[3]/span[2]/span[2]/text()').get()
        centItem = response.xpath('//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[3]/span[2]/span[3]/text()', '//*[@id="KindleALCLegacy_feature_div"]/div/div[1]/div[1]/div[1]/span[3]/span[2]/span[3]/text()').get()
        price_string = f'{valueItem},{centItem}'
        price_float = float(price_string.replace(',', '.'))
        price_convert = int(price_float * 100)
        item['present_price'] = price_convert
        item['created_at'] = datetime.now()
        print("Item emitido:", item)

        return item


