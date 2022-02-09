import requests
import json
class BaiduTranslate:
    def __init__(self,url,content):
        self.url=url
        self.headers={
            "User-Agent": "Mozilla / 5.0(Linux;Android6.0;Nexus5Build / MRA58N) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 97.0.4692.71MobileSafari / 537.36"
        }
        self.data={
            "kw": content
        }
    def res(self):
        response=requests.post(self.url,headers=self.headers,data=self.data)
        return response.content.decode()
 
    def print(self,content):
        print(content[0]['k'],content[0]['v'].split(';')[0], sep=': ')
        #for item in content:
            #print(item['k']+':'+item['v'])
 
    def run(self):
        txt=self.res()
        content=json.loads(txt)
        self.print(content['data'])
 
if __name__ == '__main__':
    
    while True:
        try:
        	content=input('请输入需要翻译的内容：')
        	ran=BaiduTranslate("https://fanyi.baidu.com/sug",content)
        	ran.run()
        except Exception as e:
        	print('请输入中文或者英文!')
        	continue
        	
        