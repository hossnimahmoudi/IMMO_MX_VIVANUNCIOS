# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
from scrapy.exporters import CsvItemExporter
from csv import QUOTE_ALL
from scrapy.mail import MailSender
import datetime
from scrapy.utils.project import get_project_settings
import socket
import logging
from twisted.python.failure import Failure
from scrapy.utils.request import referer_str
import time
import pprint

class VivanunPipeline(object):
    def __init__(self):
        self.files = {}
    @classmethod
    def from_crawler(cls, crawler):
       pipeline = cls()
       crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
       crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)


       return pipeline

    def spider_opened(self, spider):
       mailer = MailSender(mailfrom="h.mahmoudi@autobiz.com")
       settings = get_project_settings()
       hostname = socket.gethostname()
       body='''-Crawl name: {0}\n-Cache directory: {1}\n-Hostname : {2} \n-Crawler name Hosni Mahmoudi '''.format(settings.get('BOT_NAME'),settings.get('HTTPCACHE_DIR'),hostname,
       )
       mailer.send(to=["h.mahmoudi@autobiz.com"], subject="The crawl of %s is %s " % (spider.name, "launched"), body=body )
       file = open('%s.csv' % spider.name, 'w+b')
       self.files[spider] = file
       self.exporter = CsvItemExporter(file, delimiter=';', quotechar='"', quoting=QUOTE_ALL)
       self.exporter.start_exporting()
       #self.exporter.fields_to_export =['ANNONCE_LINK','NEUF_IND']
       self.exporter.fields_to_export = ["ANNONCE_LINK", "FROM_SITE", "ID_CLIENT", "ANNONCE_DATE", "ACHAT_LOC", "SOLD", "MAISON_APT", "CATEGORIE", "NEUF_IND", "NOM", "ADRESSE", "CP", "VILLE", "QUARTIER", "DEPARTEMENT", "REGION", "PROVINCE", "ANNONCE_TEXT", "ETAGE", "NB_ETAGE", "LATITUDE", "LONGITUDE", "M2_TOTALE", "SURFACE_TERRAIN", "NB_GARAGE", "PHOTO", "PIECE", "PRIX", "PRIX_M2", "URL_PROMO", "STOCK_NEUF", "PAYS_AD", "PRO_IND", "SELLER_TYPE", "MINI_SITE_URL", "MINI_SITE_ID", "AGENCE_NOM", "AGENCE_ADRESSE", "AGENCE_CP", "AGENCE_VILLE", "AGENCE_DEPARTEMENT", "EMAIL", "WEBSITE", "AGENCE_TEL", "AGENCE_TEL_2", "AGENCE_TEL_3", "AGENCE_TEL_4", "AGENCE_FAX", "AGENCE_CONTACT", "PAYS_DEALER", "FLUX", "SITE_SOCIETE_URL", "SITE_SOCIETE_ID", "SITE_SOCIETE_NAME", "AGENCE_RCS", "SPIR_ID"]


    def spider_closed(self, spider, reason):
       mailer = MailSender()
       pige = 370000
       intro = "Summary stats from Scrapy spider: \n\n"
       stats = spider.crawler.stats.get_stats()
       comptage = stats.get('item_scraped_count')
       pourcentage = comptage * 100 /pige
       body = intro +"Finish reason : " + reason +"\n" + "Item scraped count : " + str(comptage) +"\n" +"Le comptage a atteint " + str(pourcentage) +"%\n"
       mailer.send(to=["h.mahmoudi@autobiz.com","a.bouyahya@autobiz.com","k.abidi@autobiz.com","m.jami@autobiz.com"], subject="The crawl of %s is %s " % (spider.name, reason), body=body )
       self.exporter.finish_exporting()
       file = self.files.pop(spider)
       file.close()

    def process_item(self, item, spider):
       self.exporter.export_item(item)
       return item

