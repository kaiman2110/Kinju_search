import requests
from bs4 import BeautifulSoup
from retry import retry
import urllib
import time
from tqdm import tqdm
import numpy as np
import pandas as pd


# リクエストがうまくいかない場合を回避するためのやり直し
@retry(tries=3, delay=10, backoff=2)
def load_page(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    return soup


# 複数ページの住宅情報をまとめて取得
housing_data_samples = []
# スクレイピングする最大ページ数
max_page = 8
# SUUMOで港区を指定して検索した際のurl
url = 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13103&cb=0.0&ct=8.0&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2='
# ページ数フォーマットを付与
url += '&page={}'

# ページごとの処理
for page in tqdm(range(1, max_page+1)):
    # ページ情報
    soup = load_page(url.format(page))
    # 物件情報リストを指定
    mother = soup.find_all(class_='cassetteitem')
    
    # 物件ごとの処理
    for child in mother:

        # 建物情報
        data_home = []
        # カテゴリ
        data_home.append(child.find(class_='ui-pct ui-pct--util1').text)
        # 住所
        address = child.find(class_='cassetteitem_detail-col1').text
        data_home.append(address)
        # 建物名
        building_name = child.find(class_='cassetteitem_content-title').text
        data_home.append(building_name)
        
        # 住所と建物名
        data_home.append(address + building_name)
        # 最寄り駅のアクセス
        children = child.find(class_='cassetteitem_detail-col2')
        for id, grandchild in enumerate(children.find_all(class_='cassetteitem_detail-text')):
            data_home.append(grandchild.text)
        # 築年数と階数
        children = child.find(class_='cassetteitem_detail-col3')
        for grandchild in children.find_all('div'):
            data_home.append(grandchild.text)

        # 部屋情報
        rooms = child.find(class_='cassetteitem_other')
        for room in rooms.find_all(class_='js-cassette_link'):
            data_room = []
            
            # 部屋情報が入っている表を探索
            for id_, grandchild in enumerate(room.find_all('td')):
                # 階
                if id_ == 2:
                    data_room.append(grandchild.text.strip())
                # 家賃と管理費
                elif id_ == 3:
                    data_room.append(grandchild.find(class_='cassetteitem_other-emphasis ui-text--bold').text)
                    data_room.append(grandchild.find(class_='cassetteitem_price cassetteitem_price--administration').text)
                # 敷金と礼金
                elif id_ == 4:
                    data_room.append(grandchild.find(class_='cassetteitem_price cassetteitem_price--deposit').text)
                    data_room.append(grandchild.find(class_='cassetteitem_price cassetteitem_price--gratuity').text)
                # 間取りと面積
                elif id_ == 5:
                    data_room.append(grandchild.find(class_='cassetteitem_madori').text)
                    data_room.append(grandchild.find(class_='cassetteitem_menseki').text)
                # url
                elif id_ == 8:
                    get_url = grandchild.find(class_='js-cassette_link_href cassetteitem_other-linktext').get('href')
                    abs_url = urllib.parse.urljoin(url, get_url)
                    data_room.append(abs_url)
            # 物件情報と部屋情報をくっつける
            housing_data_sample = data_home + data_room
            housing_data_samples.append(housing_data_sample)
    
    # 1アクセスごとに1秒休む
    time.sleep(1)

df = pd.DataFrame(housing_data_samples)
df.columns = ['カテゴリ', '住所', '建物名', '住所と建物名', '最寄駅へのアクセス1', '最寄駅へのアクセス2', '最寄駅へのアクセス3', '築年数', '階建て', '階', '賃料', '管理費', '敷金', '礼金', '間取り', '面積', 'url']
print(df.head())
df.to_csv('./data/rental_information_list.csv')