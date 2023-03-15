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


def model_evaluation_summary(clf, x_test, y_test):
    '''
    分類器の評価結果を表示する。各データの正誤判定結果を出力する。
    :param clf: classifier
    :param x_test:
    :param y_test:
    '''

    y_predict = clf.predict(x_test)

    print('Score: ', clf.score(x_test, y_test))
    print(classification_report(y_test, y_predict))


def model_evaluation_groupname_detail(clf, x_test, y_test, i_test, df_sample):
    # テスト結果の詳細を表示
    y_predict = clf.predict(x_test)
    # y_proba = clf.predict_proba(x_test)
    y_proba = [model_predict_proba(clf, vec) for vec in x_test]
    y_maxproba = [model_predict_maxproba(clf, vec) for vec in x_test]
    y_maxprobapair = [model_predict_maxprobapair(clf, vec) for vec in x_test]

    df_test_result = pd.DataFrame(list(zip(x_test, y_test, y_predict, y_proba, y_maxproba, y_maxprobapair)),
                                  columns=['vector', 'Answer', 'Predict', 'Proba', 'MaxProba', 'MaxProbaPair'], index=i_test)

    df_test_result = df_test_result.join(df_sample['dataset_title']).join(df_sample['dataset_description'])
    df_test_result = df_test_result[['dataset_title', 'dataset_description', 'vector', 'Answer', 'Predict', 'Proba', 'MaxProba', 'MaxProbaPair']]

    return df_test_result


def model_evaluation_tag_detail(clf, mlb, x_test, y_test, i_test, df_sample, proba=False):
    # テスト結果の詳細を表示
    y_predict = clf.predict(x_test)
    y_predict_tag = mlb.inverse_transform(y_predict)
    # y_proba = clf.predict_proba(x_test)
    y_test_tag = mlb.inverse_transform(y_test)

    if proba:
        y_proba = [clf.predict_proba([ele]) for ele in x_test]
        df_test_result = pd.DataFrame({'vector':x_test.tolist(),
                               'Test':y_test.tolist(),
                               'Predict':y_predict.tolist(),
                               'Proba':y_proba,
                               'Test_tag':y_test_tag,
                               'Predict_tag':y_predict_tag}, index=i_test)
    
        df_test_result = df_test_result.join(df_sample['dataset_title']).join(df_sample['dataset_description'])
        df_test_result = df_test_result[['dataset_title', 'dataset_description', 'vector', 'Test_tag', 'Predict_tag', 'Test', 'Predict', 'Proba']]
    else:
        df_test_result = pd.DataFrame({'vector': x_test.tolist(),
                                       'Test': y_test.tolist(),
                                       'Predict': y_predict.tolist(),
                                       'Test_tag': y_test_tag,
                                       'Predict_tag': y_predict_tag}, index=i_test)

        df_test_result = df_test_result.join(df_sample['dataset_title']).join(df_sample['dataset_description'])
        df_test_result = df_test_result[
            ['dataset_title', 'dataset_description', 'vector', 'Test_tag', 'Predict_tag', 'Test', 'Predict']]

    return df_test_result
