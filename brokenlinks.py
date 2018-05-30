from bs4 import BeautifulSoup
import requests
from datetime import datetime
import csv
import re
import shutil
from numpy import unique
hostname = "https://www.fairfaxmortgage.com"
h_len = len(hostname)
h_len = 0

def get_sitemap_locs(url):
   opens=requests.get(url)
   soup=BeautifulSoup(opens.text, 'lxml')
   locs=[]
   all_links = soup.findAll('loc');
   for link in all_links:
       url = str(link).replace("<loc>","").replace("</loc>","")
       locs.append(url)
   return locs

def get_sitemap_urls(hostname):
    sitemaps = get_sitemap_locs("{}/sitemap_index.xml".format(hostname))
    urls = []
    for sitemap in sitemaps:
        urls += get_sitemap_locs(sitemap)
    return urls

    
urls = get_sitemap_urls(hostname)
i = 0


#for url in urls:
   #requestlink=requests.get(hostname + "url")
  # i += 1
  # print("{}: {} - {}".format(i, requestlink.status_code, url[h_len:]))
all_links_list=[]
r=0
for url in urls:
    opens2 = requests.get(url)
    soup2 = BeautifulSoup(opens2.text, 'lxml')
    all_links = soup2.findAll('a')
    #all_linkstwo=all_links.get('href')
    for link in all_links:
        # store links in variable
          urltwo=link.get('href')
          if urltwo not in all_links_list:
              all_links_list.append(urltwo)

url_dict = []
for url in all_links_list:
    r+=1
    try: 
        request_links=requests.get(url)
        code = request_links.status_code
        url_dict.append({
            "id" : r,
            "status_code" : code,
            "url_location" : hostname,
            "href" : url }
        )
    except:
        pass
#print(url_dict)
#for item in url_dict:
    #keys= item.keys()
   # values = item.values()
#keys= url_dict.keys()
#values=url_dict.values()
f = open('brokenlinks2.csv', "w")
#f.writelines("id", "status_code", "url_location", "href" )
f.writelines("{0}\n".format(url_dict[0].keys()).replace('dict_keys([',"").replace('])',"").replace("'",""))

for item in url_dict: 
    f.writelines("{}\n".format(item.values()).replace('dict_values([',"").replace(']', "").replace("'", "").replace(')',""))

f.close()

