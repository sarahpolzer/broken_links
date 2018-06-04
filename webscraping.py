
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import csv
import re
import shutil
import lxml
import json
hostnames = [ 'https://www.beyondexteriors.com', 'https://www.localpawpals.com/']

def get_sitemap_locs(url):
    opens=requests.get(url)
    soup=BeautifulSoup(opens.text, 'lxml')
    locs=[]
    all_links = soup.findAll('loc')
    for link in all_links:
       url = str(link).replace("<loc>","").replace("</loc>","")
       locs.append(url)
    #print(locs)
    return locs
def get_sitemap(hostname):
    sitemaps = get_sitemap_locs("{}/sitemap_index.xml".format(hostname))
    urls = []
    for sitemap in sitemaps:
        urls += get_sitemap_locs(sitemap)
    #print(urls)
    return urls

def find_links(urls):
    all_links_list = []
    for url in urls:
        opens2 = requests.get(url)
        soup2 = BeautifulSoup(opens2.text, 'lxml')
        all_links = soup2.findAll('a')
    for link in all_links:
        urltwo= link.get('href')
        if urltwo not in all_links_list:
            all_links_list.append(urltwo)
    #print(all_links_list)
    return all_links_list

def json_data(all_links_list):
    url_dict = []
    r = 0
    hostname = ['https://www.beyondexteriors.com/', 'https://www.localpawpals.com/']
    for url in all_links_list:
        r+=1
        url = str(url)
      for hostname in hostnames:  
        if hostname in url:
            try:
                request_links=requests.get(url)
                code = request_links.status_code
                url_dict.append({
                    "id" : r,
                    "status_code" : code ,
                    "url_location" : hostname[0],
                    "href" : url 
                    } )
            except:
                if 'https' not in url and 'tel' not in url:
                    url =  str(hostname) + str(url)
                    request_links=requests.get(url)
                    code = request_links.status_code
                    url_dict.append({"id" : r,
                    "status_code" : code ,
                    "url_location" : hostname[0],
                    "href" : url } )
        elif 'localpawpals' in url:
            try:
                request_links=requests.get(url)
                code = request_links.status_code
                url_dict.append({
                    "id" : r,
                    "status_code" : code ,
                    "url_location" : hostname[1],
                    "href" : url 
                    } )
            except:
                if 'https' not in url and 'tel' not in url:
                    url =  str(hostname[0]) + str(url)
                    request_links=requests.get(url)
                    code = request_links.status_code
                    url_dict.append({"id" : r,
                    "status_code" : code ,
                    "url_location" : hostname[1],
                    "href" : url } )
            
    return url_dict

def export_to_csv(hostnames):
    all_sitemaps = []
    all_links = []
    all_json_data = []
    for hostname in hostnames:
        new_sitemap = get_sitemap(hostname)
        all_sitemaps += new_sitemap
    all_links += find_links(all_sitemaps)
    all_json_data += json_data(all_links)  
    f = open('brokenlinks3.csv', "w")
    f.writelines("{0}\n".format(all_json_data[0].keys()).replace('dict_keys([',"").replace('])',"").replace("'",""))
    for item in all_json_data: 
        f.writelines("{}\n".format(item.values()).replace('dict_values([',"").replace(']', "").replace("'", "").replace(')',"").replace('[', ""))
    f.close()

export_to_csv(hostnames)