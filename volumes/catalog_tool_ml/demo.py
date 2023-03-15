#-*- coding: utf-8 -*-
#%%
from sklearn.externals import joblib
import pickle
import grpc
import time
from concurrent import futures
import os

# from IPython.display import display

# 独自定義モジュール
import datacatalog
import model_evaluation
import pick_locationname
import analyse_data_pb2
import analyse_data_pb2_grpc
os.environ.pop('http_proxy', None)
os.environ.pop('https_proxy', None)

#%%
# dataset themeのモデル読み込み
clf_theme = joblib.load("./model/model_theme.pkl")
# dataset keywordsのモデル読み込み
clf_keywords = joblib.load("./model/model_keywords.pkl")

# dataset keywordsのMultiLabelBinarizerの読み込み
with open('./model/multilabelbinarizer_keywords.pkl','rb') as f:
    mlb_keywords = pickle.load(f)

print(clf_theme)
print(clf_keywords)
print(mlb_keywords)
print(mlb_keywords.classes_)



class AnalyseServiceServicer(analyse_data_pb2_grpc.AnalyseServiceServicer):
    def __init__(self):
        pass

    def AnalyseServer(self, request_iterator, context):
        for new_msg in request_iterator:
            reply_msgs = []
            print('Receive new message! [title: {}, description: {}, type: {}]'.format(new_msg.title, new_msg.description, new_msg.analyse_type))
            # 処理判別
            if new_msg.analyse_type == 'thema':
                print('Analyse: Thema')
                eval_pred, eval_pred_toplist, eval_pred_probapair = thema_analysis(new_msg.title,
                                                                                   new_msg.description,
                                                                                   clf_theme,
                                                                                   clf_keywords,
                                                                                   mlb_keywords)
                reply_msgs.append(analyse_data_pb2.ReplyMessage(best_analyse=str(eval_pred)))
                reply_msgs.append(analyse_data_pb2.ReplyMessage(top_analyse=str(eval_pred_toplist)))
                reply_msgs.append(analyse_data_pb2.ReplyMessage(probability=str(eval_pred_probapair)))

            elif new_msg.analyse_type == 'tag':
                print('Analyse: Tag')
                eval_pred, eval_pred_toplist, eval_pred_probapair = keywords_analysis(new_msg.title,
                                                                                      new_msg.description,
                                                                                      clf_theme,
                                                                                      clf_keywords,
                                                                                      mlb_keywords)
                reply_msgs.append(analyse_data_pb2.ReplyMessage(best_analyse=str(eval_pred)))
                reply_msgs.append(analyse_data_pb2.ReplyMessage(top_analyse=str(eval_pred_toplist)))
                reply_msgs.append(analyse_data_pb2.ReplyMessage(probability=str(eval_pred_probapair)))

            elif new_msg.analyse_type == 'prefecture':
                print('Analyse: Prefacture')
                prefectures = pick_locationname.predict_location(new_msg.title,
                                                                 new_msg.description,
                                                                 mode="prefecture")
   
                print('Prefecture')
                print(prefectures)
                localgovs = pick_locationname.predict_location(new_msg.title,
                                                               new_msg.description,
                                                               mode="localgov")
                print('loclagov')
                print(localgovs)

                reply_msgs.append(analyse_data_pb2.ReplyMessage(best_analyse=str(prefectures)))
                reply_msgs.append(analyse_data_pb2.ReplyMessage(top_analyse=str(localgovs)))

            for message in reply_msgs:
                yield message            

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    analyse_data_pb2_grpc.add_AnalyseServiceServicer_to_server(AnalyseServiceServicer(), server)
    server.add_insecure_port('[::]:50251')
    server.start()
    print('Starting gRPC sample server...')
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        server.stop(0)

#%%
# ----------------------------------
# dataset theme, keywordsのモデルのテスト
# ----------------------------------

#%%
# テーマの推論
def thema_analysis(dataset_title_text,
                   dataset_description_text,
                   clf_theme,
                   clf_keywords,
                   mlb_keywords):
    # 入力情報
    vec = datacatalog.text2vec(dataset_title_text,
                               dataset_description_text, 
                               mode='dataset_title_desc2')

    print('Dataset title:', dataset_title_text)
    print('Dataset description:', dataset_description_text,'\n')

    # themeの推論結果

    print('Predicted theme:', model_evaluation.model_predict(clf_theme, vec))
    print('Predicted theme Top5:', model_evaluation.model_predict_toplist(clf_theme,vec, top=5))
    print('Predicted theme and PredictProbability:')
    print(model_evaluation.model_predict_probapair(clf_theme,vec,allpair=False,top=5))
    print('\n')

    eval_pred = model_evaluation.model_predict(clf_theme, vec)
    eval_pred_toplist = model_evaluation.model_predict_toplist(clf_theme,vec, top=5)
    eval_pred_probapair = model_evaluation.model_predict_probapair(clf_theme,vec,allpair=False,top=5)

    return eval_pred, eval_pred_toplist, eval_pred_probapair

# タグの推論
def keywords_analysis(dataset_title_text,
                      dataset_description_text,
                      clf_theme,
                      clf_keywords,
                      mlb_keywords):
    # 入力情報
    vec = datacatalog.text2vec(dataset_title_text,
                               dataset_description_text, 
                               mode='dataset_title_desc2')

    print('Dataset title:', dataset_title_text)
    print('Dataset description:', dataset_description_text,'\n')
    
    # Keywordsの推論結果
    print('Predicted keywords:', model_evaluation.multilabelmodel_predict(clf_keywords,vec,mlb_keywords))
    print('Predicted keywords Top10:', model_evaluation.multilabelmodel_predict_toplist(clf_keywords,
                                                                                        vec,
                                                                                        mlb_keywords,
                                                                                        top=10))
    print('Predicted keywords and Predict Probability Top20:')
    eval_pred = model_evaluation.multilabelmodel_predict(clf_keywords,vec,mlb_keywords)
    eval_pred_toplist = model_evaluation.multilabelmodel_predict_toplist(clf_keywords,
                                                                         vec,
                                                                         mlb_keywords,
                                                                         top=10)
    eval_pred_probapair = model_evaluation.multilabelmodel_predict_probapair(clf_keywords,
                                                                             vec,
                                                                             mlb_keywords,
                                                                             allpair=False,
                                                                             top=20)


    return eval_pred, eval_pred_toplist, eval_pred_probapair


# デモ用の表示関数の定義
def demo_print(dataset_title_text, dataset_description_text, clf_theme, clf_keywords, mlb_keywords):
    # 入力情報
    vec = datacatalog.text2vec(dataset_title_text, dataset_description_text, 
                       mode='dataset_title_desc2'
                       )

    print('Dataset title:', dataset_title_text)
    print('Dataset description:', dataset_description_text,'\n')

    # themeの推論結果

    print('Predicted theme:', model_evaluation.model_predict(clf_theme, vec))
    print('Predicted theme Top5:', model_evaluation.model_predict_toplist(clf_theme,vec, top=5))
    print('Predicted theme and PredictProbability:')
    print(model_evaluation.model_predict_probapair(clf_theme,vec,allpair=False,top=5))
    print('\n')

    # Keywordsの推論結果
    print('Predicted keywords:', model_evaluation.multilabelmodel_predict(clf_keywords,vec,mlb_keywords))
    print('Predicted keywords Top10:', model_evaluation.multilabelmodel_predict_toplist(clf_keywords,vec,mlb_keywords, top=10))
    print('Predicted keywords and Predict Probability Top20:')
    # display(model_evaluation.multilabelmodel_predict_probapair(clf_keywords,vec, mlb_keywords,allpair=False,top=20))


"""
#%%
# デモ1
dataset_title_text1 = '病児病後児保育施設'
dataset_description_text1 = '加古川市内の病児保育施設及び病後児保育施設のマップです。'
   # https://opendata-api-kakogawa.jp/ckan/dataset/byouzibyougozihoiku

demo_print(dataset_title_text1, dataset_description_text1, clf_theme, clf_keywords, mlb_keywords)


#%%
# デモ2
dataset_title_text2 = '横浜市の観光スポット一覧'
dataset_description_text2 = '横浜市市内にある観光のスポット、および、観光イベントの開催場所一覧のデータです。'

demo_print(dataset_title_text2, dataset_description_text2, clf_theme, clf_keywords, mlb_keywords)


#%%
# デモ3
dataset_title_text3 = '札幌市が提供する公衆無線LANの一覧'
dataset_description_text3 = 'Sapporo City Wi-Fiのうち、札幌市が設置しているものの一覧です。 ※Sapporo City Wi-Fiについては下記URLのページをご覧ください。'

demo_print(dataset_title_text3, dataset_description_text3, clf_theme, clf_keywords, mlb_keywords)

#%%
# デモ4
dataset_title_text4 = '【蕨市】地震ハザードマップ'
dataset_description_text4 = '蕨市地震ハザードマップは、 東京湾北部地震を想定した場合の震度分布（揺れやすさ）、液状化の危険度、建物被害の危険度（地域の危険度）を示すとともに、火災が発生した場合の延焼危険度を、避難施設、主な公共施設等に関する情報とともに、地図上に示したものです。'

demo_print(dataset_title_text4, dataset_description_text4, clf_theme, clf_keywords, mlb_keywords)
"""
serve()
test = input("hello")

if __name__ == '__main__':
  serve()

#%%
