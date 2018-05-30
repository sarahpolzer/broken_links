from bs4 import BeautifulSoup
import requests
from datetime import datetime
import csv
import re
import shutil

hostnames = [
    'https://www.321webmarketing.com',
    'https://www.accelera.com',
    'https://www.bbgbroker.com',
    'https://www.beyondexteriors.com',
    'https://www.breamspeakers.com',
    'https://www.brownfirmpllc.com',
    'https://www.caringhandsmatter.com',
    'https://www.cfcc.org',
    'https://www.choosecomforthome.com',
    'https://www.cobbdaleassistedliving.com',
    'https://www.dirtconnections.com',
    'https://www.dullesplumbinggroup.com',
    'https://www.fairfaxcityeda.org',
    'https://www.fairfaxmortgage.com',
    'https://www.fvcbank.com',
    'https://www.geddescpa.com',
    'https://www.harborlighthospice.com',
    'https://www.harmonysurgical.com',
    'https://www.itpie.com',
    'https://www.kangovou.com',
    'https://www.konceptdb.com',
    'https://www.kppblaw.com',
    'https://www.localpawpals.com',
    'https://www.mfeinsurance.com',
    'https://www.networkdepot.com',
    'https://www.presidentialheatandair.com',
    'https://www.prideimmigration.com',
    'https://www.rmsmithconstruction.com',
    'https://www.shuttersbydesign.net',
    'https://www.tech62.com',
    'https://www.tier4mattress.com',
    'https://www.zenbodytherapy.com',
]
hostname = "https://https://www.localpawpals.com"
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

all_links_list=[]

def get_sitemap(hostname):
    sitemaps = get_sitemap_locs("{}/sitemap_index.xml".format(hostname))
    urls = []
    for sitemap in sitemaps:
        urls += get_sitemap_locs(sitemap)
    return urls

def find_links(urls):
    opens2 = requests.get(url)
    soup2 = BeautifulSoup(opens2.text, 'lxml')
    all_links = soup2.findAll('a')
    for link in all_links:
        urltwo=link.get('href')
        if urltwo not in all_links_list:
            all_links_list.append(urltwo)

def json_data(all_links_list):
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
    return url_dict

def export_to_csv(hostnames):
    all_sitemaps = []
    all_links = []
    all_json_data = []
    for hostname in hostnames:
        new_sitemap = get_sitemap(hostname)
        all_sitemaps += new_sitemap
    for sitemap in all_sitemaps:
        find_links(sitemap)
        all_links += find_links
    for links in all_links:
        json_data(links)
    for json_data in all_json_data:     
        f = open('brokenlinks3.csv', "w")
        f.writelines("{0}\n".format(url_dict[0].keys()).replace('dict_keys([',"").replace('])',"").replace("'",""))
        for item in url_dict: 
            f.writelines("{}\n".format(item.values()).replace('dict_values([',"").replace(']', "").replace("'", "").replace(')',""))

        f.close()

export_to_csv("https://www.tech62.com")


#for hostname in hostnames:
    # get all urls in all sitemaps
    #urls=get_sitemap_urls(hostname)
    #for url in urls:
       # opens2 = requests.get(url)
        #soup2 = BeautifulSoup(opens2.text, 'lxml')
       # all_links = soup2.findAll('a')
        #for link in all_links:
          #urltwo=link.get('href')
         # if urltwo not in all_links_list:
             # all_links_list.append(urltwo)

#url_dict = []
#for url in all_links_list:
    #r+=1
   # try: 
       # request_links=requests.get(url)
        #code = request_links.status_code
       # url_dict.append({
           # "id" : r,
           # "status_code" : code,
           # "url_location" : hostname,
            #"href" : url }
       # )
    #except:
       ## pass
#f = open('brokenlinks3.csv', "w")
#f.writelines("{0}\n".format(url_dict[0].keys()).replace('dict_keys([',"").replace('])',"").replace("'",""))
#for item in url_dict: 
   # f.writelines("{}\n".format(item.values()).replace('dict_values([',"").replace(']', "").replace("'", "").replace(')',""))

#f.close()

export_to_csv(hostnames)