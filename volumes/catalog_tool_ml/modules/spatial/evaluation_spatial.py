
#%%
"""
データセットのタイトル、説明、データの緯度経度から、候補となるgeonames地名を出力する動作デモ
"""
#%%
import extract_spatial
import pandas as pd
#%%
from IPython.display import display
def evaluation(index, title,notes,filepath,method="hybrid"):
    print("==========================================")
    print("index: ",index)
    print("[input information]")
    print("- title: ",title)
    print("- notes: ",notes)
    print("- filepath: ",filepath)
    print("\n")

    print("[Estimation Result]")
    lngArray,latArray = extract_spatial.extract_lnglatArray_csv(filepath=filepath)
    df = extract_spatial.extractSpatialDf(title=title, notes=notes, lngArray=lngArray,latArray=latArray,method=method)
    display(df)
    print("\n")


#%%

df_test = pd.read_csv('evaluation_input.csv', header=0)
#df_test = df_test.tail()
print("[評価で用いる入力データ一覧]")
display(df_test)
print("\n")

for index, row in df_test.iterrows():
    evaluation(index=index,title=row.title,notes=row.notes,filepath=row.filepath,method="hybrid")

