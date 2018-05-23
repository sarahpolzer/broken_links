from bs4 import BeautifulSoup
import requests
from datetime import datetime
import csv
import re
import shutil

hostname = "https://www.321webmarketing.com"
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

for url in urls:
    requestlink=requests.get("{}/url".format(hostname))
    i += 1
    print("{}: {} - {}".format(i, requestlink.status_code, url[h_len:]))




