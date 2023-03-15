#%%
"""
geonamesのデータから日本語の地名を抽出するPythonスクリプト
"""
#%%
# Modules
import pandas as pd
import re
import regex
import pickle
from IPython.core.display import display

#%%
data_path = "./data/geonames/JP/JP.tsv"
# downloaded from http://download.geonames.org/export/dump/JP.zip
columns_name =[
    "geonameid",
    "name",
    "asciiname",
    "alternatenames",
    "latitude",
    "longitude",
    "feature_class",
    "feature_code",
    "country code",
    "cc2",
    "admin1 code",
    "admin2 code",
    "admin3 code",
    "admin4 code",
    "population",
    "elevation",
    "dem",
    "timezone",
    "modification date"
]

"""
geonameid         : integer id of record in geonames database
name              : name of geographical point (utf8) varchar(200)
asciiname         : name of geographical point in plain ascii characters, varchar(200)
alternatenames    : alternatenames, comma separated, ascii names automatically transliterated, convenience attribute from alternatename table, varchar(10000)
latitude          : latitude in decimal degrees (wgs84)
longitude         : longitude in decimal degrees (wgs84)
feature class     : see http://www.geonames.org/export/codes.html, char(1)
feature code      : see http://www.geonames.org/export/codes.html, varchar(10)
country code      : ISO-3166 2-letter country code, 2 characters
cc2               : alternate country codes, comma separated, ISO-3166 2-letter country code, 200 characters
admin1 code       : fipscode (subject to change to iso code), see exceptions below, see file admin1Codes.txt for display names of this code; varchar(20)
admin2 code       : code for the second administrative division, a county in the US, see file admin2Codes.txt; varchar(80) 
admin3 code       : code for third level administrative division, varchar(20)
admin4 code       : code for fourth level administrative division, varchar(20)
population        : bigint (8 byte int) 
elevation         : in meters, integer
dem               : digital elevation model, srtm3 or gtopo30, average elevation of 3''x3'' (ca 90mx90m) or 30''x30'' (ca 900mx900m) area in meters, integer. srtm processed by cgiar/ciat.
timezone          : the iana timezone id (see file timeZone.txt) varchar(40)
modification date : date of last modification in yyyy-MM-dd format
"""
# %%
# 元データ読み込み
df = pd.read_csv(data_path,header=None,sep='\t',names=columns_name)

# %%
# 元データの概要表示
df.info()

#%%
df.head()

# %%
# カンマ区切りの文字列から単語を抽出し、日本語の単語のみ抽出
def extract_JPwords_old(words):
    words = str(words) # 型を文字列にする(nanだとfloatになるため)
    list_words = words.split(',')
    list_kanjiwords = []
    for word in list_words:
        # 漢字、ひらがな、カタカナのいずれかを含むwordを抽出
        #kanjiword = regex.findall(r'\p{Script=Han}+',word)
        kanjiword = regex.findall(r'[\p{Script=Han}|\p{Script=Hiragana}|\p{Script=Katakana}]+',word)
        if len(kanjiword)>0:
            list_kanjiwords.append(kanjiword[0])
    
    return ','.join(list_kanjiwords)


#%%
def extract_JPwords(words):
    """カンマ区切りの文字列から日本語の単語を抽出する
    
    Arguments:
        words {[string]} -- [カンマ区切りで多様な言語の地名を連ねた文字列。
        例:'Acugi,Atsugi,Atsugicho,Atsugichō,Atsuki,Atugi,Atugi-chhi,Atugi-chhī,NJA,asseugi si,atswghy,atswgy  kanagawa,hou mu,hou mu ding,hou mu shi,xa sungi,Атсуги,Ацуги,Ацуґі,آتسوگی، کاناگاوا,أتسوغي,اتسوگی، کاناگاوا,อะสึงิ,厚木,厚木市,厚木町,아쓰기 시']
    
    Returns:
        [string] -- [カンマ区切りの文字列で日本語の単語のみ抽出したもの。
        例:"厚木,厚木市,厚木町"]
    """

    words = str(words) # 型を文字列にする(nanだとfloatになるため)
    list_words = words.split(',')
    list_kanjiwords = []
    list_hiraganawords = []
    list_katakanawords = []
    for word in list_words:
        # 全角空白が含まれている場合は削除する
        word = word.replace("\u3000","")

        # 半角スペース、かつ、英数字がふくまれる場合は中国語(日本語地名でない)と判定
        result_space = re.search(r' ', word)
        result_alphabet = re.search(r'\w',word)
        if result_space and result_alphabet:
            continue
        else:
            # wordに漢字,ひらがな,カタカナを含むかを調べる
            # https://note.nkmk.me/python-re-regex-character-type/
            kanjiword = regex.findall(r'\p{Script=Han}+',word)
            hiraganaword = regex.findall(r'\p{Script=Hiragana}+',word)
            katakanaword = regex.findall(r'\p{Script=Katakana}+',word)
            
            if(len(word)>1):
                if len(kanjiword)>0:
                    list_kanjiwords.append(word)
                elif len(hiraganaword)>0:
                    list_katakanawords.append(word)
                elif len(katakanaword)>0:
                    list_katakanawords.append(word)
                else:
                    pass
    
    # 適切な日本語のwordのリストを出力
    if len(list_kanjiwords)>0: #漢字を含むwordがある場合
        return ','.join(list_kanjiwords)
    #elif len(list_hiraganawords)>0: #漢字を含むwordがなく、ひらがなのwordがある場合
    #    return ','.join(list_hiraganawords)
    #elif len(list_katakanawords)>0:  #漢字を含むword、ひらがなを含むwordがなく、カタカナのwordがある場合
    #    return ','.join(list_katakanawords)
    else:
        return ''


#%%
# 関数extract_JPwordsのテスト
print(extract_JPwords("totsuka,とつか,トツカ,戸塚,戸塚区,とつか区"))
print(extract_JPwords('Acugi,Atsugi,Atsugicho,Atsugichō,Atsuki,Atugi,Atugi-chhi,Atugi-chhī,NJA,asseugi si,atswghy,atswgy  kanagawa,hou mu,hou mu ding,hou mu shi,xa sungi,Атсуги,Ацуги,Ацуґі,آتسوگی، کاناگاوا,أتسوغي,اتسوگی، کاناگاوا,อะสึงิ,厚木,厚木市,厚木町,아쓰기 시'))

# %%
# 日本語の地名を表す文字列を追加
df['JPwords'] = df.alternatenames.map(extract_JPwords)
df.head(10)

# %%
# 日本語の地名をリスト化する
list_placename =[]
for words in df[df['JPwords']!=""].JPwords:
    for word in words.split(','):
        list_placename.append(word)

# 重複する語を削除するためセットにする
set_placename = set(list_placename)

#%%
# セットをファイルに保存
with open('./data/placenameSet.pkl','wb') as f:
    pickle.dump(set_placename,f)

#%%
# ファイル読み込みのテスト
with open('./data/placenameSet.pkl','rb') as f_test:
    geonameLocation_set = pickle.load(f_test)

display(geonameLocation_set)
#%%
# geonameの地名からjanome用tokenizerの辞書を作成する
df_userdict = pd.DataFrame(columns=["location","type","yomi"])
df_userdict["location"] = list(geonameLocation_set)
df_userdict["type"] = "カスタム名詞"
df_userdict["yomi"] = "*"
df_userdict.to_csv("./data/user_simpledic.csv",header=False, index=False)
