#本程序使用deepseek coder v2辅助制作，对话记录在对应的txt文件。本程序把调用ollama的部分合并到一个文件
import feedparser
import os
import time
from datetime import datetime, timedelta
import pytz
import re

import requests
import json

def put(text):
    url = "http://localhost:11434/api/generate"
    data = {"model": "gemma2:latest", "prompt":text}

    response = requests.post(url, json=data, stream=True)
    output_string = ""

    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            json_line = json.loads(decoded_line)
            if "created_at" in json_line and "done" in json_line:
                response_content = json_line.get("response", "")
                if response_content:
                    output_string += response_content

    return(output_string)

def summarize(text):
    text="总结以下文章:"+text
    output=put(text)
    return(output)

def translate(text):
    text="把以下文章翻译为中文:"+text
    output=put(text)
    return(output)

# RSS 链接列表
rss_urls = [
    "http://www.geekpark.net/rss",
    "http://www.ifanr.com/feed",
    "https://www.oschina.net/news/rss",
    "http://sspai.com/feed",
    "https://a.jiemian.com/index.php?m=article&amp;a=rss",
    "http://www.chuapp.com/feed",
    "http://youxiputao.com/feed",
    "http://www.gamelook.com.cn/feed",
    "http://jandan.net/feed",
    "http://www.ithome.com/rss/",
    "http://www.tmtpost.com/feed",
    "https://rss.huxiu.com/",
    "http://app.chinaz.com/?app=rss",
    "http://solidot.org/index.rss"
]

# 获取当前时间并转换为 UTC 时间
def get_current_utc_time():
    return datetime.now(pytz.utc)

# 读取或创建 time.txt 文件
def read_or_create_time_file():
    if not os.path.exists("time.txt"):
        with open("time.txt", "w", encoding='utf-8') as f:
            f.write(get_current_utc_time().strftime("%Y-%m-%d %H:%M:%S"))
        return None
    else:
        with open("time.txt", "r", encoding='utf-8') as f:
            time_str = f.read().strip()
            if time_str:
                return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.utc)
            else:
                return None

# 解析日期时间字符串
def parse_date_string(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.utc)
    except ValueError:
        try:
            return datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z").astimezone(pytz.utc)
        except ValueError:
            return None

# 过滤文章
def filter_articles(articles, last_time):
    current_time = get_current_utc_time()
    filtered_articles = []
    for article in articles:
        published_time = parse_date_string(article['published'])
        if published_time is None:
            continue
        if last_time is None:
            if current_time - published_time <= timedelta(hours=24):
                filtered_articles.append(article)
        else:
            if published_time > last_time:
                filtered_articles.append(article)
    return filtered_articles

# 获取文章全文并去掉换行
def get_article_content(article):
    content = article.get('content', [{}])[0].get('value', '')
    return re.sub(r'\s+', ' ', content)

# 检查中文字符比例
def check_chinese_ratio(text):
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
    return len(chinese_chars) / len(text)

# 主函数
def main():
    last_time = read_or_create_time_file()
    all_articles = []

    for url in rss_urls:
        feed = feedparser.parse(url)
        all_articles.extend(feed.entries)

    filtered_articles = filter_articles(all_articles, last_time)

    with open("time.txt", "w", encoding='utf-8') as f:
        f.write(get_current_utc_time().strftime("%Y-%m-%d %H:%M:%S"))

    if not filtered_articles:
        print("无文章更新")
        return

    print(f"过滤后的文章总数: {len(filtered_articles)}")

    for article in filtered_articles:
        content = get_article_content(article)
        summary = summarize(content)
        file_name = datetime.now().strftime("%m%d%H")

        with open(f"{file_name}.txt", "a", encoding='utf-8') as f:
            if check_chinese_ratio(summary) < 0.5:
                translated_summary = translate(summary)
                f.write(translated_summary)
            else:
                f.write(summary)

    print("所有文章总结完成")

if __name__ == "__main__":
    main()