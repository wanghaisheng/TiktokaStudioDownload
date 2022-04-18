import requests
import json
import re
import pickle
import os
import undetected_chromedriver as uc
import string
import random
import sys
from pyairtable.formulas import match
from pyairtable import *
from webdriver_manager.chrome import ChromeDriverManager
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'upgrade-insecure-requests': '1',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
}
Max_Tring = 100
# 获取用户的某一页视频清单

proxies = {
    'http': 'socks5://127.0.0.1:1080',
    'https': 'socks5://127.0.0.1:1080'
}


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
def get_video_list_once(sec_uid, max_cursor):
    user_url_prefix = 'https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid={0}&max_cursor={1}&count=2000'

    i = 0
    result = []
    has_more = False
    while result == []:
        i = i + 1
        #sys.stdout.write('---解析视频链接中 正在第 {} 次尝试...\r'.format(str(i)))
        # sys.stdout.flush()

        user_url = user_url_prefix.format(sec_uid, max_cursor)
        response = requests.get(user_url, headers=HEADERS)
        html = json.loads(response.text)

        if len(html['aweme_list']) > 0:

            # with open ("video_list.txt",'w',encoding='utf-8') as f:
            #    json.dump(html,f,ensure_ascii=False, indent=4)
            max_cursor = html['max_cursor']
            has_more = bool(html['has_more'])
            result = html['aweme_list']
        if i > Max_Tring:
            break
    # print(result)
    nickname = None
    video_list = []
    for item in result:
        if nickname is None:
            nickname = item['author']['nickname'] if re.sub(
                r'[\/:*?"<>|]', '', item['author']['nickname']) else None

            video_list.append({
                'desc': re.sub(r'[\/:*?"<>|]', '', item['desc']) if item['desc'] else '无标题' + str(int(time.time())),
                'url': item['video']['play_addr']['url_list'][0],
                'aweme_id': item['aweme_id'],
                'vid': item['video']['vid'],
                'cover_uri': item['video']['dynamic_cover']['uri'],
                'cover_url': item['video']['dynamic_cover']['url_list'][0] if len(item['video']['dynamic_cover']['url_list']) > 0 else None,
                'author_uid': item['author']['uid'],
                'author_sec_uid': item['author']['sec_uid'],
                'author_unique_id': item['author']['unique_id'],
                'nickname': item['author']['nickname'] if re.sub(r'[\/:*?"<>|]', '', item['author']['nickname']) else None,
                'played': 0
            })
    # print(video_list)
    return nickname, video_list, max_cursor, has_more

    # while has_more and remote_count>now_count:


def addUser2dict(users,mode='douyin'):
    # "uid":"79298110705","short_id":"148174106","nickname":"苹果 姐姐"
    # sec_uid MS4wLjABAAAAnLgnj-bl5HuQ5l79HK5P9qyT0-SSdP112ZHy09OQS0s
    # MS4wLjABAAAAmCVw52QL87x5VPclHYNaS3KCSm2o7IFZt1947MfH-9k
    # pidanxiongdi
    # 皮蛋兄弟
    # user = {"sec_uid": "MS4wLjABAAAAmCVw52QL87x5VPclHYNaS3KCSm2o7IFZt1947MfH-9k", "unique_id": "pidanxiongdi","nickname":"皮蛋兄弟","uid":"xxx","short_id":"xxx"}  # create a dictionary
    existing_user=loadUser2dict(mode)
    print('exisiting user',len(existing_user))
    # totaluser=existing_user+user
    print('after adding,exisiting user',len(users))
    with open(mode+'Users.pickle', 'wb') as handle:
        pickle.dump(users, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return ''


def set_userip_call_count(userip_call_count):

    with open('ip-api-call.pickle', 'wb') as handle:
        pickle.dump(userip_call_count, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return True


def get_userip_call_count():
    print('loading ip  api call db')
    if not os.path.exists('ip-api-call.pickle'):

        with open('ip-api-call.pickle', 'wb') as handle:
            userip_call_count = {}
            pickle.dump(userip_call_count, handle, protocol=pickle.HIGHEST_PROTOCOL)    
    try:

        with open('ip-api-call.pickle', 'rb') as handle:
            userip_call_count = pickle.load(handle)
    except EOFError:

        return None

    return userip_call_count


def loadUser2dict(mode='douyin'):
    print('loading user db')
    if not os.path.exists('tiktokUsers.pickle'):

        with open('tiktokUsers.pickle', 'wb') as handle:
            user = {}
            pickle.dump(user, handle, protocol=pickle.HIGHEST_PROTOCOL)
    if not os.path.exists('douyinUsers.pickle'):

        # Create the file if it does not exist
        with open('douyinUsers.pickle', 'wb') as handle:
            user = {}
            pickle.dump(user, handle, protocol=pickle.HIGHEST_PROTOCOL)
    try:

        with open(mode+'Users.pickle', 'rb') as handle:
            users = pickle.load(handle)
    except EOFError:

        return None

    return users


def upload_streamable(video_url, user, pw):
    """Uploads a video from a url to streamable, returns the streamable url if successful"""
    api_url = 'https://api.streamable.com/import'
    headers = {'User-Agent': 'Streamable Discord Upload Bot'}
    params = {'url': video_url}
    r = requests.get(api_url,
                     auth=(user, pw),
                     headers=headers,
                     params=params,
                     proxies=proxies)

    out = json.loads(r.content)

    if out["status"]:
        return out["shortcode"]

    else:
        return None
def url_ok(url):


    try:
        response = requests.head(url)
    except Exception as e:
        # print(f"NOT OK: {str(e)}")
        return False
    else:
        if response.status_code == 400 or response.status_code==404:
            # print("OK")
            print(f"NOT OK: HTTP response code {response.status_code}")

            return False
        else:

            return True   
def get_undetected_webdriver(silence:bool=True):
    options = uc.ChromeOptions()        
    options.add_argument("--no-sandbox")        
    options.add_argument("--disable-dev-shm-usage")        

    silence = True if silence is None or "linux" in sys.platform else silence

    if silence is True:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")

    # 使用 ChromeDriverManager 托管服务，自动适配浏览器驱动

    try:
        return uc.Chrome(
            use_subprocess=True,
            headless=silence,
            options=options,
            driver_executable_path=ChromeDriverManager(log_level=0).install(),
        )
    # 避免核心并行
    except OSError:
        return uc.Chrome(use_subprocess=True,headless=silence, options=options)
    

def newbase(apikey,baseid):
    if apikey=='' or apikey is None:
        apikey=os.environ['AIRTABLE_API_KEY']
    if baseid=='' or baseid is None:

        baseid=os.environ['AIRTABLE_BASE_KEY']    
    db=Base(apikey, baseid)    
    return db
def newtable(apikey,baseid,tableid):
    if apikey=='' or apikey is None:
        apikey=os.environ['AIRTABLE_API_KEY']
    if baseid=='' or baseid is None:

        baseid=os.environ['AIRTABLE_BASE_KEY']
    if tableid=='' or tableid is None:
        tableid=os.environ['AIRTABLE_TABLE_KEY']
    # api = Api(apikey)
    table = Table(apikey, baseid, tableid)

    return table
def insert2airtable(table,rows):
    # print(rows,'====',type(rows[0]))
    if len(rows)==1:

        table.create(rows[0])
    else:
        table.create(rows)


def getrowid(table,row):

    formula = match(row)
    try:
        id =table.first(formula=formula)['id']
    except:
        id = None
    return id

def updaterow(table,rows):
    if len(rows)==1:
        id =getrowid(table,rows[0])
        if id is None:
            insert2airtable(table,rows)            
        else:
            table.update(id,rows[0])
    else:
        for row in rows:
            id =getrowid(table,[row])
            if id is None:
                insert2airtable(table,[row])            
            else:
                table.update(id,[row])      
