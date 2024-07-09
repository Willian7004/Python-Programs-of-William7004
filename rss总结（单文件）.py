import feedparser
import os
import time
from datetime import datetime, timedelta, timezone
import re
#本程序使用Deepseek Coder v2辅助制作，发布时合成一个文件。对话记录在对应的txt文件中。
from langchain_community.llms import Ollama
ollama = Ollama(base_url='http://localhost:11434',
model="gemma-2-9b-chinese:latest") #这里更换为已安装的模型

def summarize(text):
    text="总结以下文章："+text
    print(ollama(text))

# RSS 链接列表。这里只保留两个示例
rss_urls = [
    "http://www.geekpark.net/rss",
    "https://www.oschina.net/news/rss"
]

def get_articles(rss_urls):
    articles = []
    for url in rss_urls:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            articles.append({
                'title': entry.title,
                'published': entry.published,
                'summary': entry.summary,
                'link': entry.link
            })
    return articles

def read_time_from_file():
    if os.path.exists('time.txt'):
        with open('time.txt', 'r') as file:
            time_str = file.read().strip()
            if time_str:
                return datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    return None

def write_time_to_file():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('time.txt', 'w') as file:
        file.write(current_time)

def filter_articles(articles, last_time):
    current_time = datetime.now(timezone.utc)
    filtered_articles = []
    for article in articles:
        try:
            published_time = datetime.strptime(article['published'], '%a, %d %b %Y %H:%M:%S %z').astimezone(timezone.utc)
        except ValueError:
            continue
        if last_time:
            if published_time > last_time.astimezone(timezone.utc):
                filtered_articles.append(article)
        else:
            if current_time - published_time < timedelta(hours=24):
                filtered_articles.append(article)
    return filtered_articles

def get_article_content(article):
    # 这里假设 summary 就是全文，如果需要获取全文，可以使用 article['link'] 进行网络请求
    return re.sub(r'\s+', ' ', article['summary'])

def get_max_numeric_file():
    numeric_files = [f for f in os.listdir('.') if re.match(r'^\d+\.txt$', f)]
    if not numeric_files:
        return None
    max_file = max(numeric_files, key=lambda x: int(x.split('.')[0]))
    return max_file

def write_summary_to_file(summary):
    max_file = get_max_numeric_file()
    if max_file:
        with open(max_file, 'r') as file:
            if len(file.read()) < 1000:
                with open(max_file, 'a') as file:
                    file.write(str(summary))
                return
    timestamp = int(time.time())
    with open(f'{timestamp}.txt', 'w') as file:
        file.write(str(summary))

def main():
    articles = get_articles(rss_urls)
    last_time = read_time_from_file()
    filtered_articles = filter_articles(articles, last_time)
    write_time_to_file()

    if not filtered_articles:
        print("无文章更新")
        return

    print(f"过滤后的文章总数: {len(filtered_articles)}")

    for article in filtered_articles:
        content = get_article_content(article)
        summary = summarize(content)
        write_summary_to_file(summary)

    print("所有文章总结完成")

if __name__ == "__main__":
    main()