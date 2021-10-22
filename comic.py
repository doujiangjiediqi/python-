from selenium import webdriver
from selenium.webdriver.common.by import By
from lxml import etree
import requests
import os
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

url = input("请输入漫画爬取网址")
bro = webdriver.Chrome(executable_path='chromedriver')  # 利用给定的参数和给出的浏览器驱动进行模拟的浏览器创建
bro.get(url)
right_click = bro.find_element(By.CLASS_NAME, "menu_catelog")
ActionChains(bro).click(right_click).perform()  # 该网站需要进行点击从而转换网页信息
print("点击成功")
btn = bro.find_element(By.CLASS_NAME, "moreComment")  # 该网站需要点击更多内容从而获取全部的章节信息
btn.click()
print("刷新目录成功")
sleep(5)
bro_source = bro.page_source  # 将网站的所有信息导出
tree = etree.HTML(bro_source)  # 将网站的信息进行etree存储以方便提取信息
print("导入html成功")
origin_a_list = tree.xpath('//ul[@class="catalog_list row_catalog_list"]/a')  # 利用xpath提取漫画各个章节的标签并保存到标签列表中
print("创建a列表成功")
bro.quit()
url_prefix = 'http://m.qiximh1.com'
head = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
}
for a in origin_a_list:
    url_medium = url_prefix + str(a.xpath('./@href')[0].encode('utf-8'), 'utf-8')  # 拼接漫画各个章节的url
    bro_medium = webdriver.Chrome(executable_path='chromedriver')  # 利用给定的参数和给出的浏览器驱动进行模拟的浏览器创建
    bro_medium.get(url_medium)  # 将网站的所有信息导出
    medium_tree = etree.HTML(bro_medium.page_source)  # 将网站的信息进行etree存储以方便提取信息
    div_list = medium_tree.xpath('//div[@class="chapter_content"]/div')  # 利用xpath提取漫画各个章节中的各个图片内容并保存到图片内容列表中
    title_name_bytes = medium_tree.xpath('//title/text()')[0].encode('utf-8')  # 利用xpath提取漫画 各个章节的标题
    title_name = str(title_name_bytes, 'utf-8')  # 将二进制格式转化成字符串格式
    b = os.getcwd()
    file_path = b + '/' + title_name
    if not os.path.exists(file_path):  # 创建以漫画分章节标题为文件夹名称的文件夹
        os.mkdir(file_path)
    print("创建文件夹成功")
    i = 1
    for div in div_list:  # 对漫画各个章节的每一个图片内容进行操作
        img_src = div.xpath('./img/@src')[0]  # 获取漫画的img和href信息
        url = img_src.encode('utf-8')
        img_data = requests.get(url=url, headers=head).content  # 利用已经获取的图片url爬取图片
        string_name = str(url, 'utf-8')
        with open('./' + title_name + '/' + str(i) + '.jpg', "wb") as fp:
            fp.write(img_data)  # 将文件保存到文件夹中
        i = i + 1
        print("成功")
    bro_medium.quit()  # 关闭该模拟浏览器
