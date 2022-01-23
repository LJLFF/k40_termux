# -- coding: utf-8 --**
from os import path
import requests
import random
import time
import re
import sys
import os
#把cookie放进headers,进行登录
headers ={
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'cookie': 'SINAGLOBAL=2155216114230.2007.1640133847747; \
ULV=1640133847767:1:1:1:2155216114230.2007.1640133847747:; \
SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWszPgM17sPS5LPv2EzG9kc5JpX5KMhUgL.Fo-4e0epe0BpeKe2dJLoI79eC.phC2Xt; \
ALF=1671756756; \
SSOLoginState=1640220757; \
SCF=AjIzXkmiZ-ik8VEb0oEZFUU1hgLRUwqodHQh9cIK90xI8c_OukLmSGx4Vn0XkbLQ7ZdwKKdablfrywuhE1K4_EI.; \
SUB=_2A25Mx7gFDeRhGeNH6FEQ8yrNyj-IHXVvtK7NrDV8PUNbmtANLUbRkW9NStPMOogTpRPDbUX7bRvpI3CwUDmdU92R; \
XSRF-TOKEN=jCSEa46pUxNVFiDd2tMBkAo1; \
WBPSESS=OwdAG38vvBk44JSpRnrQFuh__InsqdO4XTwtT0XxFDB0qpiXUJas_ZUUGLVH8ai-7mmmZ2q1EpD0sf2pkGnQ4iC-rADTz7x0udfCDXT-U_bd5zuJ1HQvEjmfZH8pDE48H9RXeNCAkB2VvqWcEOJavQ=='
    
    }

def createFile():
	if os.path.exists('comments.txt'):
		os.remove('comments.txt')
#根据输入网址提取博文id和uid
def get_ids(first_url):
	if 'share' in first_url:
		blog_id = re.findall(r'weibo_id=(\d+)',first_url)[0]
		uid = re.findall(r'share/(\d+).html',first_url)[0]
		return (blog_id,uid)
		
	blog_id = re.findall(r'&id=(\d+)',first_url)[0]
	uid = re.findall(r'&uid=(\d+)',first_url)[0]
	return (blog_id,uid)
	
#发送请求得到json数据
def request(next_url):
    req =session.get(url=next_url,timeout=10)
    if req.status_code==200:
    	return req.json()
    else:
    	print('请求失败')
    	sys.exit(1)

#解析json数据,得到有用信息,可以用jsonpath库
def parse(html_json):
    max_id = html_json['max_id']
    data = html_json['data']#列表
    infos = []#同一用户会有多条评论不用字典
    
    if data:
    	for i in data:
    		dinfo ={}
    		user_name = i['user']['name']
    		comment = i['text_raw']
    		dinfo[user_name]= comment
    		infos.append(dinfo)
    #用户名 评论
    time.sleep((random.random())*3)
    return (max_id, infos)
    
    
def save(infos):
    for info in infos:
        for d in info.items():
        	item =d[0]+' : ' + d[1]
        	if '//@' in d[1]:
        		item= d[0] +' : ' +d[1].split('//@')[0]
        
        with open(file='comments.txt',mode='a',encoding='utf-8') as f:
            f.write(item+'\r\n')
            f.close()
            
    print(infos)
    print(len(infos))
        

def next_url(id,uid,max_id):
	
#id为博文id,   #is_mix取值为0和1表示展开某条评论与否,  #max_id初始页没有,返回的json数据中带有max_id作为下一个链接的参数值
    #count一般首页为10,后面都是20,  uid是博文的作者的id    其余字段皆是固定的,如follow/is_reload/is_show_bulletin
    
    next_url = f'https://weibo.com/ajax/statuses/buildComments?flow=0&is_reload=1&id={id}&is_show_bulletin=2&is_mix=0&\
max_id={max_id}&count=20&uid={uid}'
    return next_url

def main(blog_id,uid,max_id,sum,count):
    ids=[max_id,]#最后一页会随机指定某页的max_id,然后重复抓取 用列表存起来，有重复的就停止
    try:
        while True:
            url = next_url(blog_id,uid,max_id)
            html_json = request(url)
            max_id,infos = parse(html_json)
            sum += len(infos)
            
            if max_id in ids:
                
                save(infos)
                count += 1
                print(max_id)
                print(ids)
                print( f'最后一页第{count}页评论爬取完毕! 共爬取{sum}条评论。')
                break
            ids.append(max_id)
            #解析得到的json数据,				返回的json数据data可能为空
            if infos==[]:
            	continue
            save(infos)
            count += 1
            print(f'第{count}页爬取完毕,已爬取{sum}条评论')
             
    except Exception as e:
        print(f'出现{e}错误!')
 
if __name__ == '__main__':
	createFile()
	#根据提示输入网址   
	prompt=input('请输入第一条评论数据网址或者微博app评论分享网址: ')
	      
    #根据输入的网址得到文章id和博主id
	blog_id,uid = get_ids(prompt)
    #创建会话以后用session请求会自带第一次请求时设置的cookie信息
	session = requests.session()
    #构造第一条json数据的网址
	url =f'https://weibo.com/ajax/statuses/buildComments?flow=0&is_reload=1&id={blog_id}&is_show_bulletin=2&is_mix=0&count=10&uid={uid}'
    #请求并获得json数据
	html_json = session.get(url=url,headers=headers).json()
    
    #解析得到的json数据
	max_id,infos= parse(html_json)
    
    #保存用户名和评论
	save(infos)
	sum = len(infos)
	print(f'第1页爬取完毕,已爬取{sum}条评论')
	count =1
	main(blog_id,uid,max_id,sum,count)

'''
返回的json数据data可能为空,但是max_id还是一直在更新的
微博app分享的网址 
https://share.api.weibo.cn/share/277336167.html?weibo_id=4720172260658025
277开头为博主id, weibo_id为文章id

#展开全部评论后的没有type=feed

详细页
https://weibo.com/ajax/statuses/buildComments? 
flow=0固定的
&is_reload=1固定的
&id=4717308905260981博文id
&is_show_bulletin=2
&is_mix=0 是否展开详细
&fetch_level=1 固定
&max_id=0 第一条没有，最后一条为0,后面的maxid由前一条json数据得到
&count=20  固定 第一条为10
&uid=用户id
'''
