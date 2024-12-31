import math
import os.path
import re
import string
import tkinter as tk
from PIL import Image, ImageTk
from spire.pdf.common import *
from spire.pdf import *
from gbutil import htmlutil
import os


# 简易版——图片转换为pdf，pdf页面随图片大小浮动
def images2pdf(image_file_path, output_path, gb_code):
    os.chdir(image_file_path)
    images = []
    file_lis = os.listdir(image_file_path)
    output_path_pdf = f"{output_path}/{gb_code}.pdf"
    con = 0
    for image_path in file_lis:
        if image_path.endswith(('.jpg', '.png')):
            image = Image.open(image_path)
            # 缩小图片尺寸以减小导出文件大小
            images.append(image.convert("RGB").resize((int(image.width * 0.6), int(image.height * 0.6))))
            con += 1
            print(f'\r转换为pdf,进度：%.2f' % (con/len(file_lis) * 100) + '%', end='')
            # print(image_path + '：第%d张' % con)
    images[0].save(output_path_pdf, save_all=True, append_images=images[1:], resolution=168)
    print(f'\n转换pdf完成，存放于：{output_path}')


def images2pdf2(folder_path, output_path, gb_code):
    # spire.pdf试用版有水印，有页数限制，只能添加10页
    # 创建一个PdfDocument类的对象
    pdf = PdfDocument()

    # 清除文档页边距
    pdf.PageSettings.SetMargins(0.0)

    # 循环遍历文件夹中的图片
    # folder_path = "Images/"
    for root, directories, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            # 载入图片
            image = PdfImage.FromFile(file_path)
            # 获取图片的宽和高
            image_width = image.PhysicalDimension.Width
            image_height = image.PhysicalDimension.Height
            # 在文档中创建与图片相同大小的页面
            page = pdf.Pages.Add(SizeF(image_width, image_height))
            # 将图片绘制在页面上
            page.Canvas.DrawImage(image, 0.0, 0.0, image_width, image_height)

    # 保存PDF文档
    pdf.SaveToFile(output_path + f"/{gb_code}.pdf")
    pdf.Close()


def create_dir(output_dir: string):
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print('输出目录' + output_dir + '已创建')
        except Exception as e:
            print('创建目录' + output_dir + '失败，请手动创建后再运行程序')


def center_window(root, width, height):
    # 获取屏幕尺寸
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 计算窗口位置
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # 设置窗口位置
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.attributes('-topmost', 'true')


def show_image(image_path: str) -> None:
    """
    根据图片地址，弹出对话框显示一张图片
    :param image_path: 图片路径
    :return: None
    """

    # 创建一个简单的Tkinter窗口
    # win = tk.Toplevel()
    # win.attributes('-topmost', 'true')

    root = tk.Tk()
    root.title("验证码")

    # 加载图片
    image = Image.open(image_path)
    image = ImageTk.PhotoImage(image)
    h = image.height()
    w = image.width()

    # 创建一个标签来显示图片
    label = tk.Label(root, image=image)
    label.place(relx=0.5, rely=0.5, anchor="center")

    # 设置窗口位置在屏幕中央
    center_window(root, w, h)
    label.pack()

    # 进入Tkinter事件循环
    root.mainloop()


def merge_image(page_div, img_urls, tmp_img_path, output_img_path):
    if os.path.exists(tmp_img_path):
        if os.path.isdir(tmp_img_path) and len(os.listdir(tmp_img_path)) > 0:

            page_id = page_div.xpath('./@id')[0]
            # print('拼接第' + page_id + '页')
            for data in img_urls:
                if data['id'] == page_id:
                    url = data['url']
                    image_name = htmlutil.get_image_name(url)
                    # pdf页面大小
                    pdf_style = page_div.xpath('./@style')[0]
                    pdf_style_2 = re.findall('\d+', pdf_style)
                    pdf_size_w = int(pdf_style_2[0])  # pdf页面宽度
                    pdf_size_h = int(pdf_style_2[1])  # pdf页面高度
                    img_slice_w = math.ceil(pdf_size_w/10)  # 图片切片宽度
                    img_slice_h = math.ceil(pdf_size_h/10)  # 图片切片高度
                    im = Image.open(tmp_img_path + '\\' + image_name)
                    im_1 = Image.new(mode='RGB', size=(pdf_size_w, pdf_size_h), color='#ffffff')

                    # 遍历pdf页面div下的所有切片span
                    for span in page_div.xpath('./span'):
                        # 获取图片切片在pdf页面上的坐标
                        span_class = span.xpath('./@class')[0]  # class pdfImage-1-5
                        pdf_row = int(span_class.split('-')[1])
                        pdf_col = int(span_class.split('-')[2])
                        # 图片切片在bg图片上的位置偏移
                        span_bg_pos = span.xpath('./@style')[0]  #
                        span_bg_pos_2 = re.findall('\d+', span_bg_pos)
                        # print(span_bg_pos_2)
                        span_bg_x = int(span_bg_pos_2[0])  # 偏移量x
                        span_bg_y = int(span_bg_pos_2[1])  # 偏移量y
                        # print(span_bg_x)

                        # 拼接图片
                        im_crop = im.crop((span_bg_x, span_bg_y, span_bg_x + img_slice_w, span_bg_y + img_slice_h))
                        im_1.paste(im_crop, (pdf_row * (img_slice_w-1), pdf_col * (img_slice_h-1)))
                    # im_1.show()
                    # 缩小页面尺寸
                    # im_1 = im_1.resize((int(im_1.width * 0.8), int(im_1.height * 0.8)), 3)
                    im_1.save(output_img_path + '\\' + page_id.rjust(4, '0') + '.jpg', optimize=True)



