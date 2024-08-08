import requests
from bs4 import BeautifulSoup
import csv

def fetch_news(url):
    # 發送請求並解析 HTML
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 選擇包含新聞的元素
    articles = soup.find_all('article', class_='IFHyqb')

    # 提取標題、鏈接和時間
    news_list = []
    for article in articles:
        title_element = article.find('a', class_='JtKRv')
        title = title_element.get_text(strip=True) if title_element else '未知'
        link = title_element.get('href', '').strip() if title_element else ''
        full_link = requests.compat.urljoin(url, link)

        # 獲取新聞來源
        news_source = article.find('div', class_='vr1PYe')
        source_name = news_source.get_text(strip=True) if news_source else '未知'
        
        # 獲取新聞時間
        time_element = article.find('div', class_='UOVeFe').find('time', class_='hvbAAd') if article.find('div', class_='UOVeFe') else None
        date = time_element.get_text(strip=True) if time_element else '未知'
        
        news_list.append({
            '標題': title,
            '連結': full_link,
            '來源': source_name,
            '時間': date
        })

    return news_list

def save_to_csv(news_items, filename):
    # 定義CSV檔案的標頭
    headers = ['標題', '連結', '來源', '時間']
    
    # 打開CSV檔案並寫入資料
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        
        # 寫入標頭
        writer.writeheader()
        
        # 寫入新聞項目
        for item in news_items:
            writer.writerow(item)

# 多個網址
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

# 爬取所有網址的新聞
all_news_items = []
for url in urls:
    news_items = fetch_news(url)
    all_news_items.extend(news_items)

# 保存所有新聞到 CSV 檔案
filename = 'all_news.csv'
save_to_csv(all_news_items, filename)

print(f"所有新聞已保存到 {filename}")
