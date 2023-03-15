# -*- coding: utf-8 -*-
# MLサーバ
import joblib
import pickle
import grpc
import time
from concurrent import futures
import os
import io
import pandas as pd
import csv
import datetime

# 自作モジュール
from modules import config_reader
from modules import analyzer
from modules.themeKeywords import pick_locationname
from modules.temporal.extract_temporal import extract_temporal_from_textAndData
from modules.spatial.extract_spatial import extract_lnglatArray_csv, extractSpatialDf
from grpc_protocol import ml_analysis_pb2
from grpc_protocol import ml_analysis_pb2_grpc



class AnalyseService(ml_analysis_pb2_grpc.AnalyseServiceServicer):
    """ gRPCサーバの処理

        以下のサービスを処理する
         - テーマとキーワードを推測するサービス
         - データセット対象期間を推測するサービス
         - データセット対象地域を推測するサービス
    """

    def __init__(self):
        pass

    def ThemeKeywordAnalyseServer(self, req_iterator, context):
        """ テーマ・キーワードの推測サービス
        """
        for msg in req_iterator:
            rep_msg = []

            # レシーブメッセージの確認
            print('Receive new message:')
            print('  title: {}'.format(msg.title))
            print('  description: {}'.format(msg.description))
            print('  analyse_type: {}'.format(msg.analyse_type))

            # Themeの分析
            if msg.analyse_type == 'theme':
                print('Analysis: Theme')
                view_num = 5 # toplistの表示数

                # 分析処理
                pred, toplist, prob = analyzer.analyze_theme(msg.title, msg.description, clf_theme, view_num)

                # リプライメッセージ作成
                rep_msg.append(ml_analysis_pb2.ReplyThemeKeyword(best_analyse=str(pred)))
                rep_msg.append(ml_analysis_pb2.ReplyThemeKeyword(top_analyse=str(toplist)))
                rep_msg.append(ml_analysis_pb2.ReplyThemeKeyword(probability=str(prob)))

            # Keywordsの分析
            elif msg.analyse_type == 'tag':
                print('Analysis: Tag')
                view_num = 10 # toplistの表示数
                # 分析処理
                pred, toplist, prob = analyzer.analyze_keywords(msg.title,
                                                                msg.description,
                                                                clf_keywords,
                                                                mlb_keywords,
                                                                view_num)
                # リプライメッセージ作成
                rep_msg.append(ml_analysis_pb2.ReplyThemeKeyword(best_analyse=str(pred)))
                rep_msg.append(ml_analysis_pb2.ReplyThemeKeyword(top_analyse=str(toplist)))
                rep_msg.append(ml_analysis_pb2.ReplyThemeKeyword(probability=str(prob)))

            # Prefectureの分析
            elif msg.analyse_type == 'prefecture':
                print('Analysis: Prefecture')
                
                # 分析処理
                pref = pick_locationname.predict_location(msg.title, msg.description, mode='prefecture')
                govs = pick_locationname.predict_location(msg.title, msg.description, mode='localgov')

                # リプライメッセージ作成
                rep_msg.append(ml_analysis_pb2.ReplyThemeKeyword(best_analyse=str(pref)))
                rep_msg.append(ml_analysis_pb2.ReplyThemeKeyword(top_analyse=str(govs)))
                rep_msg.append(ml_analysis_pb2.ReplyThemeKeyword(probability='none'))

            # Error時の処理
            else:
                print('ERROR: Undefined [analyse_type](theme or tag or prefecture)')
                err_msg = 'analyse_type error'
                rep_msg.append(ml_analysis_pb2.ReplyThemeKeyword(best_analyse=str(err_msg)))
                rep_msg.append(ml_analysis_pb2.ReplyThemeKeyword(top_analyse=str(err_msg)))
                rep_msg.append(ml_analysis_pb2.ReplyThemeKeyword(probability=str(err_msg)))

            # ひとつの要素ずつリプライ
            for message in rep_msg:
                yield message

    def TemporalAnalyseServer(self, req_iterator, context):
        """ データセット対象期間推測サービス
        """
        # ユニークなファイル名作成
        now = datetime.datetime.now()
        current_datetime = now.strftime('%Y%m%d%H%M%S%f')
        temp_csv_data = conf.DIR_RECIEVE +'/' + current_datetime + 'temp_csvfile.csv'

        for msg in req_iterator:
            rep_msg = []

            # 文字列 -> リストの解析
            datalist = msg.data.split('\n')
            csv_data = []
            for _data in datalist:
                csv_data.append(_data.split(','))
            
            # None要素を削除
            for i, csvrow in enumerate(csv_data):
                if csvrow == ['']:
                    del csv_data[i]

            # 受信したデータをCSVファイルに保存
            with open(temp_csv_data, 'w', encoding='utf-8') as f:
                writer = csv.writer(f, lineterminator='\n')
                writer.writerows(csv_data)

            # 日付の分析 
            res_datetime = extract_temporal_from_textAndData(text=msg.text,
                                                             filepath=temp_csv_data,
                                                             column_name=msg.column_name,
                                                             input_datetime_format='auto')

            # 受信したファイルの削除
            os.remove(temp_csv_data)
            
            # 返信メッセージ作成
            rep_msg = []
            rep_msg.append(ml_analysis_pb2.ReplyTemporal(start_datetime=str(res_datetime[0])))
            rep_msg.append(ml_analysis_pb2.ReplyTemporal(end_datetime=str(res_datetime[1])))
            
            for message in rep_msg:
                yield message


    def SpatialAnalyseServer(self, req_iterator, context):
        """ データセット対象地域推測のサービス
        """
        print('SpatialAnalyseServer')
        print('iter')
        print(req_iterator)
        print('context')
        print(context)
        
        # ユニークなファイル名作成
        now = datetime.datetime.now()
        current_datetime = now.strftime('%Y%m%d%H%M%S%f')
        temp_csv_data = conf.DIR_RECIEVE +'/' + current_datetime + 'temp_csvfile.csv'
        print(temp_csv_data)

        for msg in req_iterator:

            # 文字列 -> リストの解析
            datalist = msg.data.split('\n')
            csv_data = []
            for _data in datalist:
                csv_data.append(_data.split(','))
            
            # None要素を削除
            for i, csvrow in enumerate(csv_data):
                if csvrow == ['']:
                    del csv_data[i]

            # 受信したデータをCSVファイルに保存
            with open(temp_csv_data, 'w', encoding='utf-8') as f:
                writer = csv.writer(f, lineterminator='\n')
                writer.writerows(csv_data)

            # 緯度経度の抽出
            lnglatArray = extract_lnglatArray_csv(temp_csv_data)
            
            # 分析
            result_spatial = extractSpatialDf(msg.title,
                                              msg.notes,
                                              lnglatArray[0],
                                              lnglatArray[1],
                                              msg.method)

            # DataFrame -> リスト
            str_df = result_spatial.values.tolist()

            # 受信したファイルの削除
            os.remove(temp_csv_data)

            rep_msg = []
            rep_msg.append(ml_analysis_pb2.ReplySpatial(spatial_list=str(str_df)))

            for message in rep_msg:
                yield message


def serve():
    """サーバの立ち上げ
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ml_analysis_pb2_grpc.add_AnalyseServiceServicer_to_server(AnalyseService(), server)
    server.add_insecure_port(conf.ML_PORT)
    server.start()
    print('=== ML SERVER START ===')

    try:
        # サーバの継続立ち上げ
        while True:
            time.sleep(60*60*60)

    except KeyboardInterrupt:
        #server.stop(0)
        pass


if __name__ == '__main__':
    """ サーバの初期設定
        ここで定義される変数はGlobalとして定義される．

        定義される変数：
         - conf: コンフィグの設定
         - clf_theme: テーマの分析モデル
         - clf_keywords: キーワードの分析モデル
         - mlb_keywords: マルチラベルキーワードの分析モデル

    """
    print('=== ML SERVER INIT ===')

    # configfile読み込み
    config_filename = 'config.ini'
    conf = config_reader.ConfigInit(config_filename)

    # モデル読み込み
    clf_theme = joblib.load(conf.CLF_MODEL_THEME)
    clf_keywords = joblib.load(conf.CLF_MODEL_KEYWORDS)
    with open(conf.MLB_MODEL_KEYWORDS, 'rb') as f:
        mlb_keywords = pickle.load(f)

    # サーバの起動
    serve()


