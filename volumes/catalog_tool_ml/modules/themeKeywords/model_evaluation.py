# -*- coding: utf-8 -*-
# モデルによる予測、モデルの評価関数を定義

#%%
#モジュールインポート
import numpy as np
from operator import itemgetter
from sklearn.metrics import classification_report

#関数の定義
def model_predict(clf, vec):
    '''
    ベクトルを入力して、推論されるラベルを出力する
    :param clf:classifier
    :param vec: vector
    :return: str, predicted label
    '''
    return clf.predict([vec])[0]


def multilabelmodel_predict(clf, vec, mlb):
    '''
    ベクトルを入力して、推論されるマルチラベルを出力する
    :param clf:classifier
    :param vec: vector
    :param mlb: MultiLabelBinarizer
    :return: tuple of predicted label
    '''
    y = clf.predict([vec])
    tuple_multilabel_predict = mlb.inverse_transform(np.array(y))[0]
    return tuple_multilabel_predict


def model_predict_proba(clf, vec):
    '''
    ベクトルを入力して、ラベルの確率リストを出力する
    :param clf: classifier
    :param vec: vector
    :return: list of probability
    '''
    return clf.predict_proba([vec])[0]


def multilabelmodel_predict_proba(clf, vec, mlb, existproba_only=True):
    '''
    ベクトルを入力して、マルチラベルの確率リストを出力する
    :param clf: classifier
    :param vec: vector
    :param mlb: MultiLableBinarizer
    :param ExistProbaOnly: 出力形式の指定(Trueだとラベルの存在確率のみ出力)
    :return: list of probability that each label exists
    '''
    array_raw = clf.predict_proba([vec])

    if existproba_only:
        #output_array = [ele[0][1] for ele in array_raw]
        output_array = [1.0 - ele[0][0] for ele in array_raw]

    else:
        output_array = [ele[0] for ele in array_raw]

    return output_array


def model_predict_probapair(clf, vec, allpair=False, top=5):
    '''
    ベクトルを入力して、ラベルとその確率のペアを出力する
    :param clf: classifier
    :param vec: vector
    :param allpair: trueの場合、全ペアを出力、falseの場合、topで指定された上位のペアを出力
    :param top: int, 出力するペアの数
    :return: list, list of (label, probability) pair
    '''

    if allpair:
        classes = clf.classes_
        proba = clf.predict_proba([vec])[0]
        return list(zip(classes, proba))
    else:
        classes = clf.classes_
        proba = clf.predict_proba([vec])[0]
        allpairlist = list(zip(classes, proba))
        return sorted(allpairlist, key=itemgetter(1), reverse=True)[0:min(top, len(proba))]


def multilabelmodel_predict_probapair(clf, vec, mlb, allpair=False, proba_threshold=0.1, top=10):
    '''
    ベクトルを入力して、マルチラベルとその確率のペアを出力する
    :param clf: classifier
    :param vec: vector
    :param mlb: MultilabelBinarizer
    :param allpair: trueの場合、全ペアを出力、falseの場合、閾値以上でtopで指定された上位のペアを出力
    :param proba_threshold: 出力対象を制限する確率の閾値
    :param top: int, 出力するペアの上限数
    :return: list, list of (label, probability) pair
    '''
    classes = mlb.classes_.tolist()
    array_raw = clf.predict_proba([vec])
    #proba = [ele[0][1] for ele in array_raw]
    proba = [1.0 - ele[0][0] for ele in array_raw]
    
    allpairlist = list(zip(classes, proba))

    if allpair:
        return allpairlist
    else:
        pairlist = []
        for tuple in allpairlist:
            if tuple[1] > proba_threshold:
                pairlist.append(tuple)
            else:
                pass
        return sorted(pairlist, key=itemgetter(1), reverse=True)[0:min(top, len(pairlist))]


def multilabelmodel_predict_toplist(clf, vec, mlb, proba_threshold=0.1, top=10):
    '''
    ベクトルを入力して、マルチラベルの確率上位のリストを出力する
    :param clf: classifier
    :param vec: vector
    :param mlb: MultilabelBinarizer
    :param proba_threshold: 出力可否を決める確率の閾値
    :param top: int, 出力するペアの上限数
    :return: list, list of label
    '''
    classes = mlb.classes_.tolist()
    array_raw = clf.predict_proba([vec])
    #proba = [ele[0][1] for ele in array_raw]
    proba = [1.0-ele[0][0] for ele in array_raw]
    
    allpairlist = list(zip(classes, proba))

    pairlist = []
    for tuple in allpairlist:
        if tuple[1] > proba_threshold:
            pairlist.append(tuple)
        else:
            pass
    toppairlist = sorted(pairlist, key=itemgetter(1), reverse=True)[0:min(top, len(pairlist))]
    toplist = []
    for probapair in toppairlist:
        toplist.append((probapair[0]))

    return toplist


def model_predict_maxprobapair(clf, vec):
    '''
    ベクトルを入力して、推論されるラベルとその確率のペアを出力する
    :param clf: classifier
    :param vec: vector
    :return: tuple of (label, probability)
    '''
    classes = clf.classes_
    proba = clf.predict_proba([vec])[0]
    allpair = dict(zip(classes, proba))
    predict = clf.predict([vec])[0]
    maxproba = allpair[predict]
    return (predict, maxproba)


def model_predict_maxproba(clf, vec):
    '''
    ベクトルを入力して、推論されるラベルの確率を出力する
    :param clf: classifier
    :param vec: vector
    :return: float, probability of predicted label
    '''
    classes = clf.classes_
    proba = clf.predict_proba([vec])[0]
    allpair = dict(zip(classes, proba))
    predict = clf.predict([vec])[0]
    maxproba = allpair[predict]
    return maxproba


def model_predict_toplist(clf, vec, proba_threshold=0.1, top=10):
    '''
    ベクトルを入力して、ラベルの確率上位のリストを出力する
    :param clf: classifier
    :param vec: vector
    :param proba_threshold: 出力可否を決める確率の閾値
    :param top: int, 出力するペアの上限数
    :return: list, list of label
    '''
    classes = clf.classes_
    array_raw = clf.predict_proba([vec])
    proba = array_raw[0]
    allpairlist = list(zip(classes, proba))

    pairlist = []
    for tuple in allpairlist:
        if tuple[1] > proba_threshold:
            pairlist.append(tuple)
        else:
            pass
    toppairlist = sorted(pairlist, key=itemgetter(1), reverse=True)[0:min(top, len(pairlist))]
    toplist = []
    for probapair in toppairlist:
        toplist.append((probapair[0]))

    return toplist

