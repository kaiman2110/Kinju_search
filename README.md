# Kinju_search
住宅手当(近住手当)が出る物件を探したい！

## 背景
2024年2月、無事内定(24卒)をいただけたがすぐ家探しをしないとでさぁ大変。  

住むならできるだけ近く(近住手当が出る)て安い物件が望ましいが、  
会社から一定の範囲内の賃貸情報のみ表示するということができない(kaiman調べ)

SUUMOでは囲んだ範囲の物件のみを表示するものがあるが、  
まずはこの条件を満たす物件全体の分布を見てみたい(あまり土地勘もないし)。  

そこで、SUUMOとかに載っている賃貸情報をスクレイピングして  
自分で○km圏内の物件を抽出しちゃえ！というお話

## 目的
会社から○km圏内の賃貸情報を取得する

## 手順
説明と注意事項
### 1.SUUMOから賃貸情報をスクレイピングで取得 [scraping.py](https://github.com/kaiman2110/Kinju_search/blob/main/src/scraping.py)
主に[こちらの記事](https://qiita.com/tomyu/items/a08d3180b7cbe63667c9)を参考にした。  
というかほぼそのままで、後の距離の計算のために住所と建物名を結合した列を新たに作成した。  

urlは、任意の[SUUMOの賃貸](https://suumo.jp/chintai/kanto/)からエリアを選択し、条件検索した際のurlに置き換えて使う。  
このとき、かなり物件の数が多くなるため、市区町村まで絞っておいたほうがいい。  

スクレイピングした結果は/data/rental_information_list.csvに保存される。


### 2.Google Maps Geocoding APIで住所から緯度経度に変換 [address2latlon.py](https://github.com/kaiman2110/Kinju_search/blob/main/src/address2latlon.py)
### 3.会社とそれぞれの住宅との距離を計算 [calc_distance.py](https://github.com/kaiman2110/Kinju_search/blob/main/src/calc_distance.py)
### 4.○km圏内の賃貸情報をMAP上に表示する map.html(現在作成中)

## 参考文献
[SUUMOの物件情報を自動取得（スクレイピング）したのでコードを解説する。](https://qiita.com/tomyu/items/a08d3180b7cbe63667c9)
