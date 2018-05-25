from bs4 import BeautifulSoup
import requests
from datetime import datetime
import csv
import re
import shutil

hostname = "http://www.beyondexteriors.com"
h_len = len(hostname)

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

giantlist = []
r=0
for url in urls:
    opens2 = requests.get(url)
    soup2 = BeautifulSoup(opens2.text, 'lxml')
    alllinks = soup2.findAll('a', href=True)
    for link in alllinks:
        giantlist.append(link)
    print(giantlist)
    #giantlist.append(al)
    #for link in alllinks:
       #url = str(link).replace("<a href=>","").replace("</a>","")
       #giantlist.append(url)
      # requestlink=requests.get(link)
      # r +=1
      # print("{}: {} - {}".format(r, requestlink.status_code, url[h_len:]))
