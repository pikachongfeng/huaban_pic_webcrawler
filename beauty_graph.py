#!/usr/bin/env python3
__author__ = 'zhangyangrong'
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver import Firefox
import requests
import lxml.html
import os

# SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
browser.set_window_size(1400, 900)

def parser(url, param):
    browser.get(url)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, param))) #等待直到定位到id为param的元素加载到dom树中
    html = browser.page_source #网页源码
    doc = lxml.html.fromstring(html) #变成字符串
    return doc
  
def get_main_url():
    print('打开主页搜寻链接中...')
    try:
        doc = parser('http://huaban.com/boards/favorite/beauty/', '#waterfall') #该网站用的是waterfall
        name = doc.xpath('//*[@id="waterfall"]/div/a[1]/div[2]/h3/text()') #h3是标题，具体到网页源码中看
        u = doc.xpath('//*[@id="waterfall"]/div/a[1]/@href') #href是文档url
        for item, fileName in zip(u, name):
            main_url = 'http://huaban.com' + item
            print('主链接已找到' + main_url)
            if '*' in fileName:
                fileName = fileName.replace('*', '')
            download(main_url, fileName)
    except Exception as e:
        print(e)

def download(main_url, fileName):
    print('-------准备下载中-------')
    try:
        doc = parser(main_url, '#waterfall')
        if not os.path.exists('image\\' + fileName):
            print('创建文件夹...')
            dirname='image/' + fileName
            os.makedirs(dirname)
        link = doc.xpath('//*[@id="waterfall"]/div/a/@href')
        # print(link)
        i = 0
        for item in link:
            i += 1
            minor_url = 'http://huaban.com' + item
            doc = parser(minor_url, '#pin_view_page')
            img_url = doc.xpath('//*[@id="baidu_image_holder"]/a/img/@src')
            img_url2 = doc.xpath('//*[@id="baidu_image_holder"]/img/@src')
            img_url +=img_url2
            try:
                url = 'http:' + str(img_url[0])
                print('正在下载第' + str(i) + '张图片，地址：' + url)
                r = requests.get(url)
                filename = './' + dirname + '/' + str(i) + '.jpg'
                with open(filename, 'wb') as fo:
                    fo.write(r.content)
            except Exception:
                print('出错了！')
    except Exception:
        print('出错啦!')


if __name__ == '__main__':
    get_main_url()