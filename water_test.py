import requests
from bs4 import BeautifulSoup

# 目標URL列表
urls = [
    'https://news.google.com/search?q=%E5%9C%8B%E9%9A%9B%E5%A4%A7%E9%9B%A8%20when%3A30d&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant',#國際大雨 when:30d
    'https://news.google.com/search?q=%E5%9C%8B%E9%9A%9B%E8%B1%AA%E9%9B%A8%20when%3A30d&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant',#國際豪雨 when:30d
    'https://news.google.com/search?q=%E5%9C%8B%E9%9A%9B%E6%9A%B4%E9%9B%A8%20when%3A30d&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant',#國際暴雨 when:30d
    'https://news.google.com/search?q=%E5%9C%8B%E9%9A%9B%E6%B7%B9%E6%B0%B4%20when%3A30d&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant',#國際淹水 when:30d
    'https://news.google.com/search?q=%E5%9C%8B%E9%9A%9B%E6%B4%AA%E6%B0%B4%20when%3A30d&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant',#國際洪水 when:30d
    'https://news.google.com/search?q=%E5%9C%8B%E9%9A%9B%E6%B0%B4%E7%81%BD%20when%3A30d&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant',#國際水災 when:30d
    'https://news.google.com/search?q=%E5%9C%8B%E9%9A%9B%E9%A2%B1%E9%A2%A8%20when%3A30d&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant',#國際颱風 when:30d
    'https://news.google.com/search?q=%E5%9C%8B%E9%9A%9B%E9%A2%B6%E9%A2%A8%20when%3A30d&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant',#國際颶風 when:30d
    'https://news.google.com/search?q=%E5%9C%8B%E9%9A%9B%E9%A2%A8%E7%81%BD%20when%3A30d&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant',#國際風災 when:30d
    'https://news.google.com/search?q=%E5%9C%8B%E9%9A%9B%E6%B5%B7%E5%98%AF%20when%3A30d&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant',#國際海嘯 when:30d
    'https://news.google.com/search?q=%E5%9C%8B%E9%9A%9B%E5%9C%B0%E9%9C%87%20when%3A30d&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant',#國際地震 when:30d
    'https://news.google.com/search?q=%E5%9C%8B%E9%9A%9B%E4%B9%BE%E6%97%B1%20when%3A30d&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant',#國際乾旱 when:30d
    'https://news.google.com/search?q=%E5%9C%8B%E9%9A%9B%E6%97%B1%E7%81%BD%20when%3A30d&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant'#國際旱災 when:30d
]

def fetch_news(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 根據Google新聞的結構來提取新聞標題、連結、來源和時間
    articles = []
    for item in soup.select('article'):
        title_element = item.find('a')
        if title_element:
            title = title_element.get_text(strip=True)
            full_link = 'https://news.google.com' + title_element['href'][1:]
            source_element = item.find('div', class_='SVJrMe')
            source_name = source_element.get_text(strip=True) if source_element else "Unknown"
            date_element = item.find('time')
            date = date_element['datetime'] if date_element else "Unknown"
            articles.append({
                '標題': title,
                '連結': full_link,
                '來源': source_name,
                '時間': date,
                '內文': ''  # 內文將在下一步中爬取
            })
    return articles

def fetch_article_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 假設內文位於<div class="article-body">內，這裡根據目標網站調整
    content_element = soup.find('div', class_='article-body')  
    content = content_element.get_text(strip=True) if content_element else None
    return content

# 爬取新聞標題、連結、來源和時間
all_articles = []
for url in urls:
    articles = fetch_news(url)
    all_articles.extend(articles)

# 針對每篇文章，爬取內文並更新結果
for article in all_articles:
    content = fetch_article_content(article['連結'])
    if content:  # 只有成功爬取到內文時才更新
        article['內文'] = content

# 輸出結果
for article in all_articles:
    if article['內文']:  # 只輸出成功爬取內文的文章
        print(f"標題: {article['標題']}")
        print(f"連結: {article['連結']}")
        print(f"來源: {article['來源']}")
        print(f"時間: {article['時間']}")
        print(f"內文: {article['內文']}\n")
