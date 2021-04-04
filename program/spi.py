import re
import uuid
import requests
import os
import numpy
import imghdr
import time
from PIL import Image
from MovieWeb.models import*
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}

download_max=1
# 获取百度图片下载图片
def download_image(id):
    download_sum = 0
    str_gsm = '80'
    # 把每个类别的图片存放在单独一个文件夹中
    save_path = 'C:/Users/Komorebi/Desktop/back/media/personimg'
    # save_path = 'C:/Users/Komorebi/Desktop/back/media/moviecover'
    person=Person.objects.get(personid=id)
    # movie=Movie.objects.get(movieid=id)
    key_word=person.name
    # key_word = movie.name

    if not os.path.exists(save_path):
        os.makedirs(save_path)
    while download_sum < download_max:
        # 下载次数超过指定值就停止下载
        if download_sum >= download_max:
            break
        str_pn = str(download_sum)
        # 定义百度图片的路径
        url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&' \
              'word=' + key_word + '&pn=' + str_pn + '&gsm=' + str_gsm + '&ct=&ic=0&lm=-1&width=0&height=0'
        # print('正在下载 %s 的第 %d 张图片.....' % (key_word, download_sum))
        try:
            # 获取当前页面的源码
            result = requests.get(url, timeout=30,headers=headers).text
            # 获取当前页面的图片URL
            img_urls = re.findall('"objURL":"(.*?)",', result, re.S)
            if len(img_urls) < 1:
                break
            # 把这些图片URL一个个下载
            for img_url in img_urls:
                # 获取图片内容
                img = requests.get(img_url, timeout=30)
                st=str(uuid.uuid1())
                img_name = save_path + '/' +st + '.jpg'
                # print(img_name)
                # 保存图片
                with open(img_name, 'wb') as f:
                    f.write(img.content)
                person.img='http://127.0.0.1:8000/'+'media/'+'personimg/'+st + '.jpg'.split('\n')[0]
                person.save()
                # movie.cover='http://127.0.0.1:8000/'+'media/'+'moviecover/'+str(int(time.time())) + '.jpg'.split('\n')[0]
                # movie.save()
                download_sum += 1
                if download_sum >= download_max:
                    break
        except Exception as e:
            print('【错误】当前图片无法下载，%s' % e)
            download_sum += 1
            continue

    print(person.personid)
    print('下载完成')




