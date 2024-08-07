import csv
import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
import random
import os

# 打印當前工作目錄
print("當前工作目錄:", os.getcwd())

# 要爬取的關鍵字清單及其英文版
keywords = {
    "大雨": "heavy rain",
    "豪雨": "torrential rain",
    "暴雨": "storm rain",
    "淹水": "flooding",
    "洪水": "flood",
    "水災": "water disaster",
    "颱風": "typhoon",
    "颶風": "hurricane",
    "風災": "wind disaster",
    "海嘯": "tsunami",
    "地震": "earthquake",
    "乾旱": "drought",
    "旱災": "dry disaster"
}

# 要爬取的網站清單
sites = [
    "udn.com",
    "tw.nextapple.com",
    "edition.cnn.com",
    "bbc.co.uk",
    "nhk.or.jp"
]

def search_google(keyword, site, num_results=5, retries=3):
    query = urllib.parse.quote_plus(keyword)
    url = f"https://www.google.com/search?q={query} site:{site} -wikipedia -dictionary -youtube -blogspot -translate"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []

            for item in soup.select('.tF2Cxc')[:num_results]:
                title_elem = item.select_one('h3')
                link_elem = item.select_one('a')
                time_elem = item.select_one('.WG9SHc')

                if title_elem and link_elem:
                    title = title_elem.text
                    link = link_elem['href']
                    timestamp = time_elem.text if time_elem else '無時間'

                    if keyword in title or keyword.lower() in title.lower():
                        results.append((title, link, timestamp))

            return results

        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                wait_time = random.uniform(3,5)
                print(f"HTTP 429 錯誤: {e}. 等待 {wait_time} 秒後重試...")
                time.sleep(wait_time)
            else:
                print(f"HTTP 錯誤: {e}")
                break

    return []

# 使用完整路徑保存文件
output_file = '/Users/kg/Desktop/水利署爬蟲/search_results.csv'

# 確認目標目錄是否存在，如果不存在則創建目錄
output_dir = os.path.dirname(output_file)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 打開 CSV 檔案以寫入模式
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    writer.writerow(['關鍵字', '網站', '標題', '網址', '時間'])

    for keyword, english_keyword in keywords.items():
        for site in sites:
            print(f"搜尋關鍵字: {keyword} (英文: {english_keyword}) 在網站: {site}")

            try:
                for title, link, timestamp in search_google(english_keyword, site):
                    writer.writerow([keyword, site, title, link, timestamp])
                    print(f"標題: {title}")
                    print(f"網址: {link}")
                    print(f"時間: {timestamp}")

                # 在每次請求之間增加隨機的等待時間
                time.sleep(random.uniform(3, 5))

            except requests.exceptions.HTTPError as e:
                print(f"HTTP 錯誤: {e}")

            print("\n" + "-"*40 + "\n")
