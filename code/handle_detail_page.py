#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests

import os

import re

from tqdm import tqdm


# In[ ]:


import time


# In[ ]:


excp_url = []


# In[ ]:


prepath = '../case/'


# In[ ]:


count = 1  ## 爬1000条就停10秒 限速 反爬虫


# In[ ]:


def find_path(loc):
    '''
    构建出url_list文件的所在路径
    '''
    tpath = prepath + loc +'/'
    folders = os.listdir(tpath)
    return [tpath+folder+'/' for folder in folders]


# In[ ]:


def parse_detail(url,fout):
    '''
    具体解析每个页面
    拿出<body></body>的内容
    除去内容中的"<>" 两个尖括号间的内容
    '''
    rep = requests.get(url)
    s = rep.content.decode('utf-8')  ## decode
    pat = '<body .*?>(.*?)</body>'
    body = re.search(pat,s,re.S)
    
    global count
    count += 1
    
    
    if body == None:
        pat = '<div class="w1200">(.*?)</div>'
        body = re.search(pat,s,re.S)
        if body == None:
            print(url)
            excp_url.append(url)
    body_str = body.group()
    body_con = re.sub('<.*?>','',body_str)
    body_con = body_con.replace('&#xa0;','').replace('&nbsp;','')
    fout.write(body_con)
    
    if count%1000 == 0:
        time.sleep(10)


# In[ ]:


def parser(path):
    fname = path + 'url_list.txt'
#     print(fname)
    with open(fname,'r',encoding='utf-8') as fin:
        lines = fin.readlines()
    fin.close()
#     print(lines)
    for line in tqdm(lines):
        line = line.strip()
        url,court,cname,time = line.split('\t') 
        with open(path+cname+'.txt','w+',encoding='utf-8') as fout:
            fout.write(cname+'\n')
            fout.write(court+'\n')
            fout.write(time+'\n')
            fout.write('\n')
            parse_detail(url,fout)
#             break
#     print(cname)


# In[ ]:


locs = os.listdir(prepath)

for loc in locs:
    print(loc)
    paths = find_path(loc)
#     print(paths)
    
    for path in paths:
        parser(path)
#         break

with open('excp_url.txt','w+',encoding='utf-8') as fep:
    fep.write('\n'.join(excp_url))


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




