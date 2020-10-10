# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import decimal
from scrapy.loader.processors import Compose
from scrapy.loader import ItemLoader


class CrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ANNONCE_LINK=scrapy.Field()
    FROM_SITE=scrapy.Field()
    ID_CLIENT=scrapy.Field()
    ANNONCE_DATE=scrapy.Field()
    ACHAT_LOC=scrapy.Field()
    SOLD=scrapy.Field()
    MAISON_APT=scrapy.Field()
    CATEGORIE=scrapy.Field()
    NEUF_IND=scrapy.Field()
    NOM=scrapy.Field()
    ADRESSE=scrapy.Field()
    CP=scrapy.Field()
    VILLE=scrapy.Field()
    QUARTIER=scrapy.Field()
    DEPARTEMENT=scrapy.Field()
    REGION=scrapy.Field()
    PROVINCE=scrapy.Field()
    ANNONCE_TEXT=scrapy.Field()
    ETAGE=scrapy.Field()
    NB_ETAGE=scrapy.Field()
    LATITUDE=scrapy.Field()
    LONGITUDE=scrapy.Field()
    M2_TOTALE=scrapy.Field()
    SURFACE_TERRAIN=scrapy.Field()
    NB_GARAGE=scrapy.Field()
    PHOTO=scrapy.Field()
    PIECE=scrapy.Field()
    PRIX=scrapy.Field()
    PRIX_M2=scrapy.Field()
    URL_PROMO=scrapy.Field()
    STOCK_NEUF=scrapy.Field()
    PAYS_AD=scrapy.Field()
    PRO_IND=scrapy.Field()
    SELLER_TYPE=scrapy.Field()
    MINI_SITE_URL=scrapy.Field()
    MINI_SITE_ID=scrapy.Field()
    AGENCE_NOM=scrapy.Field()
    AGENCE_ADRESSE=scrapy.Field()
    AGENCE_CP=scrapy.Field()
    AGENCE_VILLE=scrapy.Field()
    AGENCE_DEPARTEMENT=scrapy.Field()
    EMAIL=scrapy.Field()
    WEBSITE=scrapy.Field()
    AGENCE_TEL=scrapy.Field()
    AGENCE_TEL_2=scrapy.Field()
    AGENCE_TEL_3=scrapy.Field()
    AGENCE_TEL_4=scrapy.Field()
    AGENCE_FAX=scrapy.Field()
    AGENCE_CONTACT=scrapy.Field()
    PAYS_DEALER=scrapy.Field()
    FLUX=scrapy.Field()
    SIREN=scrapy.Field()
    SITE_SOCIETE_URL=scrapy.Field()
    SITE_SOCIETE_ID=scrapy.Field()
    SITE_SOCIETE_NAME=scrapy.Field()
    SPIR_ID=scrapy.Field()
    AUTRE=scrapy.Field()

"""
def prix_in_processor(value):
    tmp = value[0]
    try:
        return str(decimal.Decimal(tmp) / 19) # instead of 1000
    except:
        return '0'

def surface_in_processor(value):
    tmp = value[0]
    try:
        if float(tmp) > 99999999:
            return '99999999'
        else:
            return tmp
    except:
        return '0'
"""


class CrawlLoader(ItemLoader):
    pass
"""
    PRIX_in = Compose(prix_in_processor)
    M2_TOTALE_in = Compose(surface_in_processor)
    SURFACE_TERRAIN_in = Compose(surface_in_processor)
"""
