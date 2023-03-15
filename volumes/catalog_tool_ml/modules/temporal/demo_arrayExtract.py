
# %%

from extract_temporal import extract_temporal_from_data

# %%
# 日付の型が%Y/%m/%dの場合(2020/4/14)
demo_filepath = "http://www.opendata.metro.tokyo.jp/suisyoudataset/132195_event.csv"
demo_column_name = "開始日"
demo_datetime_format ="%Y/%m/%d"
#demo_array = extract_datetime64Array_csv(filepath=demo_filepath, column_name=demo_column_name,input_datetime_format=demo_datetime_format)
extract_temporal_from_data(filepath=demo_filepath, column_name=demo_column_name,input_datetime_format=demo_datetime_format)



#%%
# 日付の型が%Y-%m-%dの場合(2020-04-14)
demo_filepath = "https://www.city.bunkyo.lg.jp/library/opendata-bunkyo/10sonota/01event/131059_event.csv"
demo_column_name = "開始日"
demo_datetime_format ="%Y-%m-%d"
extract_temporal_from_data(filepath=demo_filepath, column_name=demo_column_name,input_datetime_format=demo_datetime_format)

# %%
demo_filepath = "https://stopcovid19.metro.tokyo.lg.jp/data/130001_tokyo_covid19_patients.csv"
demo_column_name = "公表_年月日"
demo_datetime_format ="%Y-%m-%d"
extract_temporal_from_data(filepath=demo_filepath, column_name=demo_column_name,input_datetime_format=demo_datetime_format)


# %%
demo_date,_ = extract_temporal_from_data(filepath=demo_filepath, column_name=demo_column_name,input_datetime_format=demo_datetime_format)

# %%
demo_date.strftime('%Y-%m-%d %H:%M:%S')
# %%
# %%
demo_filepath = "https://stopcovid19.metro.tokyo.lg.jp/data/130001_tokyo_covid19_patients_notexist.csv"
demo_column_name = "公表_年月日"
demo_datetime_format ="%Y-%m-%d"
extract_temporal_from_data(filepath=demo_filepath, column_name=demo_column_name,input_datetime_format=demo_datetime_format)

# %%
