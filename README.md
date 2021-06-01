# pa_pipermail_archives
爬取普通archives的mailing list信息

## 环境要求
- scrapy
- pymongo
- fake_useragent

就是我的conda activate pa_github

## 使用说明
同样是三只爬虫，但可惜的是爬完还需要手动操作，才可满足topic-reply的结构形式

### 总的来说，由于完全使用mongo进行数据的存储，因此需要：
  1. settings.py 中设定好本地mongo的地址、数据库名、输出位置的集合名。
  2. 如果有权限设置的话，需要在pipelines.py 中设置下用户密码。
  3. 每只爬虫中start_requests()内所需读取的前一步操作信息所在集合名等信息

### 具体四个操作步骤:


1. 获取每个年月的url
  - 需要在settings.py中设置‘目的集合’ 一般为 ‘_thread’
  - scrapy crawl ffmpeg_thread
2. 第二步，获取每个年月的话题组合情况
  - 需要在settings.py中设置‘目的集合’ 一般为 ‘_box’
  - scrapy crawl ffmpeg_box
3. 第三步，获取每个话题的具体信息
  - 需要在settings.py中设置‘目的集合’ 一般为‘_content’
  - scrapy crawl ffmpeg_content
4. 第四步，根据box中的结构信息和content中的具体邮件信息，用gao.py产生要求的topic+reply结构
  - python  gao.py  ffmpeg_libav_user_box ffmpeg_libav_user_content ffmpeg_libav_user
