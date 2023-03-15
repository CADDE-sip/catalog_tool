
#%%
"""
データセットのタイトル、説明、データの日付日時から、候補となる期間を出力して評価
"""
#%%
import pandas as pd
from extract_temporal import extract_temporal_from_textAndData

#%%
from IPython.display import display
def evaluation(index, dataset_title,dataset_notes,resource_title, resource_notes, filepath, column_name):
    print("==========================================")
    print("index: ",index)
    print("[input information]")
    print("- dataset title: ",dataset_title)
    print("- dataset notes: ",dataset_notes)
    print("- resource title: ", resource_title)
    print("- resource notes: ", resource_notes)
    print("- filepath: ",filepath)
    print("- column name: ",column_name)
    print("\n")

    print("[Estimation Result]")

    text = str(dataset_title) +" " + str(dataset_notes) + " "+ str(resource_title) + " " + str(resource_notes)
    temp_start,temp_end = extract_temporal_from_textAndData(text=text,filepath=filepath,column_name=column_name)
    print("- temporal_start: ", temp_start)
    print("- temporal_end: ", temp_end)
    print("\n")


#%%

df_test = pd.read_csv('evaluation/evaluation_input.csv', header=0)
#df_test = df_test.tail(2)
print("[評価で用いる入力データ一覧]")
display(df_test)
print("\n")

#%%
for index, row in df_test.iterrows():
    evaluation(index=index,dataset_title=row.dataset_title,dataset_notes=row.dataset_notes,resource_title=row.resource_title, resource_notes=row.resource_notes,filepath=row.filepath,column_name=row.column_name)


# %%
