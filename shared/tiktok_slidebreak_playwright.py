from enum import Flag
# from pydoc import cli
import time
import random
# import pyquery
import re
import json
import requests
import os
# from httpcore import TimeoutException
from PIL import Image
import cv2 as cv
import numpy as np
from pathlib import Path
from typing import Tuple, Optional, Union
from .util import id_generator
from collections import Counter

from playwright.sync_api import sync_playwright

useragent = [
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
]


class User_search_tiktok():
    def __init__(self):

        self._playwright = self._start_playwright()
        #     browser = p.chromium.launch()

        PROXY_SOCKS5 = "socks5://127.0.0.1:1080"
        headless = False
        # if not headless:
        #     headless = True
        proxy_option = 'dev'
        if proxy_option == "":
            print('start web page without proxy')

            browserLaunchOptionDict = {
                "headless": headless,
                # "executable_path": executable_path,
                "timeout": 30000
            }
            root_profile_directory = ''
            if not root_profile_directory:
                self.browser = self._start_browser("firefox", **browserLaunchOptionDict)
            else:
                self.browser = self._start_persistent_browser(
                    "firefox", user_data_dir=root_profile_directory, **browserLaunchOptionDict
                )
        # Open new page
            self.context = self.browser.new_context(locale='en-GB')
        else:
            print('start web page with proxy')

            browserLaunchOptionDict = {
                "headless": headless,
                "proxy": {
                    "server": PROXY_SOCKS5,
                },

                # timeout <float> Maximum time in milliseconds to wait for the browser instance to start. Defaults to 30000 (30 seconds). Pass 0 to disable timeout.#
                "timeout": 30000
            }
            root_profile_directory = ''

            if not root_profile_directory:
                self.browser = self._start_browser("firefox", **browserLaunchOptionDict)
            else:
                self.browser = self._start_persistent_browser(
                    "firefox", user_data_dir=root_profile_directory, **browserLaunchOptionDict
                )
        # Open new page
            self.context = self.browser.new_context()

    def open_page_tiktok(self):
        
        url = "https://www.tiktok.com/search/user?q=piediedie"
        page = self.browser.new_page()
        page.goto(url)
        self.page = page

        # self.driver.get()
    # print(self.driver.get_window_size()) # 有头窗口大小
        code_path = "./image/code"+id_generator()+".png"  # 验证码背景图
        if not os.path.exists("./image"):
            os.makedirs("./image")
        FLAG = True
        try:
            
            self.page.locator('//*[@id="secsdk-captcha-drag-wrapper"]/div[2]')
            while FLAG==True:
                print("正在尝试破解验证码...")

                ans = self.solve_captcha(code_path)
                if ans['success']:
                    FLAG= False
                    break
                time.sleep(4)
        except Exception as e:

            FLAG = False
            print("there is no slide")

        # self.pass_verify(code_path)
        print("driver_id:", id(self), "start a temp no slide page\n=======================")

        return self.page

    def close_driver(self):
        self.browser.close()

    def solve_captcha(self, code_path, count=0):
        self.page.reload()
        t = self.page.locator('img[class^="captcha_verify_img_slide"]')
        if os.path.exists(code_path):
            os.remove(code_path)
        print('detected captcha', t)
        time.sleep(2)
        if count > 8:  # 约15次错误尝试 会报频繁
            self.browser.close()
            self.open_driver()
            return
        try:
            print('detected capatcha image',)
            time.sleep(3)
            img = self.page.locator('img[id="captcha-verify-image"]')
            # ""加不加一样
            print('detected capatcha image', img.get_attribute('src'))
            # slide = self.page.locator("//html/body/div[4]/div/div[2]/img[2]").bounding_box()
            self.page.wait_for_selector('.captcha_verify_img_slide')

            slide=self.page.locator(".captcha_verify_img_slide").bounding_box()
#   only crop quekou area
            clip ={
                "x":0,
                "y":slide['y']-2,
                "width":self.page.viewport_size['width'],
                "height":slide['height']+1
            }
            if img.get_attribute('src'):
                time.sleep(1)
                self.page.screenshot(path=code_path,clip=clip)
            print('finished screenshot of slide')
            print('==', slide)

            print('finding offset to move')
            img = cv.imread(code_path)
            card_img=img            
            img_blur = cv.GaussianBlur(card_img, (7, 7), 1)
            img = cv.medianBlur(img,5)
            img_gray = cv.cvtColor(img_blur, cv.COLOR_BGR2GRAY)
            ret2,thresh = cv.threshold(img_gray,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
            img_canny = cv.Canny(thresh, 50, 190)
            
            kernel = np.ones((3))
            # erosion = cv.erode(img_canny, kernel, iterations=1)            
            img_dilated = cv.dilate(img_canny, kernel, iterations=1)
            # cv.imshow('img_dilated', img_dilated)
            # cv.waitKey(0)
            contours, hierarchy = cv.findContours(img_dilated,
                                                  cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
            e2 = []
            offsetlist = []
            # for contour in contours:

            for i,cnt in enumerate(contours):
                    # if the contour has no other contours inside of it
                if hierarchy[0][i][2] == -1 :
                            # if the size of the contour is greater than a threshold
                    # if  cv.contourArea(cnt) > 10000:
                    x, y, w, h = cv.boundingRect(cnt)
                    print(x,y,w,h)
                    if cnt.size > 300 and w > 40 and h > 40 and x-slide['x'] > 60:  # TUNE
                        offsetlist.append(x)
                        e2.append(cnt)
            print(offsetlist,'======!')
            final =cv.drawContours(card_img, e2, -1, (0, 255, 0), 3)

            offsetlist=sorted(list(set(offsetlist)))
    
            if len(offsetlist)==0:
                return {'success': 0}
            else:
                source = self.page.locator(".secsdk-captcha-drag-icon").bounding_box()

                for x_offset in offsetlist:
                    print('offset is', x_offset)
                    x_offset=x_offset-3
                    y_offset = 0
                    # action = ActionChains(self.driver)
                    steps_count = 5
                    box_pos_x = source['x'] + source['width'] / 2
                    box_pos_y = source['y'] + source['height'] / 2
                    self.page.mouse.move(box_pos_x, box_pos_y)
                    # self.page.locator(".secsdk-captcha-drag-icon").click()
                    print('move mouse to dragon icon and hold')

                    # self.page.mouse.click(box_pos_x, box_pos_y)

                    self.page.mouse.down()
                    print('holding', x_offset, y_offset)
                    L1 = [0.3, 0.24, 0.21, 0.14, 0.11]
                    step = (x_offset+source['width']/2-source['x'])/steps_count                        
                    for x in range(0,steps_count):
                        tmp_x =source['x'] +step*(x)
                    #   move x  是绝对坐标值 不是offset  起点相当于是盒子的中心点 由于不是整除 每次移动可能会与最终的框有一定匹配上的偏移 要么多了 要么少了
                        self.page.mouse.move(tmp_x+random.choice(L1)*source['width'], box_pos_y)
                        time.sleep(random.randint(20, 40)*0.01)
                    self.page.mouse.move(x_offset+source['width']/2, box_pos_y)

                    print('release dragon icon')
                    self.page.mouse.up()
                    # self.page.reload()
                    time.sleep(3)
                    
                    t =self.page.locator('.captcha_verify_container').is_visible()
                    print('check captcha still exist',t)
                    # time.sleep(20)
                    if  t :
                        print('still exist')
                        return {'success': 0}
                    else:
                        print('well done')
                        return {'success': 1}
        except Exception as e:
            print('pass very.....')
            return {'success': 1}


    def isVaild(self):  # 判断是否被封
        try:
            return self.browser.query_selector('//*[@id="root"]/div/div[2]/div/div[2]/div[3]/div/div/div[2]').text != "服务出现异常"
        except:
            return True

    def user_search_tiktok(self, keyword):
        # if random.randint(0,1): # 模拟崩溃
        #     raise Exception()
        # page =self.browser.new_page()

        page = self.page
        page.goto("https://www.tiktok.com/search/user?q=" + keyword)
        # try:
        #     page.wait_for_selector('div[style="display: block;"] ul li a div button')
        # except TimeoutException:
        #     if not self.isVaild():  # 被封，需要重启driver
        #         self.close_driver()
        #         raise Exception()
        #     return []  # 没被封，搜索了一些没有返回结果的特殊字符，如 https://www.tiktok.com/search/%01?source=normal_search&type=user

        return self.get_userinfo_tiktok(page)

    def get_userinfo_tiktok(self, page):  # 提取数据
        ul = page.locator('.tiktok-1fwlm1o-DivPanelContainer')
        # time.sleep(100)
        print("获取到{}位用户信息",ul.count(),ul)

        data = []
        for index in range(1,ul.count()):
            print('index====',index)
            try:
                nickname =ul.nth(index).locator('div.tiktok-133zmie-DivLink:nth-child(1) > a:nth-child(2) > p:nth-child(1)').text_content()
                signature = ul.nth(index).locator('div.tiktok-133zmie-DivLink:nth-child(1) > a:nth-child(2) > p:nth-child(3) > strong:nth-child(1)').text_content() # 用户名和简介
                avatar_thumb = ul.nth(index).locator('div.tiktok-133zmie-DivLink:nth-child(1) > a:nth-child(1) > div:nth-child(1) > span:nth-child(1) > img:nth-child(1)').get_attribute('src')
                secuid =ul.nth(index).locator('div.tiktok-133zmie-DivLink:nth-child(1) > a:nth-child(2)').get_attribute('href')
                uniqueid= ul.nth(index).locator('div.tiktok-133zmie-DivLink:nth-child(1) > a:nth-child(2) > p:nth-child(1)').text_content()
                print(nickname,secuid,uniqueid)

            # 昵称、认证、抖音号、获赞、粉丝数、简介、头像
                data.append({'secid': secuid,
                            'nickname': nickname,
                            'custom_verify': '',
                            'unique_id':uniqueid,
                            'liked': '',
                            'follower_count': ul.nth(index).locator('div.tiktok-133zmie-DivLink:nth-child(1) > a:nth-child(2) > div:nth-child(2) > strong:nth-child(2)').text_content().split('Followers')[0],
                            'signature': signature,
                            'avatar_thumb': avatar_thumb,
                            })
            except:  # 无用户名
                nickname=''
                signature = ''
                avatar_thumb = ''

            # break
        # print(data)
        return data

    @staticmethod
    def _start_playwright():
        return sync_playwright().start()

    def _start_browser(self, browser: str, **kwargs):
        if browser == "chromium":
            return self._playwright.chromium.launch(**kwargs)

        if browser == "firefox":
            return self._playwright.firefox.launch(**kwargs)

        if browser == "webkit":
            return self._playwright.webkit.launch(**kwargs)

        raise RuntimeError(
            "You have to select either 'chromium', 'firefox', or 'webkit' as browser."
        )

    def _start_persistent_browser(
        self, browser: str, user_data_dir: Optional[Union[str, Path]], **kwargs
    ):
        if browser == "chromium":
            return self._playwright.chromium.launch_persistent_context(
                user_data_dir, **kwargs
            )
        if browser == "firefox":
            return self._playwright.firefox.launch_persistent_context(
                user_data_dir, **kwargs
            )
        if browser == "webkit":
            return self._playwright.webkit.launch_persistent_context(
                user_data_dir, **kwargs
            )

        raise RuntimeError(
            "You have to select either 'chromium', 'firefox' or 'webkit' as browser."
        )

    def close(self):
        self.browser.close()
        self._playwright.stop()


if __name__ == "__main__":

    usersearch = User_search()
    # usersearch.open_page()
    # print(usersearch.user_search("pidanxiongdi"))
    # time.sleep(100)
    # for i in range(340,65535):
    #     print(driver.user_search(chr(i)))
    # u.close_driver()
