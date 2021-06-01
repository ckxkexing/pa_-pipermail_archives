'''
将获取的box 和 item content进行拼接组合
得到需要的信息。

注意配置下数据库地址和数据库名字
使用时传入三个数据库中集合的名字即可，
分别为box、item 和 目的集合

'''

import pymongo
import sys

'''
{
    "mailID": 123456,
    "title": "xxx",
    "topicContent": "xxx",
    "topicAuthorLogin": "xxx",
    "topicAuthorEmail": "xxx",
    "replyAuthor": "xxx",
    "replyAuthorEmail": "xxx",
    "replyTime": "xxxx",
    "replyContent": "xxxx"
}
'''

def change2maindict(ori):
    res = {}
    res["mailID"] = ori["url"]
    res["title"] = ori["subject"]
    res["topicContent"] = ori["content"]
    res["topicAuthorLogin"] = ori["name"]
    res["topicAuthorEmail"] = ori["email"]
    res["topicTime"] = ori["date"]
    res["replyMails"] = []
    return res

def change2replydict(ori):
    res = {}
    res["mailID"] = ori["url"]
    res["title"] = ori["subject"]
    res["replyAuthor"] = ori["name"]
    res["replyAuthorEmail"] = ori["email"]
    res["replyTime"] = ori["date"]
    res["replyContent"] = ori["content"]
    return res
# ffmpeg_libav_user_box  |  ffmpeg_libav_user_content | ffmpeg_libav_user
def main(box_name, item_name, content_name):
    client = pymongo.MongoClient("mongodb://admin:123456@127.0.0.1",27017)
    db = client["mailing_lists"]
    col_box = db[box_name]
    col_content = db[item_name]
    col_output = db[content_name]

    mp = {}
    for item in col_content.find():
        mp[item["url"]] = item["_id"]
    
    res = []
    for b in col_box.find():
        b = b["urls"]
        content = {}
        # content["url"] = b[0]
        content = change2maindict( col_content.find_one({"url":b[0]}) )
        for u in b[1:]:
            content["replyMails"].append(change2replydict(col_content.find_one({"url":u})))
        col_output.insert_one(content)

if __name__ == '__main__':
    # 需要传入三个数据库集合名字
    # box_name 、 item_name 、 result_name
    main(sys.argv[1], sys.argv[2], sys.argv[3])

