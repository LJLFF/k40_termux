from aip import AipOcr
import re
#创建并配置客户端
APP_ID='17155268'
API_KEY ='u6TWp9YGcI6CHzFzOF28E2i1'
SECRECT_KEY='ehEj7TInsEK9z2owRNCmYK6XAWM76R3a'
client=AipOcr(APP_ID,API_KEY,SECRECT_KEY)

#以二进制模式打开图片
i=open(r'/storage/emulated/0/DCIM/Screenshots/Screenshot_2021-11-29-17-45-41-332_com.quark.browser.jpg','rb')
#读取图片数据
img=i.read()

#客户端调用基本通用接口识别图片返回数据
message=client.basicGeneral(img)

#解析返回的json数据
num = message['words_result_num']
word = message['words_result']

for i in range(num):
	print(word[i]['words'])
