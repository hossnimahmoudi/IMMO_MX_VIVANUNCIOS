# -*- coding: utf-8 -*-
import scrapy
import datetime
import re
import requests

from immo_viva.mhelpers import extract_from, get_item
from immo_viva.items import CrawlItem, CrawlLoader

FROM_SITE = 'vivanuncios'
MX = 'MX'



class ImmoSpider(scrapy.Spider):
#class DirectrSpider(CrawlSpider):
    name = "IMMO_MX_VIVANUNCIOS_2020_09"
    allowed_domains = ["vivanuncios.com.mx"]
    start_urls = [
                  'https://www.vivanuncios.com.mx/vip_index.xml',
                  'https://www.vivanuncios.com.mx/sitemap_index.xml',
                  'https://www.vivanuncios.com.mx/sitemap_loccat.xml',
                  'https://www.vivanuncios.com.mx/sitemap_loccatatt.xml'
                  ]

    def parse(self,response):
        for url in self.start_urls:
            xml_list = re.findall("(https[^<>\"]+)", response.text)
            for xml in xml_list:
               response1 = requests.get(xml).text
               ads_list = re.findall("(https[^<>\"]+)", response1)
               for link_annonce in ads_list:
                   if "www.vivanuncios.com.mx/a-" in link_annonce:
                      if "a-venta-inmuebles" in str(link_annonce) or "a-venta-terrenos" in str(link_annonce) or "a-renta-inmuebles" in str(link_annonce) or "a-renta-cuartos" in str(link_annonce) or  "a-oficinas+consultorios" in str(link_annonce) or  "a-locales-comerciales" in str(link_annonce) or  "a-traspasos" in str(link_annonce) or  "a-bodegas" in str(link_annonce) or  "a-otros-bienes-raices" in str(link_annonce): 
                         yield{"ANNONCE_LINK":link_annonce}
                   elif "www.vivanuncios.com.mx/s-" in link_annonce:
                       yield scrapy.Request(url=link_annonce, callback=self.parse_page)
    def parse_page(self,response):
        base_url="https://www.vivanuncios.com.mx"
        liste_annonces=response.xpath("//a[@class='href-link tile-title-text']/@href").extract()
        for annonce in liste_annonces:
            link_annonce = base_url+str(annonce)
            if "a-venta-inmuebles" in str(link_annonce) or "a-venta-terrenos" in str(link_annonce) or "a-renta-inmuebles" in str(link_annonce) or "a-renta-cuartos" in str(link_annonce) or  "a-oficinas+consultorios" in str(link_annonce) or  "a-locales-comerciales" in str(link_annonce) or  "a-traspasos" in str(link_annonce) or  "a-bodegas" in str(link_annonce) or  "a-otros-bienes-raices" in str(link_annonce): 
                 #yield{"ANNONCE_LINK":link_annonce}
                 yield scrapy.Request(url=link_annonce,callback=self.parse_details,dont_filter=False)

        next_page=response.xpath("//link[contains(@rel ,'next')]/@href").extract_first()
        if next_page is not None:
            next_page=base_url+str(next_page)
            yield scrapy.Request(url=next_page,callback=self.parse_page)


    def parse_details(self, response):
        loader = CrawlLoader(CrawlItem(), response)

        loader.add_value('ANNONCE_LINK', response.url)

        loader.add_value('FROM_SITE', FROM_SITE)

        #loader.add_xpath('ID_CLIENT', '//span[@class="edit-favorite-icon favorite-icon icon-heart-gray"]/@data-short-adid')
        #id_client=str(response.url).split('/')[-1]
        id_client=str(re.findall('"a":{"id":"(.*?)"',response.text))
        id_client=" ".join(re.findall('\d+',id_client))
        loader.add_value('ID_CLIENT',id_client)

        # ACHAT_LOC

        tmp1 = response.xpath("//li[contains(text(),'Tipo')]/a/text()").extract_first()
        if tmp1 is not None:

            tmp1=tmp1.strip().split(',')[0]
        else :
            tmp1=""
        tmp2 = response.xpath("//li[contains(text(),'Vender/Rentar')]/a/text()").extract_first()
        #tmp3=response.xpath('//ol/li/p/text()').extract()
        #tmp4=response.xpath('//ol/li/text()').extract()
        tmp5=response.url
        tmp6=response.xpath("//h1/text()").extract_first()
        #CATEGORIE

    
        if "/a-bodegas" in response.url:
           categorie = "Bodega"
        elif "/a-locales-comerciales" in response.url:
             categorie = "Locales comerciales"
        elif "/a-venta-terrenos" in response.url:
             categorie = "Terrenos"
        elif "/a-renta-cuartos" in response.url:
             categorie = "Cuartos"
        elif "/a-oficinas+consultorios" in response.url:
             categorie = "Oficinas y Consultorios"
        elif "/a-rentas-vacacionales" or "/a-otros-bienes-raices" or "/a-venta-inmuebles" or "/a-renta-inmuebles" in response.url:
            try:
              tipo = response.xpath("//ol/li[contains(text(),'Tipo')]/a/text()").extract_first().split(",")[0]
            except:
                tipo = ""
            if tipo is not None and len(tipo)>0:
               if tipo == "Casas Vacacionales":
                  categorie = "Casas"
               elif tipo == "Departamentos vacacionales":
                    categorie = "Departamentos"
               elif tipo == "Casa":
                    categorie = "Casa"
               elif tipo == "Quintas":
                    categorie = "Quintas"
               elif tipo == "Villas":
                    categorie = "Villas"
               elif tipo == "Viñedo":
                    categorie = "Viñedos"
               elif tipo == "Haciendas":
                    categorie = "Haciendas"
               elif tipo == "Casa":
                    categorie = "Casa"
               elif tipo == "Quintas":
                    categorie = "Quintas"
               elif tipo == "Villas":
                    categorie = "Villas"
               elif tipo == "Haciendas":
                    categorie = "Haciendas"
               elif tipo == "Departamentos en Venta":
                    categorie = "Departamentos"
               elif tipo == "Casas en Venta":
                    categorie = "Casas"
               elif tipo == "Desarrollos":
                    categorie = "Desarrollos"
               elif tipo == "Departamentos en Renta":
                    categorie = "Departamentos"
               elif tipo == "Casas en Renta":
                    categorie = "Casas"
               elif tipo == "Desarrollos":
                    categorie = "Desarrollos"
               else:
                   categorie = "Departamentos"
            else:
              categorie = "Departamentos"
        else:
           categorie = ""
        loader.add_value('CATEGORIE', categorie)


        #MAISON_APT
        maison_apt=""
        if categorie=="Bodegas":
           maison_apt="16"
        elif categorie=="Bodega":
           maison_apt="16"
        elif categorie=="Bodegas en Renta":
           maison_apt="16"
        elif categorie=="Bodegas en Venta":
           maison_apt="16"
        elif categorie=="Casa":
           maison_apt="1"
        elif categorie=="Casas":
           maison_apt="1"
        elif categorie=="Casas en Renta":
           maison_apt="1"
        elif categorie=="Casas en Venta":
           maison_apt="1"
        elif categorie=="Casas Vacacionales":
           maison_apt="41"
        elif categorie=="Cuartos en Renta":
           maison_apt="2"
        elif categorie=="Departamento":
           maison_apt="2"
        elif categorie=="Departamentos":
            maison_apt="2"
        elif categorie=="Departamentos en Renta":
           maison_apt="2"
        elif categorie=="Departamentos en Venta":
           maison_apt="2"
        elif categorie=="Departamentos Vacacionales":
           maison_apt="41"
        elif categorie=="Desarrollo":
           maison_apt="8"
        elif categorie=="Locales Comerciales":
           maison_apt="17"
        elif categorie=="Locales comerciales":
            maison_apt="17"
        elif categorie=="Oficinas y Consultorios":
           maison_apt="19"
        elif categorie=="Otros":
           maison_apt="8"
        elif categorie=="Terrenos en Venta":
           maison_apt="6"
        elif categorie=="Haciendas":
           maison_apt="33"
        elif categorie=="Quintas":
           maison_apt="33"
        elif categorie=="Villas":
           maison_apt="1"
        elif categorie=="Cuartos":
           maison_apt="2"
        elif categorie=="Terrenos":
           maison_apt="6"  
  
        loader.add_value('MAISON_APT', maison_apt)
  
        # ACHAT_LOC 
        tmp1 = response.xpath("//li[contains(text(),'Tipo')]/a/text()").extract_first()
        tmp2 = response.xpath("//li[contains(text(),'Vender/Rentar')]/a/text()").extract_first()
        tmp5=response.url
        if tmp1 is not None:
            tmp1=tmp1.split(",")[0]
        else :
            tmp1=""
        if tmp2 is not None:
            tmp2=tmp2
        else:
            tmp2=""
            
        #ACHAT_LOC
        
        if "/a-rentas-vacacionales" in response.url:  
           achat_loc ="8"
        elif "/a-renta-inmuebles" in response.url: 
             achat_loc ="2"
        elif "/a-venta-inmuebles" in response.url:  
             achat_loc ="1"
        elif "/a-venta-terrenos" in response.url:   
             achat_loc ="1"
        elif "/a-renta-cuartos" in response.url:    
              achat_loc ="6"

        elif "/a-bodegas" in response.url:  
          try:
            loc = response.xpath("//li[contains(text(),'Vender/Rentar')]/a/text()").extract_first()
          except:
              loc =""
          if loc is not None and "Renta" in loc:
             achat_loc ="2"
          elif loc is not None and "Venta" in loc:
               achat_loc ="1"
          else:
            #achat_loc =""
            try: 
               nom = response.xpath("//h1/text()").extract_first()
            except:
               nom =""
            if "venta" in response.url or "vender" in response.url or "se vende" in response.url or "vendo" in response.url or "traspaso" in response.url:  
               achat_loc ="1"
            elif "venta" in nom or "vender" in nom or "se vende" in nom or "vendo" in nom or "traspaso" in nom:  
              achat_loc ="1"
            elif "renta" in response.url or "rentar" in response.url or "rento" in response.url:  
              achat_loc ="2"
            elif "RENTA" in nom or "renta" in nom or "rentar" in nom or "rento" in nom:
               achat_loc ="2"
            else:
              achat_loc =""

        elif "/a-locales-comerciales" in response.url:  
          try:
            loc = response.xpath("//li[contains(text(),'Vender/Rentar')]/a/text()").extract_first()
          except:
             loc = ""
          if loc is not None and "Renta" in loc:
             achat_loc ="2"
          elif loc is not None and "Venta" in loc:
               achat_loc ="1"
          else:
               #achat_loc =""
             try: 
               nom = response.xpath("//h1/text()").extract_first()
             except:
                nom =""
             if "venta" in response.url or "vender" in response.url or "se vende" in response.url or "vendo" in response.url or "traspaso" in response.url:  
               achat_loc ="1"
             elif "venta" in nom or "vender" in nom or "se vende" in nom or "vendo" in nom or "traspaso" in nom:  
                achat_loc ="1"
             elif "renta" in response.url or "rentar" in response.url or "rento" in response.url:  
                achat_loc ="2"
             elif "RENTA" in nom or "renta" in nom or "rentar" in nom or "rento" in nom:
                achat_loc ="2"
             else:
               achat_loc =""

        elif "/a-otros-bienes-raices" or "/a-oficinas+consultorios" in response.url: 
             try: 
               nom = response.xpath("//h1/text()").extract_first()
             except:
                nom =""
             if "venta" in response.url or "vender" in response.url or "se vende" in response.url or "vendo" in response.url or "traspaso" in response.url:  
                achat_loc ="1"
             elif "venta" in nom or "vender" in nom or "se vende" in nom or "vendo" in nom or "traspaso" in nom:  
                achat_loc ="1"
             elif "renta" in response.url or "rentar" in response.url or "rento" in response.url:  
                achat_loc ="2"
             elif "RENTA" in nom or "renta" in nom or "rentar" in nom or "rento" in nom:  
                achat_loc ="2"
             else:
                achat_loc =""
        else:
          achat_loc =""

        loader.add_value('ACHAT_LOC', achat_loc)



        
        tmp1 =''.join(response.css('ol>li::text').extract())
        tmp2 =''.join(response.css('ol>li>p::text').extract())
  

            

        if tmp1:

            tmp = tmp1
        elif tmp2:
            tmp=tmp2
        
        else:

            tmp = ""
        
        #loader.add_value('ANNONCE_TEXT', extract_from(tmp, '(.*)'))
        texte = response.xpath("//p/text()").extract_first()
        if texte is not None:
           loader.add_value('ANNONCE_TEXT', texte.replace(";","").replace('"','').replace("\r","").replace("\n",""))

        #nom annance'PROVINCE



        #qartier

        tmp1=response.url
        #tmp2=response.xpath('//span[@class="ad-li-location-content"]/text()').extract_first()
        #tmp3=response.xpath("//h2/span/a[3]/span/text()").extract_first()
        
        
        if tmp1 is not None:
            z=tmp1.strip().split("/")

            tmp1=z[4]

        else:

            tmp1=""

        if tmp1:
            tmp = tmp1
        #elif tmp2:
         #   tmp = tmp2
        #elif tmp3:
         #   tmp=tmp3
        #elif tmp4:
         #   tmp=tmp4
        else:
            tmp = ""
        ville = tmp.replace("-"," ")
        loader.add_value('VILLE', tmp.replace("-"," "))
        loader.add_value('ADRESSE', tmp)

        #PROVINCE
        PROVINCE=response.xpath('//h2/a/text()').extract_first()
        #Matching PROVINCE with VILLE
        if ville=="aguascalientes":
           PROVINCE="Aguascalientes" 
        elif ville=="baja california":
             PROVINCE="Baja California" 
        elif ville=="baja-california":
             PROVINCE="Baja California" 
        elif ville=="baja-california-sur":
             PROVINCE="Baja California Sur" 
        elif ville=="baja california sur":
             PROVINCE="Baja California Sur" 
        elif ville=="campeche":
             PROVINCE="Campeche" 
        elif ville=="chiapas":
             PROVINCE="Chiapas" 
        elif ville=="chihuahua":
             PROVINCE="Chihuahua" 
        elif ville=="chihuahua-chih":
             PROVINCE="Chihuahua" 
        elif ville=="coahuila":
             PROVINCE="Coahuila" 
        elif ville=="colima":
             PROVINCE="Colima" 
        elif ville=="distrito-federal":
             PROVINCE="DF CDMX" 
        elif ville=="durango":
             PROVINCE="Durango" 
        elif ville=="estado de mexico":
             PROVINCE="Estado de México" 
        elif ville=="estado-de-mexico":
             PROVINCE="Estado de México" 
        elif ville=="guanajuato":
             PROVINCE="Guanajuato" 
        elif ville=="guerrero":
             PROVINCE="Guerrero" 
        elif ville=="hidalgo":
             PROVINCE="Hidalgo" 
        elif ville=="jalisco":
             PROVINCE="Jalisco" 
        elif ville=="michoacan":
             PROVINCE="Michoacán" 
        elif ville=="morelos":
             PROVINCE="Morelos" 
        elif ville=="nayarit":
             PROVINCE="Nayarit" 
        elif ville=="nuevo leon":
             PROVINCE="Nuevo León" 
        elif ville=="nuevo-leon":
             PROVINCE="Nuevo León" 
        elif ville=="oaxaca":
             PROVINCE="Oaxaca" 
        elif ville=="puebla":
             PROVINCE="Puebla" 
        elif ville=="puebla-pue":
             PROVINCE="Puebla" 
        elif ville=="queretaro":
             PROVINCE="Querétaro" 
        elif ville=="queretaro-qro":
             PROVINCE="Querétaro" 
        elif ville=="quintana roo":
             PROVINCE="Quintana Roo" 
        elif ville=="quintana-roo":
             PROVINCE="Quintana Roo" 
        elif ville=="san luis potosi":
             PROVINCE="San Luis Potosí" 
        elif ville=="san-luis-potosi":
             PROVINCE="San Luis Potosí" 
        elif ville=="san-luis-potosi-slp":
             PROVINCE="San Luis Potosí" 
        elif ville=="sinaloa":
             PROVINCE="Sinaloa" 
        elif ville=="sonora":
             PROVINCE="Sonora" 
        elif ville=="tabasco":
             PROVINCE="Tabasco" 
        elif ville=="tamaulipas":
             PROVINCE="Tamaulipas" 
        elif ville=="tlaxcala":
             PROVINCE="Tlaxcala" 
        elif ville=="veracruz":
             PROVINCE="Veracruz" 
        elif ville=="veracruz-ver":
             PROVINCE="Veracruz" 
        elif ville=="yucatan":
             PROVINCE="Yucatán" 
        elif ville=="zacatecas":
             PROVINCE="Zacatecas" 
        elif ville=="acapulco-de-juarez":
             PROVINCE="Guerrero" 
        elif ville=="atotonilco-de-tula":
             PROVINCE="Hidalgo" 
        elif ville=="boca-del-rio":
             PROVINCE="Veracruz" 
        elif ville=="calimaya":
             PROVINCE="Estado de México" 
        elif ville=="cancun":
             PROVINCE="Quintana Roo" 
        elif ville=="chapultepec":
             PROVINCE="Estado de México" 
        elif ville=="corregidora":
             PROVINCE="Querétaro" 
        elif ville=="cuautlancingo":
             PROVINCE="Puebla" 
        elif ville=="del-valle-sur":
             PROVINCE="DF CDMX" 
        elif ville=="guaymas":
             PROVINCE="Sonora" 
        elif ville=="hermosillo":
             PROVINCE="Sonora" 
        elif ville=="jardines-del-pedregal":
             PROVINCE="DF CDMX" 
        elif ville=="leon":
             PROVINCE="Guanajuato" 
        elif ville=="mazatlan":
             PROVINCE="Sinaloa" 
        elif ville=="merida":
             PROVINCE="Yucatán" 
        elif ville=="metepec-edomex":
             PROVINCE="Estado de México" 
        elif ville=="mexico":
             PROVINCE="" 
        elif ville=="san-andres-cholula":
             PROVINCE="Puebla" 
        elif ville=="san-juan-del-rio-qro":
             PROVINCE="Querétaro" 
        elif ville=="san-pedro-cholula":
             PROVINCE="Estado de México" 
        elif ville=="solidaridad":
             PROVINCE="Quintana Roo" 
        elif ville=="tecamac":
             PROVINCE="Estado de México" 
        elif ville=="tijuana":
             PROVINCE="Baja California" 
        elif ville=="tizayuca":
             PROVINCE="Hidalgo" 
        elif ville=="toluca":
             PROVINCE="Estado de México"         
        PROVINCE = PROVINCE if PROVINCE else ""

        loader.add_value('PROVINCE', PROVINCE)




        tmp = response.xpath('//div[@class="map-wrapper"]/following-sibling::script/text()').re_first(r'lat: (.*),', '')
        loader.add_value('LATITUDE', tmp)

        tmp = response.xpath('//div[@class="map-wrapper"]/following-sibling::script/text()').re_first(r'lng: (.*) }', '')
        loader.add_value('LONGITUDE', tmp)

        # M2_TOTALE
    
        tmp=response.xpath("//li[contains(text(),'Superficie:')]/span/text()").extract_first()
        if tmp is not None:
            tmp=tmp.strip()
        else:
            tmp=""

        tmp = tmp if tmp else ""

        loader.add_value('M2_TOTALE', tmp)
        # END M2_TOTALE

        loader.add_xpath('NB_GARAGE', '//li[contains(text(),"Garage:")]/span/text()')
        
        photo=response.xpath("//div[@class='magnifier']/span[@class='count']/text()").extract_first()
        
        if photo is not None:

            photo=photo.split()[0]
        else:

            photo=""

        loader.add_value('PHOTO',photo)

        

        # PIECE
        #tmp_1 = response.xpath('//span[@class="pri-props-name"][contains(text(), "mara")]/following-sibling::span/text()').extract_first()
        #tmp_1 = tmp_1 if tmp_1 else ""
        #tmp_2 =  response.xpath('//span[@class="pri-props-name"][contains(text(), "MARA(S)")]/following-sibling::span/text()').extract_first()
        #tmp_2 = tmp_2 if tmp_2 else ""
        tmp =  response.xpath("//li[contains(text(),'Recámara(s)')]/span/text()").extract_first()
        

        if tmp is not None:


            tmp=tmp.strip()

            if "6+" in tmp:

                tmp="7"

            elif "4+" in tmp:

                tmp="5"

                tmp=tmp

        else :

            tmp=""

        loader.add_value('PIECE', tmp)
        # END PIECE
        #PRICE
        #tmp_1 = response.xpath('//span[@class="ad-price"]/text()').re('\d.*\d')
        #tmp_1 = tmp_1[0] if tmp_1 else ""
        #tmp_2 = response.xpath('//meta[@itemprop="priceCurrency"]/@content').extract_first()
        #tmp_2 = tmp_2 if tmp_2 else ""
        tmp_1 = response.xpath("//span[contains(@class, 'ad-price')]//text()").extract()
        tmp_1 = tmp_1[0] if tmp_1 else ""
        if "USD" in tmp_1:
           price = ''.join(tmp_1.re('\d.*\d'))
           #price = ''.join(re.findall(r'\d+',tmp_1)).replace(" ","").replace(",","")
        elif "USD" not in tmp_1:
            p1 = ''.join(re.findall(r'\d+',tmp_1)).replace(" ","").replace(",","")
            #conversion Mexican pesos to Dollar
            price = int(int(p1)/19)
            if price > 99999999:
               price = "99999999"
            price=str(price)
        else:
           price =""
        #loader.add_value('PRIX', '{} {}'.format(tmp_2, tmp_1))
        loader.add_value('PRIX', price)

        loader.add_value('PAYS_AD', MX)

        tmp= response.xpath("//h1/text()").extract_first()
        tmp= tmp if tmp else ""
        loader.add_value('NOM', tmp.replace('?','').replace(";","").replace('"','').replace("\r","").replace("\n",""))


        # SELLER_TYPE
        tmp_1 = response.xpath("//li[contains(text(),'Vendedor(a)')]/span/text()").extract_first()


        tmp_1 = tmp_1 if tmp_1 else ""
        tmp_2 = response.xpath('//span[@class="pri-props-name"][text()="Arrendador(a)"]/following-sibling::span/text()').extract_first()
        tmp_2 = tmp_2 if tmp_2 else ""
        tmp_3= response.xpath("//li[contains(text(),'Arrendador(a):')]/span/text()").extract_first()


        if tmp_1:
            tmp = tmp_1
        elif tmp_2:
            tmp = tmp_2
        elif tmp_3:
            tmp=tmp_3
        else:
            tmp = "Particular"

        loader.add_value('SELLER_TYPE', tmp)
        sellertype = tmp
        # SELLER_TYPE END

        #if sellertype.lower() in ('inmobiliaria', 'agencia'):
            #tmp = 'Y'
        if "Inmobiliaria" in sellertype:
            tmp="Y"
        elif "Agencia" in sellertype:
            tmp="Y"
        else:
            tmp = 'N'
        loader.add_value('PRO_IND', tmp)
        #mini site
        mini_site_text=str(re.findall(r'"sellerLink":"(.*)"',response.text))
        if mini_site_text !="None" or mini_site_text !="":
            mini_site_text=mini_site_text.split(",")[0]
            mini_site_url="https://www.vivanuncios.com.mx"+mini_site_text[2:(len(mini_site_text)-1)]
        else:
            mini_site_url=""

        loader.add_value('MINI_SITE_URL',mini_site_url)
        #agence nom
        agence_nom_text=str(re.findall(r'"sellerName":"(.*)"',response.text))
        if agence_nom_text !="None" or agence_nom_text !="":
            agence_nom_text=agence_nom_text.split(",")[0]
            agence_nom=agence_nom_text[2:(len(agence_nom_text)-1)]
        else:
            agence_nom_text=""
            
        loader.add_value('AGENCE_NOM',agence_nom)
        #loader.add_xpath('MINI_SITE_URL', '//a[@class="seller-panel"]/@href')
        #loader.add_xpath('AGENCE_NOM', '//span[@class="user-fname"]/text()')
        raw=""
        tel=str(re.findall(r'"adPhone":"(.*)"',response.text)).split(",")[0]
        
        tmp=[]
        if tel!="" or tel !="None":
            tel=tel.replace('+', '').replace('(', '').replace(')', '').replace(' ', '').replace("\"","")[2:]
            if (len(tel) <= 15):
               if ("-") in tel:
                    tel=tel.replace("-","")
                    loader.add_value("AGENCE_TEL", tel)
               else:
                   loader.add_value("AGENCE_TEL",tel)
                    
                    
            else:
                
                if ("-") in tel:

                    tmp=tel.split("-")



        #else:
         #   raw="" 
        #Mini_site_id
        

        if isinstance(tmp, (list)):
            if len(tmp) > 3:
                loader.add_value("AGENCE_TEL_4", tmp[3])
            if len(tmp) > 2:
                loader.add_value("AGENCE_TEL_3", tmp[2])
            if len(tmp) > 1:
                loader.add_value("AGENCE_TEL_2", tmp[1])
            if len(tmp) > 0:
                loader.add_value("AGENCE_TEL", tel)

        
        mini_site_text=str(re.findall(r'"sellerLink":"(.*)"',response.text))
        if mini_site_text !="None" or mini_site_text !="":
            mini_site_text=mini_site_text.split(",")[0]
            mini_site_url="https://www.vivanuncios.com.mx"+mini_site_text[2:(len(mini_site_text)-1)]
        else:
            mini_site_url=""


        if mini_site_url is not None:

            MINI_SITE_ID=mini_site_url.strip().split("/")[5]
            

        else:

            tmp=" "


        loader.add_value('MINI_SITE_ID', MINI_SITE_ID)






        


        yield loader.load_item()
