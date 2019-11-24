# 爬笔趣阁小说

爬趣笔阁的小说，采用 scrapy 框架。

## 思路

1. 访问笔趣阁首页获取所有小说网址和专栏页网址
2. 遍历网址，对两种类型的网址进行区分
    - 小说网址：在小说目录页面获取所有章节网址，抓取未下载的章节
    - 专栏网址：同第一步

## 反爬措施

- 每次请求生成随机 UserAgent
- 限制请求最大并发数为 5
- 禁止失败请求重试

## 数据储存

1. 小说简介数据存放在本机 MongoDB 中；
2. 小说章节数据存放在项目根目录的 `data/db`中。

![image-20191122214846015](https://klause-blog-pictures.oss-cn-shanghai.aliyuncs.com/2019-11-22-134846.png)

![image-20191122215009274](https://klause-blog-pictures.oss-cn-shanghai.aliyuncs.com/2019-11-22-135009.png)



