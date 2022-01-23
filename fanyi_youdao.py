from urllib import request, parse
import json
import tkinter as tk

#爬虫部分,传入输入得到结果
def youdao(value,result):
	#请求地址
	request_url ='http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'

	#请求参数
	form_Data ={
	'i':value, 
	'from':'AUTO',
	'to':'AUTO', 
	'smartresult':'dict', 
	'doctype':'json',
	'version':'2.1', 
	'keyform':'fanyi.web', 
	'typoResult':'false', 
	'client':'fanyideskweb'
	}
	
	#编码url参数
	data = parse.urlencode(form_Data).encode('utf-8')
	
	#发送请求
	response = request.urlopen(request_url,data)
	
	#得到响应获取二进制数据并解码为普通字符串
	html = response.read().decode('utf-8')
	
	#把字符串加载为json格式
	trans_res = json.loads(html)
	
	#如果能取到translateresult就继续往下取到想要的数据，否则返回一个空格
	show_label = trans_res['translateResult'][0][0]['tgt'] if trans_res.get('translateResult') else 'get json error'
	
	#把取到的内容以text为键添加到result字典
	result['text'] = f'{show_label}\n\n'


#tk界面部分
def init_form():
	#初始化一个界面
	form =tk.Tk()
	#设置标题
	form.title('有道中英互译')
	#设置界面大小
	form.geometry('300x260')
	
	
	#新建一个标签组件，布局到第一行
	tk.Label(form,text='在此输入待翻译内容：').grid(row=0,sticky=tk.W)
	#新建一个文本框组件并布局到第二行
	text =tk.Text(form,width=30,height=5)
	text.grid(row=1)
	
	#文本框插入默认值
	text.insert('insert','你好,世界')
	
	#新建一个标签组件布局到第三行,西(左)对齐
	tk.Label(form,text='翻译结果：').grid(row=2,sticky=tk.W)
	
	#新建一个标签,布局到第四行
	result =tk.Label(form,text='Hello,World',wraplength=400)
	result.grid(row=3)
	
	#新建一个按钮,点击执行翻译功能 ,get(1.0,'end') 行首取到行尾,就是取全部内容
	tk.Button(form,height=1,text="翻译",command=lambda : youdao(text.get(1.0,"end"),result)).grid(row=1,column=1)
	
	#退出按钮
	tk.Button(form,height=1,text="退出",command=form.destroy).grid(row=2,column=1)
	#界面开启循环,不一闪而过
	form.mainloop()
	
if __name__ == '__main__':
	init_form()
	
	
	