# -*- coding: utf-8 -*-
""" 推論関数のまとめ

"""

from modules.themeKeywords import datacatalog
from modules.themeKeywords import model_evaluation

def analyze_theme(title, desc, clf_theme, view_num):
    """ テーマを推論する関数
        
        Args:
         - title: タイトルのテキスト
         - desc: 説明文のテキスト
         - clf_theme: テーマ分類のモデル
         - view_num: toplistの表示数
        
        Returns:
         - pred: 予測結果
         - toplist: 上位リスト
         - prob: 確率リスト
    """
    vec = datacatalog.text2vec(title, desc, mode='dataset_title_desc2')

    # 推論処理
    pred = model_evaluation.model_predict(clf_theme, vec)
    toplist = model_evaluation.model_predict_toplist(clf_theme, vec, top=view_num)
    prob = model_evaluation.model_predict_probapair(clf_theme, vec, allpair=False, top=view_num)

    return pred, toplist, prob


def analyze_keywords(title, desc, clf_keywords, mlb_keywords, view_num):
    """ キーワードを推論する関数

        Args:
         - title: タイトルのテキスト
         - desc: 説明文のテキスト
         - clf_keywords: キーワードのモデル
         - mlb_keywords: マルチラベルキーワードのモデル
         - view_num: toplistの表示数
        
        Returns:
         - pred: 予測結果
         - toplist: 上位リスト
         - prob: 確率リスト
    """
    vec = datacatalog.text2vec(title, desc, mode='dataset_title_desc2')

    # 推論処理
    pred = model_evaluation.multilabelmodel_predict(clf_keywords, vec, mlb_keywords)
    toplist = model_evaluation.multilabelmodel_predict_toplist(clf_keywords,
                                                               vec,
                                                               mlb_keywords,
                                                               top=view_num)
    prob = model_evaluation.multilabelmodel_predict_probapair(clf_keywords,
                                                              vec,
                                                              mlb_keywords,
                                                              allpair=False,
                                                              top=view_num)

    return pred, toplist, prob


