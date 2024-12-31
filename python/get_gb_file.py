import os.path
import urllib.request
import urllib.parse
from datetime import datetime as dt
import threading
from gbutil import imageutil, htmlutil
from lxml import html


# 定义一些常量
# 在线预览链接
# url_preview = "http://c.gb688.cn/bzgk/gb/showGb?type=online&hcno=5ED2A10D48EE5AFF5D7C04F2683767CC"
url_preview = "http://c.gb688.cn/bzgk/gb/showGb?type=online&hcno=2544D73CA09ACBA031ACCF546FFF871B"
url_preview = ""
# 接收用户输入的在线预览url
if url_preview == "":
    url_preview = input('请粘贴标准在线预览界面的url:')
    print(url_preview)


# 验证码url
url_code = "http://c.gb688.cn/bzgk/gb/gc?_" + str(round(dt.timestamp(dt.now())*100))
# 验证码验证url  post
url_vc = "http://c.gb688.cn/bzgk/gb/verifyCode"
# User Agent
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
# 共同请求头
common_headers = {
    'Connection': 'keep-alive',
    'Host': 'c.gb688.cn',
    'User-Agent': UA,
    'Referer': url_preview
}

# 程序当前目录
cwd = os.getcwd()
# pdf image暂存目录，和程序同级。该目录下建立以hcno为名的文件夹，存放该国标的pdfimage
tmp_dir = cwd + '\\' + 'tmp'
# 输出文件目录，和程序同级。该目录下建一个目录，以hcno命名，再建两个目录，images和pdf分别存放图片和pdf
output_dir = cwd + '\\' + 'output'

print('当前目录:' + cwd)


# 创建所需目录
imageutil.create_dir(tmp_dir)
imageutil.create_dir(output_dir)


def show_img_thread():
    imageutil.show_image('code.jpg')


# 请求在线预览url，获取cookie
req = urllib.request.Request(url_preview, headers=common_headers)
req.remove_header('Referer')
req.add_header('Referer', 'https://openstd.samr.gov.cn/')
with urllib.request.urlopen(req) as f:
    setcookie = f.getheader('Set-Cookie')
    jsessionid = setcookie.split(";")[0].split("=")[1]
    # print(jsessionid)

# 带cookie请求验证码url，获取验证码图片
req_code = urllib.request.Request(url_code, headers=common_headers)
req_code.add_header('Cookie', 'JSESSIONID=' + jsessionid)
res2 = urllib.request.urlopen(req_code)
img = res2.read()

# 存储验证码
with open('code.jpg', 'w+b') as f2:
    f2.write(img)
    f2.close()

# 开启显示验证码线程
t_show_img = threading.Thread(target=show_img_thread)
# 将子线程的daemon属性设置为True，这样，当主线程结束时，子线程也会随之结束
t_show_img.daemon = True
t_show_img.start()


# 读取用户输入
print('验证码已存储在' + cwd + '\\code.jpg')
print('弹出的验证码窗口被关闭后，忘记验证码可打开该code.jpg文件查看')
vcode = input("请输入验证码：")

# 输入验证码后，请求验证码验证url,获取在线预览页面html内容
data = urllib.parse.urlencode({'verifyCode': vcode})  # post请求需要传的数据
data = data.encode('ascii')
# 请求验证
req_verify = urllib.request.Request(url_vc, headers=common_headers)
req_verify.add_header('Cookie', 'JSESSIONID=' + jsessionid)
req_verify.add_header('Origin', 'http://c.gb688.cn')

with urllib.request.urlopen(req_verify, data) as f3:
    verify_result = f3.read().decode('utf-8')
    if verify_result == 'success':
        print('验证码正确')
    else:
        print('验证码错误, 将退出程序')
        exit(1)

    if f3.status == 200:
        print('请求页面...')
        req4 = urllib.request.Request(url_preview, headers=common_headers)
        req4.add_header('Cookie', 'JSESSIONID='+jsessionid)
        r4 = urllib.request.urlopen(req4)
        page_byte_content = r4.read()
        # 在线预览页面全部html内容
        page_str_content = page_byte_content.decode('utf-8')
        # print(page_str_content)


# 解析html内容，获取页面图片url
print('请求页面完成，开始解析页面...')
parsed_html = html.fromstring(page_str_content)

# 所有pdf页面div, 即class为page的div,是一个列表
page_divs = parsed_html.xpath('//div[@class="page"]')
# 获取所有页面所需的bg
bgs = htmlutil.get_bgs(page_divs)

# 请求页面图片url，下载图片（先下载图片，后面再统一拼接）
# 获取所有pdf页面图片url
img_urls = htmlutil.get_img_urls(bgs, jsessionid, common_headers)
print("\n解析完成，开始下载页面图片")

# 创建文件夹
title = htmlutil.get_title(parsed_html)
gb_code = htmlutil.get_gb_code_from_title(title)
tmp_img_path = tmp_dir + '\\' + gb_code
output_pdf_path = output_dir + '\\' + gb_code + '\\pdf'
output_img_path = output_dir + '\\' + gb_code + '\\images'

imageutil.create_dir(tmp_img_path)
imageutil.create_dir(output_pdf_path)
imageutil.create_dir(output_img_path)

with open(output_dir + '\\' + gb_code + '\\info.txt', 't+w') as gbinfo:
    gbinfo.write(f'国标编码：{gb_code}\n')
    gbinfo.write(f'国标在线预览地址：{url_preview}\n')
    gbinfo.close()

# 下载图片
for url_map in img_urls:
    url = url_map['url']
    image_name = htmlutil.get_image_name(url)
    if not os.path.exists(tmp_img_path + '\\' + image_name):
        htmlutil.download_img(url, jsessionid, common_headers, tmp_img_path + '\\' + image_name)
    else:
        print('图片已存在：' + tmp_img_path + '\\' + image_name)


# 拼接图片生成各页面image
page_no = 1
for page_div in page_divs:
    print(f'\r拼接第 ' + str(page_no) + ' 页, 共' + str(len(img_urls)) + '页', end="")
    page_no += 1
    imageutil.merge_image(page_div, img_urls, tmp_img_path, output_img_path)

print("\n")
print('拼接图片完成，存储于：' + output_img_path)
print('tmp目录内是下载的临时文件，可删除')

# pause = input("\n\n按回车退出程序")
# 各页面生成pdf文件
imageutil.images2pdf(output_img_path, output_pdf_path, gb_code)

pause = input("\n\n按回车退出程序")
