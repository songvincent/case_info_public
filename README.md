# case_info_public
爬取案件信息公开网的公开文书。

爬取时间段：2019.7 -- 2020.7

其中 **code** 目录下存放代码，**case** 目录下存放爬取到的案件数据。

**code**: 

代码爬取过程分为两步，首先爬取每个省份下每类文书的对应的url，将其存放到对应类型文书的文件夹下的url_list下，案件信息公开网共有5类文书：**不起诉决定书、抗诉书、起诉书、刑事申诉复查决定书和其他法律文书**。因此，爬取后的文件结构为：

- case
  - 安徽
    - 不起诉决定书
    - 抗诉书
    - 起诉书
    - 刑事申诉复查决定书
    - 其他法律文书
  - 辽宁
    - 不起诉决定书
    - 抗诉书
    - 起诉书
    - ...
    - ...
  - 山西
  - 吉林
  - ...

**case_qisu.py**

这是爬虫的第一步。从原网站上爬取 **每一个省份中每一个类型** 的法律文书的url，将所有url存放到对应文件夹下的url_list.txt中。其中每一行中依次存储了 **url,所属检察院,文书名字,发表时间** 。

**handle_detail_page.py** 

这是爬虫的第二步。通过上述步骤，则在每一个文件夹下有一个url_list。根据其中的url爬取对应的网页内容进行解析，在同级目录生成对应的起诉文书。