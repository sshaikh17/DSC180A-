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


# # Download light dump data

# In[3]:


headers = requests.utils.default_headers()
headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})


# In[4]:


url = 'http://wwm.phy.bme.hu/light.html'



opened = urlopen(url)

soup = BeautifulSoup(opened, 'lxml')
all_links = soup.findAll('a')
all_links


# In[5]:


en_link = soup.findAll('a')[3]
en_link


# In[6]:


link = en_link.get("href")
link


# In[7]:


full_link = url+link
full_link
full_link2 = 'http://wwm.phy.bme.hu/LD/ld_de_wiki.zip'


# In[ ]:


wget.download(full_link2, "en_file.zip")


# In[ ]:


import zipfile
with zipfile.ZipFile("en_file.zip", "r") as zip_ref:
    zip_ref.extractall("light_dump_en_txt")


# In[10]:


##get descriptive stats


# In[ ]:





# In[ ]:





# # Get descriptive statistics

# In[1]:


#get amt of edits per article


# In[10]:


def get_edit_num(file):
    edit_num = {}
    art = file.readline()
    ct = 0

    for i in file:
        if i[0] != "^":
            edit_num[art.rstrip()] = ct
            art = i
            ct = 0
        else:
            ct +=1

    edit_num[art] = ct
    return edit_num


# In[11]:


edit_num = get_edit_num(open("light_dump_en.txt/en_wiki.txt", "r"))


# In[12]:


edit_num


# In[13]:


#edit_num


# In[14]:


#plot distribution of edit amts
edit_vals = list(edit_num.values())
edit_vals_hist = sns.distplot(edit_vals, bins = 1)
edit_vals_hist


# In[15]:


num_edits_mean = statistics.mean(edit_vals)
num_edits_mean


# In[16]:


def get_top_10(wiki_dict):
    wiki_dict = sorted(wiki_dict.items(), key = lambda x: x[1], reverse = True)
    return wiki_dict
def get_bottom_10(dict):
    wiki_dict = sorted(wiki_dict.items(), key = lambda x: x[1])
    return wiki_dict


# In[ ]:





# In[17]:


#top10_most_edited = {k: v for k, v in sorted(x.items(), key=lambda item: item[1])}
#sorted_d = sorted(d.items(), key=lambda x: x[1])

top10_least_edited = sorted(edit_num.items(), key = lambda x: x[1])
top10_least_edited


# In[18]:


top10_most_edited = sorted(edit_num.items(), key = lambda x: x[1], reverse = True )
top10_most_edited


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[25]:


#get reverts per article


# In[2]:


def access_reverts(string):
    pattern = "^\S*\s+(\S+)"
    a = re.findall(pattern, string)
    results = list(map(int, a))[0]
    return results


# In[3]:


#file = open("light_dump_en.txt/en_wiki.txt", "r")


# In[4]:


def get_reverts(file):
    reverts_ct = {}
    title =  file.readline()
    sum_reverts = 0
    for i in file:
        if line[0] != "^":
            Num_Reverts[title.rstrip()] = sum_reverts
            title = i
            sum_reverts = 0
        else:
            sum_reverts += access_reverts(i)

    reverts_ct[title.rstrip()] = sum_reverts
    return reverts_ct


# In[ ]:


#plot distribution of revert number
revert_vals = get_reverts(open("light_dump_en.txt/en_wiki.txt", "r"))
revert_vals = list(reverts_ct.values())
reverts_vals_hist = sns.distplot(reverts_vals, bins = 1)
reverts_vals_hist


# In[ ]:





# In[ ]:





# # M Statistic

# In[1]:


def get_pairs(tup_pairs):
    if len(tup_pairs) == 0:
        return {}
    
    mut_revs = {}
    checked = []
    
    for i in tup_pairs:
        if i in checked:
            continue
        if (i[1], i[0]) in checked:
            continue
        checked.append(i)
        
        for mut_revs in tup_pairs:
            if tup_pairs == (i[1], i[0]):
                if i in mut_revs:
                    mut_revs[i] = mut_revs[i] + 1
                else:
                    mut_revs[i] = 1
                    
    return mut_revs

def get_M_perArt(revs, mut_amt, edit_num):
    if len(revs) == 0:
        return 0
    
    total = 0
    for i in revs:
        total = total+min(edit_num[i[0]], edit_num[i[1]])
    
    final = len(mut_amt) * total
    
    return final

def dicts_of_genInfo(e):
    edit_num = {}
    editor_name = {}
    
    for i in sorted(e.keys(), reverse = True):
        time = e[i][0]
        revert = int(e[i][1])
        version = int(e[i][2])
        editor = e[i][3]
        
    if editor in edit_num:
        edit_num[editor] = edit_num[editor] +1
    else:
        edit_num[editor] = 1
    
    if revert == 0:
        editor_name[version] = editor
    return edit_num, editor_name


# In[2]:


def get_m_stat(edits, m_val): 
    topic = edits["title"]
    del edits["title"]
    edit_num, editor = dicts_of_genInfo(edits)
    
    t = []
    
    for i in sorted(edits.keys(), reverse = True):
        time = edits[i][0]
        revert = int(edits[i][1])
        version = int(edits[i][2])
        editor_name = edits[i][3]
        
        if revert == 1:
            rival = editor[version+1]
            t.append((editor_name, rival))
        else:
            continue

    mut_pairs_amt = get_pairs(t)
    m_val = get_M_perArt(t, mut_pairs_amt, edit_num)
    
    return m_val 


def get_data():
    file = open("light_dump_en.txt/en_wiki.txt", "r")

    m_holder = {}
    
    title_dict = {}
    title_dict["title"] = file.readline()
    
    num_edit = 0
    for i in file:
        if i[0] != "^":
            new_title = title_dict.copy()
            m_val = get_m_stat(new_title, m_holder)
            m_holder[title_dict["title"]] = m_val
            
            print(new_topic)
            print("~~~")
            
            title_dict = {}
            title_dict["title"] = i
            edit_num = 0
        else: 
            title_dict[num_edit] = i.split(" ")
        
        num_edit = num_edit +1 
        
    new_title = title_dict.copy()
    m_val = get_m_stat(new_title, m_holder)
    m_holder[title_dict["title"]] = m_val
    
    print("Top 10:")
    print(get_top_10(m_holder))
    
    print("Bottom 10:")
    print(get_bottom_10(m_holder))
    
    
    file.close()
    


# In[40]:


##graphs for replication?


# In[41]:


def make_graph(titles):
    new_title = {}
    ct = 0
    m_holder = {}
    
    new_title["title"] = titles["title"]
    for each in sorted(titles["dictionary"].keys(), reverse = True):
        new_title[ct] = titles["dictionary"][each]
        ct = ct + 1

        new_title = new_title.copy()
        m_val = get_m_stat(new_title, m_holder)   
        m_holder[ct] = m_val
        
    x = []
    for i in m_holder.keys():
        x_values.append(i)
    
    y = []
    for j in m_holder.values():
        y_values.append(j)
        
    plt.plot(x, y)
    plt.ylabel('M statistic')
    plt.xlabel('Edits over time')
    plt.show()


# In[42]:


make_graph(top_10_most_edited)


# In[ ]:





# # Raw to light dump revisited (edited Assn. 1 code)

# In[ ]:


from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import urllib.request
import time
from urllib.request import urlopen

from py7zr import unpack_7zarchive
import shutil

#import os
from pyunpack import Archive
import zipfile

from lxml import etree
import lxml
from copy import deepcopy

get_ipython().system('pip install wget --user')


import wget


headers = requests.utils.default_headers()
headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})


url = 'https://dumps.wikimedia.org/enwiki/20200101/'

url2 = 'https://dumps.wikimedia.org/'


opened = urlopen(url)

soup = BeautifulSoup(opened, 'lxml')
all_links = soup.findAll('a')
all_links

first_tag = soup.findAll('a')[127]
second_tag = soup.findAll('a')[128]

link_first = first_tag['href']
link_second = second_tag['href']


link1 = first_tag.get("href")
link2 = second_tag.get("href")

link2


first_file = url2 + link1
second_file = url2+link2
first_file

wget.download(first_file, "file1.7z")
wget.download(second_file, "file2.7z")


# #unzipping
shutil.register_unpack_format('7zip', ['.7z'], unpack_7zarchive)




shutil.unpack_archive('./file1.7z')
shutil.unpack_archive('./file2.7z')


def fast_iter(context):
    '''loops through an XML object, and writes 1000 page elements per file.'''
    page_num = 1
    
    # create an empty tree to add XML elements to ('pages')
    # and a new file to write to.
    fh = make_tmpfile(page_num)
    tree = etree.ElementTree()
    root = etree.Element("wikimedia")
    
    # loop through the large XML tree (streaming)
    for event, elem in context:
        print(page_num)
        # After 1000 pages, write the tree to the XML file
        # and reset the tree / create a new file.
        if page_num % 1000 == 0:
            
            tree._setroot(root)
            fh.write(etree.tostring(tree).decode('utf-8'))
            fh.close()
            
            fh = make_tmpfile(page_num)
            tree = etree.ElementTree()
            root = etree.Element("wikimedia")
        
        # add the 'page' element to the small tree
        root.append(deepcopy(elem))
        #print("appended!!!!!")
        page_num += 1
        

        # release uneeded XML from memory
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
            
    del context


def make_tmpfile(pagenum, dir='tempdata'):
    print("creates new file %d" %pagenum)
    '''returns a file object for a small chunk file; must close it yourself'''
    import os
    if not os.path.exists(dir):
        os.mkdir(dir)
        
    fp = os.path.join(dir, 'chunk_%d.xml' % pagenum)
    return  open(fp, mode='w')
    

# USAGE
context1 = etree.iterparse("./file1", tag='{http://www.mediawiki.org/xml/export-0.10/}page', encoding='utf-8')
context2 = etree.iterparse("file2", tag='{http://www.mediawiki.org/xml/export-0.10/}page', encoding='utf-8')

fast_iter(context1)
fast_iter(context2)



et = etree.parse('tempdata/chunk_20.xml')
root = et.getroot()
nsmap = {'ns': 'http://www.mediawiki.org/xml/export-0.10/'}

root.findall('ns:page', nsmap) # find all pages
root.xpath('*/*/*/ns:username', namespaces=nsmap) # extract all username tags
root.xpath('ns:page/ns:revision/ns:timestamp', namespaces=nsmap)  # extract all time-stamps


# In[14]:


data_holder = {"Page Title": []}
wiki_set = root.getchildren()

#to get info from each page

for each in wiki_set:
    edit_amt = 0
    
    #separate into time and username per edit
    edits_dict = {"Timestamp": [], "Username": [], "Total Number of Edits": []}
    
    for further_info in each:
        if "title" in further_info.tag:
            data_holder["Page Title"].append(further_info.text) 
        if "revision" in further_info.tag:
            
            #keep track of edits per page
            edit_amt = edit_amt + 1
            
            #get time per edit per page
            for edits in further_info:
                if "timestamp" in edits.tag:
                    edits_dict["Timestamp"].append(edits.text)
                #get username per edit per page    
                for user_info in edits:
                    if "username" in user_info.tag:
                        edits_dict["Username"].append(user_info.text)
                        
    #add the total number of edits per page at end of dict
    edits_dict["Total Number of Edits"].append(edit_amt)

    data_holder["Page Title"].append(edits_dict)
data_holder



data = pd.DataFrame.from_dict(data_holder)
data


data_holder2 = {"Page Title": []}
wiki_set = root.getchildren()


for each in wiki_set:
    version = 1
    
    info_dict = {"Timestamp": [], "Username": [], "Version": []}

    
    for further_info in each:
        if "title" in further_info.tag:
            data_holder2["Page Title"].append(further_info.text)
            print(further_info.text)
        if "revision" in further_info.tag:
            #print(further_info.tag)
            info_dict["Version"].append(version)
            print("appended")
            edit_amt = edit_amt +1
            
        for edits in further_info:
                if "timestamp" in edits.tag:
                    info_dict["Timestamp"].append(edits.text)
                #get username per edit per page    
                for user_info in edits:
                    if "username" in user_info.tag:
                        info_dict["Username"].append(user_info.text)
    data_holder2["Page Title"].append(time_dict, version_dict, time_dict)


data_holder2


# In[ ]:




