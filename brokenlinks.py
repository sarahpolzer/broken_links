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
all_links_list=[]
r=0
for url in urls:
    opens2 = requests.get(url)
    soup2 = BeautifulSoup(opens2.text, 'lxml')
    all_links = soup2.findAll('a')
    for link in all_links:
        # store links in variable
        url2 = link.get('href')
        # query each link for the status code
        r += 1
        try: 
            request_links=requests.get(url2)
            print("{}: {} - {}".format(r, request_links.status_code, url2[h_len:]))
        except:
            requests.exceptions.RequestException(url2)
            print('exception caught', url2 )
            
     