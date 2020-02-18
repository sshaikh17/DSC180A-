#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import urllib.request
import time
from urllib.request import urlopen
import zipfile
import wget

import datetime as dt
from datetime import datetime
import zipfile 

import re
import seaborn as sns
import matplotlib.pyplot as plt

import statistics



def main(targets):
    if 'data' in targets:
        headers = requests.utils.default_headers()
        headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
        
        url = 'http://wwm.phy.bme.hu/light.html'
        opened = urlopen(url)
        soup = BeautifulSoup(opened, 'lxml')
        all_links = soup.findAll('a')
        en_link = soup.findAll('a')[3]
        link = en_link.get("href")
        full_link2 = 'http://wwm.phy.bme.hu/LD/ld_de_wiki.zip'
        wget.download(full_link2, "en_file.zip")

        with zipfile.ZipFile("en_file.zip", "r") as zip_ref:
            zip_ref.extractall("light_dump_en_txt")
        return

    if 'process' in targets:
        get_edit_num(file)
        #need to add reverts per title
        #need to add editors per title
        
        return 
    if 'data-test' in targets: 
        return 
        


