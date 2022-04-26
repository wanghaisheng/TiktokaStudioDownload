#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author: https://github.com/Evil0ctal/
# @Time: 2021/11/06
# @Update: 2022/04/21
# @Function:
# 核心代码，估值1块(๑•̀ㅂ•́)و✧
# 用于爬取Douyin/TikTok数据并以字典形式返回。


import re
import json
import requests
from tenacity import *
import time

class Scraper:
    """
    Scraper.douyin():抖音视频/图集解析，返回字典。
    Scraper.tiktok():TikTok视频解析，返回字典。
    """

    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.66'
        }
        self.tiktok_headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "authority": "www.tiktok.com",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Host": "www.tiktok.com",
            "User-Agent": "Mozilla/5.0  (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/86.0.170 Chrome/80.0.3987.170 Safari/537.36",
        }

    @retry(stop=stop_after_attempt(3), wait=wait_random(min=0.2, max=2))
    def douyin(self, original_url):
        """
        利用官方接口解析抖音链接信息
        :param original_url: 抖音/TikTok链接(支持长/短链接)
        :return:包含信息的字典
        """
        headers = self.headers
        try:
            # 开始时间
            start = time.time()
            # 判断是否为个人主页链接
            if 'user' in original_url:
                return {'status': 'failed', 'reason': '暂不支持个人主页批量解析', 'function': 'Scraper.douyin()',
                        'value': original_url}
            else:
                # 原视频链接
                r = requests.get(url=original_url, headers=headers, allow_redirects=False)
                try:
                    # 2021/12/11 发现抖音做了限制，会自动重定向网址，但是可以从回执头中获取
                    long_url = r.headers['Location']
                    # 判断是否为个人主页链接
                    if 'user' in long_url:
                        return {'status': 'failed', 'reason': '暂不支持个人主页批量解析', 'function': 'Scraper.douyin()',
                                'value': original_url}
                except:
                    # 报错后判断为长链接，直接截取视频id
                    long_url = original_url
                # 正则匹配出视频ID
                try:
                    # 第一种链接类型
                    # https://www.douyin.com/video/7086770907674348841
                    key = re.findall('video/(\d+)?', long_url)[0]
                    print('视频ID为: {}'.format(key))
                except Exception:
                    # 第二种链接类型
                    # https://www.douyin.com/discover?modal_id=7086770907674348841
                    key = re.findall('modal_id=(\d+)', long_url)[0]
                    print('视频ID为: {}'.format(key))
                # 构造抖音API链接
                api_url = f'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={key}'
                print("正在请求抖音API链接: " + '\n' + api_url)
                # 将回执以JSON格式处理
                js = json.loads(requests.get(url=api_url, headers=headers).text)
                # 判断是否为图集
                if js['item_list'][0]['images'] is not None:
                    print("类型 = 图集")
                    # 类型为图集
                    url_type = 'album'
                    # 图集标题
                    album_title = str(js['item_list'][0]['desc'])
                    # 图集作者昵称
                    album_author = str(js['item_list'][0]['author']['nickname'])
                    # 图集作者签名
                    album_author_signature = str(js['item_list'][0]['author']['signature'])
                    # 图集作者UID
                    album_author_uid = str(js['item_list'][0]['author']['uid'])
                    # 图集作者抖音号
                    album_author_id = str(js['item_list'][0]['author']['unique_id'])
                    if album_author_id == "":
                        # 如果作者未修改过抖音号，应使用此值以避免无法获取其抖音ID
                        album_author_id = str(js['item_list'][0]['author']['short_id'])
                    # 尝试获取图集BGM信息
                    try:
                        # 图集BGM链接
                        album_music = str(js['item_list'][0]['music']['play_url']['url_list'][0])
                        # 图集BGM标题
                        album_music_title = str(js['item_list'][0]['music']['title'])
                        # 图集BGM作者
                        album_music_author = str(js['item_list'][0]['music']['author'])
                        # 图集BGM ID
                        album_music_id = str(js['item_list'][0]['music']['id'])
                        # 图集BGM MID
                        album_music_mid = str(js['item_list'][0]['music']['mid'])
                    except:
                        # 报错后代表无背景音乐
                        # 图集BGM链接
                        album_music = 'No BGM found'
                        # 图集BGM标题
                        album_music_title = 'No BGM found'
                        # 图集BGM作者
                        album_music_author = 'No BGM found'
                        # 图集BGM ID
                        album_music_id = 'No BGM found'
                        # 图集BGM MID
                        album_music_mid = 'No BGM found'
                    # 图集ID
                    album_aweme_id = str(js['item_list'][0]['statistics']['aweme_id'])
                    # 评论数量
                    album_comment_count = str(js['item_list'][0]['statistics']['comment_count'])
                    # 获赞数量
                    album_digg_count = str(js['item_list'][0]['statistics']['digg_count'])
                    # 播放次数
                    album_play_count = str(js['item_list'][0]['statistics']['play_count'])
                    # 分享次数
                    album_share_count = str(js['item_list'][0]['statistics']['share_count'])
                    # 上传时间戳
                    album_create_time = str(js['item_list'][0]['create_time'])
                    # 将话题保存在列表中
                    album_hashtags = []
                    for tag in js['item_list'][0]['text_extra']:
                        album_hashtags.append(tag['hashtag_name'])
                    # 将无水印图片链接保存在列表中
                    images_list = []
                    for data in js['item_list'][0]['images']:
                        images_list.append(data['url_list'][0])
                    # 结束时间
                    end = time.time()
                    # 解析时间
                    analyze_time = format((end - start), '.4f')
                    # 将信息储存在字典中
                    album_data = {'status': 'success',
                                  'analyze_time': (analyze_time + 's'),
                                  'url_type': url_type,
                                  'platform': 'douyin',
                                  'original_url': original_url,
                                  'api_url': api_url,
                                  'album_aweme_id': album_aweme_id,
                                  'album_title': album_title,
                                  'album_author': album_author,
                                  'album_author_signature': album_author_signature,
                                  'album_author_uid': album_author_uid,
                                  'album_author_id': album_author_id,
                                  'album_music': album_music,
                                  'album_music_title': album_music_title,
                                  'album_music_author': album_music_author,
                                  'album_music_id': album_music_id,
                                  'album_music_mid': album_music_mid,
                                  'album_comment_count': album_comment_count,
                                  'album_digg_count': album_digg_count,
                                  'album_play_count': album_play_count,
                                  'album_share_count': album_share_count,
                                  'album_create_time': album_create_time,
                                  'album_list': images_list,
                                  'album_hashtags': album_hashtags}
                    return album_data
                else:
                    print("类型 = 视频")
                    # 类型为视频
                    url_type = 'video'
                    # 视频标题
                    video_title = str(js['item_list'][0]['desc'])
                    # 视频作者昵称
                    video_author = str(js['item_list'][0]['author']['nickname'])
                    # 视频作者抖音号
                    video_author_id = str(js['item_list'][0]['author']['unique_id'])
                    if video_author_id == "":
                        # 如果作者未修改过抖音号，应使用此值以避免无法获取其抖音ID
                        video_author_id = str(js['item_list'][0]['author']['short_id'])
                    # 有水印视频链接
                    wm_video_url = str(js['item_list'][0]['video']['play_addr']['url_list'][0])
                    # 无水印视频链接 (在回执JSON中将关键字'playwm'替换为'play'即可获得无水印地址)
                    nwm_video_url = str(js['item_list'][0]['video']['play_addr']['url_list'][0]).replace('playwm',
                                                                                                         'play')
                    # 去水印后视频链接(2022年1月1日抖音APi获取到的URL会进行跳转，需要在Location中获取直链)
                    r = requests.get(url=nwm_video_url, headers=headers, allow_redirects=False)
                    video_url = r.headers['Location']
                    # 视频作者签名
                    video_author_signature = str(js['item_list'][0]['author']['signature'])
                    # 视频作者UID
                    video_author_uid = str(js['item_list'][0]['author']['uid'])
                    # 尝试获取视频背景音乐
                    try:
                        # 视频BGM链接
                        video_music = str(js['item_list'][0]['music']['play_url']['url_list'][0])
                        # 视频BGM标题
                        video_music_title = str(js['item_list'][0]['music']['title'])
                        # 视频BGM作者
                        video_music_author = str(js['item_list'][0]['music']['author'])
                        # 视频BGM ID
                        video_music_id = str(js['item_list'][0]['music']['id'])
                        # 视频BGM MID
                        video_music_mid = str(js['item_list'][0]['music']['mid'])
                    except:
                        # 出错代表无背景音乐
                        # 视频BGM链接
                        video_music = 'No BGM found'
                        # 视频BGM标题
                        video_music_title = 'No BGM found'
                        # 视频BGM作者
                        video_music_author = 'No BGM found'
                        # 视频BGM ID
                        video_music_id = 'No BGM found'
                        # 视频BGM MID
                        video_music_mid = 'No BGM found'
                    # 视频ID
                    video_aweme_id = str(js['item_list'][0]['statistics']['aweme_id'])
                    # 评论数量
                    video_comment_count = str(js['item_list'][0]['statistics']['comment_count'])
                    # 获赞数量
                    video_digg_count = str(js['item_list'][0]['statistics']['digg_count'])
                    # 播放次数
                    video_play_count = str(js['item_list'][0]['statistics']['play_count'])
                    # 分享次数
                    video_share_count = str(js['item_list'][0]['statistics']['share_count'])
                    # 上传时间戳
                    video_create_time = str(js['item_list'][0]['create_time'])
                    # 将话题保存在列表中
                    video_hashtags = []
                    for tag in js['item_list'][0]['text_extra']:
                        video_hashtags.append(tag['hashtag_name'])
                    # 结束时间
                    end = time.time()
                    # 解析时间
                    analyze_time = format((end - start), '.4f')
                    # 返回包含数据的字典
                    video_data = {'status': 'success',
                                  'analyze_time': (analyze_time + 's'),
                                  'url_type': url_type,
                                  'platform': 'douyin',
                                  'original_url': original_url,
                                  'api_url': api_url,
                                  'video_title': video_title,
                                  'nwm_video_url': video_url,
                                  'wm_video_url': wm_video_url,
                                  'video_aweme_id': video_aweme_id,
                                  'video_author': video_author,
                                  'video_author_signature': video_author_signature,
                                  'video_author_uid': video_author_uid,
                                  'video_author_id': video_author_id,
                                  'video_music': video_music,
                                  'video_music_title': video_music_title,
                                  'video_music_author': video_music_author,
                                  'video_music_id': video_music_id,
                                  'video_music_mid': video_music_mid,
                                  'video_comment_count': video_comment_count,
                                  'video_digg_count': video_digg_count,
                                  'video_play_count': video_play_count,
                                  'video_share_count': video_share_count,
                                  'video_create_time': video_create_time,
                                  'video_hashtags': video_hashtags}
                    return video_data
        except Exception as e:
            # 返回异常
            return {'status': 'failed', 'reason': e, 'function': 'Scraper.douyin()', 'value': original_url}

    @retry(stop=stop_after_attempt(3), wait=wait_random(min=0.2, max=2))
    def tiktok(self, original_url):
        """
        解析TikTok链接
        :param original_url:TikTok链接
        :return:包含信息的字典
        """
        headers = self.headers
        # 开始时间
        start = time.time()
        # 校验TikTok链接
        if original_url[:12] == "https://www.":
            original_url = original_url
            print("目标链接: ", original_url)
        else:
            # 从请求头中获取原始链接
            response = requests.get(url=original_url, headers=headers, allow_redirects=False)
            true_link = response.headers['Location'].split("?")[0]
            original_url = true_link
            # TikTok请求头返回的第二种链接类型
            if '.html' in true_link:
                response = requests.get(url=true_link, headers=headers, allow_redirects=False)
                original_url = response.headers['Location'].split("?")[0]
                print("目标链接: ", original_url)
        try:
            # 获取视频ID
            video_id = re.findall('video/(\d+)?', original_url)[0]
            print('获取到的TikTok视频ID是{}'.format(video_id))
            # 从TikTok网页获取部分视频数据
            tiktok_headers = self.tiktok_headers
            html = requests.get(url=original_url, headers=tiktok_headers)
            res = re.search('<script id="sigi-persisted-data">(.*)</script><script', html.text).group(1)
            resp = re.findall(r'^window\[\'SIGI_STATE\']=(.*)?;window', res)[0]
            result = json.loads(resp)
            author_id = result["ItemList"]["video"]["list"][0]
            # 从网页中获得的视频JSON数据
            video_info = result["ItemModule"][author_id]
            # 从TikTok官方API获取部分视频数据
            tiktok_api_link = 'https://api.tiktokv.com/aweme/v1/multi/aweme/detail/?aweme_ids=%5B{}%5D'.format(video_id)
            print('正在请求API链接:{}'.format(tiktok_api_link))
            response = requests.get(url=tiktok_api_link, headers=headers).text
            # 将API获取到的内容格式化为JSON
            result = json.loads(response)
            # 类型为视频
            url_type = 'video'
            # 无水印视频链接
            nwm_video_url = result["aweme_details"][0]["video"]["play_addr"]["url_list"][0]
            try:
                # 有水印视频链接
                wm_video_url = result["aweme_details"][0]["video"]['download_addr']['url_list'][0]
            except Exception:
                # 有水印视频链接
                wm_video_url = 'None'
            # 视频标题
            video_title = result["aweme_details"][0]["desc"]
            # 视频作者昵称
            video_author_nickname = result["aweme_details"][0]['author']["nickname"]
            # 视频作者ID
            video_author_id = result["aweme_details"][0]['author']["unique_id"]
            # 上传时间戳
            video_create_time = result["aweme_details"][0]['create_time']
            # 视频ID
            video_aweme_id = result["aweme_details"][0]['statistics']['aweme_id']
            # 视频BGM标题
            video_music_title = result["aweme_details"][0]['music']['title']
            # 视频BGM作者
            video_music_author = result["aweme_details"][0]['music']['author']
            # 视频BGM ID
            video_music_id = result["aweme_details"][0]['music']['id']
            # 视频BGM链接
            video_music_url = result["aweme_details"][0]['music']['play_url']['url_list'][0]
            # 评论数量
            video_comment_count = result["aweme_details"][0]['statistics']['comment_count']
            # 获赞数量
            video_digg_count = result["aweme_details"][0]['statistics']['digg_count']
            # 播放次数
            video_play_count = result["aweme_details"][0]['statistics']['play_count']
            # 下载次数
            video_download_count = result["aweme_details"][0]['statistics']['download_count']
            # 分享次数
            video_share_count = result["aweme_details"][0]['statistics']['share_count']
            # 作者粉丝数量
            video_author_followerCount = video_info['authorStats']['followerCount']
            # 作者关注数量
            video_author_followingCount = video_info['authorStats']['followingCount']
            # 作者获赞数量
            video_author_heartCount = video_info['authorStats']['heartCount']
            # 作者视频数量
            video_author_videoCount = video_info['authorStats']['videoCount']
            # 作者已赞作品数量
            video_author_diggCount = video_info['authorStats']['diggCount']
            # 将话题保存在列表中
            video_hashtags = []
            for tag in video_info['challenges']:
                video_hashtags.append(tag['title'])
            # 结束时间
            end = time.time()
            # 解析时间
            analyze_time = format((end - start), '.4f')
            # 储存数据
            video_date = {'status': 'success',
                          'analyze_time': (analyze_time + 's'),
                          'url_type': url_type,
                          'api_url': tiktok_api_link,
                          'original_url': original_url,
                          'platform': 'tiktok',
                          'video_title': video_title,
                          'nwm_video_url': nwm_video_url,
                          'wm_video_url': wm_video_url,
                          'video_author_nickname': video_author_nickname,
                          'video_author_id': video_author_id,
                          'video_create_time': video_create_time,
                          'video_aweme_id': video_aweme_id,
                          'video_music_title': video_music_title,
                          'video_music_author': video_music_author,
                          'video_music_id': video_music_id,
                          'video_music_url': video_music_url,
                          'video_comment_count': video_comment_count,
                          'video_digg_count': video_digg_count,
                          'video_play_count': video_play_count,
                          'video_share_count': video_share_count,
                          'video_download_count': video_download_count,
                          'video_author_followerCount': video_author_followerCount,
                          'video_author_followingCount': video_author_followingCount,
                          'video_author_heartCount': video_author_heartCount,
                          'video_author_videoCount': video_author_videoCount,
                          'video_author_diggCount': video_author_diggCount,
                          'video_hashtags': video_hashtags
                          }
            # 返回包含数据的字典
            return video_date
        except Exception as e:
            # 异常捕获
            return {'status': 'failed', 'reason': e, 'function': 'Scraper.tiktok()', 'value': original_url}


if __name__ == '__main__':
    # 测试类
    scraper = Scraper()
    while True:
        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                         input("Enter your Douyin/TikTok url here to test: "))[0]
        try:
            if 'douyin.com' in url:
                douyin_date = scraper.douyin(url)
                print(douyin_date)
            else:
                tiktok_date = scraper.tiktok(url)
                print(tiktok_date)
        except Exception as e:
            print("Error: " + str(e))


