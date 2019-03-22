#!/usr/bin/env python
# coding=utf-8
'''
从豆瓣电影抓取影片的短评；将数据用mongo数据库存储；用pandas对电影评论数据进行分析
'''
import requests
from lxml import etree
import re
from pymongo import MongoClient
import time



class dbSpider(object):
    def __init__(self, db, collection, cookies):
        self.db = db
        self.collection = collection
        self.cookies = cookies
        client = MongoClient()
        mongo_DB = self.db
        db = client[mongo_DB]
        self.col = db[self.collection]

    def get_html(self, url):
        try:
            r = requests.get(url, timeout=5, cookies={'cookie': self.cookies})
            r.raise_for_status()
            html = etree.HTML(r.text)
            return html
        except Exception as e:
            print('解析页面失败！' , e)
            time.sleep(2)
            self.get_html(url)

    def next_page_url(self, cur_url):
        '''
        从当前页面解析下一页的url
        :param html: 当前页面当html文件
        :return: 下一页的url链接
        '''
        html = self.get_html(cur_url)
        base_url = re.search(r'^https:.*comments', cur_url).group(0)
        print("baseurl" +base_url)
        paginator = html.xpath('//div[@id="paginator"]//a')
        for a in paginator:
           # match = re.search(r'\u4E00-\u9FA5', a.text)
            print(a.text +"    ==========")
            match =  a.text
            try:
                if match.find('后页')!= -1:
                    next_url = base_url + a.attrib['href']
                    print("=======next_url========"+next_url)
                    return next_url
            except Exception as  e :
                print(e)

        else:
            print('已经是最后一页！')
            return None

    def get_comments(self, cur_url):
        '''
        从当前html页面解析出20条评论的信息,并存入mongo数据库。获取每条评论的id,日期，评论内容，有用数量
        :param cur_url:待爬取页面url
        :return:当前页面的20条评论数据信息
        '''
        print('解析页面:%s' % cur_url)
        html = self.get_html(cur_url)
        print("html" , html)
        commList = html.xpath('//div[@class="comment-item"]')
        data = []
        for item in commList:
            user_id = item.attrib['data-cid']
            vote = item.xpath('.//span[@class="votes"]')[0].text.strip()
            user_name = item.xpath('.//span[@class="comment-info"]/a')[0].text.strip()
            status = item.xpath('.//span[@class="comment-info"]//span[1]/text()')[0].strip()
            if len(item.xpath('.//span[@class="comment-info"]//span')) == 3:
                rating = item.xpath('.//span[@class="comment-info"]//span[2]/@title')[0].strip()
                pub_time = item.xpath('.//span[@class="comment-info"]//span[3]/text()')[0].strip()
            else:
                rating = ''
                pub_time = item.xpath('.//span[@class="comment-info"]//span[2]/text()')[0].strip()
            comment_lines = item.xpath('.//span[@class="short"]')[0].text.strip()
            comment_info = {
                'user_id': user_id,
                'vote': vote,
                'user_name': user_name,
                'status': status,
                'rating': rating,
                'pub_time': pub_time,
                'comment_lines': comment_lines
            }
            data.append(comment_info)
        return data

    def saveData(self, data):
        '''

        :param data:
        :param db:
        :return:
        '''

        print('aaaaaaaa=======' , data)
        try:
            if self.col.insert_many(data):
                print('保存成功！')
        except Exception as e:
            print('保存失败。' ,e)
            return None

    def dbCrawl(self, cur_url, pageNum):
        '''
        爬取指定页数的评论，然后停止
        :param start_url:起始页
        :param pageNum: 指定需要爬取的评论页面数
        :return:
        '''
        i = 1
        while cur_url:
            if i > pageNum:
                break
            else:
                data = self.get_comments(cur_url)

                self.saveData(data)
                print('成功爬取第%d页！' % i)
                i += 1
                cur_url = self.next_page_url(cur_url)
                time.sleep(2)
        print('爬取结束！')


def get_cookies(raw_lines):
    '''
    用cookies登陆网站，才能进行更多的评论浏览。将原始cookies字符串raw_cookies转换成字段格式
    :param raw_lines: 原始cookies字符串。需每次从网站复制
    :return: 字典格式的cookies
    '''
    cookies = {}
    for line in raw_lines.split(';'):
        key, value = line.split('=', 1)
        cookies[key] = value
    return cookies


if __name__ == '__main__':
    client = MongoClient()
    db = 'douban'
    # collection = input('输入待爬取电影名称(全字母输入):\n')
    collection = '狄仁杰之四大天王'
    # raw_cookies = input('请输入最新登陆的cookie：\n')
    raw_cookies = 'bid=CO9qgTuC7-U; ll="108288"; __utmc=30149280; __utmz=30149280.1537422295.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmc=223695111; __utmz=223695111.1537422295.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __yadk_uid=xBEdSNgloIP1vyVTEELRidaYpHs5fWDL; _vwo_uuid_v2=DB9E3AB1E586B75EB212A8131164A45F0|6d86187a3ef0baf9961378b872032be4; ps=y; push_noty_num=0; push_doumail_num=0; ap_v=0,6.0; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1537504878%2C%22https%3A%2F%2Faccounts.douban.com%2Flogin%3Falias%3D2531505296%2540qq.com%26redir%3Dhttps%253A%252F%252Fmovie.douban.com%252Fsubject%252F25882296%252F%253Ftag%253D%2525E7%252583%2525AD%2525E9%252597%2525A8%2526from%253Dgaia_video%26source%3Dindex_nav%26error%3D1013%22%5D; _pk_id.100001.4cf6=8b2cda2a19a282f2.1537422291.3.1537504878.1537503051.; _pk_ses.100001.4cf6=*; __utma=30149280.1133682160.1537422295.1537503061.1537504878.3; __utma=223695111.1504769897.1537422295.1537503061.1537504878.3; __utmb=223695111.0.10.1537504878; __utmv=30149280.11970; __utmb=30149280.2.10.1537504878; ck="NmRd"; dbcl2="119705364:hUyJ7/3b5K0"'
    cookies = {'cookie': raw_cookies}
    spider = dbSpider(db=db, collection=collection, cookies=raw_cookies)
    print('开始爬取......')
    # start_url = input('输入开始爬取的url：\n')
    start_url = 'https://movie.douban.com/subject/25882296/comments?start=40&limit=20&sort=new_score&status=P'
    spider.dbCrawl(cur_url=start_url, pageNum=100) #只能爬取20*25500条评论
    print('共爬取%d条评论' % client[db][collection].count())