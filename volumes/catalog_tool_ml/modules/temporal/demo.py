#%%
from extract_temporal import extract_temporal_from_textAndData

#%%
# データに日付無し（形式対応外）、テキストに期間あり
# https://www.geospatial.jp/ckan/dataset/092045-013
demo_datasetTitle = "092045_栃木県_佐野市_イベント一覧"
demo_datasetNotes = "イベント一覧のデータです。栃木県佐野市のオープンデータです。"
demo_resourceTitle = "イベント一覧"
demo_resourceNotes = "平成29年度のイベント一覧データのCSVです。"
demo_text = demo_datasetTitle +" " + demo_datasetNotes + " " + demo_resourceTitle + " " + demo_resourceNotes
demo_filepath = "https://www.geospatial.jp/ckan/dataset/609dd2ae-90fd-49c6-8125-aff213a99e9c/resource/333574d2-4698-4f4d-8a59-c51a46c5cbcc/download/109.csv"
demo_column_name = ""
extract_temporal_from_textAndData(text=demo_text,filepath=demo_filepath,column_name=demo_column_name)


# %%
# データに日付あり、テキストに期間なし
# https://catalog.data.metro.tokyo.lg.jp/dataset/t131059d0000000001
demo_datasetTitle = "イベント一覧"
demo_datasetNotes = "文京区のイベント情報一覧です。"
demo_resourceTitle = "イベント一覧"
demo_resourceNotes = "文京区のイベント情報一覧です。"
demo_text = demo_datasetTitle +" " + demo_datasetNotes + " " + demo_resourceTitle + " " + demo_resourceNotes
demo_filepath = "https://www.city.bunkyo.lg.jp/library/opendata-bunkyo/10sonota/01event/131059_event.csv"
demo_column_name = "開始日"

extract_temporal_from_textAndData(text=demo_text,filepath=demo_filepath,column_name=demo_column_name)

# %%
# データに日付あり、テキストに期間あり
# https://catalog.data.metro.tokyo.lg.jp/dataset/t131059d0000000001
demo_datasetTitle = "2018年 イベント一覧"
demo_datasetNotes = "文京区のイベント情報一覧です。"
demo_resourceTitle = "イベント一覧"
demo_resourceNotes = "2018年の文京区のイベント情報一覧です。"
demo_text = demo_datasetTitle +" " + demo_datasetNotes + " " + demo_resourceTitle + " " + demo_resourceNotes
demo_filepath = "https://www.city.bunkyo.lg.jp/library/opendata-bunkyo/10sonota/01event/131059_event.csv"
demo_column_name = "開始日"

extract_temporal_from_textAndData(text=demo_text,filepath=demo_filepath,column_name=demo_column_name)


# %%
