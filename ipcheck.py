#筛选出可用的代理ip，存入ip_list_OK 列表中
#随机从ip_list_OK 列表中选择一个作为代理ip

from bs4 import BeautifulSoup
import requests
import random
from fake_useragent import UserAgent
import lxml

#从代理ip网站获取代理ip列表函数，并检测可用性，返回ip列表

def get_ip_list(url):#获取可用的代理ip列表，存入ip_list_OK 列表中
    ua=UserAgent()
    headers = {
                "User-Agent": ua.random
                  }
    web_data = requests.get(url,headers=headers)
    
    soup = BeautifulSoup(web_data.text, 'lxml')
    ip_data = soup.find_all('tr')[1::]
    
    ip_list= [i.find_all('td')[0].text+':' + i.find_all('td')[1].text for i in ip_data]
    ip_list = list(set(ip_list))
    print("原始ip_list为：")
    print(ip_list)
    print(len(ip_list))
    ip_list_OK=[]
    count = 0
#for 与list.remove搭配容易出错 remove会更改list个数
    for ip in ip_list:
        count += 1
        try:
            proxy_host = "http://" + ip          
            proxy_temp = {"http": proxy_host}          
            res = requests.get("http://txt.go.sohu.com/ip/soip",headers=headers,proxies=proxy_temp,timeout=2)
            if res.status_code ==200:
            #只要不是200都抛出异常
            	print(proxy_host+"  is OK")
            	ip_list_OK.append(proxy_host)
        except Exception as e:
            print(proxy_host+"  is bad")
        print(f'第{count}个ip测试结束\n')
    #print("可用ip_list为：")
    
    #print(ip_list_OK)
    return ip_list_OK

def get_random_ip(ip_list):
    #随机从ip_list_OK 列表中选择一个代理ip
    if ip_list:
    	proxy_ip = random.choice(ip_list)
    	proxies = {'http': proxy_ip}
    	return proxies
    else:
    	print('没有可用的代理ip')

#调用代理
def call(proxies):
	url = 'http://47.117.3.117/myip'
	res = requests.get(url=url,proxies=proxies)
	res.raise_for_status
	print(res.text)

if __name__ == '__main__':
    url = 'https://www.kuaidaili.com/free/inha/'
    good_ip_list = get_ip_list(url)
    proxies = get_random_ip(good_ip_list)
    print(proxies)
    call(proxies)