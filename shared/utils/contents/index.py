from ...settings import CONTACT_EMAIL

# This page contains all the html contents corresponding to `src/index.py`

# Header
# ^^^^^^
HEADER = """
    $('head').append('<script src="https://www.googletagmanager.com/gtag/js?id=G-484Z1BXPFZ"></script>')
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
    $('head').append('<meta property="og:image" content="https://raw.githubusercontent.com/wanghaisheng/TiktokaTikTokVideoDownloadTookit/main/favicon/tiktoka-1200.png">')
    $('head').append('<meta name="keywords" content="video, downloading, tiktoka,tiktok videos, free, douyin video,bulk download,">')
    $('head').append('<link rel="shortcut icon" href="https://raw.githubusercontent.com/wanghaisheng/TiktokaTikTokVideoDownloadTookit/main/favicon/favicon.ico" type="image/x-icon">')
    $('head').append('<link rel="alternate" href="ios-app://544007664/vnd.tiktoka/www.tiktokvideos.download/">')
    $('head').append('<link rel="alternate" href="android-app://com.google.android.tiktoka/http/www.tiktokvideos.download/">')
    $('head').append('<link rel="alternate" media="only screen and (max-width: 640px)" href="https://m.tiktokvideos.download/">')
    $('head').append('<link rel="alternate" media="handheld" href="https://m.tiktokvideos.download/">')
    $('#favicon32,#favicon16').remove();
    $('head').append('<meta charset="utf-8">')
    $('head').append('<meta name="viewport" content="width=device-width, initial-scale=1">
    $('head').append('<link rel="icon" type="image/png" href="favicon/android-chrome-512x512.png">')   
"""

# Footer
# ^^^^^^
FOOTER = f"""
$('FOOTER').html('✉️ <a href="mailto:tiktokadownloader@gmail.com" target="_blank">Contact</a> | 💡 <a href="/feedback">Feedback</a> | 📃 <a href="/terms">Terms of Use</a> | 🔏 <a href="/privacy">Privacy Policy</a> | <a href="https://archive.tiktokvideos.download/" >  Tiktoka Archive  </a> | <a href="https://blog.tiktokvideos.download/" >  Tiktoka Blog  </a>')
"""
# $('footer').append('<a href="https://archive.tiktokvideos.download/" >  Tiktoka Archive  </a>')
# $('footer').append('<a href="https://blog.tiktokvideos.download/" >  Tiktoka Blog  </a>')
# $('footer').append('<a href="https://trend.tiktokvideos.download/" >  Tiktoka Trends  </a>')
# $('footer').append('<a href="https://ninja.tiktokvideos.download/" >  Tiktoka Ninja  </a>')


LOAD_CSS = r"""
<style>
.img {
    width: auto;
    height: auto;
    max-width: 400;
    max-height: 300px;
    border:2px solid #fff;
    -moz-box-shadow: 10px 10px 5px #ccc;
    -webkit-box-shadow: 10px 10px 5px #ccc;
    box-shadow: 10px 10px 5px #ccc;
    -moz-border-radius:25px;
    -webkit-border-radius:25px;
    border-radius:25px;
}
</style>
"""

feaure_code = """
--------------------------------
*    # Save TikTok/Douyin Clips Individually  and in bulk

    Save one TikTok video at a time. Enter the link to a TikTok video or bunch of video links and download it to your computer.especially for Backup Your TikTok Account

*    # Save TikTok/Douyin User Clips Individually and in bulk
    Save one or more user video at a time. Enter the link to a Tiktok user or bunch of video links and download it to your computer in batch.

*    # Search User and Download user video (Coming soon)
    type user name or user id,if there is a user match the term,we can automatically download all of videos belong to this user

*    # Search keywords and Download keywords related video (Coming soon)
    type a keyword or more keywords,if there is videos match the term,we can automatically download all of videos

*    # Download New TikTok/Douyin Clips Automatically (Coming soon)

    Keep up with updates from your favorite TikTok creators and hashtags. Auto-check for new videos, grab fresh content every day without lifting a finger.

*    # Download TikTok/Douyin Videos by Date (Coming soon)

    Adjust the download date range at the in-app calendar. Download only the videos that were published during the specified time period.

*    # Save TikTok/Douyin Video Captions

    Get TikTok videos downloaded with their original captions. Hover the cursor over the video icon to see the caption in-app & copy it to the clipboard.

*    # Download Clips that Feature the Same Music (Coming soon)

    Grab all TikTok videos associated with particular audio. Enter the song name to start saving all TikTok videos that feature the track.

    """
faq_code = """
# Frequently Asked Questions

# How to download a TikTok video to Android phone?

*   Open the TikTok app or website on your phone and locate your target video.
*   Tap the Share button at the right bottom of the video and click on the Copy Link to save the video URL.
*   Paste this URL to the input box below. Click on the Search button to grab it. Refer to [How to Download TikTok Videos from Android Phone](/en/how-to-download-tiktok-videos-to-android) for details..

# How to download a TikTok video to iPhone/ipad?

The operation procedure is different depending on the OS version and device types.

iPhone with iOS 13+ or iPad with iPadOS 13+: the download can be done through the browser: Safari.

*   Open the TikTok app or website on your phone and locate your target video.
*   Tap the Share button at the right bottom of the video and click on the Copy Link to save the video URL.
*   Paste this URL to the input box above. Click on the Search button to grab it.
*   Click the Download icon at the top right corner of your browser to open the folder that holds video just downloaded.
*   Save it to your library by clicking on the Share and Save video option buttons.
    Refer to [How to Download TikTok Videos from iPhone/iPad ios13+](/en/how-to-download-tiktok-videos-to-iphone-ipad#ios13) for details.

iPhone or iPad with OS version 12 or less

*   Install the Documents by Readdle from the Apple Store. Google the name and find it in Apple Store. It is free.
*   Start the app and click on the Browser icon on its menu bar at the bottom of app window to initiate its browser function.
*   Go to this site by putting our site’s URL onto its address bar.
*   Paste the video URL into the input box and download the video as for iOS 13+ above.
    Refer to [How to Download TikTok Videos from iPhone/iPad ios12](/en/how-to-download-tiktok-videos-to-iphone-ipad#ios12) for details.

# How to download a TikTok video to Desktop PC?

*   Go to TikTok in your browser, say, Chrome, login to your account and locate your target video.
*   Tap the video and copy its URL in the browser address bar.
*   Paste this URL to the input box above. Click on the Search button to grab it. Refer to [How to Download Video from PC](/en/how-to-download-tiktok-videos-to-pc) for details.

# Where are the saved videos?

Your video is saved into the default download folder set by your browser, for instance, Downloads folder on Windows PC. You can change the default browser settings and make it manually choose the destination folder.

# Is the service provided by this site free?

Yes. It is totally free. Users have to make sure that you have a permission from the video owner to download the video. Our site does not store and keep any videos from the TikTok.

# Is there a limitation on the number of videos downloaded?

No. You can download videos as many as you like.

# Which devices are supported?

Any devices that can run the popular browsers such as Chrome, IE, Safari, Firefox are supported to use our service.

# Do I have to pay for TikTok MP4 download services?

No, you don't have to pay for anything, because our TikTok video download is always free!

# Do I need to install extensions to save videos from TT?

No. To download and remove the watermark from TikTok online, you just need a link. Paste it into the input field and select the appropriate format for conversion.

# Do I need to have a TikTok account to download videos?

No, you do not need to have a TT account. You can download any video when you have a link to it, just paste it into the download field at the top of the page and click "Download".
Our service will remove watermark from TikTok and the video will be ready to download in a few seconds.

# Can I download content from personal accounts?

Our TikTok downloader cannot access the content of private accounts and cannot save videos from there. You must make sure the account is public in order for us to download TikTok videos for you.
    """
