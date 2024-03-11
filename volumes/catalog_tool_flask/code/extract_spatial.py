# %%
"""
データまたはデータカタログのタイトル・説明文から地理空間情報の
geonamesの候補を推定するための関数群を定義
"""

# %%
# Modules
import geocoder
import requests
from requests.exceptions import Timeout
import json
import pandas as pd

# geocoderのgeoname関連マニュアル
# https://geocoder.readthedocs.io/providers/GeoNames.html

# 独自モジュール
import pick_locationname
from catalogtool_exception import CatalogToolException

# jsonファイルの読み込み
config_file_path = './config.json'
config = open(config_file_path, 'r')
config = json.load(config)

geonames_user = config['geonames']['username']

# %%
# 各種パラメータの設定
# GEONAME_USER_KEY = 'jsugawa'
GEONAME_USER_KEY = geonames_user
GEONAME_MAXROWS = 10
GEONAME_LANG = 'ja'
GEONAME_COUNTRY = 'JP'
GEONAME_FEATURECLASS = ['A', 'P']
GEONAME_KEYWORDSEARCH_URL = 'http://api.geonames.org/searchJSON'
GEONAME_KEYWORDSEARCH_STYLE = 'FULL'
GEONAME_GETFEATURE_URL = 'http://api.geonames.org/getJSON'
GEONAME_HIERARCHY_URL = 'http://api.geonames.org/hierarchyJSON'
GEONAME_FINDNEARBY_URL = 'http://api.geonames.org/findNearbyJSON'
GEONAME_FINDNEARBY_RADIUS = 20


# %%
# 関数の定義

# テキストから地名のキーワードを決める関数を定義(現状は自治体名、都道府県名のみ抽出可能)
def extract_LocationKeywords(text):
    keyword_lg_list = pick_locationname.included_localgovs(text)
    keyword_pf_list = pick_locationname.included_prefectures(text)

    if len(keyword_lg_list) > 0:
        keyword_list = keyword_lg_list
    elif len(keyword_pf_list) > 0:
        keyword_list = keyword_pf_list
    else:
        keyword_list = []

    return keyword_list


# ファイルから緯度経度の一覧を取得する
def extract_lnglatArray_csv(filepath):
    """
    CSVファイルを読み込んで緯度経度のarrayを出力する
    """
    # CSVファイルをDataframeとして読み込む
    try:
        df = pd.read_csv(filepath, encoding='shift_jis')
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(filepath, encoding='utf-8')
        except UnicodeDecodeError:
            print("Error in read_csv")
            return None

    # with open(sample_file_path, "rb") as f:
    #    encoding_sample = chardet.detect(f.read())
    #    print(encoding_sample)

    if ('緯度' in df.columns) and ('経度' in df.columns):
        # 緯度または経度に欠損がある行は削除
        df = df.dropna(subset=['緯度', '経度'])

        # 緯度、経度のnumpy arrayを取得

        lat_array = df['緯度'].values
        lng_array = df['経度'].values

        return lng_array, lat_array
    elif ('latitude' in df.columns) and ('longitude' in df.columns):

        # 緯度または経度に欠損がある行は削除
        df = df.dropna(subset=['latitude', 'longitude'])

        # 緯度、経度のnumpy arrayを取得

        lat_array = df['latitude'].values
        lng_array = df['longitude'].values

        return lng_array, lat_array
    else:
        print("Error: 緯度、経度の列がありません")
        return None

# ファイルから緯度経度のBoundingboxを取得する


def extract_lnglatBbox_csv(filepath):

    lng_array, lat_array = extract_lnglatArray_csv(filepath)
    east = lng_array.max()
    west = lng_array.min()
    north = lat_array.max()
    south = lat_array.min()

    return east, west, north, south


# 地名キーワードからgeonameを検索する関数を定義(未使用とする)
def FindByKeyword(
        locationKeyword,
        key=GEONAME_USER_KEY,
        maxRows=GEONAME_MAXROWS,
        featureClass=[],
        lang=GEONAME_LANG,
        country=GEONAME_COUNTRY):
    """
    地名のキーワードを指定して、全属性を対象に検索し、候補となるgeonameのリストを出力
    """
    g = geocoder.geonames(
        location=locationKeyword,
        key=key,
        maxRows=maxRows,
        featureClass=featureClass,
        lang=lang,
        country=country,
    )

    return g


# 地名キーワードからgeonameを検索する関数を定義
def FindByKeyword_name(
        locationKeyword,
        key=GEONAME_USER_KEY,
        maxRows=GEONAME_MAXROWS,
        featureClass=[],
        lang=GEONAME_LANG,
        country=GEONAME_COUNTRY,
        style=GEONAME_KEYWORDSEARCH_STYLE):
    """
    地名のキーワードを指定して、name属性を対象に検索し、
    候補となるgeonameを表すdictonaryのリストを出力
    """

    params = {
        'name': locationKeyword,
        'username': key,
        'maxRows': maxRows,
        'featureClass': featureClass,
        'lang': lang,
        'country': country,
        'style': style
    }

    try:
        r = requests.get(
            url=GEONAME_KEYWORDSEARCH_URL,
            params=params
        )

    except Timeout:
        raise CatalogToolException('FindByKeyword_name_Timeout', 500)

    except Exception:
        raise CatalogToolException('FindByKeyword_name_Exception', 500)

    # print('request query: ',r.url)
    # print('status code: ', r.status_code)

    if r.status_code == 401:
        raise CatalogToolException('FindByKeyword_name_NotAuthorized', 500)
    elif r.status_code == 408:
        raise CatalogToolException('FindByKeyword_name_Timeout', 500)
    elif r.status_code != 200:
        raise CatalogToolException('FindByKeyword_name_HttpError', 500)

    result_dict = json.loads(r.text)
    return result_dict['geonames']


# geoname idから属性を調べる関数を定義
def getFeautures(geonameId, key=GEONAME_USER_KEY, lang=GEONAME_LANG):
    """
    指定したgeonameIdの地名の属性値を辞書形式で出力する
    """
    params = {
        'geonameId': geonameId,
        'username': key,
        'lang': lang,
    }

    try:
        r = requests.get(
            url=GEONAME_GETFEATURE_URL,
            params=params
        )

    except Timeout:
        raise CatalogToolException('getFeautures_Timeout', 500)

    except Exception:
        raise CatalogToolException('getFeautures_Exception', 500)

    # print('request query: ',r.url)
    # print('status code: ', r.status_code)

    if r.status_code == 401:
        raise CatalogToolException('getFeautures_NotAuthorized', 500)
    elif r.status_code == 408:
        raise CatalogToolException('getFeautures_Timeout', 500)
    elif r.status_code != 200:
        raise CatalogToolException('getFeautures_HttpError', 500)

    result_dict = json.loads(r.text)
    return result_dict


# geonameIdからHierarchy(上位の地名)を調べる関数を定義
def getHierarchyList(geonameId, key=GEONAME_USER_KEY, lang=GEONAME_LANG):
    """
    指定したgeonameIdのHierarchy(上位の地名)の一覧をリストで出力する
    """
    params = {
        'geonameId': geonameId,
        'username': key,
        'lang': lang,
    }

    try:
        r = requests.get(
            url=GEONAME_HIERARCHY_URL,
            params=params
        )

    except Timeout:
        raise CatalogToolException('getHierarchyList_Timeout', 500)

    except Exception:
        raise CatalogToolException('getHierarchyList_Exception', 500)

    if r.status_code == 401:
        raise CatalogToolException('getHierarchyList_NotAuthorized', 500)
    elif r.status_code == 408:
        raise CatalogToolException('getHierarchyList_Timeout', 500)
    elif r.status_code != 200:
        raise CatalogToolException('getHierarchyList_HttpError', 500)

    # print('request query: ',r.url)
    # print('status code: ', r.status_code)

    result_dict = json.loads(r.text)
    # return result_dict['geonames']

    list_hierarychy = []
    for elem in result_dict['geonames']:
        list_hierarychy.append(elem['name'])

    return list_hierarychy


# geonameIdから上位の地名を含むFullnameを出力する関数を定義
def getFullname(geonameId, key=GEONAME_USER_KEY, lang=GEONAME_LANG, mode='Country'):
    """
    指定したgeonameIdのFullnameを出力する
    (例: 日本>千葉県>千葉市>中央区)
    """
    list = getHierarchyList(geonameId)

    if mode == 'Continent':  # 例 アジア>日本>千葉県>千葉市>中央区
        return '>'.join(list[1:])
    elif mode == 'Country':  # 例 日本>千葉県>千葉市>中央区
        return '>'.join(list[2:])
    elif mode == 'Prefecture':  # 例 千葉県>千葉市>中央区
        return '>'.join(list[3:])
    elif mode == 'Full':  # 例 Earth>アジア>日本>千葉県>千葉市>中央区
        return '>'.join(list[0:])
    else:
        return '>'.join(list)


# 緯度経度のBoundingBox範囲から検索する
# (FeatureClass='A' or 'P'のみ抽出)
def FindbyBbox(
        east, west, north, south,
        key=GEONAME_USER_KEY,
        maxRows=GEONAME_MAXROWS,
        featureClass=GEONAME_FEATURECLASS,
        lang=GEONAME_LANG,
        country=GEONAME_COUNTRY,
        style=GEONAME_KEYWORDSEARCH_STYLE):

    params = {
        'q': "",
        'username': key,
        'maxRows': maxRows,
        'featureClass': featureClass,
        'lang': lang,
        'country': country,
        'style': style,
        'east': east,
        'west': west,
        'north': north,
        'south': south,
    }

    try:
        r = requests.get(
            url=GEONAME_KEYWORDSEARCH_URL,
            params=params
        )

    except Timeout:
        raise CatalogToolException('FindbyBbox_Timeout', 500)

    except Exception:
        raise CatalogToolException('FindbyBbox_Exception', 500)

    # print('request query: ',r.url)
    # print('status code: ', r.status_code)

    if r.status_code == 401:
        raise CatalogToolException('FindbyBbox_NotAuthorized', 500)
    elif r.status_code == 408:
        raise CatalogToolException('FindbyBbox_Timeout', 500)
    elif r.status_code != 200:
        raise CatalogToolException('FindbyBbox_HttpError', 500)

    result_dict = json.loads(r.text)
    return result_dict['geonames']


def FindbyBbox_old(east, west, north, south):
    g = geocoder.geonames(
        '',
        key=GEONAME_USER_KEY,
        maxRows=GEONAME_MAXROWS,
        featureClass=GEONAME_FEATURECLASS,
        lang=GEONAME_LANG,
        country=GEONAME_COUNTRY,
        east=east,
        west=west,
        north=north,
        south=south,
    )

    return g


# 手動でFindNearby用の関数を定義(geocoderのProximity指定だと結果がいまいちだったため)
def FindNearby(
    lng, lat,
    key=GEONAME_USER_KEY,
    radius=GEONAME_FINDNEARBY_RADIUS,
    maxRows=GEONAME_MAXROWS,
    featureClass=GEONAME_FEATURECLASS,
    lang=GEONAME_LANG,
    country=GEONAME_COUNTRY,
    style=GEONAME_KEYWORDSEARCH_STYLE
):
    """
    指定した緯度、経度の近くの地名をリスト形式で出力する
    """
    params = {
        'lng': lng,
        'lat': lat,
        'username': key,
        'radius': radius,
        'maxRows': maxRows,
        'featureClass': featureClass,
        'lang': lang,
        'country': country,
        'style': style,
    }

    try:
        r = requests.get(
            url=GEONAME_FINDNEARBY_URL,
            params=params
        )

    except Timeout:
        raise CatalogToolException('FindNearby_Timeout', 500)

    except Exception:
        raise CatalogToolException('FindNearby_Exception', 500)

    # print('request query: ',r.url)
    # print('status code: ', r.status_code)

    if r.status_code == 401:
        raise CatalogToolException('FindNearby_NotAuthorized', 500)
    elif r.status_code == 408:
        raise CatalogToolException('FindNearby_Timeout', 500)
    elif r.status_code != 200:
        raise CatalogToolException('FindNearby_HttpError', 500)

    result_dict = json.loads(r.text)
    return result_dict['geonames']


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
    print("Keywords:", extract_LocationKeywords(title_text + description_text))

    # 関数extract_LocationKeywordsのテスト2
    print("==== extract_LocationKeywordsのテスト2 ====")
    title_text = "【埼玉県】公共施設情報"
    description_text = "埼玉県が保有する公共施設の住所、連絡先及び位置情報等のデータ"
    # https://opendata.pref.saitama.lg.jp/data/dataset/a2290sisetu
    print("title:", title_text)
    print("description:", description_text)
    print("Keywords:", extract_LocationKeywords(title_text + description_text))
    print("\n")

# %%
    # extract_latlngArray_csv関数のテスト
    print("==== extract_latlngArray_csvのテスト ====")
    sample_file_path = 'sample/warabi_hinansisetu.csv'
    lng_array_sample, lat_array_sample = extract_lnglatArray_csv(
        filepath=sample_file_path)
    print("file:", sample_file_path)

    print("longitude array:", lng_array_sample)
    print("latitude array:", lat_array_sample)
    print("\n")

    # extract_latlngBbox_csv関数のテスト
    print("==== extract_latlngBbox_csvのテスト ====")
    sample_file_path = 'sample/warabi_hinansisetu.csv'
    east_sample, west_sample, north_sample, south_sample = extract_lnglatBbox_csv(
        filepath=sample_file_path)
    print("file:", sample_file_path)
    print("east, west, north, south:", east_sample,
          west_sample, north_sample, south_sample)
    print("\n")

# %%
    # FindByKeyword動作テスト1
    print("==== FindByKeywordのテスト1 ====")
    locationKeyword_sample1 = '羽田空港'
    g1 = FindByKeyword(locationKeyword_sample1)
    print("Keyword: ", locationKeyword_sample1)
    for elem in g1:
        print(
            elem.geonames_id,
            elem.address,
            elem.country,
            elem.state,
            elem.lat,
            elem.lng,
            elem.feature_class, )
    print("\n")

    # FindByKeyword動作テスト2
    print("==== FindByKeywordのテスト1 ====")
    locationKeyword_sample2 = '中央区'  # 中央区
    g2 = FindByKeyword(locationKeyword_sample2, featureClass=['A', 'P'])
    print("Keyword: ", locationKeyword_sample2)
    for elem in g2:
        print(
            elem.geonames_id,
            elem.address,
            elem.country,
            elem.state,
            elem.lng,
            elem.lat,
            elem.feature_class, )
    print("\n")

# %%
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

    # print(result)
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

    # print(result)
    print("\n")

# %%
    # GetFeatures関数の動作テスト
    print("==== GetFeaturesのテスト ====")

    geonameId_sample = 8534447
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


# %%
    # getHierarchyList関数の動作テスト
    print("==== getHierarchyListのテスト ====")

    geonameId_sample = 8534447
    result = getHierarchyList(geonameId=geonameId_sample)

    print("geonameId:", geonameId_sample)
    print(result)

# %%
    # getFullname関数の動作テスト
    print("==== getFullnameのテスト1 ====")

    geonameId_sample = 8534447  # 千葉県>千葉市>中央区
    for mode_sample in ["Full", "Continent", "Country", "Prefecture"]:
        result = getFullname(geonameId=geonameId_sample, mode=mode_sample)
        print("geonameId:", geonameId_sample, "mode:", mode_sample)
        print(result)

    print("==== getFullnameのテスト2 ====")
    geonameId_sample = 6930927  # 札幌駅

    for mode_sample in ["Full", "Continent", "Country", "Prefecture"]:
        result = getFullname(geonameId=geonameId_sample, mode=mode_sample)
        print("geonameId:", geonameId_sample, "mode:", mode_sample)
        print(result)

    print("==== getFullnameのテスト3 ====")
    geonameId_sample = 1853226  # 埼玉県

    for mode_sample in ["Full", "Continent", "Country", "Prefecture"]:
        result = getFullname(geonameId=geonameId_sample, mode=mode_sample)
        print("geonameId:", geonameId_sample, "mode:", mode_sample)
        print(result)

    print("\n")


# %%
    # FindByBbox_old関数のテスト
    print("==== FindByBbox_oldのテスト ====")
    east_sample = 141.0
    west_sample = 139.9
    north_sample = 35.8
    south_sample = 35.4
    g3 = FindbyBbox_old(east=east_sample, west=west_sample,
                        north=north_sample, south=south_sample)
    print("east,west,north,south:", east_sample,
          west_sample, north_sample, south_sample)
    for elem in g3:
        print(
            elem.geonames_id,
            elem.address,
            elem.country,
            elem.state,
            elem.lng,
            elem.lat,
            elem.feature_class, )
    print("\n")

# %%
    # FindByBbox関数のテスト
    print("==== FindByBboxのテスト ====")
    east_sample = 141.0
    west_sample = 139.9
    north_sample = 35.8
    south_sample = 35.4

    result = FindbyBbox(east=east_sample, west=west_sample,
                        north=north_sample, south=south_sample)
    print("east,west,north,south:", east_sample,
          west_sample, north_sample, south_sample)

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

    # print(result)
    print("\n")


# %%
    # FindNearby関数の動作テスト
    print("==== FindNearbyのテスト ====")
    lng_sample = 139.46125
    lat_sample = 35.70552

    result = FindNearby(lng=lng_sample, lat=lat_sample)
    print("lng,lat:", lng_sample, lat_sample)

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


# %%
    # データカタログのタイトル、説明文から地名キーワードを抽出し、地名候補を出力
    print("==== データカタログのタイトル、説明文から地名キーワードを抽出し、地名候補を出力 ====")
    title_sample = "八王子市の赤ちゃん・ふらっと設置施設"
    description_sample = "【八王子市】子育て関連オープンデータ"
    # https://catalog.data.metro.tokyo.lg.jp/dataset/t132012d0000000031

    locationKeyword_list = extract_LocationKeywords(
        title_sample + description_sample)
    locationKeyword_sample = locationKeyword_list[0]

    result = FindByKeyword_name(locationKeyword_sample)
    print("title:", title_sample)
    print("description:", description_sample)
    print("Keyword:", locationKeyword_sample)

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

    # print(result)
    print("\n")


# %%
    # ファイルからboundingboxを算出し、そのエリアにある地名候補を出力
    print("==== ファイル取得から地名候補出力までのテスト ====")
    sample_file_path = 'sample/warabi_hinansisetu.csv'
    east_sample, west_sample, north_sample, south_sample = extract_lnglatBbox_csv(
        filepath=sample_file_path)
    result = FindbyBbox(east=east_sample, west=west_sample,
                        north=north_sample, south=south_sample)
    print("File:", sample_file_path)
    print("east,west,north,south:", east_sample,
          west_sample, north_sample, south_sample)

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

    # print(result)
    print("\n")


# %%
