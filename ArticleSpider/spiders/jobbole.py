# -*- coding: utf-8 -*-
import scrapy
import re
import datetime

from scrapy.http import Request
from scrapy.loader import ItemLoader
from urllib import parse

from ArticleSpider.items import JobBoleArticleItem, JobBoleItemLoader
from ArticleSpider.utils.common import get_md5


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1. 获取文章列表页中的url，并交给scray下载后进行解析
        2. 获取下一页的url并交给scrapy进行下载，下载完成后交给parse
        """

        post_nodes = response.css('div#archive div.floated-thumb div.post-thumb a')
        for post_node in post_nodes:
            front_image_url = post_node.css('img::attr(src)').extract_first('')
            post_url = post_node.css('::attr(href)').extract_first('')
            yield Request(url=parse.urljoin(response.url, post_url),
                          meta={
                              'front_image_url': parse.urljoin(response.url, front_image_url)
                          },
                          callback=self.parse_detail)

        next_page_url = response.css('a.page-numbers.next::attr(href)').extract_first('')
        if next_page_url:
            yield Request(url=parse.urljoin(response.url, next_page_url), callback=self.parse)

    def parse_detail(self, response):
        """
        解析详情页的函数
        """
        # item = JobBoleArticleItem()

        # # 使用xpath提取字段
        # title = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0]
        # create_time = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip().split(' ')[0]
        # praise_nums = response.xpath('//h10[@id="114050votetotal"]/text()').extract()[0]
        # praise_nums = praise_nums if praise_nums else '0'
        # fav_nums = response.xpath('//span[contains(@class, "bookmark-btn")]/text()').extract()[0].replace('收藏', '').strip()
        # fav_nums = fav_nums if fav_nums else '0'
        # comment_nums = response.xpath('//span[@class="btn-bluet-bigger href-style hide-on-480"]/text()').extract()[0].replace('评论', '').strip()
        # comment_nums = comment_nums if comment_nums else '0'
        # content = response.xpath('//div[@class="entry"]').extract()[0]
        # tag_list = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        # tag = ','.join(tag_list)

        # # 用css选择器筛选字段
        # title = response.css('.entry-header h1::text').extract_first('')
        # front_image_url = response.meta.get('front_image_url', '')
        # create_date = response.css('.entry-meta-hide-on-mobile::text').extract_first('')
        # create_date = re.match('[\w\W]*?(\d{4}/\d{1,2}/\d{1,2})[\w\W]*', create_date)
        # create_date = create_date[1] if create_date else ''
        # tag_list = response.css('.entry-meta-hide-on-mobile a::text').extract()
        # tags = ','.join(tag_list)
        # content = response.css('.entry').extract()[0]
        # praise_nums = response.css('#114050votetotal::text').extract_first('')
        # praise_nums = int(praise_nums) if praise_nums else 0
        # fav_nums = response.css('.bookmark-btn::text').extract_first('')
        # fav_nums = re.match('.*?(\d+).*', fav_nums)
        # fav_nums = int(fav_nums[1]) if fav_nums else 0
        # comment_nums = response.css('span.href-style.hide-on-480::text').extract_first('')
        # comment_nums = re.match('.*?(\d+).*', comment_nums)
        # comment_nums = int(comment_nums[1]) if comment_nums else 0
        #
        # try:
        #     create_date = datetime.datetime.strptime(create_date, '%Y/%m/%d').date()
        # except Exception as e:
        #     create_date = datetime.datetime.now()
        #
        # item['title'] = title
        # item['url'] = response.url
        # item['front_image_url'] = [front_image_url]
        # item['create_date'] = create_date
        # item['tags'] = tags
        # item['content'] = content
        # item['praise_nums'] = praise_nums
        # item['fav_nums'] = fav_nums
        # item['comment_nums'] = comment_nums
        # item['url_object_id'] = get_md5(response.url)

        # 用item_loader提取字段值
        front_image_url = response.meta.get('front_image_url', '')
        item_loader = JobBoleItemLoader(item=JobBoleArticleItem(), response=response)
        item_loader.add_css('title', '.entry-header h1::text')
        item_loader.add_value('url', response.url)
        item_loader.add_value('front_image_url', [front_image_url])
        item_loader.add_css('create_date', '.entry-meta-hide-on-mobile::text')
        item_loader.add_css('tags', '.entry-meta-hide-on-mobile a::text')
        item_loader.add_css('content', '.entry')
        item_loader.add_css('praise_nums', '#114050votetotal::text')
        item_loader.add_css('fav_nums', '.bookmark-btn::text')
        item_loader.add_css('comment_nums', 'span.href-style.hide-on-480::text')
        item_loader.add_value('url_object_id', get_md5(response.url))

        item = item_loader.load_item()

        yield item


