# -*- coding: utf-8 -*-
import scrapy

from yangguang.items import YangguangItem
import logging


logger = logging.getLogger(__name__)

class YgSpider(scrapy.Spider):
    name = 'yg'
    allowed_domains = ['sun0769.com']
    start_urls = ['http://wz.sun0769.com/index.php/question/questionType?type=4&page=0']

    def parse(self, response):
        # 分组
        tr_list = response.xpath("//div[@class='greyframe']/table[2]/tr/td/table/tr")
        for tr in tr_list:
            item = YangguangItem()
            item["title"] = tr.xpath("./td[2]/a[@class='news14']/text()").extract_first()
            item["href"] = tr.xpath("./td[2]/a[@class='news14']/@href").extract_first()
            item["publish_date"] = tr.xpath("./te[last()]/text()").extract_first()

            yield scrapy.Request(
                item["href"],
                callback=self.parse_detail,
                meta={"item":item}
            )

    def parse_detail(self, response):
        item = response.meta["item"]
        item["content"] = response.xpath("//td[@class='txt16_3']/text()").extract()
        item["content_img"] = response.xpath("//td[@class='txt16_3']//img/@src").extract()
        item["content_img"] = ["http://wz.sun0769.com" + i for i in item["content_img"]]
        logger.warning(item)