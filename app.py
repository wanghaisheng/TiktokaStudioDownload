import time
from functools import partial
from pywebio.platform.flask import webio_view
from shared.tiktoka import *
from shared.feedback import feedback
from shared.privacy import privacy
from shared.terms import terms
from flask import Flask
from pywebio import start_server


import os
app = Flask(__name__)

if __name__ == "__main__":
    # 初始化logs.txt
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open('logs.txt', 'a') as f:
        f.write("time: " + date + " " + "reload again!" + '\n')

    app.add_url_rule('/', 'webio_view', webio_view(partial(tiktoka, lang='')),
                     methods=['GET', 'POST', 'OPTIONS'])
    for idx,item in enumerate(supportedlang) :

        app.add_url_rule('/'+item, 'webio_view_'+item, webio_view(partial(tiktoka, lang=item)),
                     methods=['GET', 'POST', 'OPTIONS'])

    app.add_url_rule('/video', 'webio_view_video', download_video_url,
                     methods=['GET', 'POST'])

    app.add_url_rule('/bgm', 'webio_view_bgm', download_bgm_url,
                     methods=['GET', 'POST'])

    app.add_url_rule('/api', 'webio_view_api', webapi,
                     methods=['GET', 'POST'])

    app.add_url_rule('/loaddb', 'webio_view_loaddb', loaddb,
                     methods=['POST'])

    app.add_url_rule('/backupdb', 'webio_view_backupdb', backupdb,
                     methods=['GET'])


    app.add_url_rule('/feedback', 'webio_view_feedback', webio_view(feedback),
                    methods=['GET'])
    app.add_url_rule('/terms', 'webio_view_terms', webio_view(terms),
                    methods=['GET'])
    app.add_url_rule('/privacy', 'webio_view_privacy', webio_view(privacy),
                    methods=['GET'])


    if (os.environ.get('PORT')):
        port = int(os.environ.get('PORT'))
    else:
        port = 5001

    

    app.run(host='0.0.0.0',  port=port)
    # ？start_server(app,static_dir='Screenshots/',port=port)