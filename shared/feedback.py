__all__ = ['feedback']
from pywebio.output import put_html
from pywebio.platform import seo
from pywebio.platform.page import config
from pywebio.session import run_js
from shared.utils.constants import GA_JS_CODE, GA_JS_FILE,SEO_DESCRIPTION, SEO_TITLE
from shared.utils.contents.index import FOOTER, HEADER


@seo(SEO_TITLE, SEO_DESCRIPTION)
@config(theme="minty", js_file=[GA_JS_FILE], js_code=GA_JS_CODE)
def feedback() -> None:
    run_js(HEADER)
    run_js(FOOTER)

    # put_html(LANDING_PAGE_HEADING)
    put_html(r"""
    <iframe src="https://tally.so/embed/3xAAyw?alignLeft=1&hideTitle=1&transparentBackground=1" width="100%" height="1050" frameborder="0" marginheight="0" marginwidth="0" title="Feedback"></iframe>
    """)
