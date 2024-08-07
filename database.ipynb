import pandas as pd
import sqlite3

# CSV 檔案路徑
csv_file_path = 'all_news.csv'

# 讀取 CSV 檔案
df = pd.read_csv(csv_file_path)

# 連接到 SQLite 資料庫（如果資料庫不存在，會自動創建）
conn = sqlite3.connect('news.db')

# 確保資料庫中有正確的表結構
create_table_query = '''
CREATE TABLE IF NOT EXISTS news_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    url TEXT,
    source TEXT,
    date TEXT
)
'''
conn.execute(create_table_query)

# 將 DataFrame 中的資料插入 SQLite
for index, row in df.iterrows():
    title = row['標題']
    url = row['連結']
    source = row['來源']
    date_str = row['時間']  # 保持 CSV 中的時間格式不變

    # 插入資料到 SQLite
    conn.execute('''
        INSERT INTO news_item (title, url, source, date) VALUES (?, ?, ?, ?)
    ''', (title, url, source, date_str))

# 提交變更並關閉連接
conn.commit()
conn.close()

print('CSV 資料已成功儲存到 SQLite 資料庫。')