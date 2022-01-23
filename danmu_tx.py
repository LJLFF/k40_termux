import requests
import json
import json


def getHtmlWHeaders(sites: str, Headers:dict):
    url = sites
    headers = Headers
    return requests.get(url, headers=headers)  # 请求#Get方式获取网页数据

#按时间戳排序       
def sortCommentByTimestamp(commentList):
    retList = []
    while len(commentList)>0:
        minIndex = 0
        for i in range(len(commentList)):
            #第i秒
            timei = int(commentList[i]['timepoint'])
            #最小的时间戳
            timemin = int(commentList[minIndex]['timepoint'])
            # print('timei = '+str(timei))
            # print('timemin = '+str(timemin))
            #遍历整个列表 发现小于第一个默认最小值，马上把该值设置为默认值,类似于冒泡排序,循环一遍找出最小值,拿出最小值,剩下的继续找最小值
            if timei<timemin:
                # print('min='+minIndex)
                minIndex = i
        # print("min="+str(minIndex))
        #循环一遍找到最小值拿出来添加到新列表
        retList.append(commentList[minIndex])
        #原列表删除最小值，继续找剩下的序列里的最小值
        commentList.remove(commentList[minIndex])
        #执行完跳到while循环继续，直到原列表为空返回从小到大排好的列表
    return retList
   

def getFileName():
	return "蒙面舞王第二季第3期弹幕.txt"
	
def getDanmuUrl():
    # 蒙面舞王第二季第2期加更弹幕
    # url = 'https://mfm.video.qq.com/danmu?\
        # otype=json\
            # &target_id=7264589648%26vid%3Dw0040l0i2eh\
                # &timestamp='
    # 蒙面舞王第二季第3期弹幕
    url = 'https://mfm.video.qq.com/danmu?\
        otype=json\
            &target_id=7281637289%26vid%3Dm0040g1zszc\
                &timestamp='
    # 蒙面舞王第二季第3期加更弹幕
    # url = 'https://mfm.video.qq.com/danmu?\
    #     otype=json\
    #         &target_id=7293623523%26vid%3Dr0040t80yua\
    #             &timestamp='
    # 蒙面舞王第二季第4期弹幕
    # url = 'https://mfm.video.qq.com/danmu?otype=json&target_id=1227342321%26vid%3Dr0018hmh1pa&timestamp='
    return url
    
def getEndTimePoint():
    # 蒙面舞王第二季第3期时长
    endTimePoint = 4574
    # 蒙面舞王第二季第3期加更时长
    # endTimePoint = 5851
    # # 蒙面舞王第二季第4期时长
    # endTimePoint = 5660
    return endTimePoint

def main():

    # ↓ 这里是爬取不同的弹幕要修改的代码
    # 文件名
    filename = getFileName()
    # 构造url
    # 弹幕的请求地址
    url = getDanmuUrl()
    # 视频的总时间长度，单位为秒数
    endTimePoint = getEndTimePoint()
    # ↑
# 存储弹幕所有的请求地址的list
    urlList = []
    # 要获取的弹幕是哪个时间点的弹幕
    timestamp = 0
    # 弹幕获取的间隔是30s，即在第0s和第29s对地址发起请求所获取到的弹幕内容是相同的
    # 而第0s和第30s获取到的内容是不同的
    # 即腾讯视频上虽然看到的是一条条弹幕飘过、滑过、飞过
    # 但是实际上是每30s请求一批批批批批批批批弹幕内容
    # 再使用javascript让请求到的所有弹幕一条条条条条地展示出来而已
    step = 30
    # 构造所有的弹幕数据请求地址
    while timestamp <= endTimePoint:
        urlList.append(url+str(timestamp))
        timestamp += step
    # 确保最后的一批弹幕是获取到了的
    if timestamp > endTimePoint:
        urlList.append(url+str(endTimePoint))
    headers = {} # 其实请求弹幕不需要用headers，只是自己封装的工具类需要有这个参数，懒得改了...就设为空了
    with open(filename, 'w', encoding='utf-8') as f1:
        # 遍历每个url
        for i in range(len(urlList)):
            print()#默认end参数＝换行
            print(url)
            # 便于查看当前进度的，表示当前进行到哪条url了
            print('url: '+str(i)+'/'+str(len(urlList)))
            url = urlList[i]
            response = getHtmlWHeaders(url, headers)
            # 下面这行代码应该是通用的，就是避免有些网页的编码格式和本地的编码格式不匹配，导致中文或者部分字符出现乱码的情况
            # 这行代码意思就是，首先获取response.text这个字符串，然后对这个字符串使用网页响应内容所使用的编码格式（这个编码格式是随响应灵活变化的）进行编码，再使用通用的“utf-8”格式解码
            html = response.text.encode(response.encoding).decode('utf-8')
            # 通过输出可以知道这里的html变量，也就是请求后的响应内容就是json字符串的格式，因此直接json.loads转换为json对象数组
            htmlObj = json.loads(html)
            # print(htmlObj)
            # 存储每条弹幕信息对象的list
            commentList = []
            try:
            	# 将响应中的弹幕信息提取出来
                commentList = htmlObj['comments']
            except:
                print(htmlObj)
                print('htmlObj error')
                # 出了错就直接关闭整个程序
                exit()
            # 这里排序是为了使弹幕按照发送的时刻从小到大进行排序，便于观看的时候可以从前往后看
            commentList = sortCommentByTimestamp(commentList)
            
            for j in range(len(commentList)):
                try:
                    comment = commentList[j]
                    print('comment: '+str(j)+'/'+str(len(commentList)))
                    # 发送弹幕的时刻，在视频播放的多少秒发送的
                    sendPointStr = str(comment['timepoint'])
                    # 弹幕内容
                    commentContent = comment['content']
                    # 点赞数
                    upcountStr = str(comment['upcount'])
                    dataToWrite = '[ '+sendPointStr +'s ]: '+commentContent +' 点赞数：'+upcountStr 
                    print(dataToWrite)
                    f1.write(dataToWrite+'\n')    
                except:
                    print('error')
main()