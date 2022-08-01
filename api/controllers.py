from twt_tools.thread import Thread
from twt_tools.user import User
from fastapi.responses import FileResponse
import os


async def thread_json(url):
    thread = Thread(url=url, thread_name=url, output_dir="")
    return thread.thread


async def thread_pdf(url):
    thread = Thread(url=url, thread_name=url, output_dir="")
    await thread.async_build_markdown()
    thread.build_pdf()
    thread.cleanup()

    filepath = f"{thread.thread_name}.pdf"
    return FileResponse(filepath)


def delete_pdf(name):
    os.remove(f"{name}.pdf")


async def user_data(url):
    pass


async def user_json(url, limit):
    user = User(url)
    return user.get_tweets(limit)

def quote_tweet_html(tweet):
    if tweet["quotedTweet"]:
        return f"- Quoting: <a href={tweet['quotedTweet']['url']}> {tweet['quotedTweet']['url']} </a>"
    else:
        return ""

def media_html(tweet):
    if tweet["media"]:
        html = ""
        for i in tweet["media"]:
            if i.get('fullUrl'):
                html += f"<a href={i['fullUrl']}><img src={i['previewUrl']} height=180 width=360></a>"
            if i.get('variants'):
                html += f"<a href={i['variants'][0]['url']}> <img src={i['variants'][0]['url']} height=200 width=360> </a>"
        return html
    else:
        return ""

def build_html(archive):
    tweets_html = ""
    for t in archive:
        tweets_html += (f"""<div>
        <h5> {t['date']}</h5>
        <p> {t['rawContent']} </p>
        """ +
            quote_tweet_html(t) 
            + media_html(t) +
        """
        <hr>
        </div>
        """)
    return tweets_html


async def user_html(url, limit):
    archive = User(url)
    html = f"""<html> 
    <head>
        <title> {archive.get_user().username}'s archive </title>
    </head>
    {build_html(archive.get_tweets(limit))}
    </html>
    """
    return html
