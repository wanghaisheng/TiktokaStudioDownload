import time
from functools import partial
from pywebio.platform.flask import webio_view
from pywebio.platform.tornado_http import webio_handler as http_webio_handler

from shared.feedback import feedback
from shared.privacy import privacy
from shared.terms import terms
from shared.tiktoka import *
from flask import Flask
import os
app = Flask(__name__)

# if __name__ == "__main__":
# 初始化logs.txt

app.add_url_rule('/', 'webio_view', webio_view(partial(tiktoka, lang='')),
                 methods=['GET', 'POST', 'OPTIONS'])
for idx,item in enumerate(supportedlang) :
    app.add_url_rule('/'+item, 'webio_view_'+item, webio_view(partial(tiktoka, lang=item)),
                     methods=['GET', 'POST', 'OPTIONS'])
# app.add_url_rule('/en', 'webio_view_en', webio_view(partial(tiktoka, lang='en')),
#                  methods=['GET', 'POST', 'OPTIONS'])
# app.add_url_rule('/zh', 'webio_view_zh', webio_view(partial(tiktoka, lang='zh')),
#                  methods=['GET', 'POST', 'OPTIONS'])
# app.add_url_rule('/es', 'webio_view_es', webio_view(partial(tiktoka, lang='es')),
#                  methods=['GET', 'POST', 'OPTIONS'])
# # vietnam
# app.add_url_rule('/vi', 'webio_view_vi', webio_view(partial(tiktoka, lang='vi')),
#                  methods=['GET', 'POST', 'OPTIONS'])
# # Philippines
# app.add_url_rule('/fil', 'webio_view_fil', webio_view(partial(tiktoka, lang='fil')),
#                  methods=['GET', 'POST', 'OPTIONS'])
# app.add_url_rule('/ru', 'webio_view_ru', webio_view(partial(tiktoka, lang='ru')),
#                  methods=['GET', 'POST', 'OPTIONS'])
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
