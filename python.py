from selenium import webdriver
from lxml import etree

url = input("请输入小说爬取网址")
option = webdriver.ChromeOptions()
option.add_argument('headless')  # 创建浏览器参数，此处设置为浏览器后台运行
bro = webdriver.Chrome(options=option, executable_path='chromedriver')  # 利用给定的参数和给出的浏览器驱动进行模拟的浏览器创建
bro.get(url)  # 利用给定的url进行网站访问
bro_source = bro.page_source  # 将网站的所有信息导出
tree = etree.HTML(bro_source)  # 将网站的信息进行etree存储以方便提取信息
print("导入html成功")
origin_dd_list = tree.xpath('//div[@id="list"][2]/dl/dd')  # 利用xpath提取小说各个章节的标签并保存到标签列表中
print("创建dd列表成功")
print(origin_dd_list)
bro.quit()  # 关闭模拟浏览器以免内存溢出
url_prefix = 'https://www.xinwanben.com'
fp = open('./和反派.txt', "w", encoding='utf-8')  # 创建小说将要保存的txt文件
for dd in origin_dd_list:  # 对小说的每一个章节进行操作
    url_medium = url_prefix + str(dd.xpath('./a/@href')[0].encode('utf-8'), 'utf-8')  # 拼接小说各个章节的url
    bro_medium = webdriver.Chrome(options=option, executable_path='chromedriver')  # 创建新的模拟浏览器
    print(url_medium)
    bro_medium.get(url_medium)  # 将网站的所有信息导出
    medium_tree = etree.HTML(bro_medium.page_source)  # 将网站的信息进行etree存储以方便提取信息
    p_list = medium_tree.xpath('//div[@class="content"]/p')  # 利用xpath提取小说各个章节中的分行内容并保存到分行内容列表中
    print(str(medium_tree.xpath('//title/text()')[0].encode('utf-8'), 'utf-8'))
    title_name_bytes = medium_tree.xpath('//title/text()')[0].encode('utf-8')  # 利用xpath提取小说各个章节的标题
    title_name = str(title_name_bytes, 'utf-8')  # 将二进制格式转化成字符串格式
    fp.write(title_name + '\n' + '\n' + '\n')  # 将小说各个章节的标题写入txt文件中
    for p in p_list:  # 对小说各个章节的分行内容进行操作
        content = p.xpath('./text()')[0]  # 将小说各个章节的分行内容提取出来
        final_content = str(content.encode('utf-8'), 'utf-8')  # 将二进制格式转化成字符串格式
        fp.write(final_content)  # 将分行内容写入txt文件中
        print("成功")
    bro_medium.quit()  # 关闭该模拟浏览器
    b = "下一页"
    a = str(medium_tree.xpath('//a[@id="next_url"]/text()')[0].encode('utf-8'),
            'utf-8')  # 该网站的单页网页有时候不会完整显示一整章的小说，此时需要进行下一页的小说章节提取
    if a.strip() == b.strip():
        print("找到了")
        url_final = url_prefix + str(medium_tree.xpath('//a[@id="next_url"]/@href')[0].encode('utf-8'),
                                     'utf-8')  # 拼接小说章节下一页的url
        bro_final = webdriver.Chrome(options=option, executable_path='chromedriver')  # 创建新的模拟浏览器
        print(url_final)
        bro_final.get(url_final)  # 将网站的所有信息导出
        final_tree = etree.HTML(bro_final.page_source)  # 将网站的信息进行etree存储以方便提取信息
        p_list_final = final_tree.xpath('//div[@class="content"]/p')  # 利用xpath提取小说各个章节中的分行内容并保存到分行内容列表中
        for pp in p_list_final:  # 对小说各个章节的分行内容进行操作
            content_final = pp.xpath('./text()')[0]  # 将小说各个章节的分行内容提取出来
            final_content_next = str(content_final.encode('utf-8'), 'utf-8')  # 将二进制格式转化成字符串格式
            fp.write(final_content_next)  # 将分行内容写入txt文件中
            print("chenggong")
        bro_final.quit()  # 关闭该模拟浏览器
    fp.write('\n' + '\n' + '\n' + '\n')
