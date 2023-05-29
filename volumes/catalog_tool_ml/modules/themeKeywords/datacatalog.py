# -*- coding: utf-8 -*-
#%%
#import pandas as pd
import numpy as np

import janome
from janome.tokenizer import Tokenizer
from janome.tokenfilter import CompoundNounFilter, POSKeepFilter
from janome.charfilter import UnicodeNormalizeCharFilter
from janome.analyzer import Analyzer

from gensim.models.word2vec import Word2Vec
#from gensim import corpora

#from IPython.display import display
#import seaborn as sns

import re

#%% [markdown]
# ## 関数の定義



#%%
model_path = './modules/themeKeywords/PreTrained_word2vec/LearnedWordvectors_Shiroyagi/word2vec.gensim.model'
model = Word2Vec.load(model_path)
vector_size = len(model.wv.word_vec(u'テスト'))


def get_word2vec(word):
    """
    単語をword2vecでベクトルにする
    :param word: str, 単語の文字列
    :return: numpy array, 単語のベクトル表現
    """
    #return model.wv.word_vec(word, use_norm=False)
    return model.wv.word_vec(word)


def wordslist2vec(wordslist):
    """
    単語のリストをベクトルにする
    :param wordslist: 単語のリスト
    :return: numpy array, 単語リストのベクトル表現
    """
    vec_list = []

    for word in wordslist:
        # if word in model.wv.index2entity:
        #     vec_list.append(get_word2vec(word))
        # else:
        #     'なにもしない'
        try:
            vec_list.append(get_word2vec(word))
        except KeyError:
            pass

    if len(vec_list) != 0:
        return sum(vec_list) / len(vec_list)
    else:
        return np.zeros(vector_size)


def text2wordslist(text, tokens=Tokenizer(), remove_stop=True):
    """
    テキストを単語リストにする
    :param text: str, テキスト
    :param tokens: Janomeのトークナイザ
    :param remove_stop: Boolean, ストップワードを除去するか否かのフラグ
    :return: 単語リスト
    """
    char_filters = [UnicodeNormalizeCharFilter()]

    token_filters = [  # CompoundNounFilter(),
        POSKeepFilter(['名詞', '動詞', '形容詞', 'カスタム名詞'])]

    analyzer = Analyzer(char_filters=char_filters,
                        tokenizer=tokens,
                        token_filters=token_filters)

    wordslist = []
    for token in analyzer.analyze(text):
        if token.base_form != '*':
            wordslist.append(token.base_form)
        else:
            wordslist.append(token.surface)

    # ストップワードを除去する
    if remove_stop == True:
        return remove_stopwords(wordslist)
    else:
        return wordslist


def text2vec(text_dataset_title, text_dataset_desc='', text_resource_title='', text_resource_desc='', mode='dataset_title_desc'):
    '''
    データカタログのタイトル等のテキストをベクトル表現にする
    :param text_dataset_title: str
    :param text_dataset_desc: str
    :param text_resource_title: str
    :param text_resource_desc: str
    :param mode: str
    :return: vector: numpy array
    '''
    if mode == 'dataset_title_only':
        wordslist_dataset = text2wordslist(text_dataset_title)
        vec_dataset = wordslist2vec(wordslist_dataset)
        return vec_dataset
    elif mode == 'dataset_title_desc':
        wordslist_dataset = text2wordslist(text_dataset_title) + text2wordslist(text_dataset_desc)
        vec_dataset = wordslist2vec(wordslist_dataset)
        return vec_dataset
    elif mode == 'dataset_title_desc2':
        wordslist_dataset1 = text2wordslist(text_dataset_title)
        vec_dataset1 = wordslist2vec(wordslist_dataset1)
        wordslist_dataset2 = text2wordslist(text_dataset_desc)
        vec_dataset2 = wordslist2vec(wordslist_dataset2)
        return np.hstack((vec_dataset1, vec_dataset2))
    elif mode == 'dataset_resource_title':
        wordslist_dataset = text2wordslist(text_dataset_title) + text2wordslist(text_dataset_desc)
        vec_dataset = wordslist2vec(wordslist_dataset)
        wordslist_resource = text2wordslist(text_resource_title)
        vec_resource = wordslist2vec(wordslist_resource)
        return np.hstack((vec_dataset, vec_resource))
    elif mode == 'dataset_resource_title2':
        wordslist_dataset1 = text2wordslist(text_dataset_title)
        wordslist_dataset2 = text2wordslist(text_dataset_desc)
        vec_dataset1 = wordslist2vec(wordslist_dataset1)
        vec_dataset2 = wordslist2vec(wordslist_dataset2)

        wordslist_resource = text2wordslist(text_resource_title)
        vec_resource = wordslist2vec(wordslist_resource)
        return np.hstack((vec_dataset1, vec_dataset2, vec_resource))
    elif mode == 'dataset_resource_full':
        wordslist_dataset = text2wordslist(text_dataset_title) + text2wordslist(text_dataset_desc)
        vec_dataset = wordslist2vec(wordslist_dataset)
        wordslist_resource = text2wordslist(text_resource_title) + text2wordslist(text_resource_desc)
        vec_resource = wordslist2vec(wordslist_resource)
        return np.hstack((vec_dataset, vec_resource))
    elif mode == 'dataset_resource_full2':
        wordslist_dataset1 = text2wordslist(text_dataset_title)
        wordslist_dataset2 = text2wordslist(text_dataset_desc)
        vec_dataset1 = wordslist2vec(wordslist_dataset1)
        vec_dataset2 = wordslist2vec(wordslist_dataset2)

        wordslist_resource1 = text2wordslist(text_resource_title)
        wordslist_resource2 = text2wordslist(text_resource_desc)
        vec_resource1 = wordslist2vec(wordslist_resource1)
        vec_resource2 = wordslist2vec(wordslist_resource2)

        return np.hstack((vec_dataset1, vec_dataset2, vec_resource1, vec_resource2))
    else:
        print("input value error in mode")


def remove_stopwords(wordslist):
    '''
    ストップワードの単語を除去する(数字以外で始まり、かつ、ストップワードリストにない単語を残す)
    :param wordslist: list, 対象の単語リスト
    :return: list, 不要な語が削除された単語リスト
    '''
    pattern = re.compile(r'[^0-9]')
    stopwordslist = ['nan', '_', '(', ')', '年', 'こと', 'する', '「', '」', 'これ', 'それ', 'する', 'ため']

    wordslist_new = []
    for word in wordslist:
        if pattern.match(word):
            if word not in stopwordslist:
                wordslist_new.append(word)

    return wordslist_new


#%%
if __name__ == '__main__':
    print("関数remove_stopwordsのテスト:")
    words_test = ["2019年","テスト", "日本","こと"]
    print(remove_stopwords(words_test))
    print("\n")

    print("関数get_word2vecのテスト:")
    vec_test1 = get_word2vec("日本")
    print(vec_test1, type(vec_test1), vec_test1.shape)
    print("\n")

    print("関数wordslist2vecのテスト:")
    print(wordslist2vec(["テスト","日本"]))
    #print((get_word2vec("テスト")+get_word2vec("日本"))/2.0)
    print("\n")

    print("関数text2wordslistのテスト:")
    print(text2wordslist("私の出身は日本です。日本は小さくて人口が多い国です"))
    print("\n")

    print("関数text2vecのテスト:")
    title_test = "東京都の人口の推移を示すデータ"
    desc_test = "東京都の市区町村ごとの人口を表すデータです。"
    vec_test2 =text2vec(text_dataset_title=title_test, \
                text_dataset_desc=desc_test, text_resource_title='', \
                text_resource_desc='', mode='dataset_title_desc2')
    print(vec_test2, type(vec_test2), vec_test2.shape)
    print("\n")


#%%
