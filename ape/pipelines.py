# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
import pymysql

class ApePipeline(object):
    def process_item(self, item, spider):
        def process_title(title, item):
            author, music = title.split(' - ')
            music, file_format = music.split('.')
            item['author']  = author
            item['music'] = music
            item['file_format'] = file_format

        def process_info(info, item):
            for data in info:
                if re.search(r'^选自专辑', data):
                    item['album'] = data
                elif re.search(r'Kbps$', data):
                    match = re.search(r'\d+', data)
                    if match:
                        item['bits'] = data
                    else:
                        item['bits'] = None
                elif re.search(r'[\d.]+M', data):
                    item['size'] = data
                elif re.search(r'\d{4}-\d{2}-\d{2}', data):
                    item['date'] = data
                else:
                    item['language'] = data
        
        def process_pasword(password, item):
            match = re.search(r'[\w]+$', password)
            if match:
                item['download_password'] = match.group()
            else:
                item['download_password'] = None

        title = item['title']
        info = item['info']
        password = item['download_password']

        process_title(title, item)
        process_info(info, item)
        process_pasword(password, item)

        return item


class MySQLPipeline:
    table_name = 'music'
    insert_sql = f'insert into {table_name} (author, music, album, bits, size, format, url, password) values\
        (%s, %s, %s, %s, %s, %s, %s, %s)'

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            crawler.settings.get('MYSQL_HOST', 'localhost'),
            crawler.settings.get('MYSQL_UESR'),
            crawler.settings.get('MYSQL_PASSWORD'),
            crawler.settings.get('MYSQL_DATABASE', '51ape'),
        )

    def open_spider(self, spider):
        self.connect = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8mb4')
        self.cursor = self.connect.cursor()

    def close_spider(self, spider):
        self.connect.close()
    
    def process_item(self, item, spider):
        self.cursor.execute(self.insert_sql, (item['author'], item['music'], item['album'], item['bits'], 
                                    item['size'], item['file_format'], item['download_url'], item['download_password']))
        self.connect.commit()
        return item
