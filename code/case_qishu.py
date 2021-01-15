#!/usr/bin/env python
# coding: utf-8

# ### 本程序用以爬取案件信息公开网
# --2020.7.4

# #### 获得省份列表

# In[ ]:


import requests

import re

url = r'https://www.12309.gov.cn/12309/ajxxgk/index.shtml'
# url = r'https://www.12309.gov.cn/12309/gj/bj/bjshrq/zjxflws/202007/t20200702_8243278.shtml'
# requests.post(url)

con = requests.get(url).text
pat = r'<a href=".*?value="(.*?)" channelid="(.*?)">(.*?)</a>'
province_lst = re.findall(pat,con,re.S)

# province_lst[1:]


# In[ ]:


### 获得省份及其对应的缩写（缩写会被用到url中）
abbr_loc = {}
for p in province_lst[1:]:
    abbr_loc[p[0]] = p[2]
print(abbr_loc)


# #### 获取文章的具体页面

# In[ ]:


from selenium import webdriver
import time
import re


# In[ ]:


import os


# In[ ]:


raw_url = r'http://www.12309.gov.cn/12309/gj/{}/zjxflws/index.shtml?channelLevels=/fb5a41c9247547bca03ae21326c3ad51/e2d8081e3a3640719cf2b3dedfb39725/aad7cd31f5c94d219d52fd6ec0bac9bb'
# raw_url.format('jsbt')


# In[ ]:


case_type = ['起诉书','抗诉书','不起诉决定书','刑事申诉复查决定书','其他法律文书']


# In[ ]:


### 创建路径
def create_path(path):
    if os.path.isdir(path):
        pass
    else:
        os.makedirs(path)
        print("create {}".format(path))


# In[ ]:


def get_this_page_list(text):
    '''
    input: selenium解析出的文本
    return: 该页面的url_list,对应的法院，文本名称，时间
    '''
    pat = r'<li><.*?href="(.*?)"><.*?>(.*?)</b>(.*?)</a><span class="date">(.*?)</span></li>'
    lst = re.findall(pat,text)
    return lst


# In[ ]:


### 将获得的详情页按case_type分类
def classfier(dlst):
    tlst = [[],[],[],[],[]]
    for dl in dlst:
        for i in range(4):
            if case_type[i] in dl[2]:
                tlst[i].append(dl)
                break
        if i == 4:
            tlst[i].append(dl)
    return tlst


# In[ ]:


### 将内容存储到特定文件夹下的url_list.txt
def save(lst,path):
    with open(path+'url_list.txt','w+',encoding = 'utf-8') as fout:
        for l in lst:
            fout.write('\t'.join(l)+'\n')

def save_to_file(loc,res_lst):
    for i in range(5):
        path = '../case/'+loc+'/'+case_type[i]+'/'
        create_path(path)
        save(res_lst[i],path)


# In[ ]:


browser = webdriver.Firefox(log_path = "webdriver.log")

for k,v in abbr_loc.items():
    res_lst = [[],[],[],[],[]]  ### 为每一个地区设置一个五分类（以case_type分类）
    
    url = raw_url.format(k)
    browser.get(url)
    while True:
        
        time.sleep(1)
        text = browser.page_source
        detail_lst = get_this_page_list(text)
        if len(detail_lst) == 0:
            break
        clst = classfier(detail_lst)
        for i in range(5):
            res_lst[i].extend(clst[i])
        if len(re.findall('nextbtn',text)) == 0:
            break
        browser.find_element_by_class_name('nextbtn').click()  ## brower变成了下一页
        
    save_to_file(v,res_lst)
browser.close()    


# In[ ]:


# save_to_file(v,res_lst)

# browser.get('http://www.ajxxgk.jcy.gov.cn/12309/gj/sxa/zjxflws/index.shtml?channelLevels=/fb5a41c9247547bca03ae21326c3ad51/e2d8081e3a3640719cf2b3dedfb39725/10b5647319a64672bd5417039620dc23')
# time.sleep(0.5)
# text = browser.page_source
# # print(browser.page_source)

# browser.find_element_by_class_name('nextbtn').click()
# time.sleep(1)
# text = browser.page_source
# print(browser.page_source)
# # print(ele_nextbtn)
# browser.close()


# In[ ]:




