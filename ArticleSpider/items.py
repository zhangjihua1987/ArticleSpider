# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import re
import datetime


import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from scrapy.loader import ItemLoader


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, '%Y/%m/%d').date()
    except Exception as e:
        create_date = datetime.datetime.now()
    return create_date


def date_match(value):
    create_date = re.match('[\w\W]*?(\d{4}/\d{1,2}/\d{1,2})[\w\W]*', value)
    create_date = create_date[1] if create_date else ''
    return create_date


def nums_match(value):
    nums = re.match('[\w\W]*?(\d+)[\w\W]*', value)
    nums = nums[1] if nums else 0
    return nums


def tags_join(value):
    tags = ','.join(value)
    return tags


def return_value(value):
    return value


class JobBoleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field(
        input_processor=MapCompose(lambda x: x + '-jobbole',),
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    front_image_path = scrapy.Field()
    create_date = scrapy.Field(
        input_processor=MapCompose(date_match, date_convert),
    )
    tags = scrapy.Field(
        output_processor=Join(','),
    )
    content = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor=MapCompose(nums_match)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(nums_match)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(nums_match)
    )
