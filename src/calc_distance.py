from geopy.distance import geodesic
import pandas as pd

# dfで読み込む
df = pd.read_csv("./data/latitude_longitude.csv", index_col=[0])

# lambdaで一括計算
location = (35.658581, 139.745433)  # 基準となる建物(会社)の緯度経度
df["distance"] = df.apply(lambda x:geodesic((x["lat"], x["lng"]), location), axis=1)
df.to_csv("./data/distance.csv")
print(df.head())

# 範囲内の住宅のみ抽出
df = df[df["distance"] < 2]
df.to_csv("./data/housing_within_range.csv")
