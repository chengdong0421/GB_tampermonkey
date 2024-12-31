from time import sleep

import requests
from bs4 import BeautifulSoup
import string
import urllib.request


def get_bgs(page_divs):
    """
    解析class=page的div,返回div的id和bg对应关系
    :param page_divs:
    :return:
    """
    bgs = []
    for page_div in page_divs:
        page_id = page_div.xpath('./@id')[0]
        page_bg = page_div.xpath('./@bg')[0]
        bgs.append({'id': page_id, 'bg': page_bg})
    return bgs


def get_img_urls(bgs: list, jsessionid: string, common_headers):
    img_urls = []
    count = 0
    for bg in bgs:
        count += 1
        print(f'\r解析进度：%.2f' % (count/len(bgs) * 100) + '%', end="")
        bg_str = bg['bg']
        url_img = 'http://c.gb688.cn/bzgk/gb/viewGbImg?fileName=' + bg_str
        req_img = urllib.request.Request(url_img, headers=common_headers)
        req_img.add_header('Cookie', 'JSESSIONID=' + jsessionid)
        with urllib.request.urlopen(req_img) as res_img:
            if res_img.status == 200:
                img_urls.append({'id': bg['id'], 'bg': bg['bg'], 'url': res_img.url})
    return img_urls


def download_img(img_url: string, jsessionid: string, common_headers, img_name):
    print('开始下载: ' + img_name)
    req_img_redirect = urllib.request.Request(img_url, headers=common_headers)
    req_img_redirect.add_header('Cookie', 'JSESSIONID=' + jsessionid)
    req_img_redirect.add_header('Cache-Alive', 'chunked')
    img_response = urllib.request.urlopen(req_img_redirect)

    page_img = img_response.read()

    with open(img_name, 'w+b') as pageImgFile:
        pageImgFile.write(page_img)
        pageImgFile.close()
    sleep(2)
    print('下载完成: ' + img_name)

    return 0


def get_title(full_html):
    """
    从html文件内容获取title
    :param full_html:
    :return:
    """
    return full_html.xpath('//title/text()')[0]


def get_hcno(preview_url):
    """
    从在线预览url中提取hcno
    :param preview_url:
    :return:
    """
    return preview_url.split('hcno=')[1]


def get_image_name(image_url):
    """
    从图片url地址中获取图片文件名
    :param image_url:
    :return:
    """
    return image_url.split('/')[-1]


def get_gb_code_from_image_url(image_url: string):
    """
    从图片url地址中获取国标编码
    :param image_url:
    :return:
    """
    return image_url.split('/')[-2].replace('/', '_')


def get_gb_code_from_title(gb_title: string):
    """
    从html页面title中获取国标编码
    :param gb_title:
    :return:
    """
    return gb_title.split('|')[1].replace(' ', '').replace('/', '_')
