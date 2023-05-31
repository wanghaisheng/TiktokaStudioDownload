


# 欢迎使用 `TikToka™ tiktok/douyin videos Download tookit` (抖音在线解析)




 Tiktoka Studio Downloader Lite  running in your browser using WebAssembly and Pyodide 
 
 
      

How this works

 tiktoka studio Downloader  Lite runs the full  Tiktoka Studio Downloader server-side  Python web application directly in your browser, using the Pyodide build of Python compiled to WebAssembly.

When you launch the demo, your browser will download and start executing a full Python interpreter, install the  Tiktoka Studio Downloader package (and its dependencies), download one or more SQLite database files and start the application running in a browser window (actually a Web Worker attached to that window).




tiktoka视频下载工具，批量Douyin/TikTok解析下载无水印视频/图集，并将结果显示在网页上。同时支持API调用，可配合iOS快捷指令APP实现应用内下载。基于抖音官方API/非官方api/selenium等技术，实现在线、离线下载


## Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/wanghaisheng/TiktokaDownload)


# azure deploy

## widnows  az cli 

https://anduin.aiursoft.com/post/2020/3/19/install-azure-cli-on-windows-10-and-use-it-in-bash




        """
        获取关键词搜索结果
        :param keyword:
        :param cursor: 上一页会返回下一页的cursor值
        :param search_source: search_source为搜索类型，目前支持以下取值：
  video_search: 搜索视频
  poi: 搜索地点
  user: 搜索用户，此时keyword建议填用户的short_id(抖音号)
  challenge: 搜索话题/挑战
        :param sort_type: sort_type: 对结果排序，取值为 0（综合排序），1（最多点赞），2（最新发布）
        :param publish_time: 限制发布时间，取值为 0（不限），1（一天内），7（一周内），182（半年内）
        :return:
        """
            short_url
            long_url
            aweme_id
            aweme_detail = result['result']['aweme_detail']
            author_name = aweme_detail['author']['nickname']
            author_sec_uid = aweme_detail['author']['sec_uid']
            author_id = aweme_detail['author_user_id']
            author_url = f"https://www.douyin.com/user/{author_sec_uid}?&author_id={author_id}"
            comment_count = aweme_detail['statistics']['comment_count']
            digg_count = aweme_detail['statistics']['digg_count']
            share_count = aweme_detail['statistics']['share_count']
            collect_count = aweme_detail['statistics']['collect_count']
            create_time = aweme_detail['create_time']
            timeArray = time.localtime(create_time)
            post_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    "用户名",
    "用户ID",
    "用户签名",
    "用户粉丝",
    "用户关注数",
    "用户获赞数",
    "用户作品ID",
    "用户作品链接",
    "用户作品标题",
    "用户作品评论数",
    "用户作品点赞数",
    "用户作品下载数",
    "用户作品分享数",
    "用户作品转发数",
    "用户作品发布时间",

DY_API_PATH = {
    'post': '/api/douyin/aweme/post',
    'favorite': '/api/douyin/aweme/favorite',
    'challenge': '/api/douyin/aweme/challenge',
    'user_detail': '/api/douyin/aweme/user/detail',
    'challenge_detail': '/api/douyin/aweme/challenge/detail',
    'challenge_related': '/api/douyin/aweme/poi/challenge/related',
    'detail': '/api/douyin/aweme/detail',
    'comment': '/api/douyin/aweme/comment',
    'comment_reply': '/api/douyin/aweme/comment/reply',
    'promotion': '/api/douyin/aweme/promotion',
    'product_item': '/api/douyin/haohuo/product/item',
    'search': '/api/douyin/aweme/search',
    'poi_detail': '/api/douyin/aweme/poi/detail',
    'poi_aweme': '/api/douyin/aweme/poi/aweme',
    'user_follower_list': '/api/douyin/aweme/user/follower/list',
    'user_following_list': '/api/douyin/aweme/user/following/list',
    'hotsearch_brand_category': '/api/douyin/aweme/hotsearch/brand/category',
    'hotsearch_brand_weekly_list': '/api/douyin/aweme/hotsearch/brand/weekly/list',
    'hotsearch_brand_billboard': '/api/douyin/aweme/hotsearch/brand/billboard',
    'hotsearch_brand_detail': '/api/douyin/aweme/hotsearch/brand/detail'
}



    result = dy.get_post(user_id=96671888371, max_cursor=0)
    # result = dy.get_post(user_id=u_id, max_cursor=0)
    print(result)
    if result is not None:
        while 'max_cursor' in result['result'].keys():
            print(result)
            aweme_list = result['result']['aweme_list']
            for aweme in aweme_list:
                user_name = aweme['author']['nickname']
                uid = aweme['author']['uid']
                sign = aweme['author']['signature']
                # user = "UNI星球"
                fans = "20.2w"
                follower = 3
                like_count = "200.6w"
                # user_url = "https://www.douyin.com/user/MS4wLjABAAAASnmoVotBsVhd4vE1FxuawkL75r_Hc8PQynaM5UAqUvE?enter_method=video_title&author_id=98289525851&group_id=6916409351733366019&log_pb=%7B%22impr_id%22%3A%22021625638344237fdbddc0100fff0030a0a1a880000002020eba6%22%7D&enter_from=video_detail"
                aweme_id = aweme['aweme_id']
                aweme_url = f"https://www.douyin.com/video/{aweme_id}"
                desc = aweme['desc']
                comment_count = aweme['statistics']['comment_count']
                digg_count = aweme['statistics']['digg_count']
                download_count = aweme['statistics']['download_count']
                forward_count = aweme['statistics']['forward_count']
                share_count = aweme['statistics']['share_count']
                ts = aweme['create_time']
                timeArray = time.localtime(ts)
                create_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
