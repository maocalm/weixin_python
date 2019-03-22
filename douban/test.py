import re
import requests
import requests
from lxml import etree
import re
from pymongo import MongoClient
import time


cur_url = 'https://movie.douban.com/subject/25882296/reviews?start=80'
base_url = re.search(r'https:.*sub', cur_url).group(0)
print(base_url)


curl = 'https://movie.douban.com/subject/25882296/comments?start=220&limit=20&sort=new_score&status=P&percent_type='

get_comments(cur_url)

def get_comments(self, cur_url):
    '''
    从当前html页面解析出20条评论的信息,并存入mongo数据库。获取每条评论的id,日期，评论内容，有用数量
    :param cur_url:待爬取页面url
    :return:当前页面的20条评论数据信息
    '''
    print('解析页面:%s' % cur_url)
    html = self.get_html(cur_url)
    print("html", html)
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
        comment_lines = item.xpath('.//p/text()')[0].strip()
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