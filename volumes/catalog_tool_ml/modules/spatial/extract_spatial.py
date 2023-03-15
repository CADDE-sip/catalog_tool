#%%
"""
データまたはデータカタログのタイトル・説明文から地理空間情報の
geonamesの候補を推定するための関数群を定義
"""

#%%
# Modules
import requests
import json
import pandas as pd

# 独自モジュール
#import pick_locationname
from modules.spatial import pick_locationname


# %%
# 各種パラメータの設定
GEONAME_USER_KEY = 'jsugawa'
GEONAME_MAXROWS = 10
GEONAME_LANG = 'ja'
GEONAME_COUNTRY = 'JP'
GEONAME_FEATURECLASS = [] # クエリ結果をfeature classで制限しない
# GEONAME_FEATURECLASS = ['A','P']
GEONAME_KEYWORDSEARCH_URL = 'http://api.geonames.org/searchJSON'
GEONAME_KEYWORDSEARCH_STYLE = 'FULL'
GEONAME_GETFEATURE_URL = 'http://api.geonames.org/getJSON'
GEONAME_HIERARCHY_URL = 'http://api.geonames.org/hierarchyJSON'
GEONAME_FINDNEARBY_URL = 'http://api.geonames.org/findNearbyJSON'
GEONAME_FINDNEARBY_RADIUS = 20
GEONAME_SELECTKEYWORDS = 3


# %%
# 関数の定義

def extract_LocationKeywords_old(text):
    keyword_lg_list = pick_locationname.included_localgovs(text)
    keyword_pf_list = pick_locationname.included_prefectures(text)

    if len(keyword_lg_list) > 0:
        keyword_list = keyword_lg_list
    elif len(keyword_pf_list) > 0:
        keyword_list = keyword_pf_list
    else:
        keyword_list = []
    
    return keyword_list


def extract_LocationKeywords(text,mode="nonDuplicatedList"):
    return pick_locationname.included_geonameLocation(text=text,mode=mode)


def select_LocationKeywords(list_location):
        """[入力されたキーワードを選別して出力する。現状は先頭の複数のキーワードを出力]
        
        Arguments:
            list_location {[list]} -- [元の地名キーワードのリスト]
        
        Returns:
            [list] -- [選別された地名キーワードのリスト]
        """
        list_selected_location = list_location[:GEONAME_SELECTKEYWORDS]
        
        return list_selected_location


def extract_lnglatArray_csv(filepath):
    """[summary]緯度や経度の列があるCSVファイルから緯度経度のデータ列を取得する

    Args:
        filepath ([str]): [CSVファイルのパス。URLでもよい]]

    Returns:
        [tuple]: [経度のArray、緯度のArrayのtuple]
    """

    # CSVファイルをDataframeとして読み込む
    filepath = str(filepath)

    try:
        df = pd.read_csv(filepath,encoding='shift_jis')
    except UnicodeDecodeError:
        try :
            df = pd.read_csv(filepath,encoding='cp932')
        except UnicodeDecodeError:
            try :
                df = pd.read_csv(filepath,encoding='utf-8')
            except UnicodeDecodeError:
                print("Error in read_csv")
                return ([],[])
    except FileNotFoundError:
        print("File Not Found")
        return ([],[])

    if ('緯度' in df.columns) and ('経度' in df.columns):
        # 緯度または経度に欠損がある行は削除
        df = df.dropna(subset=['緯度', '経度'])
        # 緯度、経度のnumpy arrayを取得
        lat_array = df['緯度'].values
        lng_array = df['経度'].values

        return lng_array,lat_array
    elif ('latitude' in df.columns) and ('longitude' in df.columns):
        # 緯度または経度に欠損がある行は削除
        df = df.dropna(subset=['latitude', 'longitude'])
        # 緯度、経度のnumpy arrayを取得
        lat_array = df['latitude'].values
        lng_array = df['longitude'].values

        return lng_array,lat_array
    elif ('lat' in df.columns) and ('lng' in df.columns):

        # 緯度または経度に欠損がある行は削除
        df = df.dropna(subset=['lat', 'lng'])
        # 緯度、経度のnumpy arrayを取得
        lat_array = df['lat'].values
        lng_array = df['lng'].values

        return lng_array,lat_array
    else:
        print("Error: 緯度、経度の列がありません")
        return ([],[])


def FindByKeyword_name(
    locationKeyword, 
    key=GEONAME_USER_KEY,
    maxRows=GEONAME_MAXROWS,
    featureClass=[],
    lang=GEONAME_LANG,
    country=GEONAME_COUNTRY,
    style=GEONAME_KEYWORDSEARCH_STYLE):
    """[summary]地名キーワードを指定してname属性を対象に検索し、候補となるgeonameを表すdictionaryのリストを出力

    Args:
        locationKeyword ([str]): [地名キーワードの文字列。地名キーワードは一つ]
        key ([str], optional): [geoname Web APIのAPI key]. Defaults to GEONAME_USER_KEY.
        maxRows ([int], optional): [出力する候補の上限]. Defaults to GEONAME_MAXROWS.
        featureClass (list, optional): [地名の属性("P"や"A"等)のみ出力候補に出す際につかう]. Defaults to [].
        lang ([str], optional): [geoname検索で用いる言語]. Defaults to GEONAME_LANG.
        country ([str], optional): [geoname検索対象とする国]. Defaults to GEONAME_COUNTRY.
        style ([type], optional): [出力の形式]. Defaults to GEONAME_KEYWORDSEARCH_STYLE.

    Returns:
        [list]: [geonameを表すdictionaryのリスト]
    """

    params ={
    'name':locationKeyword,
    'username':key,
    'maxRows':maxRows,
    'featureClass':featureClass,
    'lang':lang,
    'country':country,
    'style':style
    }

    r = requests.get(
        url=GEONAME_KEYWORDSEARCH_URL,
        params=params
        )

    #print('request query: ',r.url)
    #print('status code: ', r.status_code)

    result_dict = json.loads(r.text)
    return result_dict['geonames']


def getFeautures(geonameId, key=GEONAME_USER_KEY, lang=GEONAME_LANG):
    """[summary]geoname idから属性を調べる関数。指定したgeonameIdの地名の属性値を辞書形式で出力する。

    Args:
        geonameId ([int]): [geonameのID]
        key ([str], optional): [geoname Web APIのAPI key]. Defaults to GEONAME_USER_KEY.
        lang ([str], optional): [geoname検索で用いる言語]. Defaults to GEONAME_LANG.

    Returns:
        [dict]: [geonameの属性情報を含む辞書形式データ]
    """

    params ={
        'geonameId':geonameId,
        'username':key,
        'lang':lang,
    }

    r = requests.get(
        url=GEONAME_GETFEATURE_URL,
        params=params
        )

    #print('request query: ',r.url)
    #print('status code: ', r.status_code)

    result_dict = json.loads(r.text)
    return result_dict


# geonameIdからHierarchy(上位の地名)を調べる関数を定義
def getHierarchyList(geonameId, key=GEONAME_USER_KEY, lang=GEONAME_LANG):
    """[summary]geonameIdからHierarchy(上位の地名)を調べる関数。指定したgeonameIdのHierarchy(上位の地名)の一覧をリストで出力する。

    Args:
        geonameId ([int]): [geonameのID]
        key ([str], optional): [geoname Web APIのAPI key]. Defaults to GEONAME_USER_KEY.
        lang ([str], optional): [geoname検索で用いる言語]. Defaults to GEONAME_LANG.

    Returns:
        [list]: [上位の地名のリスト]
    """

    params ={
        'geonameId':geonameId,
        'username':key,
        'lang':lang,
    }

    r = requests.get(
        url=GEONAME_HIERARCHY_URL,
        params=params
        )

    #print('request query: ',r.url)
    #print('status code: ', r.status_code)

    result_dict = json.loads(r.text)
    # return result_dict['geonames']

    list_hierarychy=[]
    for elem in result_dict['geonames']:
        list_hierarychy.append(elem['name'])

    return list_hierarychy


# を定義
def getFullname(geonameId, key=GEONAME_USER_KEY, lang=GEONAME_LANG, mode='Country'):
    """[summary]geonameIdから上位の地名を含むFullnameを出力する関数.
    指定したgeonameIdのFullname(例: 日本>千葉県>千葉市>中央区)を出力する。

    Args:
        geonameId ([int]): [geonameのID]
        key ([str], optional): [geoname Web APIのAPI key]. Defaults to GEONAME_USER_KEY.
        lang ([str], optional): [geoname検索で用いる言語]. Defaults to GEONAME_LANG.
        mode (str, optional): [出力形式のモード。最上位をどこにするかを指定]. Defaults to 'Country'.

    Returns:
        [str]: [上位の地名を含むFullname]
    """
    list = getHierarchyList(geonameId)

    if mode == 'Continent': # 例 アジア>日本>千葉県>千葉市>中央区
        return '>'.join(list[1:])
    elif mode == 'Country': # 例 日本>千葉県>千葉市>中央区
        return '>'.join(list[2:])
    elif mode == 'Prefecture': # 例 千葉県>千葉市>中央区
        return '>'.join(list[3:])
    elif mode == 'Full': # 例 Earth>アジア>日本>千葉県>千葉市>中央区
        return '>'.join(list[0:])
    else:
        return '>'.join(list)


def FindbyBbox(
    east, west, north, south,
    name="",
    key=GEONAME_USER_KEY,
    maxRows=GEONAME_MAXROWS,
    featureClass=GEONAME_FEATURECLASS,
    lang=GEONAME_LANG,
    country=GEONAME_COUNTRY,
    style=GEONAME_KEYWORDSEARCH_STYLE):
    """[summary]緯度経度のBoundingBox範囲を指定して、その中にある地名を検索する関数。

    Args:
        east ([float]): [BoundingBoxのeastの値]
        west ([float]): [BoundingBoxのwestの値]
        north ([float]): [BoundingBoxのnorthの値]
        south ([float]): [BoundingBoxのsouthの値]
        name (str, optional): [地名のキーワード]. Defaults to "".
        key ([str], optional): [geoname Web APIのAPI key]. Defaults to GEONAME_USER_KEY.
        maxRows ([int], optional): [出力する候補の上限]. Defaults to GEONAME_MAXROWS.
        featureClass ([list], optional): [地名の属性("P"や"A"等)のみ出力候補に出す際につかう]. Defaults to GEONAME_FEATURECLASS.
        lang ([str], optional): [geoname検索で用いる言語]. Defaults to GEONAME_LANG.
        country ([str], optional): [geoname検索対象とする国]. Defaults to GEONAME_COUNTRY.
        style ([str], optional): [出力の形式]. Defaults to GEONAME_KEYWORDSEARCH_STYLE.

    Returns:
        [list]: [geonameを表すdictionaryのリスト]
    """

    params ={
    'name':name,
    'username':key,
    'maxRows':maxRows,
    'featureClass':featureClass,
    'lang':lang,
    'country':country,
    'style':style,
    'east':east,
    'west':west,
    'north':north,
    'south':south,
    }

    r = requests.get(
        url=GEONAME_KEYWORDSEARCH_URL,
        params=params
        )

    #print('request query: ',r.url)
    #print('status code: ', r.status_code)

    result_dict = json.loads(r.text)
    try:
        return result_dict['geonames']
    except:
        print("geonames query result has an error:")
        print(result_dict)
        return []


def FindNearby(
    lng,lat, 
    key=GEONAME_USER_KEY, 
    radius=GEONAME_FINDNEARBY_RADIUS, 
    maxRows=GEONAME_MAXROWS, 
    featureClass=GEONAME_FEATURECLASS,
    lang=GEONAME_LANG, 
    country=GEONAME_COUNTRY,
    style=GEONAME_KEYWORDSEARCH_STYLE
    ):
    """[summary]指定した地点の近くの地名を検索する関数。指定した緯度、経度の近くの地名をリスト形式で出力する

    Args:
        lng ([float]): [経度の値]
        lat ([float]): [緯度の値]
        key ([str], optional): [geoname Web APIのAPI key]. Defaults to GEONAME_USER_KEY.
        radius ([int], optional): [検索対象の範囲を表す半径(km)]. Defaults to GEONAME_FINDNEARBY_RADIUS.
        maxRows ([int], optional): [出力する候補の上限]. Defaults to GEONAME_MAXROWS.
        featureClass ([list], optional): [地名の属性("P"や"A"等)のみ出力候補に出す際につかう]. Defaults to GEONAME_FEATURECLASS.
        lang ([str], optional): [geoname検索で用いる言語]. Defaults to GEONAME_LANG.
        country ([str], optional): [geoname検索対象とする国]. Defaults to GEONAME_COUNTRY.
        style ([str], optional): [出力の形式]. Defaults to GEONAME_KEYWORDSEARCH_STYLE.

    Returns:
        [list]: [geonameを表すdictionaryのリスト]
    """

    params ={
        'lng':lng,
        'lat':lat,
        'username':key,
        'radius':radius,
        'maxRows':maxRows,
        'featureClass':featureClass,
        'lang':lang,
        'country':country,
        'style':style,
    }

    r = requests.get(
        url=GEONAME_FINDNEARBY_URL,
        params=params
        )

    # print('request query: ',r.url)
    # print('status code: ', r.status_code)

    result_dict = json.loads(r.text)
    return result_dict['geonames']


def datasetText2spatialDf(title, notes,style="full"):
    """[summary]タイトルと説明からgeoname情報のdataframeを出力する

    Args:
        title ([str]): データセットのタイトル
        notes ([str]): データセットの説明
        style (str, optional):geonamesのクエリ方法. Defaults to "full".

    Returns:
        [dataframe]: [geonameクエリ結果をdataframe形式にしたデータ]
    """

    # タイトルと説明のテキストから地名キーワードを抽出
    textAll = title + " " + notes 
    keywords_dict = dict(extract_LocationKeywords(textAll,mode="Counter"))
    
    # 地名キーワードごとにgeonamesでクエリ
    result_dict={}
    for keyword in keywords_dict.keys():
        result_dict[keyword] = FindByKeyword_name(keyword,style=style)

    # 地名キーワード毎にデータフレームにして、検索方法、キーワードとその頻度を列に追加
    list_df = []
    for key,value in result_dict.items():
        df = pd.DataFrame(value)
        df["searchMethod"]="keyword"
        df["searchKeyword"] = key
        df["searchKeywordCount"] = keywords_dict[key]
        list_df.append(df)

    # 地名キーワード毎のデータフレームを結合
    df_all = pd.concat(list_df)

    return df_all


def lnglatArray2spatialDf(lngArray,latArray,style="full"):
    """緯度のArray及び経度のArrayからそのBBoxにある地名のgeoname情報のdataframeを出力する

    Args:
        lngArray ([np.array]]): 経度のArray
        latArray ([np.array]): [緯度のArray]
        style (str, optional): [geonamesのクエリ方法]. Defaults to "full".

    Returns:
        [dataframe]]: [geonameクエリ結果をdataframe形式にしたデータ]
    """
    if len(lngArray)==len(latArray) and len(lngArray)!=0 and len(latArray)!=0:
        # Bboxを計算
        east = max(lngArray)
        west = min(lngArray)
        north = max(latArray)
        south = min(latArray)

        # Bboxでgeonamesにクエリ
        result_list = FindbyBbox(east=east,west=west,north=north,south=south,style=style)
    
        # クエリ結果をDataframeにして検索方法の列を追加して出力
        df = pd.DataFrame(result_list)
        df["searchMethod"]="Bbox"

        return df
    else:
        print("Error: input format error in lngArray,latArray")
        return None


def correctFreq(row):
    if row['searchKeywordCount'] > 1.0:
        return row['freqAppearance'] + int(row['searchKeywordCount']) -1
    else:
        return row['freqAppearance']


def mergeSortDataframe(dataframe_keywordResult,dataframe_BboxResult,sortMode="hybrid"):
    """[summary]キーワードで検索したgeonameクエリ結果とBboxで検索したgeonameクエリ結果をマージ及びソート

    Args:
        dataframe_keywordResult ([dataframe]): [キーワードで検索したgeonameクエリ結果]
        dataframe_BboxResult ([dataframe]): [Bboxで検索したgeonameクエリ結果]
        sortMode (str, optional): [ソート方法]. Defaults to "hybrid".

    Returns:
        [dataframe]: [マージ及びソートされたgeonameクエリ結果]]
    """
    df_keywordResult=dataframe_keywordResult.copy()
    df_BboxResult=dataframe_BboxResult.copy()

    # 2種のクエリ結果を結合
    df_AllResult = pd.concat([df_keywordResult,df_BboxResult])
    df_AllResult = df_AllResult.fillna({'searchKeywordCount': 0})
    df_AllResult = df_AllResult[["geonameId","name","fcl","lat","lng","adminName1","adminName2","score","searchMethod","searchKeyword","searchKeywordCount"]]

    if sortMode=="hybrid":
        # 重複する行を計算
        freqDict = df_AllResult["geonameId"].value_counts().to_dict()
        
        # 登場頻度の列を追加
        df_AllResult["freqAppearance"] = df_AllResult["geonameId"].map(freqDict)
        df_AllResult["freqAppearance"] = df_AllResult.apply(correctFreq, axis=1)

        # 両方の方法でヒットしたgeonameIdのsearchMethodを置換
        duplicated_geonameId_list = [key for key in freqDict.keys()]
        dict_geoname_bothMethodIncluded={}
        for geonameId in duplicated_geonameId_list:
            method_included =set(df_AllResult[df_AllResult["geonameId"]==geonameId]["searchMethod"].values)
            if "keyword" in method_included and "Bbox" in method_included:
                dict_geoname_bothMethodIncluded[geonameId] = "keyword&Bbox"
            elif "keyword" in method_included:
                dict_geoname_bothMethodIncluded[geonameId] = "keyword"
            elif "Bbox" in method_included:
                dict_geoname_bothMethodIncluded[geonameId] = "Bbox"
            else:
                dict_geoname_bothMethodIncluded[geonameId] = "unknown"

        df_AllResult["searchMethod"] = df_AllResult["geonameId"].map(dict_geoname_bothMethodIncluded)

        # 並べ替え（頻度、検索方法、スコアで）
        df_AllResult = df_AllResult.sort_values(['freqAppearance', 'searchMethod','score'], ascending=[False, False,False])
        
        # 重複する行を削除
        df_AllResult = df_AllResult.drop_duplicates(subset="geonameId",keep="first")

        df_AllResult = df_AllResult.reset_index(drop=True)
    
    elif sortMode=="keywordFirst":
        # 並べ替え（検索方法(キーワードを先)、スコアで）
        df_AllResult = df_AllResult.sort_values(['searchMethod','searchKeywordCount','score'], ascending=[False,False,False])
        df_AllResult = df_AllResult.drop_duplicates(subset="geonameId",keep="first")
        df_AllResult = df_AllResult.reset_index(drop=True)
    
    elif sortMode=="BboxFirst":
        # 並べ替え（検索方法(キーワードを後)、スコアで）
        df_AllResult = df_AllResult.sort_values(['searchMethod','searchKeywordCount','score'], ascending=[True,False,False])
        df_AllResult = df_AllResult.drop_duplicates(subset="geonameId",keep="first")
        df_AllResult=df_AllResult.reset_index(drop=True)

    else:
        pass

    return df_AllResult


def lnglatArrayWithName2spatialDf(lngArray,latArray,title,notes,style="full"):
    """[summary]緯度のArray及び経度のArray及びデータセットのタイトル・説明から該当する候補を出力する。
    キーワードにヒットし、かつ、そのBBoxにある地名のgeoname情報のdataframeを出力する

    Args:
        lngArray ([np.array]): [経度のarray]
        latArray ([np.array]): [緯度のarray]
        title ([str]): [データセットのタイトル]
        notes ([str]): [データセットの説明]
        style (str, optional): [description]. Defaults to "full".

    Returns:
        [datframe]: [地名のgeoname情報のdataframe]
    """

    title = str(title)
    notes = str(notes)
    allText = title + " " + notes
    if len(lngArray)==len(latArray) and len(lngArray)!=0 and len(latArray)!=0:
        # Bboxを計算
        east = max(lngArray)
        west = min(lngArray)
        north = max(latArray)
        south = min(latArray)

        keywords_dict = dict(extract_LocationKeywords(allText,mode="Counter"))
    
        # 地名キーワードごとにgeonamesでクエリ(BBox内に制限)
        result_dict={}
        for keyword in keywords_dict.keys():
            result_dict[keyword] = FindbyBbox(east=east,west=west,north=north,south=south,name=keyword,style=style)

        # 地名キーワード毎にデータフレームにして、検索方法、キーワードとその頻度を列に追加
        list_df = []
        for key,value in result_dict.items():
            df = pd.DataFrame(value)
            df["searchMethod"]="keyword&Bbox"
            df["searchKeyword"] = key
            df["searchKeywordCount"] = keywords_dict[key]
            list_df.append(df)
        
        df_AllResult = pd.concat(list_df)

        # 並べ替え（キーワード頻度、スコアで）
        df_AllResult = df_AllResult.sort_values(['searchKeywordCount','score'], ascending=[False, False])
        # 重複排除
        df_AllResult = df_AllResult.drop_duplicates(subset="geonameId",keep="first")
        df_AllResult = df_AllResult.reset_index(drop=True)

        # 必要な列のみ残す
        df_AllResult = df_AllResult[["geonameId","name","fcl","lat","lng","adminName1","adminName2","score","searchMethod","searchKeyword","searchKeywordCount"]]


        return df_AllResult
    else:
        print("Error: input format error in lngArray,latArray")
        return None


def extractSpatialDf(title, notes, lngArray,latArray,method="hybrid"):
    """[summary]タイトル、説明、緯度経度の列からgeonamesの地名候補をDataframe形式で出力

    Args:
        title ([str]): [データセットのタイトル]
        notes ([str]): [データセットの説明]
        lngArray ([np.array]): [経度のArray]
        latArray ([np.array]): [緯度のArray]
        method (str, optional): [マージ・ソートの方法]. Defaults to "hybrid".

    Returns:
        [dataframe]: [geonamesの地名の候補]]
    """
    title = str(title)
    notes = str(notes)

    # 入力値のパターン判定
    keywords_dict = dict(extract_LocationKeywords(title+ " "+ notes,mode="Counter"))
    if len(keywords_dict)>0:
        if len(lngArray)==len(latArray) and len(lngArray)!=0 and len(latArray)!=0:
            pattern = "both"
        else:
            pattern = "keyword_only"
    else:
        if len(lngArray)==len(latArray) and len(lngArray)!=0 and len(latArray)!=0:
            pattern = "Bbox_only"
        else:
            pattern = "None"

    # 入力値のパターンごとに出力を計算
    if pattern == "both":
        if method == "overlap":
            return lnglatArrayWithName2spatialDf(lngArray=lngArray,latArray=latArray,title=title,notes=notes,style="full")
        else:
            df_keywordResult = datasetText2spatialDf(title=title, notes=notes,style="full")
            df_BboxResult = lnglatArray2spatialDf(lngArray=lngArray,latArray=latArray,style="full")
            if method == "hybrid":
                return mergeSortDataframe(df_keywordResult,df_BboxResult,sortMode="hybrid")
            elif method == "keywordFirst":
                return mergeSortDataframe(df_keywordResult,df_BboxResult,sortMode="keywordFirst")
            elif method == "BboxFirst":
                return mergeSortDataframe(df_keywordResult,df_BboxResult,sortMode="BboxFirst")
            else:
                print("Error: method which is not defined used")
                return None

    elif pattern == "keyword_only":
        df_keywordResult = datasetText2spatialDf(title=title, notes=notes,style="full")
        
        # 並べ替え（キーワード頻度、スコアで）
        df_keywordResult = df_keywordResult.sort_values(['searchKeywordCount','score'], ascending=[False, False])
        # 重複排除
        df_keywordResult = df_keywordResult.drop_duplicates(subset="geonameId",keep="first")
        df_keywordResult = df_keywordResult.reset_index(drop=True)

        # 必要な列のみ残す
        df_keywordResult = df_keywordResult[["geonameId","name","fcl","lat","lng","adminName1","adminName2","score","searchMethod","searchKeyword","searchKeywordCount"]]
        return df_keywordResult

    elif pattern == "Bbox_only":
        df_BboxResult = lnglatArray2spatialDf(lngArray=lngArray,latArray=latArray,style="full")
        df_BboxResult = df_BboxResult.sort_values(['score'], ascending=[False])
        df_BboxResult = df_BboxResult.reset_index(drop=True)
        df_BboxResult = df_BboxResult[["geonameId","name","fcl","lat","lng","adminName1","adminName2","score","searchMethod"]]
        return df_BboxResult
    else:
        return None


'''
def get_geonameCandidates_old(text, filepath):
        # テキストからキーワード抽出してgeoname候補を出力
        result_list1 = []
        locationKeyword_list = extract_LocationKeywords(text)
        selected_locationKeyword_list = select_LocationKeywords(locationKeyword_list)

        for keyword in selected_locationKeyword_list:
            result = FindByKeyword_name(keyword)
            for elem in result:
                result_list1.append(elem)

        # データファイルから緯度経度抽出したgeoname候補を出力
        if extract_lnglatBbox_csv(filepath=filepath) is not None:
            east_sample, west_sample, north_sample, south_sample = extract_lnglatBbox_csv(filepath=filepath)
            result_list2 = FindbyBbox(east=east_sample,west=west_sample,north=north_sample,south=south_sample)
        else:
            result_list2 =[]

        # Result listをくっつける
        result_list = result_list1 + result_list2
        #result_list = result_list2

        # 結合した結果をdataframeにしてgeonameId重複を排除
        if len(result_list) >0:
            df = pd.DataFrame(result_list)
            df_merged = df[~df.geonameId.duplicated()][['geonameId','countryName','adminName1','adminName2','name','lng','lat','fcl']]
            return df_merged
        else:
            return pd.DataFrame(columns=['geonameId','countryName','adminName1','adminName2','name','lng','lat','fcl'])
'''

# %%
# 関数の動作テスト
if __name__ == '__main__':
    # 関数extract_LocationKeywordsのテスト1
    print("==== extract_LocationKeywordsのテスト1 ====")
    title_text = "【蕨市】避難施設一覧"
    description_text = "蕨市内の避難施設の一覧です。"
    # https://opendata.pref.saitama.lg.jp/data/dataset/c-users-2348-desktop
    print("title:", title_text)
    print("description:", description_text)
    print("Keywords:",extract_LocationKeywords(title_text + " " +description_text))
    print("\n")

    # 関数extract_LocationKeywordsのテスト2
    print("==== extract_LocationKeywordsのテスト2 ====")
    title_text = "【埼玉県】公共施設情報"
    description_text = "埼玉県で保有する公共施設の住所、連絡先及び位置情報等のデータ"
    # https://opendata.pref.saitama.lg.jp/data/dataset/a2290sisetu
    print("title:", title_text)
    print("description:", description_text)
    print("Keywords:",extract_LocationKeywords(title_text + " " +description_text))
    print("\n")

    # 関数extract_LocationKeywordsのテスト3
    print("==== extract_LocationKeywordsのテスト3 ====")
    title_text = "通行実績デ－タ"
    description_text = "パイオニア製カーナビゲーションより取得した通行実績データです。このデータの特長は次の通りです。災害の発生の有無に寄らず、1時間毎に通行実績データを生成しております。防災・減災、復旧・復興を使用目的とする限り、災害時・平常時、災害の規模、災害の種類を問わず活用いただけます。日本全国の道路をカバーしております。プライバシー保護のため、3台以上の通行実績が確認できない道路の通行実績データは生成されません。交通規制や渋滞状況を表示できる地図サービスに通行実績データを簡単に重ねて表示できます。"
    # https://www.geospatial.jp/ckan/dataset/pioneertsukojissekidata
    print("title:", title_text)
    print("description:", description_text)
    print("Keywords:",extract_LocationKeywords(title_text + " " +description_text))
    print("\n")


#%%
    # extract_latlngArray_csv関数のテスト
    print("==== extract_latlngArray_csvのテスト ====")
    sample_file_path = 'sample/warabi_hinansisetu.csv'
    lng_array_sample, lat_array_sample,  = extract_lnglatArray_csv(filepath=sample_file_path)
    print("file:", sample_file_path)

    print("longitude array:", lng_array_sample)
    print("latitude array:",lat_array_sample)
    print("\n")


    # extract_latlngBbox_csv関数のテスト
    print("==== extract_latlngBbox_csvのテスト ====")
    sample_file_path = 'sample/warabi_hinansisetu.csv'
    east_sample, west_sample, north_sample, south_sample = extract_lnglatBbox_csv(filepath=sample_file_path)
    print("file:", sample_file_path)
    print("east, west, north, south:",east_sample, west_sample, north_sample, south_sample)
    print("\n")


#%%
    # FindByKeyword_name動作テスト1
    print("==== FindByKeyword_nameのテスト ====")
    locationKeyword_sample1 = '羽田空港'
    result = FindByKeyword_name(locationKeyword_sample1)
    print("Keyword: ", locationKeyword_sample1)
    print("Result Count: ", len(result))
    print("Result:")

    for elem in result:
        print(
            elem['geonameId'],
            elem['countryName'],
            elem['adminName1'],
            elem['adminName2'],
            elem['name'],
            elem['lng'],
            elem['lat'],
            elem['fcl']
        )

    #print(result)
    print("\n")
    # FindByKeyword_name動作テスト2
    print("==== FindByKeyword_nameのテスト ====")
    locationKeyword_sample2 = '中央区'
    result = FindByKeyword_name(locationKeyword_sample2)
    print("Keyword: ", locationKeyword_sample2)
    print("Result Count: ", len(result))
    print("Result:")

    for elem in result:
        print(
            elem['geonameId'],
            elem['countryName'],
            elem['adminName1'],
            elem['adminName2'],
            elem['name'],
            elem['lng'],
            elem['lat'],
            elem['fcl']
        )

    #print(result)
    print("\n")

#%%
    # GetFeatures関数の動作テスト
    print("==== GetFeaturesのテスト ====")

    geonameId_sample=8534447
    result_elem = getFeautures(geonameId=geonameId_sample)

    print("geonameId:", geonameId_sample)
    print(
        result_elem['geonameId'],
        result_elem['name'],
        result_elem['countryName'],
        result_elem['adminName1'],
        result_elem['adminName2'],
        result_elem['lng'],
        result_elem['lat'],
        result_elem['fcl'],
        result_elem['bbox']
    )
    print("\n")


#%%
    # getHierarchyList関数の動作テスト
    print("==== getHierarchyListのテスト ====")

    geonameId_sample=8534447
    result = getHierarchyList(geonameId=geonameId_sample)

    print("geonameId:", geonameId_sample)
    print(result)

#%%
    # getFullname関数の動作テスト
    print("==== getFullnameのテスト1 ====")

    geonameId_sample=8534447 # 千葉県>千葉市>中央区
    for mode_sample in ["Full", "Continent", "Country", "Prefecture"]:
        result = getFullname(geonameId=geonameId_sample,mode=mode_sample)
        print("geonameId:", geonameId_sample, "mode:", mode_sample)
        print(result)

    print("==== getFullnameのテスト2 ====")
    geonameId_sample=6930927 # 札幌駅
    
    for mode_sample in ["Full", "Continent", "Country", "Prefecture"]:
        result = getFullname(geonameId=geonameId_sample,mode=mode_sample)
        print("geonameId:", geonameId_sample, "mode:", mode_sample)
        print(result)

    print("==== getFullnameのテスト3 ====")
    geonameId_sample=1853226 # 埼玉県
    
    for mode_sample in ["Full", "Continent", "Country", "Prefecture"]:
        result = getFullname(geonameId=geonameId_sample,mode=mode_sample)
        print("geonameId:", geonameId_sample, "mode:", mode_sample)
        print(result)
    
    print("\n")


#%%
    # FindByBbox関数のテスト
    print("==== FindByBboxのテスト ====")
    east_sample=141.0
    west_sample=139.9
    north_sample=35.8
    south_sample=35.4

    result = FindbyBbox(east=east_sample,west=west_sample,north=north_sample,south=south_sample)
    print("east,west,north,south:", east_sample,west_sample,north_sample,south_sample)

    print("Result Count: ", len(result))
    print("Result:")

    for elem in result:
        print(
            elem['geonameId'],
            elem['countryName'],
            elem['adminName1'],
            elem['adminName2'],
            elem['name'],
            elem['lng'],
            elem['lat'],
            elem['fcl']
        )

    #print(result)
    print("\n")



#%%
    # FindNearby関数の動作テスト
    print("==== FindNearbyのテスト ====")
    lng_sample = 139.46125
    lat_sample = 35.70552

    result = FindNearby(lng=lng_sample,lat=lat_sample)
    print("lng,lat:", lng_sample,lat_sample)

    for elem in result:
        print(
            elem['geonameId'],
            elem['countryName'],
            elem['adminName1'],
            elem['adminName2'],
            elem['name'],
            elem['lng'],
            elem['lat'],
            elem['fcl'],
            elem['distance']
        )

    print("\n")

