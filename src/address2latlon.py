# 住所を緯度経度情報に変換する
import googlemaps
import pandas as pd
from tqdm import tqdm
import time
from retry import retry


df = pd.read_csv("./data/rental_information_list.csv", index_col=[0])
# print(df.head())


@retry(tries=3, delay=10, backoff=2)
def translate_address_coordinates(address):
  gm = googlemaps.Client(key='YourAPIKey')
  res = gm.geocode(address)
  #print("res:", res)
  return res[0]['geometry']['location']


# 住所のuniqueから緯度経度を取得
all_addresses = {}
full_addresses = df['住所と建物名'].unique()

# 住所のユニークごとに処理を行う
for address in tqdm(full_addresses):
    # 住所から緯度経度を取得
    coordinate = translate_address_coordinates(address)
    all_addresses[address] = coordinate
    # 1アクセスごとに1秒休む
    time.sleep(1)


coordinates = pd.DataFrame(all_addresses).T
coordinates.reset_index(inplace=True)
coordinates.rename(columns={
    'index':'住所と建物名',
    0:'経度',
    1:'緯度'
}, inplace=True)

df_lon_lat = pd.merge(df, coordinates, on='住所と建物名', how='left')
print(df_lon_lat.head())
df_lon_lat.to_csv("./data/latitude_longitude.csv")

