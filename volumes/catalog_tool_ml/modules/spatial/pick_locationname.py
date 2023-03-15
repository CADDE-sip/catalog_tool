#%%
"""
テキストに含まれる市区町村やその都道府県を出力（複数あればリスト）する関数群を定義

全国地方公共団体コード
http://www.soumu.go.jp/denshijiti/code.html

「都道府県コード及び市区町村コード」
（令和元年5月1日現在）
http://www.soumu.go.jp/main_content/000618153.xls
"""

#%%
#モジュールインポート
import pandas as pd
import pickle
import janome
from janome.tokenizer import Tokenizer
from janome.tokenfilter import CompoundNounFilter, POSKeepFilter
from janome.charfilter import UnicodeNormalizeCharFilter
from janome.analyzer import Analyzer
import collections

#%%
# Excelファイル読み込み、Dataframeに取り込む
df = pd.read_excel('data/list_pref_localgov.xls')

df = df.rename(columns={
    '団体コード':'code',
    '都道府県名\n（漢字）':'prefecture',
    '市区町村名\n（漢字）':'local_gov',
    '都道府県名\n（カナ）':'prefecture_kana',
    '市区町村名\n（カナ）':'local_gov_kana',
    }
    )

# 不要な列を削除
df = df.drop(columns=['prefecture_kana', 'local_gov_kana'])

# 都道府県のみの行と、市区町村を含む行を識別するフラグの列を作成
df["is_prefecture"] = df['local_gov'].isnull()
#df["is_duplicated"] = df.duplicated(subset=['local_gov'])

# 都道府県のセット
prefecture_set = set(df['prefecture'])

# 市区町村のセット(同名の市区町村（都道府県は異なる）があるのに注意)
localgov_set = set(df[~df['is_prefecture']]['local_gov'])

## Geoname地名セット読み込み
#with open('./data/placenameSet.pkl','rb') as f:
#    geonameLocation_set = pickle.load(f)

#geonameLocation_set

#%%
# 関数の定義

def flatten_by_extend(nested_list):
    """ネスト化されたリストをフラットにする
    """
    flat_list = []
    for e in nested_list:
        flat_list.extend(e)
    return flat_list


def included_prefectures_fromPref(text):
    """テキストに含まれる都道府県名を抽出し、その都道府県名のリスト
    　　を出力する
    """
    list_pref = []
    for prefecture in prefecture_set:
        if prefecture in text:
            list_pref.append(prefecture)
    return list_pref


def included_prefectures_fromLocalgov(text):
    """テキストに含まれる自治体名を抽出し、自治体が所属する都道府県名のリストを出力する
    """
    list_pref = []
    for localgov in localgov_set:
        if localgov in text:
            list_pref.append(df[df['local_gov']==localgov]['prefecture'].values.tolist())
    return list(set(flatten_by_extend(list_pref)))


def included_prefectures(text):
    """テキストに含まれる都道府県名や市区町村名を抽出し、その都道府県名のリスト
    　　を出力する
    """
    # テキストから都道府県名を抽出
    list_pref1 = included_prefectures_fromPref(text)

    # テキストから自治体名を抽出し、対応する都道府県名を抽出
    list_pref2 = included_prefectures_fromLocalgov(text)

    # マージ
    list_all = list(set(list_pref1 + list_pref2))
    return list_all


def included_localgovs(text):
    """テキストに含まれる自治体名を抽出し、その自治体名のリスト
    　　を出力する
    """
    list_localgov = []
    for localgov in localgov_set:
        if localgov in text:
            list_localgov.append(localgov)
    return list_localgov


def predict_location(dataset_title_text="", dataset_description_text="", mode="prefecture"):
    """データセットのタイトル、説明文などから該当する自治体の都道府県名（リスト）を出力する
    """
    text = dataset_title_text + dataset_description_text

    if mode == "prefecture":
        return included_prefectures(text)
    elif mode == "localgov":
        return included_localgovs(text)
    else:
        print("指定したmodeが間違っています")


#%%
# 地名のjanome用の辞書を作成し、Tokenizerを作成
#tokenizer = Tokenizer("./data/user_simpledic.csv", udic_type="simpledic", udic_enc="utf8")
tokenizer = Tokenizer("./modules/spatial/data/user_simpledic.csv", udic_type="simpledic", udic_enc="utf8")

# 地名抽出用の関数の定義
def text2wordslist(text, tokens=tokenizer):
    """[summary]テキストを地名辞書を活用して形態素分析し、テキストにあるカスタム名詞の単語のリストを出力する
    
    Arguments:
        text {[str]} -- [テキスト]
    
    Keyword Arguments:
        tokens {[object]} -- [Janome Tokenizer] (default: {tokenizer})
    
    Returns:
        [list] -- [list of words]
    """
    #char_filters = [UnicodeNormalizeCharFilter()]
    char_filters = []

    #token_filters = [CompoundNounFilter(),POSKeepFilter(['名詞', 'カスタム名詞'])]
    token_filters = [POSKeepFilter(['カスタム名詞'])]


    analyzer = Analyzer(char_filters=char_filters,
                        tokenizer=tokens,
                        token_filters=token_filters)

    wordslist = []
    for token in analyzer.analyze(text):
        if token.base_form != '*':
            wordslist.append(token.base_form)
        else:
            wordslist.append(token.surface)

    return wordslist

#%%
def included_geonameLocation(text, mode="nonDuplicatedList"):
    """テキストに含まれるGeonameの地名を抽出し、その地名のリストを出力する
    
    Arguments:
        text {[string]} -- [テキスト]
    """
    locationWordList = text2wordslist(text=text)
    if mode == "nonDuplicatedList":
        return list(set(locationWordList)) #重複排除したのちにリストにして出力
    elif mode == "DuplicatedList":
        return locationWordList
    elif mode == "Counter":
        return collections.Counter(locationWordList)
    else:
        return list(set(locationWordList))


#%%
if __name__ == '__main__':
    print('テスト1:')
    text1 ="石川県白山市と美里町のデータ"
    print(text1)
    print('抽出した市区町村名: ',included_localgovs(text1))
    print('抽出した都道府県名: ',included_prefectures(text1))
    print("-------------------")

    print('テスト2:')
    text2 ="白山市と小松市と福井市と敦賀市のデータ"
    print(text2)
    print('抽出した市区町村名: ',included_localgovs(text2))
    print('抽出した都道府県名: ',included_prefectures(text2))
    print("-------------------")

    print('テスト3:')
    text3 ="東京都と北海道のデータ"
    print(text3)
    print('抽出した市区町村名: ',included_localgovs(text3))
    print('抽出した都道府県名: ',included_prefectures(text3))
    print("-------------------")

    print('テスト4:')
    title_text4 ="関東のデータ"
    description_text4 = "東京都世田谷区と神奈川県横浜市のハザードマップです"
    print("タイトル: ", title_text4)
    print("説明文: ", description_text4)
    print('抽出した市区町村名: ',predict_location(title_text4,description_text4,mode="localgov"))
    print('抽出した都道府県名: ',predict_location(title_text4,description_text4,mode="prefecture"))
    print("-------------------")

    #市町村名、都道府県名がない場合の動作
    print('テスト5:')
    title_text5 ="データ"
    description_text5 = "ハザードマップです"
    print("タイトル: ", title_text5)
    print("説明文: ", description_text5)
    print('抽出した市区町村名: ',predict_location(title_text5,description_text5,mode="localgov"))
    print('抽出した都道府県名: ',predict_location(title_text5,description_text5,mode="prefecture"))
    print("-------------------")

    # 同名の市町村がある場合
    print('テスト6:')
    title_text6 ="朝日町のデータ"
    description_text6 = "朝日町のハザードマップです"
    print("タイトル: ", title_text6)
    print("説明文: ", description_text6)
    print('抽出した市区町村名: ',predict_location(title_text6,description_text6,mode="localgov"))
    print('抽出した都道府県名: ',predict_location(title_text6,description_text6,mode="prefecture"))
    print("-------------------")

    # Geonameの地名抽出のテスト
    print('テスト7:Geonameの地名抽出のテスト')
    print(included_geonameLocation("私の家は皇居の近くにあります。皇居は東京都千代田区にあります。大森駅は品川区にあります"))
    print(included_geonameLocation('東京スカイツリーへのお越しは、東武スカイツリーライン「とうきょうスカイツリー駅」が便利です。'))
    print(included_geonameLocation('このデータは神奈川県の横浜市戸塚区の避難所一覧のデータです'))
    print(included_geonameLocation("都営地下鉄大門駅 屋内地図・施設情報および測位機器（BLEビーコン）設置位置・属性情報データ"))
    print(included_geonameLocation("町田市において、町田駅周辺で行った通行量調査データです"))
    print("-------------------")



# %%
