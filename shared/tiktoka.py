#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author: https://github.com/wanghaisheng/
# @Update: 2022/03/17
from functools import partial
from pywebio import config, session
import tarfile
from pywebio.input import *
from pywebio.output import *
from pywebio.platform.flask import webio_view
from retrying import retry
from datetime import datetime
from .douyin_get_videos_user_sec_id_undetected import get_user_video_list_douyin_undetected
from werkzeug.urls import url_quote
from flask import Flask, request, jsonify, make_response
from flask import url_for
import re
from .scraper import  *

import json
import platform
import random
import time
import pandas as pd
import urllib
import os
import time
import requests
import unicodedata
import sys
from pywebio.session import defer_call, info as session_info, run_async, eval_js
from pywebio import start_server, output, config
import pickle
from plane import *
from shared.utils.contents.index import *

from .douyin_slidebreak_playwright import *
# from .douyin_get_videos_user_sec_id import get_user_video_list_douyin_pl, get_playright
import pandas as pd
from urllib.parse import urlparse, urlunsplit, urlsplit
from playwright.sync_api import sync_playwright
from .util import *


app = Flask(__name__)
title = "TikToka™ tiktok/douyin videos Batch Download tookit"
description = "TikToka tiktok videos batch download for one user,for specific hashtags,challenges or keywords,no wartermark videos"

headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.66'
    # "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
}

supportedlang = ['en', 'zh', 'fr', 'es', 'ru', 'vi', 'fil']


files = [file_path for _, _, file_path in os.walk('i18n/languages')]
for file_name in files[0]:  # note that it has list of lists
    if '.json' in file_name:
        if not file_name.split('.json')[0] in supportedlang:
            supportedlang.append(file_name.split('.json')[0])
# update new language just by add .json files


def translations(lang):
    if os.path.exists('i18n/languages/'+lang+'.json'):
        path = 'i18n/languages/'+lang+'.json'
    else:
        path = 'i18n/languages/en.json'

    with open(path, encoding='utf-8') as fd:
        return json.load(fd)


for idx, item in enumerate(supportedlang):
    labelname = item+'_labels'
    labelname = translations(item)
    en_labels = translations('en')
    # zh_labels = translations('zh')
    # es_labels = translations('es')
    # fr_labels = translations('fr')
    # ru_labels = translations('ru')
app.label = en_labels


def uri_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except:
        return False


def find_url(kouling,site):
    # Parse the link in the Douyin share password and return to the list
    # auto add separator between urls
    # try to deal  without http https
    # r = kouling.replace('https:', "http:").split('http://')
    # r = list(filter(None, r))
    # # r =extract(input,URL)
    # r = [x.replace(' ', '') for x in r]
    # r = ["https://"+x for x in r if len(x) > 5]

    douyinresult = []
    tiktokresult = []
    r = re.findall(
        'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', kouling)
    print('url separating', r)
    if 'user:' in kouling or "user：" in kouling:
        kouling = kouling.replace('user:', '')
        kouling = kouling.replace("user：", '')
        kouling = kouling.replace('\n', ' ')
        kouling = kouling.replace('\r', ' ')
        search_terms = kouling.split(' ')
        userprefix_douyin = 'https://www.douyin.com/user/'
        userprefix_tiktok = 'https://www.tiktok.com/'
        if len(search_terms) > 0:
            if site=='douyin':
                usersearch_douyin = User_search_douyin()


                for keyword in search_terms:
                    with use_scope('loading'):

                        put_loading(shape='border', color='success').style(
                            'width:4rem; height:4rem') 
                        put_text('try to search whether user exists ',keyword)                   
                        d = usersearch_douyin.user_search_douyin(keyword)
                        if len(d) > 0:
                            if validate_uidhome(userprefix_douyin+d[0]['secid']):

                                douyinresult.append(userprefix_douyin+d[0]['secid'])
                            else:
                                put_text('this user is banned or deleted',userprefix_douyin+d[0]['secid'])                   

                        usersearch_douyin.close()
                    clear('loading')
            elif site=='tiktok':
                usersearch_tiktok = User_search_tiktok()

                usersearch_tiktok.open_page_tiktok()
                print('found user keyword', search_terms)

                for keyword in search_terms:
                    t = usersearch_tiktok.user_search_tiktok(keyword)
                    if len(t) > 0:
                        tiktokresult.append(userprefix_tiktok+t[0]['secid'])

                usersearch_tiktok.close()
    URL = build_new_regex("URL", "https?:\\/\\/[!-+\\--~]+")
    url_lists = [[x.value for x in list(extract(t, URL))][0] for t in r]

    # url.append(formaturl(re.findall(regexpatternforurl,i.value)[0]))
    print('url validating', url_lists)
    url_lists = list(set(url_lists))

    for i in url_lists:
        if uri_validator(i):
            if 'douyin' in i:

                douyinresult.append(i)
            elif 'tiktok' in i:
                tiktokresult.append(i)
    if site=='douyin':
        return douyinresult
    elif site=='tiktok':
        return tiktokresult


def valid_check(data):
    # 校验输入的内容
    print('validate input start')
    # url_list = find_url(kou_ling)

    kou_ling = data

    userinput_url_list = re.findall(
        'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', kou_ling)
    print('found url in user input', userinput_url_list)
    # 对每一个链接进行校验
    if len(userinput_url_list) == 0:
        if 'user:' in kou_ling or "user：" in kou_ling:
            pass
        else:
            return '抖音分享口令有误!'


def clean_filename(string, author_name):
    # 替换不能用于文件名的字符
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", string)  # 替换为下划线
    # 表情类特殊符号是没法zip的
    filename = 'tiktokadownloader_' + new_title + '_' + author_name
    return filename


def clean_filename_new(string, author_name):
    # 替换不能用于文件名的字符
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", string)  # 替换为下划线
    # 表情类特殊符号是没法zip的
    CN_EN_NUM = sum([CHINESE, ENGLISH, NUMBER])

    filename = ' '.join([t.value for t in list(extract(string, CN_EN_NUM))])
    # filename = 'tiktokadownloader_' + new_title + '_' + author_name
    return filename


def error_do(e, func_name, input_value=''):
    # 输出一个毫无用处的信息
    display_label = app.label

    put_html("<hr>")
    put_error(display_label['unexpected_error_hint'])
    put_html(display_label['unexpected_error_hint_title'])
    put_table([
        ['函数名', '原因'],
        [func_name, str(e)]])
    put_html("<hr>")
    put_markdown(display_label['unexpected_error_hint_detail'])
    put_link(display_label['returnhome'], '/')
    # 将错误记录在logs.txt中
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open('logs.txt', 'a') as f:
        f.write(date + ":\n" + func_name + ': ' + str(e) +
                '\n' + "Input value: " + input_value + '\n')



def loadingbar(id, init=0, label=''):
    # 写一个进度条装装样子吧 :)
    set_scope(id, position=3)
    with use_scope(id):
        put_processbar(id, init, label)
        # for i in range(1, 4):
        #     set_processbar('bar', i / 3)
        #     time.sleep(0.1)
    # return


def gettiktokVideoUrl(vid):
    # vid='7060417683145133338'
    res=requests.get("api.tiktokv.com/aweme/v1/multi/aweme/detail/?aweme_ids=%5B" + vid + "%5D", headers)
    data = res.read()
    obj = json.loads(data.decode("utf-8"))
    return obj["aweme_details"][0]["video"]["play_addr"]["url_list"][0]



def get_tiktok_url(tiktok_link):
    # 校验TikTok链接
    if tiktok_link[:12] == "https://www.":
        return tiktok_link
    else:
        try:
            # 从请求头中获取原始链接
            response = requests.get(
                url=tiktok_link, headers=headers, allow_redirects=False)
            true_link = response.headers['Location'].split("?")[0]
            # TikTok请求头返回的第二种链接类型
            if '.html' in true_link:
                response = requests.get(
                    url=true_link, headers=headers, allow_redirects=False)
                true_link = response.headers['Location'].split("?")[0]
            return true_link
        except Exception as e:
            error_do(e, get_tiktok_url, tiktok_link)


def filter_deleted_videos(original_url, videoid):
    # 利用官方接口解析链接信息
    print('filer_deleted_videos getting video info', original_url)
    if videoid == '':
        videoid, videotitle = get_videoid_from_url(original_url)

    api_url = f'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={videoid}'
    print("Sending request to: " + '\n' + api_url)
    js = ''
    try:
        print('choose request')
        js = json.loads(requests.get(url=api_url, headers=headers).text)

    except:
        pass

    if len(js['item_list']) == 0:
        # if 'Windows' in platform.system():
        try:
            print('fitler_deleted_videos try playwright')
            with sync_playwright() as p:
                page, res = get_playright(p, api_url)
                js = res.json()
        except:

            driver = get_undetected_webdriver()
            print('undetected web driver started')
            print(api_url)
            driver.get(api_url)
            content = driver.page_source
            pre = driver.find_element_by_tag_name("pre").text
            js = json.loads(pre)

    if len(js['item_list']) == 0:
        print('video is deleted')
        return True, '', ''
    else:
        print('video is ok')

        return False, js, videoid


def get_videoid_from_url(original_url):
    videoid = ''
    videotitle = ''
    if 'https://www.douyin.com/video' in original_url:
        if '?' in original_url:
            original_url = original_url.split('?')[0]
            print('=========', original_url)
        videoid = original_url.split('https://www.douyin.com/video/')[1]
    else:
        try:
            # 原视频链接
            with sync_playwright() as p:

                page, res = get_playright(p, original_url)
                long_url = res.url
                videoid = re.findall('video/(\d+)?', long_url)[0]
                videotitle = page.locator('//html/head/title').text_content()
                print('========', videotitle)
        except:
            # try to avoid ban of server ip
            r = requests.head(url=original_url, allow_redirects=False)
            try:
                # 2021/12/11 发现抖音做了限制，会自动重定向网址，不能用以前的方法获取视频ID了，但是还是可以从请求头中获取。
                long_url = r.headers['Location']
            except:
                # 报错后判断为长链接，直接截取视频id
                long_url = original_url
            videoid = re.findall('video/(\d+)?', long_url)[0]

    return videoid, videotitle


def validate_uidhome(original_url):
    try:
        r = requests.get(url=original_url, headers=headers)
        if r.status_code == 200:
            return True
        else:
            return False
    except:
        return False



@app.route("/api")
def webapi():
    # 创建一个Flask应用获取POST参数并返回结果
    display_label = app.label
    try:
        content = request.args.get("url")
        if content:
            post_content = find_url(content)[0]
            # 将API记录在API_logs.txt中
            date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            with open('API_logs.txt', 'a') as f:
                f.write(date + " : " + post_content + '\n')
            # 校验是否为TikTok链接
            if 'tiktok.com' in post_content:
                try:
                    video_info = get_video_info_tiktok(post_content)
                    nwm_link = tiktok_nwm(post_content, display_label)
                    # 返回TikTok信息json
                    return jsonify(Status='Success', Type='Video', video_url=nwm_link,
                                   video_music=video_info['music']['playUrl'],
                                   video_title=video_info['desc'], video_author=video_info['author'],
                                   video_author_id=video_info['authorId'], original_url=post_content,
                                   music_title=video_info['music']['title'], music_author=video_info['music']['authorName'],
                                   followerCount=video_info['authorStats']['followingCount'],
                                   followingCount=video_info['authorStats']['followingCount'],
                                   likes_recived=video_info['authorStats']['heart'],
                                   video_count=video_info['authorStats']['videoCount'],
                                   water_mark_url=video_info['video']['playAddr'])
                except Exception:
                    return jsonify(Status='Failed!', Reason='Check the link!')
            # 如果关键字不存在则判断为抖音链接
            elif 'douyin.com' in post_content:
                try:
                    response_data, result_type, api_url = get_video_info(
                        post_content)
                    if result_type == 'image':
                        # 返回图集信息json
                        return jsonify(Status='Success', Type='Image', image_url=response_data[0],
                                       image_music=response_data[1],
                                       image_title=response_data[2], image_author=response_data[3],
                                       image_author_id=response_data[4], original_url=response_data[5])
                    else:
                        # 返回视频信息json
                        return jsonify(Status='Success', Type='Video', video_url=response_data[0],
                                       video_music=response_data[1],
                                       video_title=response_data[2], video_author=response_data[3],
                                       video_author_id=response_data[4], original_url=response_data[5])
                except:
                    return jsonify(Status='Failed!', Reason='Check the link!')
            else:
                return jsonify(Status='Failed!', Reason='Check the link!')

    except Exception as e:
        # 异常捕获
        error_do(e, 'webapi', '')
        return jsonify(Message="解析失败", Reason=str(e), Result=False)

def download_video_(video_url,file_name):

    print('get download mp4 url', video_url)
    video_mp4 = requests.get(video_url, headers).content
    # Encapsulate the video byte stream into a response object
    response = make_response(video_mp4)
    # Add response header information
    response.headers['Content-Type'] = "video/mp4"
    # Fuck, it took my boss to solve the file Chinese name problem
    try:
        filename = file_name.encode('latin-1')
    except UnicodeEncodeError:
        filenames = {
            'filename': unicodedata.normalize('NFKD', file_name).encode('latin-1', 'ignore'),
            'filename*': "UTF-8''{}".format(url_quote(file_name) + '.mp4'),
        }
    else:
        filenames = {'filename': file_name}
    # attachment means to download as an attachment
    response.headers.set('Content-Disposition', 'attachment', **filenames)
    return response

def download_video_url():

    input_url = request.args.get("url")
    file_name = request.args.get("name")
    print('input_url', input_url)
    video_url = input_url
    print('filenmae', file_name)
    api = Scraper()    
    try:
        if 'douyinvod.com' in input_url and not file_name == '':
            pass
        elif 'v.douyin.com' in input_url or 'www.douyin.com' in input_url:

            result,resulttpye = api.douyin_videoinfo(input_url)
            # 视频链接
            video_url = result['nwm_video_url']
            # 视频标题
            video_title = result['video_title']
            # 作者昵称
            video_author = result['video_author']
            # 清理文件名
            file_name = clean_filename(video_title, video_author)
            # Clean up the file name
        elif 'tiktok.com' in input_url:


            result = api.tiktok_videoinfo(input_url)
            # 无水印地址
            video_url = result['nwm_video_url']
            # 视频标题
            video_title = result['video_title']
            # 作者昵称
            video_author = result['video_author']
            # 清理文件名
            file_name = clean_filename(video_title, video_author)

            return jsonify(Status='Success! Click to download!', No_WaterMark_Link=download_url)
        else:
            return jsonify(Status='Failed!', Reason='Check the link!')
        # video_title = 'video_title'
        print('get download mp4 url', video_url)
        video_mp4 = requests.get(video_url, headers).content
        # Encapsulate the video byte stream into a response object
        response = make_response(video_mp4)
        # Add response header information
        response.headers['Content-Type'] = "video/mp4"
        # Fuck, it took my boss to solve the file Chinese name problem
        try:
            file_name = file_name.encode('latin-1')
        except UnicodeEncodeError:
            filenames = {
                'filename': unicodedata.normalize('NFKD', file_name).encode('latin-1', 'ignore'),
                'filename*': "UTF-8''{}".format(url_quote(file_name) + '.mp4'),
            }
        else:
            filenames = {'filename': file_name}
        # attachment means to download as an attachment
        response.headers.set('Content-Disposition', 'attachment', **filenames)
        return response
    except Exception as e:
        error_do(e, 'download_video_url')
        return jsonify(Status='Failed!', Reason='Check the link!')


# @app.route("/bgm", methods=["POST", "GET"])
def download_bgm_url():
    # 返回视频下载请求
    display_label = app.label

    content = request.args.get("url")
    input_url = find_url(content)[0]
    try:
        if 'douyin.com' in input_url:
            video_info, result_type, api_url = get_video_info(input_url)
            if video_info[1] == "None":
                return jsonify(Status='Failed', Reason='This link has no music to get!')
            else:
                # 音频链接
                bgm_url = video_info[1]
                # 视频标题
                bgm_title = video_info[2]
                # 作者昵称
                author_name = video_info[3]
                # 清理文件名
                file_name = clean_filename(bgm_title, author_name)
        elif 'tiktok.com' in input_url:
            video_info = get_video_info_tiktok(input_url)
            bgm_url = video_info['music']['playUrl']
            # 视频标题
            bgm_title = video_info['music']['title']
            print('title: ', bgm_title)
            # 作者昵称
            author_name = video_info['music']['authorName']
            print('authorName: ', author_name)
            # 清理文件名
            file_name = clean_filename(bgm_title, author_name)
            print(file_name)
        else:
            return jsonify(Status='Failed', Reason='This link has no music to get!')
        video_bgm = requests.get(bgm_url, headers).content
        # 将bgm字节流封装成response对象
        response = make_response(video_bgm)
        # 添加响应头部信息
        response.headers['Content-Type'] = "video/mp3"
        # 他妈的,费了我老大劲才解决文件中文名的问题
        try:
            filename = file_name.encode('latin-1')
        except UnicodeEncodeError:
            filenames = {
                'filename': unicodedata.normalize('NFKD', file_name).encode('latin-1', 'ignore'),
                'filename*': "UTF-8''{}".format(url_quote(file_name) + '.mp3'),
            }
        else:
            filenames = {'filename': file_name + '.mp3'}
        # attachment表示以附件形式下载
        response.headers.set('Content-Disposition', 'attachment', **filenames)
        return response
    except Exception as e:
        error_do(e, 'download_bgm_url', '')
        return jsonify(Status='Failed!', Reason='Check the link!')


def put_result(video_info, label, idx, result_type):
    # 根据解析格式向前端输出表格

    # put_text('processing ', str(idx+1), 'video now ',position=-1)

    # bao cun dao kv value
    print('getting douyin result',video_info['original_url'],result_type)
    short_api_url = '/api?url=' + video_info['original_url']
    result = {}
    
    if result_type == 'video':
        download_video = '/video?url=' + video_info['original_url']

        download_bgm = '/bgm?url=' +video_info['original_url']
        # result['url']=video_info[0].replace('http://','https://')
        result['url'] = video_info['original_url']
        result['name'] = video_info['video_title']
        if video_info['video_title'] == '' or len(video_info['video_title']) < 2:
            result['downloadlink'] = download_video
        else:
            result['downloadlink'] = '/video?url=' + \
                video_info['nwm_video_url']+'&name='+video_info['video_title']
        print('debg=============')
        put_collapse(str(idx+1)+' : '+video_info['video_title']+'-'+video_info['video_author']+'-video detail:',
                     put_table([
                         [label['douyin_type'], label['douyin_content']],
                         [label['douyin_Format'], result_type],
                         [label['douyin_Video_raw_link'], put_link(
                             label['douyin_Video_raw_link_hint'], video_info['nwm_video_url'].replace('http://', 'https://'), new_window=True)],
                         [label['douyin_Video_download'], put_link(
                             label['douyin_Video_download_hint'], download_video, new_window=True)],
                         [label['douyin_Background_music_raw_link'], put_link(
                             label['douyin_Background_music_raw_link_hint'], video_info['video_music'], new_window=True)],
                         [label['douyin_Background_music_download'], put_link(
                             label['douyin_Background_music_download_hint'], download_bgm, new_window=True)],
                         [label['douyin_Video_title'], video_info['video_title']],
                         [label['douyin_Author_nickname'], video_info['video_author']],
                         [label['douyin_Author_Douyin_ID'], video_info['video_author_id']],
                         [label['douyin_Original_video_link'], put_link(
                             label['douyin_Original_video_link_hint'], video_info['original_url'], new_window=True)],
                         [label['douyin_Current_video_API_link'], put_link(
                             label['douyin_Current_video_API_link_hint'], video_info['api_url'], new_window=True)],
                         [label['douyin_Current_video_streamline_API_link'], put_link(
                             label['douyin_Current_video_streamline_API_link_hint'], short_api_url, new_window=True)]
                     ]), open=False)
    else:
        download_bgm = '/bgm?url=' + video_info[5]
        put_collapse('bgm detail:',
                     put_table([
                         [label['douyin_type'], label['douyin_content']],
                         [label['douyin_Format'], result_type],
                         [label['douyin_Background_music_raw_link'], put_link(
                             label['douyin_Background_music_raw_link_hint'], video_info['album_music'], new_window=True)],
                         [label['douyin_Background_music_download'], put_link(
                             label['douyin_Background_music_download_hint'], download_bgm, new_window=True)],
                         [label['douyin_Video_title'], video_info['album_title']],
                         [label['douyin_Author_nickname'], video_info['album_author']],
                         [label['douyin_Author_Douyin_ID'], video_info['album_author_id']],
                         [label['douyin_Original_video_link'], put_link(
                             label['douyin_Original_video_link_hint'], video_info['original_url'], new_window=True)],
                         [label['douyin_Current_video_API_link'], put_link(
                             label['douyin_Current_video_API_link_hint'], video_info['api_url'], new_window=True)],
                         [label['douyin_Current_video_streamline_API_link'], put_link(
                             label['douyin_Current_video_streamline_API_link_hint'], short_api_url, new_window=True)]
                     ]), open=False)
        for i in video_info['album_list']:
            put_collapse('picture detail:',
                         put_table([
                             [label['douyin_Picture_straight_link'], put_link(
                                 label['douyin_Picture_straight_link_hint'], i, new_window=True), put_image(i)]
                         ]), open=False)
    # put_text(result)
    return result


def coldstart():
    # load users

    # record operation video clip
    # fcreator to final
    # upload video to ytb douyin tiktok
    print('auto')


def backup(sec_uid):
    # 单独视频上传
    # 压缩包上传

    return ''

def put_tiktok_result(video_info, label, idx, result_type):

    # 将TikTok结果显示在前端
    # put_text('processing ', str(idx+1), 'video now ',position=0)
    print('getting tiktok result', video_info)
    short_api_url = '/api?url=' + video_info['original_url']
    result = {}
    download_url = '/video?url=' + video_info['original_url']
    api_url = '/api?url=' + video_info['original_url']
    put_table([
        [label['tiktok_type'], label['tiktok_content']],
        [label['tiktok_Video_title'], video_info['video_title']],
        [label['tiktok_Video_direct_link_with_watermark'], put_link(label['tiktok_Video_direct_link_with_watermark_hint'], video_info['wm_video_url'], new_window=True)],
        [label['tiktok_Video_direct_link_without_watermark'], put_link(
            label['tiktok_Video_direct_link_without_watermark_hint'], video_info['nwm_video_url'], new_window=True)],
        [label['tiktok_Video_direct_link_without_watermark'], put_link(
            label['tiktok_Video_direct_link_without_watermark_hint'], download_url, new_window=True)],
        [label['tiktok_Background_music_raw_link'], video_info['video_music_title'] +
         " - " + video_info['video_music_author']],
        [label['tiktok_Background_music_raw_link'], put_link(label['tiktok_Background_music_raw_link_hint'], video_info['video_music_url'], new_window=True)],
        [label['tiktok_Author_nickname'], video_info['video_author_nickname']],
        [label['tiktok_Author_user_ID'], video_info['video_author_id']],
        [label['titkok_Follower_count'], video_info['video_author_followerCount']],
        [label['tiktok_Following_count'], video_info['video_author_followingCount']],
        [label['tiktok_Total_likes_get'], video_info['video_author_heartCount']],
        [label['tiktok_videos_count'], video_info['video_author_videoCount']],
        [label['tiktok_Original_video_link'], put_link(
            label['tiktok_Original_video_link_hint'], video_info['original_url'], new_window=True)],
        [label['tiktok_Current_video_API_link'], put_link(
            label['tiktok_Current_video_API_link_hint'], video_info['api_url'], new_window=True)]
    ])


def ios_pop_window():
    with popup("iOS快捷指令"):
        put_text('快捷指令需要在抖音或TikTok的APP内，浏览你想要无水印保存的视频或图集。')
        put_text('点击分享按钮，然后下拉找到 "抖音TikTok无水印下载" 这个选项。')
        put_text('如遇到通知询问是否允许快捷指令访问xxxx (域名或服务器)，需要点击允许才可以正常使用。')
        put_text('该快捷指令会在你相册创建一个新的相薄方便你浏览保存到内容。')
        put_html('<br>')
        put_link('[点击获取快捷指令]', 'https://www.icloud.com/shortcuts/e8243369340548efa0d4c1888dd3c170',
                 new_window=True)


def oneinalldownload_pop_window(html):
    print('==============')
    with popup("save all"):
        print('1=========')
        # put_html(html)
        put_text('===========')


def compress_file(tar_file, target_file):
    # tar_file是输出压缩包名字以及目录("./output/mp4.tar")，target_file是要打包的目录或文件名("./files")
    if os.path.isfile(target_file):
        with tarfile.open(tar_file, 'w') as tar:
            tar.add(target_file)
            return 'finished'
    else:
        with tarfile.open(tar_file, 'w') as tar:
            for root, dirs, files in os.walk(target_file):
                for single_file in files:
                    filepath = os.path.join(root, single_file)
                    tar.add(filepath)
            return 'finished'


def video_download_window(result_dict):
    try:
        # result_dict = {'文件名': '链接'}
        total_amount = len(result_dict)
        download_time = (time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()))
        # 存储根目录
        save_path = './web/saved_videos/' + (download_time + '_total_' + str(total_amount) + '_videos')
        # 判断目录是否存在
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        # 弹出窗口
        with popup("正在服务器后台下载视频(共{}个下载任务)".format(str(len(result_dict)))):
            # 下载索引计数
            session.set_env(auto_scroll_bottom=True)

            download_count = 0
            # 遍历字典的键和值
            for file_name, url in result_dict.items():
                try:
                    download_count += 1
                    url=url.replace('/video?url=','')
                    put_info('正在下载第{}个视频:\n{}'.format(download_count, file_name))
                    print('url=====',url)
                    response = requests.get(url, headers=headers)
                    print('shipinxiazai',response.status_code)
                    data = response.content
                    if data:
                        file_path = '{}/{}.{}'.format(save_path, file_name, 'mp4')
                        if not os.path.exists(file_path):
                            with open(file_path, 'wb') as f:
                                f.write(data)
                                f.close()
                                put_success('{}下载成功'.format(file_name))
                except Exception as e:
                    download_count += 1
                    put_error('视频下载失败，将跳过该视频。')
                    continue
            with use_scope('xiazaizhong'):
                put_html('<hr>')

                put_html('<h3>💾结果页视频合集准备中</h3>')
                output_path = save_path + '/output'
                tarfile_name = download_time + '_total_' + str(total_amount) + '_videos.tar'
                output_file = output_path + '/' + tarfile_name

                put_info('正在压缩视频文件，请勿关闭当前弹窗，完成后会在下方显示按钮...')
                # 判断目录是否存在
                if not os.path.exists(output_path):
                    os.mkdir(output_path)
                if download_count == total_amount:

                    if compress_file(tar_file=output_file, target_file=save_path) == 'finished':
                        clear('xiazaizhong')
                        put_html('<h3>💾结果页视频合集下载完成</h3>')
                        put_info('压缩视频已完成...')

                        tar = open(output_file, "rb").read()
                        put_file(tarfile_name, tar, '点击下载视频合集压缩包')
    except Exception as e:
        print(str(e))



def api_document_pop_window():
    with popup("API documentation"):
        put_markdown("💽API documentation")
        put_markdown("The API can convert the request parameters into the non-watermarked video/picture direct link that needs to be extracted, and it can be downloaded in-app with the IOS shortcut.")
        put_link('[Chinese document]', 'https://github.com/Evil0ctal/TikTokDownloader_PyWebIO#%EF%B8%8Fapi%E4%BD%BF%E7%94%A8',
                 new_window=True)
        put_html('<br>')
        put_link('[English document]',
                 'https://github.com/Evil0ctal/TikTokDownloader_PyWebIO/blob/main/README.en.md#%EF%B8%8Fapi-usage',
                 new_window=True)
        put_html('<hr>')
        put_markdown("🛰️API reference")
        put_markdown('Douyin/TikTok extracting request parameters')
        put_code(
            'http://localhost(Server IP):80/api?url="Copied (TikTok/TikTok) (Share text/link)"\n#Return JSON')
        put_markdown('Douyin/TikTok video download request parameters')
        put_code('http://localhost(Server IP):80/download_video?url="Duplicated Douyin/TikTok link"\n#Return to mp4 file download request')
        put_markdown('TikTok video/atlas audio download request parameters')
        put_code('http://localhost(Server IP):80/download_bgm?url="Duplicated Douyin/TikTok link"\n#Return to mp3 file download request')


def error_log_popup_window():
    with popup('Error log'):
        content = open(r'./logs.txt', 'rb').read()
        put_file('logs.txt', content=content)
        with open('./logs.txt', 'r') as f:
            content = f.read()
            put_text(str(content))


return_home = """
location.href='/'
"""


def log_popup_window():
    with popup('错误日志'):
        put_html('<h3>⚠️关于解析失败</h3>')
        put_text('目前已知短时间大量访问抖音或Tiktok可能触发其验证码。')
        put_text('若多次解析失败后，请等待一段时间再尝试。')
        put_html('<hr>')
        put_text('请检查以下错误日志:')
        content = open(r'./logs.txt', 'rb').read()
        put_file('logs.txt', content=content)
        with open('./logs.txt', 'r') as f:
            content = f.read()
            put_text(str(content))


def doc_popup_window(display_label):
    with popup('%s' % display_label['doc']):
        put_html('<h3>%s</h3>' % display_label['uservideo'])
        put_image('https://views.whatilearened.today/views/github/evil0ctal/TikTokDownload_PyWebIO.svg',
                  title='访问记录')
        put_html('<hr>')
        put_html('<h3>⭐Github</h3>')
        put_markdown(
            '[TikTokDownloader_PyWebIO](https://github.com/Evil0ctal/TikTokDownloader_PyWebIO)')
        put_html('<hr>')
        put_html('<h3>🎯反馈</h3>')
        put_markdown(
            '提交：[issues](tiktokadownloader@gmail.com)')
        put_html('<hr>')
        put_html('<h3>🌐视频/图集批量下载</h3>')
        put_markdown(
            '可以使用[IDM](https://www.zhihu.com/topic/19746283/hot)之类的工具对结果页面的链接进行嗅探。')
        put_html('<hr>')
        put_html('<h3>💖WeChat</h3>')
        put_markdown('微信：[Evil0ctal](https://mycyberpunk.com/)')
        # "uid":"79298110705","short_id":"148174106","nickname":"苹果 姐姐"
        put_html('<hr>')
        # sec_uid MS4wLjABAAAAnLgnj-bl5HuQ5l79HK5P9qyT0-SSdP112ZHy09OQS0s


def about_popup_window():
    with popup('更多信息'):
        put_html('<h3>👀访问记录</h3>')
        put_image('https://views.whatilearened.today/views/github/evil0ctal/TikTokDownload_PyWebIO.svg',
                  title='访问记录')
        put_html('<hr>')
        put_html('<h3>⭐Github</h3>')
        put_markdown(
            '[TikTokDownloader_PyWebIO](https://github.com/Evil0ctal/TikTokDownloader_PyWebIO)')
        put_html('<hr>')
        put_html('<h3>🎯反馈</h3>')
        put_markdown(
            '提交：[issues](tiktokadownloader@gmail.com)')
        put_html('<hr>')
        put_html('<h3>🌐视频/图集批量下载</h3>')
        put_markdown(
            '可以使用[IDM](https://www.zhihu.com/topic/19746283/hot)之类的工具对结果页面的链接进行嗅探。')
        put_html('<hr>')
        put_html('<h3>💖WeChat</h3>')
        put_markdown('微信：[Evil0ctal](https://mycyberpunk.com/)')
        put_html('<hr>')


def sponsor_popup_window():
    with popup('赏份盒饭'):
        put_html('<h3>👀微信</h3>')
        put_image('https://views.whatilearened.today/views/github/evil0ctal/TikTokDownload_PyWebIO.svg',
                  title='访问记录')
        put_html('<hr>')
        put_html('<h3>⭐支付宝</h3>')
        put_markdown(
            '[TikTokDownloader_PyWebIO](https://github.com/Evil0ctal/TikTokDownloader_PyWebIO)')
        put_html('<hr>')
        put_html('<h3>🎯反馈</h3>')
        put_markdown(
            '提交：[issues](tiktokadownloader@gmail.com)')
        put_html('<hr>')
        put_html('<h3>🌐buymeacoffee</h3>')
        put_markdown(
            'find me here[buymeacoffee](https://www.buymeacoffee.com/madegamedev)。')
        put_html('<hr>')
        put_html('<h3>Patreon</h3>')
        put_markdown('Patreon ：[Evil0ctal](https://mycyberpunk.com/)')
        put_html('<hr>')


def language_pop_window():
    with popup('Select Site Language'):
        put_link('[Chinese Language]', 'https://douyin.wtf')
        put_html('<br>')
        put_link('[English Language]', 'https://en.douyin.wtf')


def locale(lang):
    # put_text("You click %s button" % lang_val)
    return translations(lang)
    # put_text("You title %s is" % local.title_label, type(local.title_label))


def chooselang(lang):
    print('you choose', lang)

    # local.label=locale(lang)
    # print('////',local.label)


def formaturl(url):
    if not re.match('(?:http|ftp|https)://', url):
        if url.startwith("//"):
            url = url.replace("//", '')
        return 'https://{}'.format(url)
    return url


js_file = "https://www.googletagmanager.com/gtag/js?id=G-484Z1BXPFZ"
js_code = """
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());

gtag('config', 'G-484Z1BXPFZ');
"""

ga_code = """
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());

gtag('config', 'G-484Z1BXPFZ');
</script>

"""

ldjson = """

"""
quick3js = """
<script>
function makeid(length) {
    var result           = '';
    var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
    result += characters.charAt(Math.floor(Math.random() * 
charactersLength));
}
return result;
}
function download_files(%s) {
function download_next(i) {
    if (i >= files.length) {
    return;
    }
    var a = document.createElement('a');
    a.href = files[i]["downloadlink"];
    a.target = '_parent';
    //a.target = '_blank';

    // Use a.download if available, it prevents plugins from opening.
    if ('download' in a) {

    strValue=files[i]["name"]
    // Test whether strValue is empty
    if (!strValue || strValue.trim() === "" || (strValue.trim()).length === 0) {
        a.download = makeid(10)
    }        
    a.download = files[i]['name'];
    }
    // Add a to the doc for click to work.
    (document.body || document.documentElement).appendChild(a);
    if (a.click) {
    a.click(); // The click method is supported by most browsers.
    } else {
    $(a).click(); // Backup using jquery
    }
    // Delete the temporary link.
    a.parentNode.removeChild(a);
    // Download the next file with a small timeout. The timeout is necessary
    // for IE, which will otherwise only download the first file.
    setTimeout(function() {
    download_next(i + 1);
    }, 500);
}
// Initiate the first download.
download_next(0);
}



</script>

"""

quick3 = """
<script>
function makeid(length) {
    var result           = '';
    var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
    result += characters.charAt(Math.floor(Math.random() * 
charactersLength));
}
return result;
}
function download_files(files) {
function download_next(i) {
    if (i >= files.length) {
    return;
    }
    var a = document.createElement('a');
    a.href = files[i]["downloadlink"];
    a.target = '_parent';
    //a.target = '_blank';

    // Use a.download if available, it prevents plugins from opening.
    if ('download' in a) {

    strValue=files[i]["name"]
    // Test whether strValue is empty
    if (!strValue || strValue.trim() === "" || (strValue.trim()).length === 0) {
        a.download = makeid(10)
    }        
    a.download = files[i]['name'];
    }
    // Add a to the doc for click to work.
    (document.body || document.documentElement).appendChild(a);
    if (a.click) {
    a.click(); // The click method is supported by most browsers.
    } else {
    $(a).click(); // Backup using jquery
    }
    // Delete the temporary link.
    a.parentNode.removeChild(a);
    // Download the next file with a small timeout. The timeout is necessary
    // for IE, which will otherwise only download the first file.
    setTimeout(function() {
    download_next(i + 1);
    }, 500);
}
// Initiate the first download.
download_next(0);
}


// Here's a live example that downloads three test text files:
function do_dl() {
    download_files(%s);
};
</script>

<button onclick="do_dl();">%s.</button>

"""


def loaddb():
    dbfileurl = request.args.get("dburl")
    mode = request.args.get("mode")
    try:

        solditems = requests.get(dbfileurl)  # (your url)
        data = solditems.json()
        users = loadUser2dict(mode)
        totaluser = users+data
        # update existing db
        try:

            with open(mode+'Users.pickle', 'wb') as handle:
                pickle.dump(totaluser, handle,
                            protocol=pickle.HIGHEST_PROTOCOL)
        except EOFError:

            return None
    except:
        print('file url is broken')
    return ''


def backupdb():
    mode = request.args.get("mode")
    # github action daily api call to backup db files
    try:
        user = loadUser2dict(mode)
        print(type(user), user)
        return user
    except:
        print('file url is broken')
        return ''


def show_msg_newuser():
    put_text("This is a new user not in our database. need longer time to process")


# @seo(SEO_TITLE, SEO_DESCRIPTION)
# @config(theme="minty", js_file=[GA_JS_FILE], js_code=GA_JS_CODE)
# def lang():

#     popup('Choose your preferred language', [
#         put_buttons(['English', 'Chinese'], onclick=tiktoka)
#     ], closable=True)


video_tutorial_HEADING = r"""
<h2 align="center"><strong>Watch basic tutorials</strong></h1>
"""

videojs=r"""
<link href="https://cdnjs.cloudflare.com/ajax/libs/video.js/7.10.2/video-js.min.css" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/video.js/7.10.2/video.min.js"></script>

"""

mediaelement="""
<script src="https://cdnjs.cloudflare.com/ajax/libs/mediaelement/5.0.5/mediaelement.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/mediaelement/5.0.5/mediaelement-and-player.min.js"></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/mediaelement/5.0.5/mediaelementplayer.min.css" rel="stylesheet">
$('video, audio').mediaelementplayer({
	// Do not forget to put a final slash (/)
	pluginPath: 'https://cdnjs.cloudflare.com/ajax/libs/mediaelement/5.0.5/',
	// this will allow the CDN to use Flash without restrictions
	// (by default, this is set as `sameDomain`)
	shimScriptAccess: 'always'
	// more configuration
});
"""


def changelanguage(lang):
    session.run_js("window.open('/"+lang+"')")
    # session.run_js("location.href='/'"+lang)


@config(title=title, description=description)
def tiktoka(lang=''):
    print('default browser language ', session_info.user_language)
    # close_popup()

    if lang == '':
        choosedlang = session_info.user_language
        lang = choosedlang
    else:
        clear('introduction')
    put_buttons(supportedlang, onclick=changelanguage)
    # print('you manually change to ', lang)
    session.run_js(
        'WebIO._state.CurrentSession.on_session_close(()=>{setTimeout(()=>location.reload(), 40000})')

    display_label = locale(lang)
    session.set_env(title=display_label['head_title'])

    # 设置favicon
    # $('head').append('<script src ="https://cdn.jsdelivr.net/npm/jquery@3.6.0/dist/jquery.min.js"></script>')

    session.run_js("""
    $('head').append('<script src="https://www.googletagmanager.com/gtag/js?id=G-484Z1BXPFZ"></script>')
    """)
    session.run_js("""
    $('head').append('<link rel="canonical" href="https://www.tiktokvideos.download/">')
    $('head').append('<link rel="alternate" hreflang="en-gb" href="https://www.tiktokvideos.download/en" />')
    $('head').append('<link rel="alternate" hreflang="en-us" href="https://www.tiktokvideos.download/en" />')
    $('head').append('<link rel="alternate" hreflang="en" href="https://www.tiktokvideos.download" />')
    $('head').append('<link rel="alternate" hreflang="ru"  href="https://www.tiktokvideos.download/ru" />')
    $('head').append('<link rel="alternate" hreflang="es"  href="https://www.tiktokvideos.download/es" />')
    $('head').append('<link rel="alternate" hreflang="fr" href="https://www.tiktokvideos.download/fr" />')
    $('head').append('<link rel="alternate" hreflang="vi" href="https://www.tiktokvideos.download/vi" />')
    $('head').append('<link rel="alternate" hreflang="fil" href="https://www.tiktokvideos.download/fil" />')
    $('head').append('<link rel="alternate" hreflang="x-default"  href="https://www.tiktokvideos.download" />')
    """)
    put_html(ga_code)
    session.run_js("""
    $('head').append('<meta property="og:image" content="https://raw.githubusercontent.com/wanghaisheng/TiktokaTikTokVideoDownloadTookit/main/favicon/tiktoka-1200.png">')
    $('head').append('<meta name="keywords" content="video, downloading, tiktoka,tiktok videos, free, douyin video,bulk download,">')
    $('head').append('<link rel="shortcut icon" href="https://raw.githubusercontent.com/wanghaisheng/TiktokaTikTokVideoDownloadTookit/main/favicon/favicon.ico" type="image/x-icon">')
    $('head').append('<link rel="alternate" href="ios-app://544007664/vnd.tiktoka/www.tiktokvideos.download/">')
    $('head').append('<link rel="alternate" href="android-app://com.google.android.tiktoka/http/www.tiktokvideos.download/">')
    $('head').append('<link rel="alternate" media="only screen and (max-width: 640px)" href="https://m.tiktokvideos.download/">')
    $('head').append('<link rel="alternate" media="handheld" href="https://m.tiktokvideos.download/">')
    """
                   )

    favicon_url = "favicon/android-chrome-512x512.png"
    session.run_js("""
    $('#favicon32,#favicon16').remove();
    $('head').append('<meta charset="utf-8">')
    $('head').append('<meta name="description" content=%s />')
    $('head').append('<meta name="viewport" content="width=device-width, initial-scale=1">
    $('head').append('<link rel="icon" type="image/png" href=%s>')
    """ % (display_label['head_description'], favicon_url))
    # 修改footer
    # session.run_js("""$('footer').remove()""")
    # tiktok.com 和邮件爬取 抽奖工具的站
# $('footer').append('<a href="https://trend.tiktokvideos.download/" >  Tiktoka Trends  </a>')
# $('footer').append('<a href="https://ninja.tiktokvideos.download/" >  Tiktoka Ninja  </a>')
# Footer
# ^^^^^^
    # session.run_js(mediaelement)
    put_html(videojs)

    session.run_js(FOOTER
                   )

    if session.info.user_agent.is_pc:

        put_markdown(
            """<div align='center' ><font size='14'>%s</font></div>""" % display_label['title'])
        put_markdown(
            """<div align='center' ><font size='14'>%s</font></div>""" % display_label['sub_title'])
        put_markdown(
            """<div align='center' ><font size='12'>%s</font></div>""" % display_label["third_title"])
    elif session.info.user_agent.is_mobile:
        put_markdown(
            """<div align='center' ><font size='5'>%s</font></div>""" % display_label['title'])
        put_markdown(
            """<div align='center' ><font size='4'>%s</font></div>""" % display_label['sub_title'])
        put_markdown(
            """<div align='center' ><font size='4'>%s</font></div>""" % display_label["third_title"])
    elif session.info.user_agent.is_tablet:
        put_markdown(
            """<div align='center' ><font size='12'>%s</font></div>""" % display_label['title'])
        put_markdown(
            """<div align='center' ><font size='12'>%s</font></div>""" % display_label['sub_title'])
        put_markdown(
            """<div align='center' ><font size='10'>%s</font></div>""" % display_label["third_title"])
    put_html('<hr>')
    # put_row([
    # put_button("%s"%display_label['mobilepop'], onclick=lambda: ios_pop_window(), link_style=True, small=True),
    #  put_button("API", onclick=lambda: api_document_pop_window(),
    #             link_style=True, small=True),
    #  put_button("%s"%display_label['log'], onclick=lambda: log_popup_window(),
    #             link_style=True, small=True),
    # #  put_button("%s"%display_label['about'], onclick=lambda: about_popup_window(),
    # #             link_style=True, small=True),
    #  put_button("%s"%display_label['doc'], onclick=lambda: doc_popup_window(display_label),
    # #             link_style=True, small=True),
    #  put_button("%s"%display_label['support'], onclick=lambda: sponsor_popup_window(),
    #             link_style=True, small=True)
    # ])

    with use_scope('introduction'):

        put_collapse('Why do you need Tiktoka Downloader', [
            put_markdown(
                '##  One easy way to download everything off TikTok/Douyin'),
            put_markdown(
                ' Are you looking for a tool to Download TikTok Videos from Accounts and Hashtags '),
            put_markdown('TikToka Downloader is the ultimate TikTok/Douyin Downloader. Download TikTok challenges, captions, whole accounts, hashtags, song-related and single videos in high quality. '),

        ], open=False)

        put_collapse('Check out awesome Tiktoka Downloader features', [
            put_markdown(feaure_code),
            # put_markdown('#  Download TikTok user videos '),
            # put_markdown('#  Backup Your TikTok Account '),
        ], open=False)

        put_collapse('Tiktoka Downloader FAQ', [
            put_markdown(faq_code),

        ], open=False)
        put_html("<br>")
        put_html(video_tutorial_HEADING)
        multilink='static/oneinall.mp4'
        multilink_gif = open('./Screenshots/oneinall.gif', 'rb').read()  
        downloaduservideo_gif = open('./Screenshots/downloaduservideo.gif', 'rb').read()  
        searchuservideo_gif = open('./Screenshots/douyinusersearch.gif', 'rb').read()  
        # print(multilink_gif)
        downloaduservideo='static/downloaduservideo.mp4'
        searchuservideo='https://raw.githubusercontent.com/wanghaisheng/TiktokaDownload/main/Screenshots/douyinusersearch.mp4?token=GHSAT0AAAAAABTWDUKZVF5EXKQVWYW2FF7SYTI6B4Q'

        
        if session.info.user_agent.is_mobile:
            put_markdown('**{}**'.format(display_label['oneinall_hint'])),
            put_image(multilink_gif)
            # put_html('<video class="videojs vjs-default-skin vjs-9-16" controls preload="auto" width="320" poster="" data-setup="{}" src={url} </video>'.format("{}",url=multilink))
            put_html("<br>")            
            put_html("<br>")
            put_markdown('**{}**'.format(display_label['oneinalluser_hint'])),
            # put_html('<video class="videojs vjs-default-skin vjs-9-16" controls preload="auto" width="320" poster="" data-setup="{}" src={url} </video>'.format("{}",url=downloaduservideo))
            put_image(downloaduservideo_gif)
            
            put_html("<br>")
            put_html("<br>")

            put_markdown('**{}**'.format(display_label['oneinallsearchuser_hint'])),
            # put_html('<video class="videojs vjs-default-skin vjs-9-16" controls preload="auto" width="320" poster="" data-setup="{}" src={url} </video>'.format("{}",url=searchuservideo))
            put_image(searchuservideo_gif)

        else:
            put_row([put_markdown('**一次下载多个视频**'),
                put_image(multilink_gif)

                # put_html('<video class="videojs vjs-default-skin vjs-16-9" controls preload="auto" width="640" poster="" data-setup="{}" src={url} </video>'.format("{}",url=multilink))
                ])
            put_html("<br>")

            put_row([put_markdown('**下载某个用户所有视频**'),
                # put_html('<video class="videojs vjs-default-skin vjs-16-9" controls preload="auto" width="640" poster="" type="video/mp4" data-setup="{}" src={url} </video>'.format("{}",url=downloaduservideo))
                put_image(downloaduservideo_gif)
                            
                            ])
            put_html("<br>")

            put_row([put_markdown('**搜索某个用户并下载所有视频**'),
                # put_html('<video class="videojs vjs-default-skin vjs-16-9" controls preload="auto" width="640" poster="" data-setup="{}" src={url} </video>'.format("{}",url=searchuservideo))
                put_image(searchuservideo_gif)
                
                ])

        put_html("<br>")
        put_html("<br>")
        put_html("<br>")
        userip = session.info.user_ip
        userip_call_count = get_userip_call_count()
        if userip_call_count == {} or not userip in userip_call_count:
            if session.info.user_agent.is_mobile:
                put_row([
                 None,
                    put_button("New User Tour", onclick=partial(downloadview, display_label),
                               color='primary', outline=False)
                
                    ,None

                ],size='25% 50% 25%'),
                put_html("<br>"),

                put_row([
                 None,
                    put_button("start your Tiktoka journey", onclick=partial(downloadview, display_label),
                               color='primary', outline=False)
                
                    ,None

                ],size='65% 15% 20%')

            else:
                put_row([
                    put_button("New User Tour", onclick=partial(downloadview, display_label),
                               color='primary', outline=False), None, put_button("start your jouney", onclick=partial(downloadview, display_label),
                                                                                 color='primary', outline=False)
                ])
        else:
            put_row([
                None,
                put_button("start your jouney", onclick=partial(downloadview, display_label),
                            color='primary', outline=False)
            
                ,None

            ],size='35% 50% 15%')

        # downloadview(display_label)

def leixingnoti(leixing):

    with use_scope(leixing):
        put_text(leixing)
        if leixing=='link':
            textarea("%s" % display_label['kouling'], type=TEXT, required=True,
                 placeholder='===========', position=0, name='url')
        elif leixing=='user':
            textarea("%s" % display_label['kouling'], type=TEXT, required=True,
                 placeholder='user', position=0, name='url')            

def downloadview(display_label):
    clear('introduction')
    sites = [{'label': 'douyin', 'value': 'douyin', 'selected': True}, {
        'label': 'tiktok', 'value': 'tiktok', 'selected': False}]
    leixing = [{'label': 'raw link', 'value': 'link', 'selected': True},
     {'label': 'user profile', 'value': 'user', 'selected': False},
     {'label': 'tag', 'value': 'tag', 'selected': False,'disabled':True},
     {'label': 'keyword', 'value': 'keyword', 'selected': False},
        
        ]

    inputdata = input_group("get what you want all in one click", [

        radio("choose one from supported sites", sites, inline=True, name='site'),
        radio("choose one from supported type", leixing, inline=True, name='leixing',onchange=lambda val: leixingnoti('url', value=val)),

    ])
    kou_ling=''

    if inputdata['leixing']=='link':

        kou_ling = textarea("%s" % display_label['kouling'], type=TEXT, validate=valid_check, required=True,
                        placeholder=display_label['placeholder_link'], position=0)

    elif  inputdata['leixing']=='user':


        kou_ling = textarea("%s" % display_label['kouling'], type=TEXT, validate=valid_check, required=True,
                        placeholder=display_label['placeholder_user'], position=0)
    elif  inputdata['leixing']=='keyword':

        kou_ling = textarea("%s" % display_label['kouling'], type=TEXT, validate=valid_check, required=True,
                        placeholder=display_label['placeholder_search'], position=0)

    elif  inputdata['leixing']=='tag':

        kou_ling = textarea("%s" % display_label['kouling'], type=TEXT, validate=valid_check, required=True,
                        placeholder=display_label['placeholder_tag'], position=0)


    site = inputdata['site']
    userip = session.info.user_ip
    userip_call_count = get_userip_call_count()
    if userip_call_count == {} or not userip in userip_call_count:
        userip_call_count[userip] = 0
        set_userip_call_count(userip_call_count)

    if userip_call_count[userip] > 50:
        popup('you have maximize daily limit,you can increase your limit through support ', [
            put_row([put_html('<h3>面包多</h3>'), None,
                     put_html('<h3>buymeacoffee</h3>')]),
            put_row([put_html('<br>'), None, put_html('<br>')]),
            put_row([put_html('<br>'), None, put_html('<br>')]),
            put_row([put_markdown('[赏份盒饭](https://mianbaoduo.com/o/bread/YpibmZ9w)'), put_markdown('[buy me a coffee](https://www.buymeacoffee.com/madegamedev)。'), ])], size=PopupSize.LARGE)
    else:
        if userip_call_count[userip] > 5:
            popup('Help us', [
            put_row([put_html('<h3>面包多</h3>'), None,
                     put_html('<h3>buymeacoffee</h3>')]),
            put_row([put_html('<br>'), None, put_html('<br>')]),
            put_row([put_html('<br>'), None, put_html('<br>')]),
            put_row([put_markdown('[赏份盒饭](https://mianbaoduo.com/o/bread/YpibmZ9w)'), put_markdown('[buy me a coffee](https://www.buymeacoffee.com/madegamedev)。'), ])], size=PopupSize.LARGE)
            session.set_env(auto_scroll_bottom=True)
        # put_text(userip_call_count[userip] )

        if kou_ling:
            if kou_ling == 'hefan':
                put_row([

                    put_button("%s" % display_label['mobilepop'], onclick=lambda: ios_pop_window(
                    ), link_style=True, small=True),
                    put_button("API", onclick=lambda: api_document_pop_window(),
                               link_style=True, small=True),
                    put_button("%s" % display_label['log'], onclick=lambda: log_popup_window(),
                               link_style=True, small=True),
                    put_button("%s" % display_label['about'], onclick=lambda: about_popup_window(),
                               link_style=True, small=True),
                    put_button("%s" % display_label['doc'], onclick=lambda: doc_popup_window(display_label),
                               link_style=True, small=True),
                    put_button("%s" % display_label['support'], onclick=lambda: sponsor_popup_window(),
                               link_style=True, small=True)

                ])
                popup('Donate to help us continue service', [
                    put_button("%s" % display_label['support'], onclick=lambda: sponsor_popup_window(),
                               link_style=True, small=True),
                    put_link('%s' % display_label['returnhome'], '/')])
            else:
                if site=='douyin':
                    douyin_url_list = find_url(kou_ling,site)
                    if len(douyin_url_list)>0:
                        douyinview(douyin_url_list,display_label,userip,userip_call_count,session)
                elif site=='tiktok':
                    tiktok_url_list = find_url(kou_ling,site)
                    if len(tiktok_url_list)>0:

                        tiktokview(tiktok_url_list,display_label,userip,userip_call_count,session)

def douyinview(douyin_url_list,display_label,userip,userip_call_count,session):
    # if session.info.user_agent.is_pc:

    #     put_markdown(
    #         """<div align='center' ><font size='14'>%s</font></div>""" % display_label['title'])
    #     put_markdown(
    #         """<div align='center' ><font size='14'>%s</font></div>""" % display_label['sub_title'])
    #     put_markdown(
    #         """<div align='center' ><font size='12'>%s</font></div>""" % display_label["third_title"])
    # elif session.info.user_agent.is_mobile:
    #     put_markdown(
    #         """<div align='center' ><font size='5'>%s</font></div>""" % display_label['title'])
    #     put_markdown(
    #         """<div align='center' ><font size='4'>%s</font></div>""" % display_label['sub_title'])
    #     put_markdown(
    #         """<div align='center' ><font size='4'>%s</font></div>""" % display_label["third_title"])
    # elif session.info.user_agent.is_tablet:
    #     put_markdown(
    #         """<div align='center' ><font size='12'>%s</font></div>""" % display_label['title'])
    #     put_markdown(
    #         """<div align='center' ><font size='12'>%s</font></div>""" % display_label['sub_title'])
    #     put_markdown(
    #         """<div align='center' ><font size='10'>%s</font></div>""" % display_label["third_title"])
    # put_html('<hr>')
    start = time.time()
    allquickdownloadlist = []

    try:

        douyin_standlone_video_url_list = []
        douyin_user_video_url_list = []
        scaper = Scraper()

        douyin_userhomelist = []

        if len(douyin_url_list) > 0:
            toast('parsing user input', position='right',
                    color='#2188ff', duration=3)
            loadingbar(id='extractingurl', init=0.3,
                        label='extracting input urls')
            for idx, url in enumerate(douyin_url_list):
                videoidhome,secuidhome=scaper.douyin_url2videoid(url)
                if not videoidhome=='':
                    douyin_standlone_video_url_list.append(videoidhome)
                else:
                    if not secuidhome=='':
                        douyin_userhomelist.append(secuidhome)
                    
                if len(douyin_url_list) == 1:
                    for i in range(1, 4):
                        set_processbar('extractingurl', i / 3)
                        time.sleep(0.1)
                else:
                    set_processbar(
                        'extractingurl', (idx+1) / len(douyin_url_list))

            clear('extractingurl')
            if len(douyin_standlone_video_url_list) > 0:

                print(douyin_standlone_video_url_list)
                msg = 'STEP 2 : analysing ' + \
                    str(len(douyin_standlone_video_url_list)) + \
                    ' videos from standlone links'
                toast(msg, position='right',
                        color='#2188ff', duration=5)
                loadingbar(id='svd', init=0.3,
                            label='specific videos downloading')
                for idx, long_url in enumerate(douyin_standlone_video_url_list):

                    videoid = long_url.split(
                        'www.douyin.com/video/')[-1]
                    # deleted, js, key = filter_deleted_videos(
                        # long_url, videoid)
                    # if deleted == False:
                    videoinfo,resulttype=scaper.douyin_videoinfo(videoid)
                    if videoinfo is None:
                        put_text('this video is not supported yet',long_url)
                    else:
                        result = put_result(
                                videoinfo, display_label, idx, resulttype)
                        allquickdownloadlist.append(result)
                    if len(douyin_standlone_video_url_list) == 1:
                        for i in range(1, 4):
                            set_processbar('svd', i / 3)
                            time.sleep(0.1)
                    else:
                        set_processbar(
                            'svd', (idx+1) / len(douyin_standlone_video_url_list))

                clear('svd')
            if len(douyin_userhomelist) > 0:
                usersearch_douyin = User_search_douyin()

                msg = 'start to extract user videos'
                toast(msg, position='right',
                        color='#2188ff', duration=3)
                loadingbar(id='alluser', init=0.3,
                            label='user videos downloading')
                # users = loadUser2dict(mode='douyin')
                # print('===', users)
                for idx, item in enumerate(douyin_userhomelist):

                    secuid = item.split('/')[-1]
                    secuidhome = item
                    urls = []
                    user=supabaseuserquery('tiktoka_douyin_users',secuid)
                    if len(user)>0:
                        print('this is a exsiting user', secuid)
                        videoids = user['video_ids']
                        urls=['https://www.douyin.com/video/'+x for x in videoids]
                    else:
                        # 冷热缓存 将supabase  firebase作为冷存储
                        toast('This is a new user not in our database. may need longer time to process',
                                position='right', color='#2188ff', duration=5, onclick=show_msg_newuser)
                        loadingbar(id='nuser', init=0.3,
                                    label='new user indexing')
                        try:

                            videoids = usersearch_douyin.get_user_video_list_douyin_pl(
                                secuidhome)
                            usersearch_douyin.close()
                        except:
                            videoids = get_user_video_list_douyin_undetected(
                                secuidhome)
                        urls=['https://www.douyin.com/video/'+x for x in videoids]

                        supabaseuserupdate('tiktoka_douyin_users',{'video_ids':videoids},secuid)
                        set_processbar(
                            'nuser', (idx+1) / len(douyin_userhomelist))
                        time.sleep(0.1)
                        # addUser2dict(users)
                        # douyintable=newtable(os.environ['AIRTABLE_API_KEY'],
                        # os.environ['TIKTOKA_AIRTABLE_BASE_KEY'],
                        # os.environ['DOUYIN_AIRTABLE_TABLE_KEY']
                        # )
                        # rows=[{
                        #     'secuid':secuid,
                        #     'urls':urls,
                        #     'updateAt':datetime.now()
                        # }]
                        # updaterow(douyintable,rows)
                        clear('nuser')
                    time.sleep(1)

                    msg = 'removing watermark +1'
                    toast(msg, position='right',
                            color='#2188ff', duration=2)
                    douyin_user_video_url_list.extend(urls)
                    if len(douyin_userhomelist) == 1:
                        for i in range(1, 4):
                            set_processbar('alluser', i / 3)
                            time.sleep(0.1)
                    else:
                        set_processbar(
                            'alluser', (idx+1) / len(douyin_userhomelist))

                clear('alluser')

            if len(douyin_user_video_url_list) > 0:
                print('douyin_user_video_url_list',douyin_user_video_url_list)
                msg = 'STEP 3 : analysing ' + \
                    str(len(douyin_user_video_url_list)) + \
                    ' videos from userhome links'
                toast(msg, position='right',
                        color='#2188ff', duration=5)
                loadingbar(id='alluservideo', init=0.3,
                            label='all user videos downloading')
                for idx, long_url in enumerate(douyin_user_video_url_list):

                    # if '/user' in long_url:
                    #     continue
                    videoid = long_url.split(
                        'https://www.douyin.com/video/')[1]
                    # query videois in db to check exist and deleted
                    # deleted, js, key = filter_deleted_videos(
                    #     long_url, videoid)
                    # if deleted == False:
                    #     result = put_result(
                    #         long_url, display_label, idx, js, key)
                    #     allquickdownloadlist.append(result)
                    videoinfo,resulttype=scaper.douyin_videoinfo(videoid)
                    if videoinfo is None:
                        put_text('this video is not supported yet',long_url)
                    else:
                        result = put_result(
                                videoinfo, display_label, idx, resulttype)
                        allquickdownloadlist.append(result)
                    msg = 'removing watermark +1'
                    toast(msg, position='right',
                            color='#2188ff', duration=2)
                    if len(douyin_user_video_url_list) == 1:
                        for i in range(1, 4):
                            set_processbar('alluservideo', i / 3)
                            time.sleep(0.1)
                    else:
                        set_processbar(
                            'alluservideo', (idx+1) / len(douyin_user_video_url_list))
                clear('alluservideo')
        # Analysis end time
        end = time.time()
        put_html("<br><hr>")
        put_text('Parsing is complete! time consuming: %.4fs' %
                    (end - start))

        # put_html(quick3%(allquickdownloadlist,display_label['quickdownload']))

        popup('Finished processing',
                [put_html(quick3 % (allquickdownloadlist, display_label['quickdownload'])),
                put_link('%s' % display_label['returnhome'], '/')

                ],
                size=PopupSize.LARGE)
        if userip in userip_call_count:
            userip_call_count[userip] = userip_call_count[userip]+1
            set_userip_call_count(userip_call_count)

    except Exception as e:
        # exception catch
        error_do(e, 'main')
        end = time.time()
        put_text('Parsing is complete! time consuming: %.4fs' %
                    (end - start))
    print(allquickdownloadlist,'-==================')
    allquickdownloadlistdict={}
    for i in allquickdownloadlist:
        allquickdownloadlistdict[i['name']]=i['downloadlink']
    put_row([
    put_button("Try again", onclick=lambda: session.run_js(
        return_home), color='success', outline=False),
    # put_button(display_label['quickdownload'], onclick=lambda: session.run_js(
    #     quick3js%allquickdownloadlist), color='success', outline=False)
                put_button("get tar/zip", onclick=lambda: video_download_window(allquickdownloadlistdict))        
        ])    
# session.run_js("download_files(%s);"%allquickdownloadlist)

def tiktokview(tiktok_url_list,display_label,userip,userip_call_count):
    start = time.time()
    allquickdownloadlist = []

    try:

        tiktok_standlone_video_url_list = []
        tiktok_user_video_url_list = []

        tiktok_userhomelist = []

        if len(tiktok_url_list) > 0:
            toast('parsing user input', position='right',
                    color='#2188ff', duration=3)
            loadingbar(id='extractingurl', init=0.3,
                        label='extracting input urls')
            for idx, url in enumerate(tiktok_url_list):

                if 'v.tiktok.com' in url:
                    with sync_playwright() as p:

                        page, res = get_playright(p, url)
                        long_url = res.url
                        print('===', long_url)
                        if '?' in long_url:
                            long_url = long_url.split('?')[0]
                        if '/user' in long_url:
                            tiktok_userhomelist.append(long_url)
                        elif '/video' in long_url:
                            tiktok_standlone_video_url_list.append(
                                long_url)
                elif 'www.tiktok.com/video' in url:
                    if '?' in url:
                        url = url.split('?')[0]
                    tiktok_standlone_video_url_list.append(url)
                elif 'www.tiktok.com/user' in url:
                    if '?' in url:
                        url = url.split('?')[0]
                    tiktok_userhomelist.append(url)
                elif 'www.iestiktok.com/share/user' in url:
                    userprefix = 'https://www.tiktok.com/user/'
                    # https://www.iestiktok.com/share/user/MS4wLjABAAAAqzSH2QSxlt5qxYcTiSQ7Fqlho9lDUAaEZgIdgs4xl0E?with_sec_did=1&sec_uid=MS4wLjABAAAAqzSH2QSxlt5qxYcTiSQ7Fqlho9lDUAaEZgIdgs4xl0E&u_code=h6k5ffc9&did=MS4wLjABAAAAypaUWYLhajUUAlLsugFR6fwDjeKmAC0do3pCzmJckSo&iid=MS4wLjABAAAAMbQPjJHaOPuA5-EPckp4s49p8sAFL6YvWvQO1nIzKqaooAW91pQgsN1NAfkoEGhi&ecom_share_track_params=%7B%22is_ec_shopping%22:%221%22%7D&utm_campaign=client_share&app=aweme&utm_medium=ios&tt_from=copy&utm_source=copy
                    secuid = url.split(
                        '?')[0].split('share/user/')[-1]
                    secuidhome = userprefix + secuid
                    tiktok_userhomelist.append(secuidhome)
                if len(tiktok_url_list) == 1:
                    for i in range(1, 4):
                        set_processbar('extractingurl', i / 3)
                        time.sleep(0.1)
                else:
                    set_processbar(
                        'extractingurl', (idx+1) / len(tiktok_url_list))

            clear('extractingurl')
            if len(tiktok_standlone_video_url_list) > 0:

                msg = 'STEP 2 : analysing ' + \
                    str(len(tiktok_standlone_video_url_list)) + \
                    ' videos from standlone links'
                toast(msg, position='right',
                        color='#2188ff', duration=5)
                loadingbar(id='svd', init=0.3,
                            label='specific videos downloading')
                for idx, long_url in enumerate(tiktok_standlone_video_url_list):

                    if '/user' in long_url:
                        continue
                    videoid = long_url.split(
                        'https://www.tiktok.com/video/')[1]
                    deleted, js, key = filter_deleted_videos(
                        long_url, videoid)
                    if deleted == False:
                        result = put_result(
                            url, display_label, idx, js, key)
                        allquickdownloadlist.append(result)
                    if len(tiktok_standlone_video_url_list) == 1:
                        for i in range(1, 4):
                            set_processbar('svd', i / 3)
                            time.sleep(0.1)
                    else:
                        set_processbar(
                            'svd', (idx+1) / len(tiktok_standlone_video_url_list))

                clear('svd')
            if len(tiktok_userhomelist) > 0:
                msg = 'start to extract user videos'
                toast(msg, position='right',
                        color='#2188ff', duration=3)
                loadingbar(id='alluser', init=0.3,
                            label='user videos downloading')
                users = loadUser2dict(mode='tiktok')
                # print('===', users)
                for idx, item in enumerate(tiktok_userhomelist):

                    secuid = item.split('/')[-1]
                    secuidhome = item
                    urls = []
                    if not users == {} and secuid in users:
                        print('this is a exsiting user', secuid)
                        urls = users[secuid]
                    else:
                        # 冷热缓存 将airtable作为冷存储
                        toast('This is a new user not in our database. may need longer time to process',
                                position='right', color='#2188ff', duration=5, onclick=show_msg_newuser)
                        loadingbar(id='nuser', init=0.3,
                                    label='new user indexing')
                        try:
                            urls = scraper.get_user_video_list_tiktok_pl(
                                secuidhome)
                        except:
                            # urls = get_user_video_list_tiktok_undetected(secuidhome)
                            pass
                        users[secuid] = urls
                        set_processbar(
                            'nuser', (idx+1) / len(tiktok_userhomelist))
                        time.sleep(0.1)
                        addUser2dict(users)
                        # tiktoktable=newtable(os.environ['AIRTABLE_API_KEY'],
                        # os.environ['TIKTOKA_AIRTABLE_BASE_KEY'],
                        # os.environ['DOUYIN_AIRTABLE_TABLE_KEY']
                        # )
                        # rows=[{
                        #     'secuid':secuid,
                        #     'urls':urls,
                        #     'updateAt':datetime.now()
                        # }]
                        # updaterow(tiktoktable,rows)
                        clear('nuser')
                    time.sleep(1)

                    msg = 'removing watermark +1'
                    toast(msg, position='right',
                            color='#2188ff', duration=2)
                    tiktok_user_video_url_list.extend(urls)
                    if len(tiktok_userhomelist) == 1:
                        for i in range(1, 4):
                            set_processbar('alluser', i / 3)
                            time.sleep(0.1)
                    else:
                        set_processbar(
                            'alluser', (idx+1) / len(tiktok_userhomelist))

                clear('alluser')

            if len(tiktok_user_video_url_list) > 0:

                msg = 'STEP 3 : analysing ' + \
                    str(len(tiktok_user_video_url_list)) + \
                    ' videos from userhome links'
                toast(msg, position='right',
                        color='#2188ff', duration=5)
                loadingbar(id='alluservideo', init=0.3,
                            label='all user videos downloading')
                for idx, long_url in enumerate(tiktok_user_video_url_list):

                    if '/user' in long_url:
                        continue
                    videoid = long_url.split(
                        'https://www.tiktok.com/video/')[1]
                    deleted, js, key = filter_deleted_videos(
                        long_url, videoid)
                    if deleted == False:
                        result = put_result(
                            url, display_label, idx, js, key)
                        allquickdownloadlist.append(result)
                    msg = 'removing watermark +1'
                    toast(msg, position='right',
                            color='#2188ff', duration=2)
                    if len(tiktok_user_video_url_list) == 1:
                        for i in range(1, 4):
                            set_processbar('alluservideo', i / 3)
                            time.sleep(0.1)
                    else:
                        set_processbar(
                            'alluservideo', (idx+1) / len(tiktok_user_video_url_list))
                clear('alluservideo')
        # Analysis end time
        end = time.time()
        put_html("<br><hr>")
        put_text('Parsing is complete! time consuming: %.4fs' %
                    (end - start))

        # put_html(quick3%(allquickdownloadlist,display_label['quickdownload']))

        popup('Finished processing',
                [put_html(quick3 % (allquickdownloadlist, display_label['quickdownload'])),
                put_link('%s' % display_label['returnhome'], '/')

                ],
                size=PopupSize.LARGE)
        if userip in userip_call_count:
            userip_call_count[userip] = userip_call_count[userip]+1
            set_userip_call_count(userip_call_count)

    except Exception as e:
        # exception catch
        error_do(e, 'main')
        end = time.time()
        put_text('Parsing is complete! time consuming: %.4fs' %
                    (end - start))
    put_link('%s' % display_label['returnhome'], '/')
    put_button("Try again", onclick=lambda: run_js(
        return_home), color='success', outline=True),
# session.run_js("download_files(%s);"%allquickdownloadlist)
