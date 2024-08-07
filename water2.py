'''
利用google news網站進行爬蟲
'''
import csv
import requests
from bs4 import BeautifulSoup

def generate_search_url(keyword):
    base_url = 'https://news.google.com/search?q={}&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant'
    return base_url.format(requests.utils.quote(keyword))

def fetch_news(url, keyword):
    # 發送請求並解析 HTML
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 選擇包含新聞的父元素
    articles = soup.find_all('a', class_='VDXfz')
    
    news_list = []
    
    for article in articles:
        # 提取標題
        title = article.get_text(strip=True)
        
        # 提取鏈接
        link = article.get('href', '').strip()
        
        # 完整的鏈接URL
        full_link = requests.compat.urljoin(url, link)
        
        news_list.append({
            'keyword': keyword,
            'title': title,
            'link': full_link
        })

    return news_list

# 關鍵字列表
keywords = {
    "大雨",https://news.google.com/search?q=%E5%A4%A7%E9%9B%A8%20when%3A30d&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant
    "豪雨",https://news.google.com/search?q=%E8%B1%AA%E9%9B%A8%20when%3A30d&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant
    "暴雨",https://news.google.com/search?q=%E6%9A%B4%E9%9B%A8%20when%3A30d&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant
    "淹水",https://news.google.com/search?q=%E6%B7%B9%E6%B0%B4%20when%3A30d&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant
    "洪水",https://news.google.com/search?q=%E6%B4%AA%E6%B0%B4%20when%3A30d&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant
    "水災",https://news.google.com/search?q=%E6%B0%B4%E7%81%BD%20when%3A30d&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant
    "颱風",https://news.google.com/search?q=%E9%A2%B1%E9%A2%A8%20when%3A30d&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant
    "颶風",https://news.google.com/search?q=%E9%A2%B6%E9%A2%A8%20when%3A30d&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant
    "風災",https://news.google.com/search?q=%E9%A2%A8%E7%81%BD%20when%3A30d&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant
    "海嘯",https://news.google.com/search?q=%E6%B5%B7%E5%98%AF%20when%3A30d&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant
    "地震",https://news.google.com/search?q=%E5%9C%B0%E9%9C%87%20when%3A30d&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant
    "乾旱",https://news.google.com/search?q=%E4%B9%BE%E6%97%B1%20when%3A30d&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant
    "旱災",https://news.google.com/search?q=%E6%97%B1%E7%81%BD%20when%3A30d&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant
}

# 打開 CSV 檔案以寫入模式
with open('water2.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['關鍵字', '標題', '網址'])

    for keyword in keywords:
        search_url = generate_search_url(keyword)
        print(f"正在搜尋關鍵字: {keyword}")
        
        news_items = fetch_news(search_url, keyword)
        
        for item in news_items:
            writer.writerow([item['keyword'], item['title'], item['link']])
            print(f"標題: {item['title']}")
            print(f"url: {item['link']}")
            print()

print("新聞資料已成功保存至 water2.csv")
