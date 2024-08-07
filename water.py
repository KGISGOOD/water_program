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
            'title': title,
            'link': full_link,
            'source': source_name,
            'date': date
        })

    return news_list

def save_to_csv(news_items, filename):
    # 定義CSV檔案的標頭
    headers = ['title', 'link', 'source', 'date']
    
    # 打開CSV檔案並寫入資料
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        
        # 寫入標頭
        writer.writeheader()
        
        # 寫入新聞項目
        for item in news_items:
            writer.writerow(item)

# 使用函數爬取新聞
url = 'https://news.google.com/search?q=%E9%A2%B1%E9%A2%A8%20when%3A30d&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant'
news_items = fetch_news(url)

# 保存新聞到 CSV 檔案
filename = 'water.csv'
save_to_csv(news_items, filename)

print(f"新聞已保存到 {filename}")
