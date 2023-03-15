#%%
"""[summary]テキストやデータから対象期間に関する情報を抽出するための関数群を定義する
"""

#%%
import re
import datetime
import calendar
import pandas as pd
from datetime import datetime

#%%
# 正規表現パターン

#年または年度を抽出する正規表現
pattern_gengou_Calyear = r'(明治|大正|昭和|平成|令和)(\d{1,2}|元)年[^(度|\d)]'
pattern_seireki_Calyear = r'(\d{4})年[^(度|\d)]'
pattern_gengou_Fisyear = r'(明治|大正|昭和|平成|令和)(\d{1,2}|元)年度'
pattern_seireki_Fisyear = r'(\d{4})年度'

# 年月を抽出する正規表現
pattern_gengou_Cal_YearMonth = r'(明治|大正|昭和|平成|令和)(\d{1,2}|元)年(\d{1,2})月[^\d]'
pattern_seireki_Cal_YearMonth = r'(\d{4})年(\d{1,2})月[^\d]'

#年月日を抽出する正規表現
pattern_gengou_Cal_YearMonthDay = r'(明治|大正|昭和|平成|令和)(\d{1,2}|元)年(\d{1,2})月(\d{1,2})日'
pattern_seireki_Cal_YearMonthDay = r'(\d{4})年(\d{1,2})月(\d{1,2})日'

#%%
# 関数の定義(文字列から情報抽出)
def transNumber_zenkaku2hankaku(text_include_zenkakuNumber):
    text_include_zenkakuNumber = str(text_include_zenkakuNumber)
    table= str.maketrans({
        "１":"1",
        "２":"2",
        "３":"3",
        "４":"4",
        "５":"5",
        "６":"6",
        "７":"7",
        "８":"8",
        "９":"9",
        "０":"0"
    })
    return text_include_zenkakuNumber.translate(table)


#文字列から和暦の年を抽出して、それに基づいてtemporalを出力する
def extract_temporal_JapaneseYear(text):
    text = transNumber_zenkaku2hankaku(text)

    list_startendTuple = []
    list_JapaneseYear = re.findall(pattern_gengou_Calyear,text)
    for japaneseYear in list_JapaneseYear:
        gengo, gengo_year = japaneseYear
        gengo_year = gengo_year.replace("元","1")
        # print(gengo, gengo_year)
        
        if gengo == "令和":
            seireki_year = int(gengo_year)+ 2019 -1
        elif gengo == "平成":
            seireki_year = int(gengo_year)+ 1989 -1
        elif gengo == "昭和":
            seireki_year = int(gengo_year)+ 1926 -1

        start_date = datetime(seireki_year, 1, 1)
        end_date = datetime(seireki_year,12,31)
        # print(seireki_year,start_date,end_date)
        list_startendTuple.append((start_date,end_date))

    return list_startendTuple


#文字列から西暦の年を抽出して、それに基づいてtemporalを出力する
def extract_temporal_standardYear(text):
    text = transNumber_zenkaku2hankaku(text)

    list_startendTuple = []
    list_standardYear = re.findall(pattern_seireki_Calyear,text)
    for standardYear in list_standardYear:
        # print(standardYear)
        
        seireki_year = int(standardYear)
            
        start_date = datetime(seireki_year, 1, 1)
        end_date = datetime(seireki_year,12,31)
        # print(seireki_year,start_date,end_date)
        list_startendTuple.append((start_date,end_date))
        
    return list_startendTuple


#文字列から和暦の年度を抽出して、それに基づいてtemporalを出力する
def extract_temporal_FisJapaneseYear(text):
    text = transNumber_zenkaku2hankaku(text)

    list_startendTuple = []
    list_JapaneseYear = re.findall(pattern_gengou_Fisyear,text)
    for japaneseYear in list_JapaneseYear:
        gengo, gengo_year = japaneseYear
        gengo_year = gengo_year.replace("元","1")
        # print(gengo, gengo_year)
        
        if gengo == "令和":
            seireki_year = int(gengo_year)+ 2019 -1
        elif gengo == "平成":
            seireki_year = int(gengo_year)+ 1989 -1
        elif gengo == "昭和":
            seireki_year = int(gengo_year)+ 1926 -1

        start_date = datetime(seireki_year, 4, 1)
        end_date = datetime(seireki_year+1,3,31)
        # print(seireki_year,start_date,end_date)
        list_startendTuple.append((start_date,end_date))

    return list_startendTuple


#文字列から西暦の年度を抽出して、それに基づいてtemporalを出力する
def extract_temporal_FisStandardYear(text):
    text = transNumber_zenkaku2hankaku(text)

    list_startendTuple = []
    list_standardYear = re.findall(pattern_seireki_Fisyear,text)
    for standardYear in list_standardYear:
        # print(standardYear)
        
        seireki_year = int(standardYear)
            
        start_date = datetime(seireki_year, 4, 1)
        end_date = datetime(seireki_year+1,3,31)
        # print(seireki_year,start_date,end_date)
        list_startendTuple.append((start_date,end_date))
        
    return list_startendTuple


#文字列から和暦の年月を抽出して、それに基づいてtemporalを出力する
def extract_temporal_JapaneseYearMonth(text):
    text = transNumber_zenkaku2hankaku(text)

    list_startendTuple = []
    list_JapaneseYearMonth = re.findall(pattern_gengou_Cal_YearMonth,text)
    for japaneseYearMonth in list_JapaneseYearMonth:
        gengo, gengo_year,month = japaneseYearMonth
        gengo_year = gengo_year.replace("元","1")
        # print(gengo, gengo_year,month)
        
        if gengo == "令和":
            seireki_year = int(gengo_year)+ 2019 -1
        elif gengo == "平成":
            seireki_year = int(gengo_year)+ 1989 -1
        elif gengo == "昭和":
            seireki_year = int(gengo_year)+ 1926 -1

        month = int(month)

        start_date = datetime(seireki_year, month, 1)
        end_date = datetime(seireki_year,month,int(calendar.monthrange(seireki_year, month)[1]))
        # print(seireki_year,start_date,end_date)
        list_startendTuple.append((start_date,end_date))

    return list_startendTuple


#文字列から西暦の年月を抽出して、それに基づいてtemporalを出力する
def extract_temporal_StandardYearMonth(text):
    text = transNumber_zenkaku2hankaku(text)

    list_startendTuple = []
    list_StandardYearMonth = re.findall(pattern_seireki_Cal_YearMonth,text)
    for standardYearMonth in list_StandardYearMonth:
        year,month = standardYearMonth
        # print(year, month)
        
        seireki_year = int(year)
        month = int(month)
        
        start_date = datetime(seireki_year, month, 1)
        end_date = datetime(seireki_year,month,int(calendar.monthrange(seireki_year, month)[1]))
        # print(seireki_year,start_date,end_date)
        list_startendTuple.append((start_date,end_date))

    return list_startendTuple


#文字列から和暦の年月日を抽出して、それに基づいてtemporalを出力する
def extract_temporal_JapaneseYearMonthDay(text):
    text = transNumber_zenkaku2hankaku(text)

    list_startendTuple = []
    list_JapaneseYearMonthDay = re.findall(pattern_gengou_Cal_YearMonthDay,text)
    for japaneseYearMonthDay in list_JapaneseYearMonthDay:
        gengo, gengo_year,month,day = japaneseYearMonthDay
        gengo_year = gengo_year.replace("元","1")
        # print(gengo, gengo_year,month,day)
        
        if gengo == "令和":
            seireki_year = int(gengo_year)+ 2019 -1
        elif gengo == "平成":
            seireki_year = int(gengo_year)+ 1989 -1
        elif gengo == "昭和":
            seireki_year = int(gengo_year)+ 1926 -1

        month = int(month)
        day = int(day)

        start_date = datetime(seireki_year, month, day)
        end_date = start_date
        # print(seireki_year,start_date,end_date)
        list_startendTuple.append((start_date,end_date))

    return list_startendTuple


#文字列から西暦の年月日を抽出して、それに基づいてtemporalを出力する
def extract_temporal_StandardYearMonthDay(text):
    text = transNumber_zenkaku2hankaku(text)

    list_startendTuple = []
    list_StandardYearMonthDay = re.findall(pattern_seireki_Cal_YearMonthDay,text)
    for standardYearMonthDay in list_StandardYearMonthDay:
        year,month,day = standardYearMonthDay
        # print(year, month,day)
        
        seireki_year = int(year)
        month = int(month)
        day = int(day)
        
        start_date = datetime(seireki_year, month, day)
        end_date = start_date
        
        list_startendTuple.append((start_date,end_date))

    return list_startendTuple


# 文字列からtemporalの候補リストを出力する
def extract_temporal_from_text(text):
    list1 = extract_temporal_JapaneseYear(text)
    list2 = extract_temporal_standardYear(text)
    list3 = extract_temporal_FisJapaneseYear(text)
    list4 = extract_temporal_FisStandardYear(text)
    list5 = extract_temporal_JapaneseYearMonth(text)
    list6 = extract_temporal_StandardYearMonth(text)
    list7 = extract_temporal_JapaneseYearMonthDay(text)
    list8 = extract_temporal_StandardYearMonthDay(text)

    # リストをmerge
    list_merge = list1 + list2 + list3 + list4 + list5 + list6 + list7 + list8
    
    if len(list_merge)==0:
        return (None,None)
    else:
        # startが最新のものを採用する（暫定）
        list_merge = sorted(list_merge,key = lambda x:x[0])
        return list_merge[-1]


#%%
# 関数の定義（データから対象期間を抽出）

def dataframe_read_from_csv(filepath):
    
    filepath = str(filepath)

    try:
        df = pd.read_csv(filepath,encoding='shift_jis')
        return df
    except UnicodeDecodeError:
        try :
            df = pd.read_csv(filepath,encoding='cp932')
            return df
        except UnicodeDecodeError:
            try :
                df = pd.read_csv(filepath,encoding='utf-8')
                return df
            except UnicodeDecodeError:
                print("Error: Error in read_csv")
                return None
    except FileNotFoundError:
        print("Error: File Not Found")
        return None
    except:
        print("Error: Unknown Error")
        return None


def extract_datetime64Array_csv(filepath,column_name,input_datetime_format="auto"):

    # CSVファイルを読み込んでDataframeとして取り込む
    df = dataframe_read_from_csv(filepath=filepath)

    if df is None:
        return []

    if (column_name in df.columns):
        # 日付時刻の列に欠損がある行は削除
        df = df.dropna(subset=[column_name])
        datetime_series = df[column_name]

        # 日付時刻(datetime64型)のnumpy arrayを取得
        if input_datetime_format=="auto":
            try:
                datetime_array = pd.to_datetime(arg=datetime_series,infer_datetime_format=True).values
                
                return datetime_array
            except :
                print("Error: 選択した列のデータを認識できませんでした")
                return []
        else:
            try:
                datetime_array = pd.to_datetime(arg=datetime_series,format=input_datetime_format).values
                
                return datetime_array
            except :
                print("Error: 選択した列のデータを認識できませんでした")
                return []
        
    else:
        print("Error: 指定したcolumn_nameの列が見つかりません")
        return []


def datetime64Array_to_temporal(datetime64Array):
    if len(datetime64Array)==0:
        print("Error: zero length array")
        return (None,None)
    else:
        temporal_start = min(datetime64Array)
        temporal_end = max(datetime64Array)

        temporal_start = temporal_start.astype('datetime64[m]').astype(datetime)
        temporal_end = temporal_end.astype('datetime64[m]').astype(datetime)

        return (temporal_start, temporal_end)


def extract_temporal_from_data(filepath,column_name,input_datetime_format="auto"):
    datetime64Array = extract_datetime64Array_csv(filepath=filepath,column_name=column_name,input_datetime_format=input_datetime_format)
    temporal_start, temporal_end = datetime64Array_to_temporal(datetime64Array)

    return (temporal_start, temporal_end)


#%%
#関数の定義（総合判断）
def extract_temporal_from_textAndData(text, filepath, column_name,input_datetime_format="auto"):
    temporal_start_text, temporal_end_text = extract_temporal_from_text(text)
    temporal_start_data, temporal_end_data = extract_temporal_from_data(filepath=filepath,column_name=column_name,input_datetime_format=input_datetime_format)

    # データがある場合はそれを優先する
    if (temporal_start_data is not None) and (temporal_end_data is not None):
        return (temporal_start_data, temporal_end_data)
    else: # データがない場合は、テキストからの情報を利用する
        if (temporal_start_text is not None) and (temporal_end_text is not None):
            return (temporal_start_text, temporal_end_text)
        else: # 両方ない場合
            return (None, None)