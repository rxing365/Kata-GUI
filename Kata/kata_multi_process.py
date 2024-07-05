# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 13:21:13 2024

@author: 28187
"""
import sys
from janome.tokenizer import Tokenizer
import re
from pykakasi import kakasi
from bs4 import BeautifulSoup
import os
import shutil
import zipfile
from concurrent.futures import ProcessPoolExecutor
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage


output_folder = "temp_kata_gui"
output_html_path = 'html_kata_gui'


def empty_folder(folder_path):
    shutil.rmtree(folder_path, ignore_errors=True)
    os.makedirs(folder_path, exist_ok=True)


def convert_to_gotou(word):
    conv = kakasi()
    result = conv.convert(word)
    result_with_brackets = ""

    for item in result:
        result_with_brackets += "<ruby><rb>{}</rb><rt>{}</rt></ruby>".format(item['orig'], item['hira'])

    return result_with_brackets


def is_first_character_kanji(word):
    kanji_pattern = re.compile(r'^[\u4e00-\u9faf]')
    return bool(re.match(kanji_pattern, word[0]))


def process_japanese_text_with_conversion(text, flag):
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(text)
    result = ""

    for token in tokens:
        word = token.surface
        if word in ['<', 'ruby', '>', '</', 'rt', '></', '><']:
            result += f"{word}"
        elif word == "rb":
            flag = not flag
            result += f"{word}"
        elif flag and is_first_character_kanji(word):
            conv = kakasi()
            converted_word = conv.convert(word)[0]
            result += f"<ruby><rb>{converted_word['orig']}</rb><rt>{converted_word['hira']}</rt></ruby>"
        else:
            result += f"{word}"
    return result


def extract_and_save_html_from_epub(epub_file_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with zipfile.ZipFile(epub_file_path, 'r') as epub_zip:
        file_list = epub_zip.namelist()

        for file_name in file_list:
            if file_name.lower().endswith(('.html', '.xhtml')):
                content = epub_zip.read(file_name).decode('utf-8')
                soup = BeautifulSoup(content, 'html.parser')
                clean_content = soup.prettify()

                output_file_path = os.path.join(output_folder, os.path.basename(file_name))

                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    output_file.write(clean_content)

                print(f"Extracted: {output_file_path}")


def create_new_html(file_path, _output_html_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')

    paragraphs = soup.body.find_all('p')
    flag = True
    for paragraph in paragraphs:
        p = paragraph
        processed_text = process_japanese_text_with_conversion(paragraph.prettify(), flag)
        paragraph.string = ''
        paragraph.append(BeautifulSoup(processed_text, 'html.parser'))
    filename = os.path.basename(file_path)
    output_new_html_path = os.path.join(_output_html_path, filename)
    with open(output_new_html_path, 'wb') as new_file:
        new_file.write(str(soup).encode('utf-8'))


def get_book_contents_location(unzipped_epub_path):
    result = "OEBPS\\xhtml"
    # 解析XML文件
    with open(unzipped_epub_path + "\\META-INF\\container.xml", 'r', encoding='utf-8') as file:
        xml_data = file.read()
    root = ET.fromstring(xml_data)

    opf_location = root[0][0].attrib['full-path']
    # 解析opf文件
    with open(unzipped_epub_path + "\\" + opf_location, 'r', encoding='utf-8') as file:
        xml_data = file.read()
    root = ET.fromstring(xml_data)
    # 查找含有内容位置的标签
    first_item = root.find('.//{http://www.idpf.org/2007/opf}item[@media-type="application/xhtml+xml"]')

    # 获取href属性
    href_attribute = first_item.get('href')

    # 获取opf的所在目录，内容的目录是基于opf文件位置的
    directory_1 = os.path.dirname(opf_location)

    # 获取内容（html文件）所在目录
    directory_2 = os.path.dirname(os.path.join(directory_1, href_attribute))

    # print(directory_2)

    return directory_2


def replace_files_in_epub(epub_path, source_folder, output_epub_path):
    temp_dir = "temp_epub"
    os.makedirs(temp_dir, exist_ok=True)
    book_contents_dir = ""

    try:
        with zipfile.ZipFile(epub_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        book_contents_dir = get_book_contents_location(temp_dir)

        shutil.rmtree(os.path.join(temp_dir, book_contents_dir), ignore_errors=True)
        shutil.copytree(source_folder, os.path.join(temp_dir, book_contents_dir))

        with zipfile.ZipFile(output_epub_path, 'w') as zip_ref:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    zip_ref.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), temp_dir))

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def process_single_html_file(file_name):
    file_path = os.path.join(output_folder, file_name)
    create_new_html(file_path, output_html_path)
    print(f"Working on {file_path}...")


def process_all_files_in_folder_parallel(folder_path):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # 多进程代码
    with ProcessPoolExecutor() as executor:
        executor.map(process_single_html_file, files)
    # 单进程代码
    # for file_path in files:
    #     process_single_html_file(file_path)


def process_epub(epub_file_path):
    print("Working...")
    empty_folder(output_folder)
    empty_folder(output_html_path)
    extract_and_save_html_from_epub(epub_file_path, output_folder)
    process_all_files_in_folder_parallel(output_folder)
    final_output_path = os.path.join(os.path.dirname(epub_file_path), "new_" + os.path.basename(epub_file_path))
    replace_files_in_epub(epub_file_path, output_html_path, final_output_path)

    # 获取当前运行目录
    current_directory = os.getcwd()

    # 定义要删除的文件夹名称
    folders_to_delete = [output_folder, output_html_path]

    # 遍历文件夹列表并删除它们
    for folder in folders_to_delete:
        folder_path = os.path.join(current_directory, folder)
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            print(f"Deleted folder: {folder_path}")
        else:
            print(f"Folder does not exist: {folder_path}")


def process_file(epub_file_path):
    if os.path.splitext(epub_file_path.lower())[1] == '.epub':
        try:
            process_epub(epub_file_path)
        except FileNotFoundError:
            print(f"'{epub_file_path}' NOT FOUND.")
        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            print("COMPLETED")
    else:
        print("NOT AN EPUB FILE!")


def select_file():
    # 打开文件选择对话框并获取文件路径
    file_path = filedialog.askopenfilename()
    if file_path:  # 如果用户选择了文件，更新标签内容以显示文件路径
        path_label.config(text=file_path)


def process_button_click():
    # 获取用户选择的文件路径并处理文件
    file_path = path_label.cget("text")
    if file_path:  # 确保用户选择了文件
        process_file(file_path)
        completion_label.config(text="Completed!")


def get_asset_path(filename):
    _dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    path = os.path.join(_dir, filename)
    return path


if __name__ == "__main__":
    # 创建主窗口
    root = tk.Tk()
    root.title("Kata - GUI")
    # 加载图标图像
    icon = PhotoImage(file=get_asset_path('icon/compose_edit_paper_pencil_write_icon.png'))
    # 设置窗口图标
    root.iconphoto(True, icon)

    # 创建标签和按钮
    path_label = tk.Label(root, text="", width=50, wraplength=300)
    select_button = tk.Button(root, text="Select .epub File", command=select_file)
    process_button = tk.Button(root, text="PROCESS", command=process_button_click)
    completion_label = tk.Label(root, text="", width=20)

    # 布局组件，增加按钮之间的间距
    path_label.pack(pady=10)  # 在标签上方增加10像素的间距
    select_button.pack(pady=10)  # 在按钮上方增加10像素的间距
    process_button.pack(pady=10)  # 在按钮上方增加10像素的间距
    completion_label.pack(pady=10)  # 在标签上方增加10像素的间距

    # 运行主循环
    root.mainloop()
