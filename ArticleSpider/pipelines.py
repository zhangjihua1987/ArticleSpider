# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs


import MySQLdb
import MySQLdb.cursors
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class ArticleJsonExport(object):
    """
    使用原生方式导出json
    """
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        """
        处理item的函数
        函数名，参数都是固定的写法
        """
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def spider_closed(self, spiser):
        """
        spider关闭后的处理函数
        函数名，参数都是固定的写法
        """
        self.file.close()


class JasonExporterPipeline(object):
    """
    使用Exportor导出json文件
    """
    def __init__(self):
        self.file = open('article_exporter.json', 'wb')

        # 生成一个scrapy的Exporter实例
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        # 关闭导出
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item



class ArticleImagesPipeline(ImagesPipeline):
    """
    处理图片的pipeline
    继承scrapy自带的ImagesPipeline
    重构其item_completed方法
    """

    def item_completed(self, results, item, info):
        for status, value in results:
            item['front_image_path'] = value['path']
        return item


class MysqlPipeline(object):
    """
    用原生同步的方式将item写入mysql
    """
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'xuecheng871144', 'article_spider', charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into jobbole_article(title, create_date, url, fav_nums, url_object_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item['title'], item['create_date'], item['url'], item['fav_nums'], item['url_object_id']))
        self.conn.commit()
        return item


class MysqlTwistedPipeline(object):
    """
    利用twisted异步将数据写入数据库
    """
    def __init__(self, db_pool):
        self.db_pool = db_pool

    @classmethod
    def from_settings(cls, settings):

        # 以下变量名称要与MySQLdb.connetion.Connetion中的参数名称一直
        db_params = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )

        db_pool = adbapi.ConnectionPool('MySQLdb', **db_params)
        return cls(db_pool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变为异步执行
        query = self.db_pool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)  # 异常处理

    def handle_error(self, failure):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql = """
                 insert into jobbole_article(title, create_date, url, fav_nums, url_object_id)
                 VALUES (%s, %s, %s, %s, %s)
             """
        cursor.execute(insert_sql, (item['title'], item['create_date'], item['url'], item['fav_nums'], item['url_object_id']))
