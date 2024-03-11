# -*- coding: utf-8 -*-
import requests
import urllib
from ckanapi import RemoteCKAN, NotAuthorized, NotFound, ValidationError, CKANAPIError, ServerIncompatibleError

import datetime
import json
import traceback
import os
import uuid
import copy

from history_manager import regist_new_record
from history_manager import regist_history_record
from catalogtool_exception import CatalogToolException

QUERY_ESCAPE_REPLACE = [
    {'word': '+', 'replace': r'\+'},
    {'word': '-', 'replace': r'\-'},
    {'word': '&&', 'replace': r'\&\&'},
    {'word': '||', 'replace': r'\|\|'},
    {'word': '!', 'replace': r'\!'},
    {'word': '(', 'replace': r'\('},
    {'word': ')', 'replace': r'\)'},
    {'word': '{', 'replace': r'\{'},
    {'word': '}', 'replace': r'\}'},
    {'word': '[', 'replace': r'\['},
    {'word': ']', 'replace': r'\]'},
    {'word': '^', 'replace': r'\^'},
    {'word': '"', 'replace': r'\"'},
    {'word': '~', 'replace': r'\~'},
    {'word': '*', 'replace': r'\*'},
    {'word': '?', 'replace': r'\?'},
    {'word': ':', 'replace': r'\:'},
    {'word': '<', 'replace': r'\<'},
    {'word': '>', 'replace': r'\>'},
    {'word': '/', 'replace': r'\/'}
]

WITH_OTHER_FIELDS = [
    'trading_policy_use_application',
    'scope_of_disclosure',
    'terms_of_use_permissible_region',
    'privacy_policy_contains_personal_data',
    'warranty_express_warranty',
    'warranty_leagal_compliance'
]

WITH_OTHER_FIELDS_DATE = [
    'data_effective_period',
    'usage_license_period'
]

OTHER_TEMPLATE = 'その他'
OTHER_VALUE_START_INDEX = 4
OTHER_VALUE_END_INDEX = -1

# リストから辞書型リストに変換


def list2dictlist(keys):
    dictlist_keys = []
    for k in keys:
        dictlist_keys.append({'name': k})

    return list(dictlist_keys)

# 現在時刻文字列取得


def get_datetime():
    now = datetime.datetime.now()
    return now.strftime('%Y%m%d%H%M%S%f')

# 現在時刻列取得


def get_datetime_iso():
    return datetime.datetime.now()

# データ取得


def get_data(n_data, key):
    if key not in n_data or n_data[key] == '' or n_data[key] is None:
        return ''
    else:
        return n_data[key]

# オブジェクトデータ取得


def get_vkobject_data(n_data, key):
    if key not in n_data or n_data[key] is None:
        return ''
    else:
        if 'value' not in n_data[key] or n_data[key]['value'] is None:
            return ''
        else:
            return n_data[key]['value']

# NGSIデータモデル取得


def get_ngsi_data_model(app, n_data, key):
    origial_data_model = get_data(n_data, key)
    # NGSIデータモデル取得
    if not origial_data_model:
        return origial_data_model
    ret = {
        'attrs': {}
    }
    # NGSIデータモデル整形
    for key in origial_data_model:
        data_model_dic = {}
        data_model_dic = {
            str(key['attribute']): {
                'description': key['description'],
                'type': key['dataType'],
                'value': key['example'],
                'metadata': {}
            }
        }
        # メタデータ整形
        for metadata in key['metadata']:
            metadata_dic = {}
            metadata_dic = {
                str(metadata['metadataName']): {
                    'description': metadata['description'],
                    'type': metadata['dataType'],
                    'value': metadata['example']
                }
            }
            data_model_dic[str(key['attribute'])
                           ]['metadata'].update(metadata_dic)
        ret['attrs'].update(data_model_dic)
    # JSON形式でCKANへ登録
    return json.dumps(ret, ensure_ascii=False)

# 交換実績記録用リソースID取得


def get_resource_id_for_provenance(app, n_data, dataurl, file_dir, publisher_id, history_url, token):
    app.logger.warning('get_resource_id_for_provenance')
    app.logger.warning(n_data)

    resource_id_for_provenance = ''
    if not dataurl:
        app.logger.warning('dataurl is not set.')
        return resource_id_for_provenance

    dataname = get_data(n_data, 'dataname')
    if not dataname or not os.path.isfile(file_dir + dataname):
        app.logger.warning('dataname is not set.')
        return resource_id_for_provenance

    previous_event_id = get_data(n_data, 'previousEventId')
    if previous_event_id:
        # 公開履歴登録
        resource_id_for_provenance, mes = regist_history_record(
            app, history_url, dataurl, (file_dir + dataname), publisher_id, previous_event_id, token)
    else:
        # 新規来歴登録
        resource_id_for_provenance, mes = regist_new_record(
            app, history_url, dataurl, (file_dir + dataname), publisher_id, token)
    return resource_id_for_provenance

# 利用規約情報の追加


def user_terms(terms):
    register_list = []
    for term_line in terms:
        if 'label' not in term_line:
            continue
        if ('value' not in term_line or term_line['value'] is None
           or term_line['value'] == [] or term_line['value'] == ''):
            register_list.extend(
                [{'key': str(term_line['label']), 'value': ''}])
        elif type(term_line['value']) is list:
            register_list.extend([{'key': str(term_line['label']),
                                   'value': str(','.join(term_line['value']))}])
        else:
            register_list.extend([{'key': str(term_line['label']),
                                   'value': str(term_line['value'])}])
    return register_list

# 利用規約情報(jsonデータ)の追加


def user_terms_json(termsjson):
    register_list_json = []
    for term_line_json in termsjson:
        if 'label' not in term_line_json:
            continue
        elif 'value' not in term_line_json or term_line_json['value'] is None or term_line_json['value'] == []:
            register_list_json.extend([{'key': str(term_line_json['label']),
                                        'value': ''}])
        else:
            register_list_json.extend([{'key': str(term_line_json['label']),
                                        'value': str(json.dumps(term_line_json['value'], ensure_ascii=False))}])
    return register_list_json

# リソース詳細情報の追加


def add_data_details(app, data, publisher_id, file_dir, history_url, token):

    # データの配信情報の追加
    regist_info = []
    for n_data in data:
        _register_dict = {}

        _time_str = str(get_datetime_iso())

        # カタログ登録リクエストに設定されていない項目はCKANに登録するカタログ項目に加えない
        if 'filename' in n_data.keys():
            _register_dict.update({'name': get_data(n_data, 'filename')})
        if 'description' in n_data.keys():
            _register_dict.update(
                {'description': get_data(n_data, 'description')})

        # 配信の作成日は画面入力項目でないため、空判定が不要
        _issued = get_data(n_data, 'issued')
        if _issued:
            _register_dict.update({'issued': _issued})
        else:
            _register_dict.update({'issued': _time_str})
        # 配信の更新日は画面入力項目でないため、空判定が不要
        _register_dict.update({'modified': _time_str})

        if 'id' in n_data.keys():
            _register_dict.update({'id': get_data(n_data, 'id')})
        if 'licensetitle' in n_data.keys():
            _register_dict.update(
                {'license_title': get_data(n_data, 'licensetitle')})
        if 'licenseurl' in n_data.keys():
            _register_dict.update(
                {'license_url': get_data(n_data, 'licenseurl')})
        if 'usrRight' in n_data.keys():
            _register_dict.update({'rights': get_data(n_data, 'usrRight')})
        if 'accessRights' in n_data.keys():
            _register_dict.update(
                {'access_rights': get_data(n_data, 'accessRights')})
        if 'accessRightsUrl' in n_data.keys():
            _register_dict.update(
                {'access_rights_url': get_data(n_data, 'accessRightsUrl')})
        if 'haspolicyUrl' in n_data.keys():
            _register_dict.update(
                {'haspolicy_url': get_data(n_data, 'haspolicyUrl')})
        if 'conformsTo' in n_data.keys():
            _register_dict.update(
                {'conforms_to': get_data(n_data, 'conformsTo')})
        # 配信のダウンロードURLは入力必須項目のため、空判定が不要
        _register_dict.update({'url': get_data(n_data, 'downloadUrl')})
        if 'explainurl' in n_data.keys():
            _register_dict.update(
                {'explain_url': get_data(n_data, 'explainurl')})
        if 'size' in n_data.keys():
            _register_dict.update({'size': get_data(n_data, 'size')})
        if 'mimetype' in n_data.keys():
            _register_dict.update(
                {'mime_type': get_vkobject_data(n_data, 'mimetype')})
        if 'format' in n_data.keys():
            _register_dict.update({'format': get_data(n_data, 'format')})
        if 'compressFormat' in n_data.keys():
            _register_dict.update(
                {'compress_format': get_vkobject_data(n_data, 'compressFormat')})
        if 'packageFormat' in n_data.keys():
            _register_dict.update(
                {'package_format': get_vkobject_data(n_data, 'packageFormat')})

        if 'schema' in n_data.keys():
            _register_dict.update({'schema': get_data(n_data, 'schema')})
        if 'schemaType' in n_data.keys():
            _register_dict.update(
                {'schema_type': get_vkobject_data(n_data, 'schemaType')})
        if 'ngsiEntityType' in n_data.keys():
            _register_dict.update(
                {'ngsi_entity_type': get_data(n_data, 'ngsiEntityType')})
        if 'ngsiTenant' in n_data.keys():
            _register_dict.update(
                {'ngsi_tenant': get_data(n_data, 'ngsiTenant')})
        if 'ngsiServicePath' in n_data.keys():
            _register_dict.update(
                {'ngsi_service_path': get_data(n_data, 'ngsiServicePath')})
        if 'ngsiDataModel' in n_data.keys():
            _register_dict.update(
                {'ngsi_data_model': get_ngsi_data_model(app, n_data, 'ngsiDataModel')})
        if 'dataServiceTitle' in n_data.keys():
            _register_dict.update(
                {'data_service_title': get_data(n_data, 'dataServiceTitle')})
        if 'dataServiceEndpointUrl' in n_data.keys():
            _register_dict.update(
                {'data_service_endpoint_url': get_data(n_data, 'dataServiceEndpointUrl')})
        if 'dataServiceEndpointDescription' in n_data.keys():
            _register_dict.update({'data_service_endpoint_description': get_data(
                n_data, 'dataServiceEndpointDescription')})

        # リソース提供手段の識別子は入力必須項目のため、空判定が不要
        _register_dict.update(
            {'caddec_resource_type': get_vkobject_data(n_data, 'resourceType')})
        # コネクタ利用の要否は入力必須項目のため、空判定が不要
        _register_dict.update(
            {'caddec_contract_required': get_vkobject_data(n_data, 'contractRequired')})
        # 契約確認の要否は入力必須項目のため、空判定が不要
        _register_dict.update(
            {'caddec_required': get_vkobject_data(n_data, 'connectRequired')})

        # NGSIデータの場合は、来歴管理用のURLを作成（カタログには登録しない）
        _resource_type = get_vkobject_data(n_data, 'resourceType')
        _dataurl = get_data(n_data, 'downloadUrl')
        if _resource_type == 'api/ngsi':
            _ngsiTenant = get_data(n_data, 'ngsiTenant')
            _ngsiServicePath = get_data(n_data, 'ngsiServicePath')
            if _ngsiTenant:
                _dataurl = _dataurl + ',Fiware-Service=' + _ngsiTenant
            if _ngsiServicePath:
                _dataurl = _dataurl + ',Fiware-ServicePath=' + _ngsiServicePath

        # 新規来歴登録
        _resource_id_for_provenance = get_data(
            n_data, 'resourceIDForProvenance')
        _get_resource_id_for_provenance = get_vkobject_data(
            n_data, 'getResourceIDForProvenance')
        _new_resource_id_for_provenance = ''
        if _get_resource_id_for_provenance == 'yes':
            _dataurl = urllib.parse.quote(_dataurl)
            _new_resource_id_for_provenance = get_resource_id_for_provenance(
                app, n_data, _dataurl, file_dir, publisher_id, history_url, token)
        if _new_resource_id_for_provenance:
            _resource_id_for_provenance = _new_resource_id_for_provenance

        app.logger.warning('_resource_id_for_provenance')
        app.logger.warning(_resource_id_for_provenance)
        app.logger.warning('_new_resource_id_for_provenance')
        app.logger.warning(_new_resource_id_for_provenance)
        if _resource_id_for_provenance:
            _register_dict.update(
                {'caddec_resource_id_for_provenance': _resource_id_for_provenance})

        regist_info.extend([_register_dict])

    data_infomation = regist_info

    return data_infomation

# データ詳細情報の追加


def data_details(data):
    detail_list = []
    for _detail in data:
        if 'label' not in _detail:
            continue
        if 'value' not in _detail or _detail['value'] is None or _detail['value'] == [] or _detail['value'] == '':
            detail_list.extend([{'key': str(_detail['label']), 'value': ''}])
        elif type(_detail['value']) is list:
            detail_list.extend([{'key': str(_detail['label']),
                                 'value': str(','.join(_detail['value']))}])
        else:
            detail_list.extend(
                [{'key': str(_detail['label']), 'value': str(_detail['value'])}])

    return detail_list

# 分類情報の追加


def class_data(data):
    class_list = []

    if not data or data == '' or data == []:
        class_list = [{'key': 'theme', 'value': ''}]
    else:
        class_list = [{'key': 'theme', 'value': str(','.join(data))}]

    return class_list

# 登録情報のファイル保存（評価機能）


def write_data(data):
    with open('data/log_get_data.txt', mode='w') as f:
        f.write(str(data))

# カタログ情報作成


def create_catalog(app, ckan_addr, file_dir, data, history_url, token):
    # 登録情報のユニークなID設定
    current_time = get_datetime()

    extras_dict = []

    # 登録IDの追加
    packagename = u'ckan' + str(current_time)

    # データセットの説明ページURLの設定
    if 'dataset_description_url' in data and data['dataset_description_url']:
        dataset_description_url = data['dataset_description_url']
    else:
        dataset_description_url = ''

    # 主分類の追加(extras)
    if 'dataset_class' in data and data['dataset_class']:
        _cl = class_data(data['dataset_class'])
        extras_dict.extend(_cl)

    # データ作成者情報の追加(extras)
    extras_dict.extend(data_details(data['data_creator']))

    # データセット情報(任意)情報の追加(extras)
    extras_dict.extend(data_details(data['datasetoptional']))

    # データセットのIDの追加(extras)
    if data['selected_mode'] == 'edit':
        extras_dict.extend([{'key': 'identifier',
                             'value': data['identifier']}])
    else:
        str_dataset = 'dataset/' if ckan_addr.endswith('/') else '/dataset/'
        extras_dict.extend([{'key': 'identifier',
                             'value': str(ckan_addr) + str_dataset + packagename}])

    # データセットのURLの追加(extras)
    if data['selected_mode'] == 'edit':
        extras_dict.extend([{'key': 'dataset_url',
                             'value': data['dataset_url']}])
    else:
        if ckan_addr.endswith('/'):
            str_dataset = 'dataset/' if ckan_addr.endswith(
                '/') else '/dataset/'
        extras_dict.extend([{'key': 'dataset_url',
                             'value': str(ckan_addr) + str_dataset + packagename}])

    # 発行日の追加(extras)
    if data['selected_mode'] == 'edit':
        extras_dict.extend([{'key': 'issued',
                             'value': data['issued']}])
    else:
        extras_dict.extend([{'key': 'issued',
                             'value': str(get_datetime_iso())}])

    # 変更日の追加(extras)
    extras_dict.extend([{'key': 'modified',
                         'value': str(get_datetime_iso())}])

    # 利用条件の追加(extras)
    _ut = user_terms(data['user_terms'])
    extras_dict.extend(_ut)

    # 利用条件(jsonデータ)の追加(extras)
    _utj = user_terms_json(data['user_terms_json'])
    extras_dict.extend(_utj)

    # 提供者IDの取得
    publisher_id = ''
    for _detail in data['data_creator']:
        if _detail['label'] == 'caddec_provider_id':
            publisher_id = _detail['value']

    # リソース詳細情報の追加
    _di = add_data_details(
        app, data['filedata_details'], publisher_id, file_dir, history_url, token)
    app.logger.warning('リソース情報の追加')
    app.logger.warning(data['filedata_details'])
    app.logger.warning(_di)

    # タグ情報の追加
    if 'dataset_key' in data:
        dictlist_keys = list2dictlist(data['dataset_key'])
    else:
        dictlist_keys = []

    # ライセンス情報の追加
    app.logger.warning(json.dumps(data, indent=2, ensure_ascii=False))
    # app.logger.warning('license_url:')
    # app.logger.warning(data['license_url'])
    if 'data_terms' not in data or not data['data_terms']:
        license_id = ''
    else:
        license_id = data['data_terms']
    if 'license_title' not in data or not data['license_title']:
        license_title = ''
    else:
        license_title = str(data['license_title'])
    if 'license_url' not in data or not data['license_url']:
        license_url = ''
    else:
        license_url = str(data['license_url'])

    print('Data Resouce')
    print(_di)

    app.logger.warning('--- Data Upload To CKAN Start ---')
    app.logger.warning('name:')
    app.logger.warning(packagename)
    app.logger.warning('title:')
    app.logger.warning(str(data['catalogTitle']))
    app.logger.warning('notes:')
    app.logger.warning(str(data['catalogDescription']))
    app.logger.warning('url:')
    app.logger.warning(dataset_description_url)
    app.logger.warning('extras:')
    app.logger.warning(json.dumps(extras_dict, indent=2, ensure_ascii=False))
    app.logger.warning('tags:')
    app.logger.warning(dictlist_keys)
    app.logger.warning('resources:')
    app.logger.warning(_di)
    app.logger.warning('license_id:')
    app.logger.warning(license_id)
    app.logger.warning('license_title:')
    app.logger.warning(license_title)
    app.logger.warning('license_url:')
    app.logger.warning(license_url)
    app.logger.warning('owner_org:')
    app.logger.warning(data['regist_org'])

    return packagename, dataset_description_url, extras_dict, dictlist_keys, _di, license_id, license_title, license_url


def connect_ckan(apikey, addr):
    """CKANへ接続する

      Arguments:
        data: CKANのデータ情報
        addr: CKANの登録アドレス(config.iniに記載)
      Return:
        CKANの接続情報

    """
    session = requests.Session()
    ckan_api = RemoteCKAN(addr, apikey=apikey, session=session)
    return ckan_api


def get_ckan_info(app, release_ckan_apikey, release_ckan_addr, detail_ckan_apikey=None, detail_ckan_addr=None):
    """ CKAN情報取得

    Arguments:
        app: flaskのアプリケーションオブジェクト
        release_ckan_apikey: 横断CKAN用ユーザパスワード
        release_ckan_addr: 横断用登録先CKANアドレス
        detail_ckan_apikey: 詳細CKAN用ユーザパスワード
        detail_ckan_addr: 詳細用登録先CKANアドレス

    Returns:
      ckan_info: CKAN情報のリスト
        - title: カタログのタイトル
        - description: カタログの説明
        - url: カタログの記載のホームページ
        - ckan_type: CKANタイプ(release | detail)
    """

    ckan_info = []
    try:
        # 横断検索用CKAN情報取得
        if release_ckan_apikey and release_ckan_addr:
            release_ckan = connect_ckan(release_ckan_apikey, release_ckan_addr)
            ret = release_ckan.action.status_show()
            app.logger.warning('横断検索用CKAN情報取得')
            app.logger.warning(ret)
            release_ckan_info = {
                'title': ret['site_title'],
                'description': ret['site_description'],
                'url': ret['site_url'],
                'ckan_type': 'release'
            }
            ckan_info.append(release_ckan_info)

    except NotAuthorized:
        app.logger.error(traceback.format_exc())
        app.logger.warning('CKAN情報取得 横断検索用CKAN 認証エラー')
        raise CatalogToolException('get_ckan_info_release_NotAuthorized', 500)
    except NotFound:
        app.logger.error(traceback.format_exc())
        app.logger.warning('CKAN情報取得 横断検索用CKAN 検索エラー')
        raise CatalogToolException('get_ckan_info_release_NotFound', 500)
    except ValidationError:
        app.logger.error(traceback.format_exc())
        app.logger.warning('CKAN情報取得 横断検索用CKAN 変数エラー')
        raise CatalogToolException(
            'get_ckan_info_release_ValidationError', 500)
    except CKANAPIError:
        app.logger.error(traceback.format_exc())
        app.logger.warning('CKAN情報取得 横断検索用CKAN APIエラー')
        raise CatalogToolException('get_ckan_info_release_CKANAPIError', 500)
    except ServerIncompatibleError:
        app.logger.error(traceback.format_exc())
        app.logger.warning('CKAN情報取得 横断検索用CKAN 互換性エラー')
        raise CatalogToolException(
            'get_ckan_info_release_ServerIncompatibleError', 500)
    except AttributeError:
        app.logger.error(traceback.format_exc())
        app.logger.warning('CKAN情報取得 横断検索用CKAN 属性エラー')
        raise CatalogToolException('get_ckan_info_release_AttributeError', 500)
    except Exception:
        app.logger.error(traceback.format_exc())
        app.logger.warning('CKAN情報取得 横断検索用CKAN 例外')
        raise CatalogToolException('get_ckan_info_release_Exception', 500)

    try:
        # 詳細検索用CKAN
        if detail_ckan_apikey and detail_ckan_addr:
            detail_ckan = connect_ckan(detail_ckan_apikey, detail_ckan_addr)
            ret = detail_ckan.action.status_show()
            detail_ckan_info = {
                'title': ret['site_title'],
                'description': ret['site_description'],
                'url': ret['site_url'],
                'ckan_type': 'detail'
            }
            ckan_info.append(detail_ckan_info)

    except NotAuthorized:
        app.logger.error(traceback.format_exc())
        app.logger.warning('CKAN情報取得 詳細検索用CKAN 認証エラー')
        raise CatalogToolException('get_ckan_info_detail_NotAuthorized', 500)
    except NotFound:
        app.logger.error(traceback.format_exc())
        app.logger.warning('CKAN情報取得 詳細検索用CKAN 検索エラー')
        raise CatalogToolException('get_ckan_info_detail_NotFound', 500)
    except ValidationError:
        app.logger.error(traceback.format_exc())
        app.logger.warning('CKAN情報取得 詳細検索用CKAN 変数エラー')
        raise CatalogToolException('get_ckan_info_detail_ValidationError', 500)
    except CKANAPIError:
        app.logger.error(traceback.format_exc())
        app.logger.warning('CKAN情報取得 詳細検索用CKAN APIエラー')
        raise CatalogToolException('get_ckan_info_detail_CKANAPIError', 500)
    except ServerIncompatibleError:
        app.logger.error(traceback.format_exc())
        app.logger.warning('CKAN情報取得 詳細検索用CKAN 互換性エラー')
        raise CatalogToolException(
            'get_ckan_info_detail_ServerIncompatibleError', 500)
    except AttributeError:
        app.logger.error(traceback.format_exc())
        app.logger.warning('CKAN情報取得 詳細検索用CKAN 属性エラー')
        raise CatalogToolException('get_ckan_info_detail_AttributeError', 500)
    except Exception:
        app.logger.error(traceback.format_exc())
        app.logger.warning('CKAN情報取得 詳細検索用CKAN 例外')
        raise CatalogToolException('get_ckan_info_detail_Exception', 500)

    return ckan_info


def get_license_list(app, release_apikey, release_ckan_addr, detail_apikey, detail_ckan_addr):
    """ ラインセンスリスト取得

      Arguments:
        app: flaskのアプリケーションオブジェクト
        release_apikey: 横断検索用CKANのsysadminのapikey
        release_ckan_addr: 横断検索用CKANアドレス
        detail_apikey: 詳細検索用CKANのsysadminのapikey
        detail_ckan_addr: 詳細検索用CKANアドレス

      Returns:
        license_list
    """

    license_list = []
    release_license_list = []
    detail_license_list = []

    try:
        # 横断検索用CKANからライセンスリスト取得
        if release_apikey and release_ckan_addr:
            release_ckan_api = connect_ckan(release_apikey, release_ckan_addr)
            release_license_list = release_ckan_api.action.license_list()

    except NotAuthorized:
        app.logger.error(traceback.format_exc())
        app.logger.warning('ラインセンスリスト取得 横断検索用CKAN 認証エラー')
        raise CatalogToolException(
            'get_license_list_release_NotAuthorized', 500)
    except NotFound:
        app.logger.error(traceback.format_exc())
        app.logger.warning('ラインセンスリスト取得 横断検索用CKAN 検索エラー')
        raise CatalogToolException('get_license_list_release_NotFound', 500)
    except ValidationError:
        app.logger.error(traceback.format_exc())
        app.logger.warning('ラインセンスリスト取得 横断検索用CKAN 変数エラー')
        raise CatalogToolException(
            'get_license_list_release_ValidationError', 500)
    except CKANAPIError:
        app.logger.error(traceback.format_exc())
        app.logger.warning('ラインセンスリスト取得 横断検索用CKAN APIエラー')
        raise CatalogToolException(
            'get_license_list_release_CKANAPIError', 500)
    except ServerIncompatibleError:
        app.logger.error(traceback.format_exc())
        app.logger.warning('ラインセンスリスト取得 横断検索用CKAN 互換性エラー')
        raise CatalogToolException(
            'get_license_list_release_ServerIncompatibleError', 500)
    except AttributeError:
        app.logger.error(traceback.format_exc())
        app.logger.warning('ラインセンスリスト取得 横断検索用CKAN 属性エラー')
        raise CatalogToolException(
            'get_license_list_release_AttributeError', 500)
    except Exception:
        app.logger.error(traceback.format_exc())
        app.logger.warning('ラインセンスリスト取得 横断検索用CKAN 例外')
        raise CatalogToolException('get_license_list_release_Exception', 500)

    try:
        # 詳細検索用CKANからライセンスリスト取得
        if detail_apikey and detail_ckan_addr:
            detail_ckan_api = connect_ckan(detail_apikey, detail_ckan_addr)
            detail_license_list = detail_ckan_api.action.license_list()

    except NotAuthorized:
        app.logger.error(traceback.format_exc())
        app.logger.warning('ラインセンスリスト取得 詳細検索用CKAN 認証エラー')
        raise CatalogToolException(
            'get_license_list_detail_NotAuthorized', 500)
    except NotFound:
        app.logger.error(traceback.format_exc())
        app.logger.warning('ラインセンスリスト取得 詳細検索用CKAN 検索エラー')
        raise CatalogToolException('get_license_list_detail_NotFound', 500)
    except ValidationError:
        app.logger.error(traceback.format_exc())
        app.logger.warning('ラインセンスリスト取得 詳細検索用CKAN 変数エラー')
        raise CatalogToolException(
            'get_license_list_detail_ValidationError', 500)
    except CKANAPIError:
        app.logger.error(traceback.format_exc())
        app.logger.warning('ラインセンスリスト取得 詳細検索用CKAN APIエラー')
        raise CatalogToolException('get_license_list_detail_CKANAPIError', 500)
    except ServerIncompatibleError:
        app.logger.error(traceback.format_exc())
        app.logger.warning('ラインセンスリスト取得 詳細検索用CKAN 互換性エラー')
        raise CatalogToolException(
            'get_license_list_detail_ServerIncompatibleError', 500)
    except AttributeError:
        app.logger.error(traceback.format_exc())
        app.logger.warning('ラインセンスリスト取得 詳細検索用CKAN 属性エラー')
        raise CatalogToolException(
            'get_license_list_detail_AttributeError', 500)
    except Exception:
        app.logger.error(traceback.format_exc())
        app.logger.warning('ラインセンスリスト取得 詳細検索用CKAN 例外')
        raise CatalogToolException('get_license_list_detail_Exception', 500)

    # ライセンスリスト整形
    # 横断・詳細検索用CKANから取得
    # 共通値を抽出してリストを作成
    if release_license_list and detail_license_list:
        for release_license in release_license_list:
            for detail_license in detail_license_list:
                if release_license['title'] == detail_license['title']:
                    license_list.append({
                        'title': release_license['title'],
                        'id': release_license['id'],
                        'url': release_license['url']
                    })

    # 横断検索用CKANから取得
    elif release_license_list:
        for _license_data in release_license_list:
            license_list.append({
                'title': _license_data['title'],
                'id': _license_data['id'],
                'url': _license_data['url']
            })

    # 詳細検索用CKANから取得
    elif detail_license_list:
        for _license_data in detail_license_list:
            license_list.append({
                'title': _license_data['title'],
                'id': _license_data['id'],
                'url': _license_data['url']
            })
    app.logger.warning('license_list')
    app.logger.warning(license_list)

    return license_list


def regist_release(app, file_dir, release_catalog, detail_catalog, history_url, token,
                   release_ckan_apikey, release_ckan_addr, detail_ckan_apikey, detail_ckan_addr):
    """ 横断検索カタログ登録

    横断検索カタログを登録する
    既存の詳細検索カタログと紐づく横断検索カタログを作成する場合は、詳細検索用データセットIDを発行し、
    横断検索カタログの作成と詳細検索用カタログの更新をする

    Args:
        app: flaskのアプリケーションオブジェクト
        file_dir: リソースファイル置き場
        release_catalog: 登録する横断検索カタログ情報
        detail_catalog: 更新する詳細検索カタログ情報
        history_url: 来歴管理URL
        release_ckan_apikey: 横断検索用CKANapikey
        release_ckan_addr: 横断検索用CKANアドレス
        detail_ckan_apikey: 詳細検索用CKANapikey
        detail_ckan_addr: 詳細検索用CKANアドレス

    Returns:
        message: カタログ登録結果メッセージ
        release: 横断検索カタログ登録結果
          - ckan_url: 登録した横断検索カタログのURL
          - pkg: 登録した横断検索カタログ情報
        detail: 詳細検索カタログ登録結果
          - ckan_url: 登録した詳細検索カタログのURL
          - pkg: 登録した詳細検索カタログ情報
    """

    app.logger.warning('=== regist_release ===')
    result = {
        'message': 'error',
        'release': {'ckan_url': None, 'pkg': None},
        'detail': {'ckan_url': None, 'pkg': None}
    }

    app.logger.warning('横断検索カタログ登録用データ作成開始')
    # 詳細検索カタログと紐づく横断検索カタログを作成する場合
    if release_catalog['selected_mode'] == 'release-link-detail_duplicate':
        # 詳細検索用データセットID生成
        caddec_dataset_id_for_detail = str(uuid.uuid5(uuid.uuid4(), 'name'))
        # 横断検索カタログと詳細検索用カタログの詳細検索用データセットIDとして設定
        for _release in release_catalog['data_creator']:
            if _release['label'] == 'caddec_dataset_id_for_detail':
                _release['value'] = caddec_dataset_id_for_detail
                break
        for _detail in detail_catalog['data_creator']:
            if _detail['label'] == 'caddec_dataset_id_for_detail':
                _detail['value'] = caddec_dataset_id_for_detail
                break

    # 横断検索カタログ登録用データ作成
    packagename, description_url, extras, tags, resources, license_id, license_title, license_url = create_catalog(
        app, release_ckan_addr, file_dir, release_catalog, history_url, token)

    # 横断検索カタログのCKAN登録
    try:
        session = requests.Session()
        ckan_api = RemoteCKAN(
            release_ckan_addr, apikey=release_ckan_apikey, session=session)
        pkg = ckan_api.action.package_create(name=packagename,
                                             title=str(
                                                 release_catalog['catalogTitle']),
                                             notes=str(
                                                 release_catalog['catalogDescription']),
                                             url=str(description_url),
                                             extras=extras,
                                             tags=tags,
                                             resources=resources,
                                             license_id=license_id,
                                             license_title=license_title,
                                             license_url=license_url,
                                             owner_org=release_catalog['regist_org'])
        app.logger.warning('横断検索カタログ登録結果')
        app.logger.warning(json.dumps(pkg, indent=2, ensure_ascii=False))
        result['message'] = 'success'
        result['release']['pkg'] = pkg
        str_dataset = 'dataset/' if release_ckan_addr.endswith(
            '/') else '/dataset/'
        result['release']['ckan_url'] = str(
            release_ckan_addr) + str_dataset + str(packagename)

    except NotAuthorized:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ登録 横断検索用CKAN 認証エラー')
        raise CatalogToolException('regist_release_release_NotAuthorized', 500)
    except NotFound:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ登録 横断検索用CKAN 検索エラー')
        raise CatalogToolException('regist_release_release_NotFound', 500)
    except ValidationError:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ登録 横断検索用CKAN 変数エラー')
        raise CatalogToolException(
            'regist_release_release_ValidationError', 500)
    except CKANAPIError:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ登録 横断検索用CKAN APIエラー')
        raise CatalogToolException('regist_release_release_CKANAPIError', 500)
    except ServerIncompatibleError:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ登録 横断検索用CKAN 互換性エラー')
        raise CatalogToolException(
            'regist_release_release_ServerIncompatibleError', 500)
    except AttributeError:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ登録 横断検索用CKAN 属性エラー')
        raise CatalogToolException(
            'regist_release_release_AttributeError', 500)
    except Exception:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ登録 横断検索用CKAN 例外')
        raise CatalogToolException('regist_release_release_Exception', 500)

    # 詳細検索用カタログと紐づく横断検索カタログを作成する場合
    if release_catalog['selected_mode'] == 'release-link-detail_duplicate':
        # 詳細検索カタログ登録用データ作成
        packagename, description_url, extras, tags, resources, license_id, license_title, license_url = create_catalog(
            app, detail_ckan_addr, file_dir, detail_catalog, history_url, token)
        packagename = detail_catalog['ckan_data_name']

        # 詳細検索カタログのCKAN登録
        try:
            session = requests.Session()
            ckan_api = RemoteCKAN(
                detail_ckan_addr, apikey=detail_ckan_apikey, session=session)
            pkg = ckan_api.action.package_update(name=(detail_catalog['ckan_data_name']),
                                                 title=str(
                                                     detail_catalog['catalogTitle']),
                                                 notes=str(
                                                     detail_catalog['catalogDescription']),
                                                 url=str(
                                                     description_url),
                                                 extras=extras,
                                                 tags=tags,
                                                 resources=resources,
                                                 license_id=license_id,
                                                 license_title=license_title,
                                                 license_url=license_url,
                                                 owner_org=detail_catalog['regist_org'])
            app.logger.warning('詳細検索カタログ登録結果')
            app.logger.warning(json.dumps(pkg, indent=2, ensure_ascii=False))
            result['message'] = 'success'
            result['detail']['pkg'] = pkg
            str_dataset = 'dataset/' if detail_ckan_addr.endswith(
                '/') else '/dataset/'
            result['detail']['ckan_url'] = str(
                detail_ckan_addr) + str_dataset + str(packagename)

        except NotAuthorized:
            app.logger.error(traceback.format_exc())
            app.logger.error('横断検索カタログ登録での詳細検索カタログ編集 詳細検索用CKAN 認証エラー')
            raise CatalogToolException(
                'regist_release_detail_NotAuthorized', 500)
        except NotFound:
            app.logger.error(traceback.format_exc())
            app.logger.error('横断検索カタログ登録での詳細検索カタログ編集 詳細検索用CKAN 検索エラー')
            raise CatalogToolException('regist_release_detail_NotFound', 500)
        except ValidationError:
            app.logger.error(traceback.format_exc())
            app.logger.error('横断検索カタログ登録での詳細検索カタログ編集 詳細検索用CKAN 変数エラー')
            raise CatalogToolException(
                'regist_release_detail_ValidationError', 500)
        except CKANAPIError:
            app.logger.error(traceback.format_exc())
            app.logger.error('横断検索カタログ登録での詳細検索カタログ編集 詳細検索用CKAN APIエラー')
            raise CatalogToolException(
                'regist_release_detail_CKANAPIError', 500)
        except ServerIncompatibleError:
            app.logger.error(traceback.format_exc())
            app.logger.error('横断検索カタログ登録での詳細検索カタログ編集 詳細検索用CKAN 互換性エラー')
            raise CatalogToolException(
                'regist_release_detail_ServerIncompatibleError', 500)
        except AttributeError:
            app.logger.error(traceback.format_exc())
            app.logger.error('横断検索カタログ登録での詳細検索カタログ編集 詳細検索用CKAN 属性エラー')
            raise CatalogToolException(
                'regist_release_detail_AttributeError', 500)
        except Exception:
            app.logger.error(traceback.format_exc())
            app.logger.error('横断検索カタログ登録での詳細検索カタログ編集 詳細検索用CKAN 例外')
            raise CatalogToolException('regist_release_detail_Exception', 500)

    return result


def regist_detail(app, file_dir, release_catalog, detail_catalog, history_url, token,
                  release_ckan_apikey, release_ckan_addr, detail_ckan_apikey, detail_ckan_addr):
    """ 詳細検索カタログ登録

    詳細検索カタログを登録する
    既存の横断検索カタログと紐づく詳細検索カタログを作成する場合は、詳細検索用データセットIDを発行し、
    詳細検索カタログの作成と横断検索用カタログの更新をする

    Args:
        app: flaskのアプリケーションオブジェクト
        file_dir: リソースファイル置き場
        release_catalog: 更新する横断検索カタログ情報
        detail_catalog: 登録する詳細検索カタログ情報
        history_url: 来歴管理URL
        release_ckan_apikey: 横断検索用CKANapikey
        release_ckan_addr: 横断検索用CKANアドレス
        detail_ckan_apikey: 詳細検索CKAN用apikey
        detail_ckan_addr: 詳細検索用CKANアドレス

    Returns:
        message: カタログ登録結果メッセージ
        release: 横断検索カタログ登録結果
          - ckan_url: 登録した横断検索カタログのURL
          - pkg: 登録した横断検索カタログ情報
        detail: 詳細検索カタログ登録結果
          - ckan_url: 登録した詳細検索カタログのURL
          - pkg: 登録した詳細検索カタログ情報
    """

    app.logger.warning('=== regist_detail ===')
    result = {
        'message': 'error',
        'release': {'ckan_url': None, 'pkg': None},
        'detail': {'ckan_url': None, 'pkg': None}
    }

    # 横断検索カタログと紐づく詳細検索カタログを作成する場合
    if detail_catalog['selected_mode'] == 'detail-link-release_duplicate':
        # 詳細検索用データセットID生成
        caddec_dataset_id_for_detail = str(uuid.uuid5(uuid.uuid4(), 'name'))
        # 横断検索カタログと詳細検索カタログの詳細検索用データセットIDとして設定
        for _release in release_catalog['data_creator']:
            if _release['label'] == 'caddec_dataset_id_for_detail':
                _release['value'] = caddec_dataset_id_for_detail
                break
        for _detail in detail_catalog['data_creator']:
            if _detail['label'] == 'caddec_dataset_id_for_detail':
                _detail['value'] = caddec_dataset_id_for_detail
                break

    # 詳細検索カタログ登録用データ作成
    packagename, description_url, extras, tags, resources, license_id, license_title, license_url = create_catalog(
        app, detail_ckan_addr, file_dir, detail_catalog, history_url, token)

    # 詳細検索カタログのCKAN登録
    try:
        session = requests.Session()
        ckan_api = RemoteCKAN(
            detail_ckan_addr, apikey=detail_ckan_apikey, session=session)
        pkg = ckan_api.action.package_create(name=packagename,
                                             title=str(
                                                 detail_catalog['catalogTitle']),
                                             notes=str(
                                                 detail_catalog['catalogDescription']),
                                             url=str(description_url),
                                             extras=extras,
                                             tags=tags,
                                             resources=resources,
                                             license_id=license_id,
                                             license_title=license_title,
                                             license_url=license_url,
                                             owner_org=detail_catalog['regist_org'])
        app.logger.warning('詳細検索カタログ登録結果')
        app.logger.warning(json.dumps(pkg, indent=2, ensure_ascii=False))
        result['message'] = 'success'
        result['detail']['pkg'] = pkg
        str_dataset = 'dataset/' if detail_ckan_addr.endswith(
            '/') else '/dataset/'
        result['detail']['ckan_url'] = str(
            detail_ckan_addr) + str_dataset + str(packagename)

    except NotAuthorized:
        app.logger.error(traceback.format_exc())
        app.logger.error('詳細検索カタログ登録 詳細検索用CKAN 認証エラー')
        raise CatalogToolException('regist_detail_detail_NotAuthorized', 500)
    except NotFound:
        app.logger.error(traceback.format_exc())
        app.logger.error('詳細検索カタログ登録 詳細検索用CKAN 検索エラー')
        raise CatalogToolException('regist_detail_detail_NotFound', 500)
    except ValidationError:
        app.logger.error(traceback.format_exc())
        app.logger.error('詳細検索カタログ登録 詳細検索用CKAN 変数エラー')
        raise CatalogToolException('regist_detail_detail_ValidationError', 500)
    except CKANAPIError:
        app.logger.error(traceback.format_exc())
        app.logger.error('詳細検索カタログ登録 詳細検索用CKAN APIエラー')
        raise CatalogToolException('regist_detail_detail_CKANAPIError', 500)
    except ServerIncompatibleError:
        app.logger.error(traceback.format_exc())
        app.logger.error('詳細検索カタログ登録 詳細検索用CKAN 互換性エラー')
        raise CatalogToolException(
            'regist_detail_detail_ServerIncompatibleError', 500)
    except AttributeError:
        app.logger.error(traceback.format_exc())
        app.logger.error('詳細検索カタログ登録 詳細検索用CKAN 属性エラー')
        raise CatalogToolException('regist_detail_detail_AttributeError', 500)
    except Exception:
        app.logger.error(traceback.format_exc())
        app.logger.error('詳細検索カタログ登録 詳細検索用CKAN 例外')
        raise CatalogToolException('regist_detail_detail_Exception', 500)

    # 横断検索カタログと紐づく詳細検索カタログを作成する場合
    if detail_catalog['selected_mode'] == 'detail-link-release_duplicate':
        # 横断検索カタログ登録用データ作成
        packagename, description_url, extras, tags, resources, license_id, license_title, license_url = create_catalog(
            app, release_ckan_addr, file_dir, release_catalog, history_url, token)
        packagename = release_catalog['ckan_data_name']

        # 横断検索カタログのCKAN登録
        try:
            session = requests.Session()
            ckan_api = RemoteCKAN(
                release_ckan_addr, apikey=release_ckan_apikey, session=session)
            pkg = ckan_api.action.package_update(name=(release_catalog['ckan_data_name']),
                                                 title=str(
                                                     release_catalog['catalogTitle']),
                                                 notes=str(
                                                     release_catalog['catalogDescription']),
                                                 url=str(
                                                     description_url),
                                                 extras=extras,
                                                 tags=tags,
                                                 resources=resources,
                                                 license_id=license_id,
                                                 license_title=license_title,
                                                 license_url=license_url,
                                                 owner_org=release_catalog['regist_org'])
            app.logger.warning('横断検索カタログ登録結果')
            app.logger.warning(json.dumps(pkg, indent=2, ensure_ascii=False))
            result['message'] = 'success'
            result['release']['pkg'] = pkg
            str_dataset = 'dataset/' if release_ckan_addr.endswith(
                '/') else '/dataset/'
            result['release']['ckan_url'] = str(
                release_ckan_addr) + str_dataset + str(packagename)

        except NotAuthorized:
            app.logger.error(traceback.format_exc())
            app.logger.error('詳細検索カタログ登録での横断検索カタログ編集 横断検索用CKAN 認証エラー')
            raise CatalogToolException(
                'regist_detail_release_NotAuthorized', 500)
        except NotFound:
            app.logger.error(traceback.format_exc())
            app.logger.error('詳細検索カタログ登録での横断検索カタログ編集 横断検索用CKAN 検索エラー')
            raise CatalogToolException('regist_detail_release_NotFound', 500)
        except ValidationError:
            app.logger.error(traceback.format_exc())
            app.logger.error('詳細検索カタログ登録での横断検索カタログ編集 横断検索用CKAN 変数エラー')
            raise CatalogToolException(
                'regist_detail_release_ValidationError', 500)
        except CKANAPIError:
            app.logger.error(traceback.format_exc())
            app.logger.error('詳細検索カタログ登録での横断検索カタログ編集 横断検索用CKAN APIエラー')
            raise CatalogToolException(
                'regist_detail_release_CKANAPIError', 500)
        except ServerIncompatibleError:
            app.logger.error(traceback.format_exc())
            app.logger.error('詳細検索カタログ登録での横断検索カタログ編集 横断検索用CKAN 互換性エラー')
            raise CatalogToolException(
                'regist_detail_release_ServerIncompatibleError', 500)
        except AttributeError:
            app.logger.error(traceback.format_exc())
            app.logger.error('詳細検索カタログ登録での横断検索カタログ編集 横断検索用CKAN 属性エラー')
            raise CatalogToolException(
                'regist_detail_release_AttributeError', 500)
        except Exception:
            app.logger.error(traceback.format_exc())
            app.logger.error('詳細検索カタログ登録での横断検索カタログ編集 横断検索用CKAN 例外')
            raise CatalogToolException('regist_detail_release_Exception', 500)

    return result


def regist_both(app, file_dir, release_catalog, detail_catalog, history_url, token,
                release_ckan_apikey, release_ckan_addr, detail_ckan_apikey, detail_ckan_addr):
    """ 横断検索カタログ・詳細検索カタログ登録

    横断検索カタログ、詳細検索カタログを登録し、詳細検索用データセットIDで紐づける

    Args:
        app: flaskのアプリケーションオブジェクト
        file_dir: リソースファイル置き場
        release_catalog: 登録する横断検索カタログ情報
        detail_catalog: 登録する詳細検索カタログ情報
        history_url: 来歴管理URL
        release_ckan_apikey: 横断検索用CKANapikey
        release_ckan_addr: 横断検索用CKANアドレス
        detail_ckan_apikey: 詳細検索CKANapikey
        detail_ckan_addr: 詳細検索用CKANアドレス

    Returns:
        message: カタログ登録結果メッセージ
        release: 横断検索カタログ登録結果
          - ckan_url: 登録した横断検索カタログのURL
          - pkg: 登録した横断検索カタログ情報
        detail: 詳細検索カタログ登録結果
          - ckan_url: 登録した詳細検索カタログのURL
          - pkg: 登録した詳細検索カタログ情報
    """

    app.logger.warning('=== regist_both ===')
    result = {
        'message': 'error',
        'release': {'ckan_url': None, 'pkg': None},
        'detail': {'ckan_url': None, 'pkg': None}
    }

    # 詳細検索用データセットID生成
    caddec_dataset_id_for_detail = str(uuid.uuid5(uuid.uuid4(), 'name'))
    # 横断検索カタログと詳細検索用カタログの詳細検索用データセットIDとして設定
    for _release in release_catalog['data_creator']:
        if _release['label'] == 'caddec_dataset_id_for_detail':
            _release['value'] = caddec_dataset_id_for_detail
            break
    for _detail in detail_catalog['data_creator']:
        if _detail['label'] == 'caddec_dataset_id_for_detail':
            _detail['value'] = caddec_dataset_id_for_detail
            break

    # 横断検索カタログ登録用データ作成
    packagename, description_url, extras, tags, resources, license_id, license_title, license_url = create_catalog(
        app, release_ckan_addr, file_dir, release_catalog, history_url, token)

    # 横断検索カタログのCKAN登録
    try:
        session = requests.Session()
        ckan_api = RemoteCKAN(
            release_ckan_addr, apikey=release_ckan_apikey, session=session)
        pkg = ckan_api.action.package_create(name=packagename,
                                             title=str(
                                                 release_catalog['catalogTitle']),
                                             notes=str(
                                                 release_catalog['catalogDescription']),
                                             url=str(description_url),
                                             extras=extras,
                                             tags=tags,
                                             resources=resources,
                                             license_id=license_id,
                                             license_title=license_title,
                                             license_url=license_url,
                                             owner_org=release_catalog['regist_org'])
        app.logger.warning('横断検索カタログ登録結果')
        app.logger.warning(json.dumps(pkg, indent=2, ensure_ascii=False))
        result['message'] = 'success'
        result['release']['pkg'] = pkg
        str_dataset = 'dataset/' if release_ckan_addr.endswith(
            '/') else '/dataset/'
        result['release']['ckan_url'] = str(
            release_ckan_addr) + str_dataset + str(packagename)

    except NotAuthorized:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ・詳細検索カタログ登録 横断検索用CKAN 認証エラー')
        raise CatalogToolException('regist_both_release_NotAuthorized', 500)
    except NotFound:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ・詳細検索カタログ登録 横断検索用CKAN 検索エラー')
        raise CatalogToolException('regist_both_release_NotFound', 500)
    except ValidationError:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ・詳細検索カタログ登録 横断検索用CKAN 変数エラー')
        raise CatalogToolException('regist_both_release_ValidationError', 500)
    except CKANAPIError:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ・詳細検索カタログ登録 横断検索用CKAN APIエラー')
        raise CatalogToolException('regist_both_release_CKANAPIError', 500)
    except ServerIncompatibleError:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ・詳細検索カタログ登録 横断検索用CKAN 互換性エラー')
        raise CatalogToolException(
            'regist_both_release_ServerIncompatibleError', 500)
    except AttributeError:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ・詳細検索カタログ登録 横断検索用CKAN 属性エラー')
        raise CatalogToolException('regist_both_release_AttributeError', 500)
    except Exception:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ・詳細検索カタログ登録 横断検索用CKAN 例外')
        raise CatalogToolException('regist_both_release_Exception', 500)

    # 詳細検索カタログ登録用データ作成
    packagename, description_url, extras, tags, resources, license_id, license_title, license_url = create_catalog(
        app, detail_ckan_addr, file_dir, detail_catalog, history_url, token)

    # 詳細検索カタログのCKAN登録
    try:
        session = requests.Session()
        ckan_api = RemoteCKAN(
            detail_ckan_addr, apikey=detail_ckan_apikey, session=session)
        pkg = ckan_api.action.package_create(name=packagename,
                                             title=str(
                                                 detail_catalog['catalogTitle']),
                                             notes=str(
                                                 detail_catalog['catalogDescription']),
                                             url=str(description_url),
                                             extras=extras,
                                             tags=tags,
                                             resources=resources,
                                             license_id=license_id,
                                             license_title=license_title,
                                             license_url=license_url,
                                             owner_org=detail_catalog['regist_org'])
        app.logger.warning('詳細検索カタログ登録結果')
        app.logger.warning(json.dumps(pkg, indent=2, ensure_ascii=False))
        result['message'] = 'success'
        result['detail']['pkg'] = pkg
        str_dataset = 'dataset/' if detail_ckan_addr.endswith(
            '/') else '/dataset/'
        result['detail']['ckan_url'] = str(
            detail_ckan_addr) + str_dataset + str(packagename)

    except NotAuthorized:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ・詳細検索カタログ登録 詳細検索用CKAN 認証エラー')
        raise CatalogToolException('regist_both_detail_NotAuthorized', 500)
    except NotFound:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ・詳細検索カタログ登録 詳細検索用CKAN 検索エラー')
        raise CatalogToolException('regist_both_detail_NotFound', 500)
    except ValidationError:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ・詳細検索カタログ登録 詳細検索用CKAN 変数エラー')
        raise CatalogToolException('regist_both_detail_ValidationError', 500)
    except CKANAPIError:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ・詳細検索カタログ登録 詳細検索用CKAN APIエラー')
        raise CatalogToolException('regist_both_detail_CKANAPIError', 500)
    except ServerIncompatibleError:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ・詳細検索カタログ登録 詳細検索用CKAN 互換性エラー')
        raise CatalogToolException(
            'regist_both_detail_ServerIncompatibleError', 500)
    except AttributeError:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ・詳細検索カタログ登録 詳細検索用CKAN 属性エラー')
        raise CatalogToolException('regist_both_detail_AttributeError', 500)
    except Exception:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ・詳細検索カタログ登録 詳細検索用CKAN 例外')
        raise CatalogToolException('regist_both_detail_Exception', 500)

    return result


def edit_release(app, file_dir, data, history_url, token, apikey, ckan_addr):
    """ 横断検索カタログを編集する

    Args:
        app: flaskのアプリケーションオブジェクト
        file_dir: リソースファイル置き場
        data: 編集するカタログ情報
        history_url: 来歴管理URL
        apikey: ユーザパスワード
        ckan_addr: 登録先CKANアドレス

    """

    data['selected_mode'] == 'edit'

    result = {
        'message': 'error',
        'ckan_url': '',
        'pkg': None
    }

    # CKANへデータの更新
    packagename, description_url, extras, tags, resources, license_id, license_title, license_url = create_catalog(
        app, ckan_addr, file_dir, data, history_url, token)
    packagename = data['ckan_data_name']

    try:
        session = requests.Session()
        ckan_api = RemoteCKAN(ckan_addr, apikey=apikey, session=session)
        pkg = ckan_api.action.package_update(name=(data['ckan_data_name']),
                                             title=str(data['catalogTitle']),
                                             notes=str(
                                                 data['catalogDescription']),
                                             url=str(description_url),
                                             extras=extras,
                                             tags=tags,
                                             resources=resources,
                                             license_id=license_id,
                                             license_title=license_title,
                                             license_url=license_url,
                                             owner_org=data['regist_org'])

        result['message'] = 'success'
        str_dataset = 'dataset/' if ckan_addr.endswith('/') else '/dataset/'
        result['ckan_url'] = str(ckan_addr) + str_dataset + str(packagename)
        result['pkg'] = pkg

    except NotAuthorized:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ編集 横断検索用CKAN 認証エラー')
        raise CatalogToolException('edit_release_NotAuthorized', 500)
    except NotFound:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ編集 横断検索用CKAN 検索エラー')
        raise CatalogToolException('edit_release_NotFound', 500)
    except ValidationError:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ編集 横断検索用CKAN 変数エラー')
        raise CatalogToolException('edit_release_ValidationError', 500)
    except CKANAPIError:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ編集 横断検索用CKAN APIエラー')
        raise CatalogToolException('edit_release_CKANAPIError', 500)
    except ServerIncompatibleError:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ編集 横断検索用CKAN 互換性エラー')
        raise CatalogToolException('edit_release_ServerIncompatibleError', 500)
    except AttributeError:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ編集 横断検索用CKAN 属性エラー')
        raise CatalogToolException('edit_release_AttributeError', 500)
    except Exception:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ編集 横断検索用CKAN 例外')
        raise CatalogToolException('edit_release_Exception', 500)

    return result


def edit_detail(app, file_dir, data, history_url, token, apikey, ckan_addr):
    """ 詳細検索カタログを編集する

    Args:
        app: flaskのアプリケーションオブジェクト
        file_dir: リソースファイル置き場
        data: 編集するカタログ情報
        history_url: 来歴管理URL
        apikey: ユーザパスワード
        ckan_addr: 登録先CKANアドレス

    """

    data['selected_mode'] == 'edit'

    result = {
        'message': 'error',
        'ckan_url': '',
        'pkg': None
    }

    # CKANへデータの更新
    packagename, description_url, extras, tags, resources, license_id, license_title, license_url = create_catalog(
        app, ckan_addr, file_dir, data, history_url, token)
    packagename = data['ckan_data_name']

    try:
        session = requests.Session()
        ckan_api = RemoteCKAN(ckan_addr, apikey=apikey, session=session)

        pkg = ckan_api.action.package_update(name=(data['ckan_data_name']),
                                             title=str(data['catalogTitle']),
                                             notes=str(
                                                 data['catalogDescription']),
                                             url=str(description_url),
                                             extras=extras,
                                             tags=tags,
                                             resources=resources,
                                             license_id=license_id,
                                             license_title=license_title,
                                             license_url=license_url,
                                             owner_org=data['regist_org'])

        result['message'] = 'success'
        str_dataset = 'dataset/' if ckan_addr.endswith('/') else '/dataset/'
        result['ckan_url'] = str(ckan_addr) + str_dataset + str(packagename)
        result['pkg'] = pkg

    except NotAuthorized:
        app.logger.error(traceback.format_exc())
        app.logger.error('詳細検索カタログ編集 詳細検索用CKAN 認証エラー')
        raise CatalogToolException('edit_detail_NotAuthorized', 500)
    except NotFound:
        app.logger.error(traceback.format_exc())
        app.logger.error('詳細検索カタログ編集 詳細検索用CKAN 検索エラー')
        raise CatalogToolException('edit_detail_NotFound', 500)
    except ValidationError:
        app.logger.error(traceback.format_exc())
        app.logger.error('詳細検索カタログ編集 詳細検索用CKAN 変数エラー')
        raise CatalogToolException('edit_detail_ValidationError', 500)
    except CKANAPIError:
        app.logger.error(traceback.format_exc())
        app.logger.error('詳細検索カタログ編集 詳細検索用CKAN APIエラー')
        raise CatalogToolException('edit_detail_CKANAPIError', 500)
    except ServerIncompatibleError:
        app.logger.error(traceback.format_exc())
        app.logger.error('詳細検索カタログ編集 詳細検索用CKAN 互換性エラー')
        raise CatalogToolException('edit_detail_ServerIncompatibleError', 500)
    except AttributeError:
        app.logger.error(traceback.format_exc())
        app.logger.error('詳細検索カタログ編集 詳細検索用CKAN 属性エラー')
        raise CatalogToolException('edit_detail_AttributeError', 500)
    except Exception:
        app.logger.error(traceback.format_exc())
        app.logger.error('詳細検索カタログ編集 詳細検索用CKAN 例外')
        raise CatalogToolException('edit_detail_Exception', 500)

    return result


def edit_both(app, file_dir, release_catalog, detail_catalog, history_url, token,
              release_ckan_apikey, release_ckan_addr, detail_ckan_apikey=None, detail_ckan_addr=None):
    """ 横断検索カタログ・詳細検索カタログを編集する

    Args:
        app: flaskのアプリケーションオブジェクト
        file_dir: リソースファイル置き場
        release_catalog: 登録する横断検索カタログ情報
        detail_catalog: 登録する横断検索カタログ情報
        history_url: 来歴管理URL
        release_ckan_apikey: 横断CKAN用ユーザパスワード
        release_ckan_addr: 横断用登録先CKANアドレス
        detail_ckan_apikey: 詳細CKAN用ユーザパスワード
        detail_ckan_addr: 詳細用登録先CKANアドレス

    """

    release_catalog['selected_mode'] == 'edit'
    detail_catalog['selected_mode'] == 'edit'

    result = {
        'message': 'error',
        'release': {'ckan_url': '', 'pkg': None},
        'detail': {'ckan_url': '', 'pkg': None}
    }

    # 横断検索カタログ編集
    ret_edit_release = edit_release(
        app, file_dir, release_catalog, history_url, token, release_ckan_apikey, release_ckan_addr)

    result['message'] = ret_edit_release['message']
    result['release']['ckan_url'] = ret_edit_release['ckan_url']
    result['release']['pkg'] = ret_edit_release['pkg']

    # 詳細検索カタログ編集
    ret_edit_detail = edit_detail(
        app, file_dir, detail_catalog, history_url, token, detail_ckan_apikey, detail_ckan_addr)

    result['message'] = ret_edit_detail['message']
    result['detail']['ckan_url'] = ret_edit_detail['ckan_url']
    result['detail']['pkg'] = ret_edit_detail['pkg']

    return result


def update_catalog_caddec_dataset_id_for_detail(app, update_ckan_type, organization,
                                                ckan_api, caddec_dataset_id_for_detail):
    """削除対象のカタログと紐づくカタログの詳細検索用データセットIDを空値で更新する

        Arguments:
        app: flaskのアプリケーションオブジェクト
            update_ckan_type: 更新対象となるカタログの登録先CKAN
            organization: 組織情報
            ckan_api: 更新対象となるカタログのAPI
            caddec_dataset_id_for_detail: 詳細検索用データセットID
    """

    # 詳細検索用データセットIDが設定されている場合は、紐づくカタログを検索
    sub_query = 'caddec_dataset_id_for_detail:' + \
        str(caddec_dataset_id_for_detail)
    try:
        if organization:
            # ユーザに紐づく組織情報あり
            for _org in organization:
                filter = 'organization:' + _org
                sub_catalog = ckan_api.action.package_search(
                    q=sub_query, fq=filter)
                if sub_catalog:
                    break
        else:
            # ユーザに紐づく組織情報なし
            sub_catalog = ckan_api.action.package_search(q=sub_query)

    except NotAuthorized:
        app.logger.error('カタログ検索 認証エラー')
        message_id = 'update_catalog_caddec_dataset_id_for_detail_search_' + \
            update_ckan_type + '_NotAuthorized'
        raise CatalogToolException(message_id, 500)
    except NotFound:
        app.logger.warning(
            '紐づく詳細検索カタログ[caddec_dataset_id_for_detail:' + caddec_dataset_id_for_detail + '] なし')
        return
    except ValidationError:
        app.logger.error('カタログ検索 変数エラー')
        message_id = 'update_catalog_caddec_dataset_id_for_detail_search_' + \
            update_ckan_type + '_ValidationError'
        raise CatalogToolException(message_id, 500)
    except CKANAPIError:
        app.logger.error('カタログ検索 APIエラー')
        message_id = 'update_catalog_caddec_dataset_id_for_detail_search_' + \
            update_ckan_type + '_CKANAPIError'
        raise CatalogToolException(message_id, 500)
    except ServerIncompatibleError:
        app.logger.error('カタログ検索 互換性エラー')
        message_id = 'update_catalog_caddec_dataset_id_for_detail_search_' + \
            update_ckan_type + '_ServerIncompatibleError'
        raise CatalogToolException(message_id, 500)
    except AttributeError:
        app.logger.error('カタログ検索 属性エラー')
        message_id = 'update_catalog_caddec_dataset_id_for_detail_search_' + \
            update_ckan_type + '_AttributeError'
        raise CatalogToolException(message_id, 500)
    except Exception:
        app.logger.error('カタログ検索 例外')
        message_id = 'update_catalog_caddec_dataset_id_for_detail_search_' + \
            update_ckan_type + '_Exception'
        raise CatalogToolException(message_id, 500)

    if not sub_catalog:
        # 紐づくカタログなし
        return

    sub_catalog = sub_catalog['results'][0]

    # 紐づくカタログの詳細検索用データセットIDを未設定でカタログ更新をする
    for _extra in sub_catalog['extras']:
        if not _extra['key'] == 'caddec_dataset_id_for_detail':
            continue
        app.logger.warning('sub_catalog[extras]')
        app.logger.warning(sub_catalog['extras'])
        _extra['value'] = ''

    try:
        ckan_api.action.package_update(name=str(sub_catalog['name']),
                                       title=str(sub_catalog['title']),
                                       notes=str(sub_catalog['notes']),
                                       url=str(sub_catalog['url']),
                                       extras=sub_catalog['extras'],
                                       tags=sub_catalog['tags'],
                                       resources=sub_catalog['resources'],
                                       license_id=sub_catalog['license_id'],
                                       license_title=sub_catalog['license_title'],
                                       license_url=sub_catalog['license_url'],
                                       owner_org=sub_catalog['owner_org'])

    except NotAuthorized:
        app.logger.error('カタログ更新 認証エラー')
        message_id = 'update_catalog_caddec_dataset_id_for_detail_update_' + \
            update_ckan_type + '_NotAuthorized'
        raise CatalogToolException(message_id, 500)
    except NotFound:
        app.logger.error('カタログ更新 検索エラー')
        message_id = 'update_catalog_caddec_dataset_id_for_detail_update_' + \
            update_ckan_type + '_NotFound'
        raise CatalogToolException(message_id, 500)
    except ValidationError:
        app.logger.error('カタログ更新 変数エラー')
        message_id = 'update_catalog_caddec_dataset_id_for_detail_update_' + \
            update_ckan_type + '_ValidationError'
        raise CatalogToolException(message_id, 500)
    except CKANAPIError:
        app.logger.error('カタログ更新 APIエラー')
        message_id = 'update_catalog_caddec_dataset_id_for_detail_update_' + \
            update_ckan_type + '_CKANAPIError'
        raise CatalogToolException(message_id, 500)
    except ServerIncompatibleError:
        app.logger.error('カタログ更新 互換性エラー')
        message_id = 'update_catalog_caddec_dataset_id_for_detail_update_' + \
            update_ckan_type + '_ServerIncompatibleError'
        raise CatalogToolException(message_id, 500)
    except AttributeError:
        app.logger.error('カタログ更新 属性エラー')
        message_id = 'update_catalog_caddec_dataset_id_for_detail_update_' + \
            update_ckan_type + '_AttributeError'
        raise CatalogToolException(message_id, 500)
    except Exception:
        app.logger.error('カタログ更新 例外')
        message_id = 'update_catalog_caddec_dataset_id_for_detail_update_' + \
            update_ckan_type + '_Exception'
        raise CatalogToolException(message_id, 500)


def search_delete_catalog(app, delete_ckan_type, organization, ckan_api, ckan_addr, id):

    ckan_url = None
    title = None
    caddec_dataset_id_for_detail = None

    # 削除対象のカタログをidから検索
    try:
        main_catalog = ckan_api.action.package_show(id=id)
        if organization:
            # 指定された組織名と一致しないカタログであればNotFound
            if not organization == main_catalog['organization']['name']:
                raise NotFound

    except NotAuthorized:
        app.logger.error('カタログ検索 認証エラー')
        message_id = 'search_delete_catalog_' + delete_ckan_type + '_NotAuthorized'
        raise CatalogToolException(message_id, 500)
    except NotFound:
        app.logger.warning('該当するカタログ[id:' + id + '] なし')
        return ckan_url, title, caddec_dataset_id_for_detail
    except ValidationError:
        app.logger.error('カタログ検索 変数エラー')
        message_id = 'search_delete_catalog_' + delete_ckan_type + '_ValidationError'
        raise CatalogToolException(message_id, 500)
    except CKANAPIError:
        app.logger.error('カタログ検索 APIエラー')
        message_id = 'search_delete_catalog_' + delete_ckan_type + '_CKANAPIError'
        raise CatalogToolException(message_id, 500)
    except ServerIncompatibleError:
        app.logger.error('カタログ検索 互換性エラー')
        message_id = 'search_delete_catalog_' + \
            delete_ckan_type + '_ServerIncompatibleError'
        raise CatalogToolException(message_id, 500)
    except AttributeError:
        app.logger.error('カタログ検索 属性エラー')
        message_id = 'search_delete_catalog_' + delete_ckan_type + '_AttributeError'
        raise CatalogToolException(message_id, 500)
    except Exception:
        app.logger.error('カタログ検索 例外')
        message_id = 'search_delete_catalog_' + delete_ckan_type + '_Exception'
        raise CatalogToolException(message_id, 500)

    str_dataset = 'dataset/' if ckan_addr.endswith('/') else '/dataset/'
    ckan_url = str(ckan_addr) + str_dataset + main_catalog['name']
    title = main_catalog['title']

    # 詳細検索用データセットID取得
    for _extra in main_catalog['extras']:
        if not _extra['key'] == 'caddec_dataset_id_for_detail':
            continue
        if not _extra['value']:
            app.logger.warning('main_catalog[extras]')
            app.logger.warning(main_catalog['extras'])
            caddec_dataset_id_for_detail = _extra['value']
            break

    return ckan_url, title, caddec_dataset_id_for_detail


def delete_catalogs(app, organization, release_catalog, detail_catalog, release_ckan_apikey,
                    release_ckan_addr, detail_ckan_apikey, detail_ckan_addr):
    """CKANからカタログを削除する

        Arguments:
            organization: 組織情報
            release_catalog: 削除対象となる横断検索カタログのIDリスト
            detail_catalog: 削除対象となる詳細検索カタログのIDリスト
            release_ckan_apikey: 横断CKAN用ユーザパスワード
            release_ckan_addr: 横断用登録先CKANアドレス
            detail_ckan_apikey: 詳細CKAN用ユーザパスワード
            detail_ckan_addr: 詳細用登録先CKANアドレス
    """

    app.logger.warning('delete_catalogs')
    app.logger.warning('release_catalog')
    app.logger.warning(release_catalog)
    app.logger.warning('detail_catalog')
    app.logger.warning(detail_catalog)

    # 'release': [ { 'ckan_url': '', 'title': '' } ]
    # 'detail': [ { 'ckan_url': '', 'title': '' } ]
    result = {
        'message': 'suceess',
        'release': [],
        'detail': []
    }

    release_ckan = None
    detail_ckan = None
    if release_catalog:
        release_ckan = connect_ckan(release_ckan_apikey, release_ckan_addr)
        if detail_ckan_apikey and detail_ckan_addr:
            detail_ckan = connect_ckan(detail_ckan_apikey, detail_ckan_addr)
        for release_id in release_catalog:
            delete_catalog = {
                'ckan_url': '',
                'title': ''
            }
            # 削除対象のカタログをidから検索
            try:
                ckan_url, title, caddec_dataset_id_for_detail = search_delete_catalog(
                    app, 'release', organization, release_ckan, release_ckan_addr, release_id)
                delete_catalog['ckan_url'] = ckan_url
                delete_catalog['title'] = title
                delete_catalog['caddec_dataset_id_for_detail'] = caddec_dataset_id_for_detail

                # 詳細検索用CKAN接続している、かつ、詳細検索用データセットIDが設定されている場合
                if detail_ckan and caddec_dataset_id_for_detail:
                    update_catalog_caddec_dataset_id_for_detail(
                        app, 'detail', organization, detail_ckan, caddec_dataset_id_for_detail)

            except CatalogToolException as e:
                # 削除対象のカタログ取得失敗
                app.logger.warning('削除対象カタログ検索：' + e.message_id)
                result['message'] += '\n' + e.message_id
                continue

            try:
                release_ckan.action.package_delete(id=release_id)

            except NotAuthorized:
                app.logger.warning('横断検索カタログ削除 認証エラー')
                result['message'] += '\n' + \
                    'delete_catalogs_release_NotAuthorized'
                continue
            except NotFound:
                app.logger.warning('横断検索カタログ削除 検索エラー')
                result['message'] += '\n' + 'delete_catalogs_release_NotFound'
                continue
            except ValidationError:
                app.logger.warning('横断検索カタログ削除 変数エラー')
                result['message'] += '\n' + \
                    'delete_catalogs_release_ValidationError'
                continue
            except CKANAPIError:
                app.logger.warning('横断検索カタログ削除 APIエラー')
                result['message'] += '\n' + \
                    'delete_catalogs_release_CKANAPIError'
                continue
            except ServerIncompatibleError:
                app.logger.warning('横断検索カタログ削除 互換性エラー')
                result['message'] += '\n' + \
                    'delete_catalogs_release_ServerIncompatibleError'
                continue
            except AttributeError:
                app.logger.warning('横断検索カタログ削除 属性エラー')
                result['message'] += '\n' + \
                    'delete_catalogs_release_AttributeError'
                continue
            except Exception:
                app.logger.warning('横断検索カタログ削除 例外')
                result['message'] += '\n' + 'delete_catalogs_release_Exception'
                continue

            result['release'].append(delete_catalog)

    if detail_catalog:
        detail_ckan = connect_ckan(detail_ckan_apikey, detail_ckan_addr)
        if release_ckan_apikey and release_ckan_addr:
            release_ckan = connect_ckan(release_ckan_apikey, release_ckan_addr)
        for detail_id in detail_catalog:
            delete_catalog = {
                'ckan_url': '',
                'title': ''
            }
            # 削除対象のカタログをidから検索
            try:
                ckan_url, title, caddec_dataset_id_for_detail = search_delete_catalog(
                    app, 'detail', organization, detail_ckan, detail_ckan_addr, detail_id)
                delete_catalog['ckan_url'] = ckan_url
                delete_catalog['title'] = title
                delete_catalog['caddec_dataset_id_for_detail'] = caddec_dataset_id_for_detail

                # 詳細検索用CKAN接続している、かつ、詳細検索用データセットIDが設定されている場合
                if release_ckan and caddec_dataset_id_for_detail:
                    update_catalog_caddec_dataset_id_for_detail(
                        app, 'release', organization, release_ckan, caddec_dataset_id_for_detail)

            except CatalogToolException as e:
                # 削除対象のカタログ取得失敗
                app.logger.warning('削除対象カタログ検索：' + e.message_id)
                result['message'] += '\n' + e.message_id
                continue

            try:
                detail_ckan.action.package_delete(id=detail_id)

            except NotAuthorized:
                app.logger.warning('詳細検索カタログ削除 認証エラー')
                result['message'] += '\n' + \
                    'delete_catalogs_detail_NotAuthorized'
                continue
            except NotFound:
                app.logger.warning('詳細検索カタログ削除 検索エラー')
                result['message'] += '\n' + 'delete_catalogs_detail_NotFound'
                continue
            except ValidationError:
                app.logger.warning('詳細検索カタログ削除 変数エラー')
                result['message'] += '\n' + \
                    'delete_catalogs_detail_ValidationError'
                continue
            except CKANAPIError:
                app.logger.warning('詳細検索カタログ削除 APIエラー')
                result['message'] += '\n' + \
                    'delete_catalogs_detail_CKANAPIError'
                continue
            except ServerIncompatibleError:
                app.logger.warning('詳細検索カタログ削除 互換性エラー')
                result['message'] += '\n' + \
                    'delete_catalogs_detail_ServerIncompatibleError'
                continue
            except AttributeError:
                app.logger.warning('詳細検索カタログ削除 属性エラー')
                result['message'] += '\n' + \
                    'delete_catalogs_detail_AttributeError'
                continue
            except Exception:
                app.logger.warning('詳細検索カタログ削除 例外')
                result['message'] += '\n' + 'delete_catalogs_detail_Exception'
                continue

            result['detail'].append(delete_catalog)

    if not result['message']:
        result['message'] = 'success'

    result['message'].lstrip('\n')

    return result


def search_both(app, keyword, url, organization, release_ckan_apikey, release_ckan_addr,
                detail_ckan_apikey, detail_ckan_addr, start=0, rows=1000):
    """ 横断・詳細検索カタログ検索

        Args:
          app: flaskのアプリケーションオブジェクト
          keyword: 検索キーワード
          url: CKANデータセット名
          release_ckan_apikey: 横断CKANアプリキー
          release_ckan_addr: 横断CKANアドレス
          detail_ckan_apikey: 詳細CKANアプリキー
          detail_ckan_addr: 詳細CKANアドレス
          start: 検索結果取得開始位置
          rows: 検索結果取得数

        Returns:
          検索したカタログ情報
          {
              'message': 'message',
              'datasets': [
                  {
                      'release': { カタログデータ },
                      'detail': { カタログデータ }
                  }
              ]
          }
    """

    result = {
        'message': 'error',
        'datasets': []
    }

    # tmp_result = [ { 'organization' : 'organization', 'catalogs':[ {'release': {}, 'detail': {} ] } ]
    tmp_result = []

    if not organization:
        data = {
            'organization': None,
            'catalogs': []
        }
        tmp_result.append(data)
    else:
        for user_org in organization:
            data = {
                'organization': '',
                'catalogs': []
            }
            data['organization'] = user_org
            tmp_result.append(data)

    try:
        # 横断検索用CKAN接続
        release_ckan = connect_ckan(release_ckan_apikey, release_ckan_addr)

        # 横断検索用CKAN検索
        release_datasets = {}
        if url:
            search_result = release_ckan.action.package_show(id=url)
            for __data in tmp_result:
                if __data['organization'] == search_result['organization']['name'] or __data['organization'] is None:
                    # 取得データの組織とユーザの組織が一致する場合、検索結果とする（管理者ユーザの場合は組織名一致の判定不要）
                    __data['catalogs'].append(
                        {'release': search_result, 'detail': {}})
        else:
            for __data in tmp_result:
                if __data['organization'] is None:
                    # 組織フィルタ―なし
                    release_datasets = release_ckan.action.package_search(
                        q=keyword, start=start, rows=rows)
                else:
                    # 組織フィルターあり
                    filter = 'organization:' + __data['organization']
                    release_datasets = release_ckan.action.package_search(
                        q=keyword, fq=filter, start=start, rows=rows)

                if not release_datasets['results']:
                    continue

                for __result in release_datasets['results']:
                    __data['catalogs'].append(
                        {'release': __result, 'detail': {}})

    except NotAuthorized:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ検索 横断検索用CKAN 認証エラー')
        raise CatalogToolException('search_both_release_NotAuthorized', 500)
    except NotFound:
        # カタログが見つからない場合はスルー
        app.logger.error('横断検索カタログ検索 横断検索用CKAN 検索エラー')
        result['message'] = '横断検索用CKANに該当カタログはありません。'
    except ValidationError:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ検索 横断検索用CKAN 変数エラー')
        raise CatalogToolException('search_both_release_ValidationError', 500)
    except CKANAPIError:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ検索 横断検索用CKAN APIエラー')
        raise CatalogToolException('search_both_release_CKANAPIError', 500)
    except ServerIncompatibleError:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ検索 横断検索用CKAN 互換性エラー')
        raise CatalogToolException(
            'search_both_release_ServerIncompatibleError', 500)
    except AttributeError:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ検索 横断検索用CKAN 属性エラー')
        raise CatalogToolException('search_both_release_AttributeError', 500)
    except Exception:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ検索 横断検索用CKAN 例外')
        raise CatalogToolException('search_both_release_Exception', 500)

    if not detail_ckan_apikey or not detail_ckan_addr:
        # 詳細検索用CKANの設定なし
        app.logger.warning('詳細検索用カタログ未接続')
        result['message'] = 'success'
        for __result in tmp_result:
            for __dataset in __result['catalogs']:
                result['datasets'].append(__dataset)
        return result

    try:
        # 詳細検索用CKAN接続
        detail_ckan = connect_ckan(detail_ckan_apikey, detail_ckan_addr)

        # 詳細検索用CKAN検索
        detail_datasets = {}
        if url:
            search_result = detail_ckan.action.package_show(id=url)
            for __data in tmp_result:
                if __data['organization'] == search_result['organization']['name'] or __data['organization'] is None:
                    # 取得データの組織とユーザの組織が一致する場合、検索結果とする（管理者ユーザの場合は組織名一致の判定不要）
                    # __data['catalogs'].append({'release': search_result, 'detail': {}})

                    # 詳細検索結果から、詳細検索用データセットID取得
                    detail_caddec_dataset_id_for_detail = ''
                    for __extra in search_result['extras']:
                        if not __extra['key'] == 'caddec_dataset_id_for_detail':
                            # 詳細検索用データセットID以外読み飛ばし
                            continue
                        if not __extra['value']:
                            # 詳細検索用データセットIDの設定なし
                            break

                        detail_caddec_dataset_id_for_detail = __extra['value']

                    # 詳細検索結果から、詳細検索用データセットIDが見つからない場合、単独のカタログとして追加
                    if not detail_caddec_dataset_id_for_detail:
                        __data['catalogs'].append(
                            {'release': {}, 'detail': search_result})
                        continue

                    # 横断検索結果から、詳細検索用データセットIDが紐づくカタログを検索して紐づける
                    for __dataset in __data['catalogs']:
                        if not __dataset['release']:
                            # 横断検索カタログが設定されていない（詳細検索カタログ単独の場合）は読み飛ばし
                            continue

                        # 横断検索結果から、詳細検索用データセットID取得
                        release_caddec_dataset_id_for_detail = ''
                        for __extra in __dataset['release']['extras']:
                            if not __extra['key'] == 'caddec_dataset_id_for_detail':
                                # 詳細検索用データセットID以外読み飛ばし
                                continue
                            if not __extra['value']:
                                # 詳細検索用データセットIDの設定なし
                                break

                            release_caddec_dataset_id_for_detail = __extra['value']

                        # 横断検索結果から、詳細検索用データセットIDが見つからない場合は、単独のカタログとして読み飛ばし
                        if not release_caddec_dataset_id_for_detail:
                            continue

                        if detail_caddec_dataset_id_for_detail == release_caddec_dataset_id_for_detail:
                            # 横断検索カタログと詳細検索カタログの詳細検索用データセットIDが一致した場合は、同じ場所に追加
                            __dataset['detail'] = search_result
                            break

                    # 横断検索結果の詳細検索用データセットIDをチェックして、紐づく横断検索カタログが見つからなかった場合、単独のカタログとして追加
                    if not (detail_caddec_dataset_id_for_detail == release_caddec_dataset_id_for_detail):
                        __data['catalogs'].append(
                            {'release': {}, 'detail': search_result})

        else:
            for __data in tmp_result:
                if __data['organization'] is None:
                    # 組織フィルタ―なし
                    detail_datasets = detail_ckan.action.package_search(
                        q=keyword, start=start, rows=rows)
                else:
                    # 組織フィルターあり
                    filter = 'organization:' + __data['organization']
                    detail_datasets = detail_ckan.action.package_search(
                        q=keyword, fq=filter, start=start, rows=rows)

                if not detail_datasets['results']:
                    continue

                for __detail in detail_datasets['results']:
                    # 詳細検索結果から、詳細検索用データセットID取得
                    detail_caddec_dataset_id_for_detail = ''
                    for __extra in __detail['extras']:
                        if not __extra['key'] == 'caddec_dataset_id_for_detail':
                            # 詳細検索用データセットID以外読み飛ばし
                            continue
                        if not __extra['value']:
                            # 詳細検索用データセットIDの設定なし
                            break

                        detail_caddec_dataset_id_for_detail = __extra['value']

                    # 詳細検索結果から、詳細検索用データセットIDが見つからない場合、単独のカタログとして追加
                    if not detail_caddec_dataset_id_for_detail:
                        __data['catalogs'].append(
                            {'release': {}, 'detail': __detail})
                        continue

                    # 横断検索結果から、詳細検索用データセットIDが紐づくカタログを検索して紐づける
                    for __dataset in __data['catalogs']:
                        if not __dataset['release']:
                            # 横断検索カタログが設定されていない（詳細検索カタログ単独の場合）は読み飛ばし
                            continue

                        # 横断検索結果から、詳細検索用データセットID取得
                        release_caddec_dataset_id_for_detail = ''
                        for __extra in __dataset['release']['extras']:
                            if not __extra['key'] == 'caddec_dataset_id_for_detail':
                                # 詳細検索用データセットID以外読み飛ばし
                                continue
                            if not __extra['value']:
                                # 詳細検索用データセットIDの設定なし
                                break

                            release_caddec_dataset_id_for_detail = __extra['value']

                        # 横断検索結果から、詳細検索用データセットIDが見つからない場合は、単独のカタログとして読み飛ばし
                        if not release_caddec_dataset_id_for_detail:
                            continue

                        if detail_caddec_dataset_id_for_detail == release_caddec_dataset_id_for_detail:
                            # 横断検索カタログと詳細検索カタログの詳細検索用データセットIDが一致した場合は、同じ場所に追加
                            __dataset['detail'] = __detail
                            break

                    # 横断検索結果の詳細検索用データセットIDをチェックして、紐づく横断検索カタログが見つからなかった場合、単独のカタログとして追加
                    if not detail_caddec_dataset_id_for_detail == release_caddec_dataset_id_for_detail:
                        __data['catalogs'].append(
                            {'release': {}, 'detail': __detail})

    except NotAuthorized:
        app.logger.error(traceback.format_exc())
        app.logger.error('詳細検索カタログ検索 詳細検索用CKAN 認証エラー')
        raise CatalogToolException('search_both_detail_NotAuthorized', 500)
    except NotFound:
        # カタログが見つからない場合はスルー
        app.logger.error('詳細検索カタログ検索 詳細検索用CKAN 検索エラー')
        result['message'] = '詳細検索用CKANに該当カタログはありません。'
    except ValidationError:
        app.logger.error(traceback.format_exc())
        app.logger.error('詳細検索カタログ検索 詳細検索用CKAN 変数エラー')
        raise CatalogToolException('search_both_detail_ValidationError', 500)
    except CKANAPIError:
        app.logger.error(traceback.format_exc())
        app.logger.error('詳細検索カタログ検索 詳細検索用CKAN APIエラー')
        raise CatalogToolException('search_both_detail_CKANAPIError', 500)
    except ServerIncompatibleError:
        app.logger.error(traceback.format_exc())
        app.logger.error('詳細検索カタログ検索 詳細検索用CKAN 互換性エラー')
        raise CatalogToolException(
            'search_both_detail_ServerIncompatibleError', 500)
    except AttributeError:
        app.logger.error(traceback.format_exc())
        app.logger.error('詳細検索カタログ検索 詳細検索用CKAN 属性エラー')
        raise CatalogToolException('search_both_detail_AttributeError', 500)
    except Exception:
        app.logger.error(traceback.format_exc())
        app.logger.error('詳細検索カタログ検索 詳細検索用CKAN 例外')
        raise CatalogToolException('search_both_detail_Exception', 500)

    # カタログデータのみを検索結果として返す
    for __result in tmp_result:
        for __dataset in __result['catalogs']:
            result['datasets'].append(__dataset)

    result['message'] = 'success'

    return result


def search_release(app, keyword, url, organization, release_ckan_apikey, release_ckan_addr,
                   detail_ckan_apikey=None, detail_ckan_addr=None, start=0, rows=1000):
    """ 横断検索カタログ検索

        Args:
          app: flaskのアプリケーションオブジェクト
          keyword: 検索キーワード
          url: CKANデータセット名
          release_ckan_apikey: 横断CKANアプリキー
          release_ckan_addr: 横断CKANアドレス
          detail_ckan_apikey: 詳細CKANアプリキー
          detail_ckan_addr: 詳細CKANアドレス
          start: 検索開始位置
          rows: 検索結果数

        Returns:
          検索したカタログ情報
    """

    result = {
        'message': 'error',
        'datasets': []
    }

    tmp_result = []

    if not organization:
        data = {
            'organization': None,
            'catalogs': []
        }
        tmp_result.append(data)
    else:
        for user_org in organization:
            data = {
                'organization': '',
                'catalogs': []
            }
            data['organization'] = user_org
            tmp_result.append(data)

    try:
        # 横断検索用CKAN接続
        release_ckan = connect_ckan(release_ckan_apikey, release_ckan_addr)

        # 横断検索用CKAN検索
        if url:
            search_result = release_ckan.action.package_show(id=url)
            for __data in tmp_result:
                if __data['organization'] == search_result['organization']['name'] or __data['organization'] is None:
                    # 取得データの組織とユーザの組織が一致する場合、検索結果とする（管理者ユーザの場合は組織名一致の判定不要）
                    __data['catalogs'].append(
                        {'release': search_result, 'detail': {}})
        else:
            for __data in tmp_result:
                release_datasets = {}
                if __data['organization'] is None:
                    # 組織フィルタ―なし
                    release_datasets = release_ckan.action.package_search(
                        q=keyword, start=start, rows=rows)
                else:
                    # 組織フィルターあり
                    filter = 'organization:' + __data['organization']
                    release_datasets = release_ckan.action.package_search(
                        q=keyword, fq=filter, start=start, rows=rows)

                if not release_datasets['results']:
                    continue
                for __result in release_datasets['results']:
                    __data['catalogs'].append(
                        {'release': __result, 'detail': {}})

    except NotAuthorized:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ検索 横断検索用CKAN 認証エラー')
        raise CatalogToolException('search_release_release_NotAuthorized', 500)
    except NotFound:
        # カタログが見つからない場合はスルー
        app.logger.error('横断検索カタログ検索 横断検索用CKAN 検索エラー')
        result['message'] = '横断検索用CKANに該当カタログはありません。'
    except ValidationError:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ検索 横断検索用CKAN 変数エラー')
        raise CatalogToolException(
            'search_release_release_ValidationError', 500)
    except CKANAPIError:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ検索 横断検索用CKAN APIエラー')
        raise CatalogToolException('search_release_release_CKANAPIError', 500)
    except ServerIncompatibleError:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ検索 横断検索用CKAN 互換性エラー')
        raise CatalogToolException(
            'search_release_release_ServerIncompatibleError', 500)
    except AttributeError:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ検索 横断検索用CKAN 属性エラー')
        raise CatalogToolException(
            'search_release_release_AttributeError', 500)
    except Exception:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ検索 横断検索用CKAN 例外')
        raise CatalogToolException('search_release_release_Exception', 500)

    if not detail_ckan_apikey or not detail_ckan_addr:
        # 詳細検索用CKANの設定なし
        app.logger.warning('詳細検索用カタログ未接続')
        result['message'] = 'success'
        for __result in tmp_result:
            for __dataset in __result['catalogs']:
                result['datasets'].append(__dataset)
        return result

    try:
        # 詳細検索用CKAN接続
        detail_ckan = connect_ckan(detail_ckan_apikey, detail_ckan_addr)

        # 詳細検索用CKAN検索
        for __data in tmp_result:
            for __catalog in __data['catalogs']:
                for __extra in __catalog['release']['extras']:

                    if not __extra['key'] == 'caddec_dataset_id_for_detail':
                        # 詳細検索用データセットID以外読み飛ばし
                        continue

                    if not __extra['value']:
                        # 詳細検索用データセットIDの設定なし
                        break

                    caddec_dataset_id_for_detail = __extra['value']
                    search_word = 'caddec_dataset_id_for_detail:' + \
                        str(caddec_dataset_id_for_detail)
                    detail_datasets = {}
                    if __data['organization'] is None:
                        # 組織フィルタ―なし
                        detail_datasets = detail_ckan.action.package_search(
                            q=search_word)
                    else:
                        # 組織フィルタ―あり
                        filter = 'organization:' + __data['organization']
                        detail_datasets = detail_ckan.action.package_search(
                            q=search_word, fq=filter)

                    if detail_datasets['results']:
                        __catalog['detail'] = detail_datasets['results'][0]

    except NotAuthorized:
        app.logger.error(traceback.format_exc())
        app.logger.error('詳細検索カタログ検索 詳細検索用CKAN 認証エラー')
        raise CatalogToolException('search_release_detail_NotAuthorized', 500)
    except NotFound:
        # カタログが見つからない場合はスルー
        app.logger.error('詳細検索カタログ検索 詳細検索用CKAN 検索エラー')
        result['message'] = '詳細検索用CKANに該当カタログはありません。'
    except ValidationError:
        app.logger.error(traceback.format_exc())
        app.logger.error('詳細検索カタログ検索 詳細検索用CKAN 変数エラー')
        raise CatalogToolException(
            'search_release_detail_ValidationError', 500)
    except CKANAPIError:
        app.logger.error(traceback.format_exc())
        app.logger.error('詳細検索カタログ検索 詳細検索用CKAN APIエラー')
        raise CatalogToolException('search_release_detail_CKANAPIError', 500)
    except ServerIncompatibleError:
        app.logger.error(traceback.format_exc())
        app.logger.error('詳細検索カタログ検索 詳細検索用CKAN 互換性エラー')
        raise CatalogToolException(
            'search_release_detail_ServerIncompatibleError', 500)
    except AttributeError:
        app.logger.error(traceback.format_exc())
        app.logger.error('詳細検索カタログ検索 詳細検索用CKAN 属性エラー')
        raise CatalogToolException('search_release_detail_AttributeError', 500)
    except Exception:
        app.logger.error(traceback.format_exc())
        app.logger.error('詳細検索カタログ検索 詳細検索用CKAN 例外')
        raise CatalogToolException('search_release_detail_Exception', 500)

    # カタログデータのみを検索結果として返す
    for __result in tmp_result:
        for __dataset in __result['catalogs']:
            result['datasets'].append(__dataset)

    result['message'] = 'success'

    return result


def search_detail(app, keyword, url, organization, release_ckan_apikey, release_ckan_addr,
                  detail_ckan_apikey=None, detail_ckan_addr=None, start=0, rows=1000):
    """ カタログ検索

        Args:
          app: flaskのアプリケーションオブジェクト
          keyword: 検索キーワード
          url: CKANデータセット名
          release_ckan_apikey: 横断CKANアプリキー
          release_ckan_addr: 横断CKANアドレス
          detail_ckan_apikey: 詳細CKANアプリキー
          detail_ckan_addr: 詳細CKANアドレス
          start: 検索開始位置
          rows: 検索結果数

        Returns:
          検索したカタログ情報
    """

    result = {
        'message': 'error',
        'datasets': []
    }

    tmp_result = []

    if not organization:
        data = {
            'organization': None,
            'catalogs': []
        }
        tmp_result.append(data)
    else:
        for user_org in organization:
            data = {
                'organization': '',
                'catalogs': []
            }
            data['organization'] = user_org
            tmp_result.append(data)

    try:
        # 詳細検索用CKAN接続
        detail_ckan = connect_ckan(detail_ckan_apikey, detail_ckan_addr)

        # 詳細検索用CKAN検索
        detail_datasets = {}
        if url:
            search_result = detail_ckan.action.package_show(id=url)
            for __data in tmp_result:
                if __data['organization'] == search_result['organization']['name'] or __data['organization'] is None:
                    # 取得データの組織とユーザの組織が一致する場合、検索結果とする（管理者ユーザの場合は組織名一致の判定不要）
                    __data['catalogs'].append(
                        {'release': {}, 'detail': search_result})
        else:
            for __data in tmp_result:
                if __data['organization'] is None:
                    # 組織フィルタ―なし
                    detail_datasets = detail_ckan.action.package_search(
                        q=keyword, start=start, rows=rows)
                else:
                    # 組織フィルターあり
                    filter = 'organization:' + __data['organization']
                    detail_datasets = detail_ckan.action.package_search(
                        q=keyword, fq=filter, start=start, rows=rows)

                if not detail_datasets['results']:
                    continue
                for __result in detail_datasets['results']:
                    __data['catalogs'].append(
                        {'release': {}, 'detail': __result})

    except NotAuthorized:
        app.logger.error(traceback.format_exc())
        app.logger.error('詳細検索カタログ検索 詳細検索用CKAN 認証エラー')
        raise CatalogToolException('search_detail_detail_NotAuthorized', 500)
    except NotFound:
        # カタログが見つからない場合はスルー
        app.logger.error('詳細検索カタログ検索 詳細検索用CKAN 検索エラー')
        result['message'] = '詳細検索用CKANに該当カタログはありません。'
    except ValidationError:
        app.logger.error(traceback.format_exc())
        app.logger.error('詳細検索カタログ検索 詳細検索用CKAN 変数エラー')
        raise CatalogToolException('search_detail_detail_ValidationError', 500)
    except CKANAPIError:
        app.logger.error(traceback.format_exc())
        app.logger.error('詳細検索カタログ検索 詳細検索用CKAN APIエラー')
        raise CatalogToolException('search_detail_detail_CKANAPIError', 500)
    except ServerIncompatibleError:
        app.logger.error(traceback.format_exc())
        app.logger.error('詳細検索カタログ検索 詳細検索用CKAN 互換性エラー')
        raise CatalogToolException(
            'search_detail_detail_ServerIncompatibleError', 500)
    except AttributeError:
        app.logger.error(traceback.format_exc())
        app.logger.error('詳細検索カタログ検索 詳細検索用CKAN 属性エラー')
        raise CatalogToolException('search_detail_detail_AttributeError', 500)
    except Exception:
        app.logger.error(traceback.format_exc())
        app.logger.error('詳細検索カタログ検索 詳細検索用CKAN 例外')
        raise CatalogToolException('search_detail_detail_Exception', 500)

    if not release_ckan_apikey or not release_ckan_addr:
        # 横断検索用CKANの設定なし
        app.logger.warning('横断検索用カタログ未接続')
        result['message'] = 'success'
        for __result in tmp_result:
            for __dataset in __result['catalogs']:
                result['datasets'].append(__dataset)
        return result

    try:
        # 横断検索用CKAN接続
        release_ckan = connect_ckan(release_ckan_apikey, release_ckan_addr)

        # 横断検索用CKAN検索
        for __data in tmp_result:
            for __catalog in __data['catalogs']:
                for __extra in __catalog['detail']['extras']:

                    if not __extra['key'] == 'caddec_dataset_id_for_detail':
                        # 詳細検索用データセットID以外読み飛ばし
                        continue

                    if not __extra['value']:
                        # 詳細検索用データセットIDの設定なし
                        break

                    caddec_dataset_id_for_detail = __extra['value']
                    search_word = 'caddec_dataset_id_for_detail:' + \
                        str(caddec_dataset_id_for_detail)
                    if __data['organization'] is None:
                        # 組織フィルタ―なし
                        release_datasets = release_ckan.action.package_search(
                            q=search_word)
                    else:
                        # 組織フィルタ―あり
                        filter = 'organization:' + __data['organization']
                        release_datasets = release_ckan.action.package_search(
                            q=search_word, fq=filter)

                    if release_datasets['results']:
                        __catalog['release'] = release_datasets['results'][0]

    except NotAuthorized:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ検索 横断検索用CKAN 認証エラー')
        raise CatalogToolException('search_detail_release_NotAuthorized', 500)
    except NotFound:
        # カタログが見つからない場合はスルー
        app.logger.error('横断検索カタログ検索 横断検索用CKAN 検索エラー')
        result['message'] = '詳細検索用CKANに該当カタログはありません。'
    except ValidationError:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ検索 横断検索用CKAN 変数エラー')
        raise CatalogToolException(
            'search_detail_release_ValidationError', 500)
    except CKANAPIError:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ検索 横断検索用CKAN APIエラー')
        raise CatalogToolException('search_detail_release_CKANAPIError', 500)
    except ServerIncompatibleError:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ検索 横断検索用CKAN 互換性エラー')
        raise CatalogToolException(
            'search_detail_release_ServerIncompatibleError', 500)
    except AttributeError:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ検索 横断検索用CKAN 属性エラー')
        raise CatalogToolException('search_detail_release_AttributeError', 500)
    except Exception:
        app.logger.error(traceback.format_exc())
        app.logger.error('横断検索カタログ検索 横断検索用CKAN 例外')
        raise CatalogToolException('search_detail_release_Exception', 500)

    # カタログデータのみを検索結果として返す
    for __result in tmp_result:
        for __dataset in __result['catalogs']:
            result['datasets'].append(__dataset)

    result['message'] = 'success'

    return result


def extra_other(search_result, label):
    """CKAN登録カタログextrasから自由記述値を取得

        Arguments:
            search_result: カタログ検索結果
            label: オートコンプリート実行フィールドのCKAN変数名

        Returns:
            auto_value: オートコンプリート表示結果
    """
    auto_value = []
    for catalog in search_result:
        for extra in catalog['extras']:
            if extra['key'] != label:
                continue
            extra_value_list = extra['value'].split(',')
            for val in extra_value_list:
                if val.startswith(OTHER_TEMPLATE):
                    other_string = val[OTHER_VALUE_START_INDEX:OTHER_VALUE_END_INDEX]
                    if other_string and other_string not in auto_value:
                        auto_value.append(other_string)

    return auto_value


def date_extra_other(search_result, label):
    """CKAN登録カタログの利用期間データの自由記述値を取得

        Arguments:
            search_result: カタログ検索結果
            label: オートコンプリート実行フィールドのCKAN変数名

        Returns:
            auto_value: オートコンプリート表示結果
    """
    auto_value = []
    if label == 'data_effective_period':
        date_key = 'dataEffectivePeriodType'
    else:
        date_key = 'usageLicensePeriodType'
    for catalog in search_result:
        for extra in catalog['extras']:
            if extra['key'] != label:
                continue
            date_dictionary = json.loads(extra['value'])
            if not date_dictionary[0][date_key] == 'note':
                continue
            other_value = date_dictionary[0]['note']
            if not other_value:
                # 空値は候補から排除
                continue
            if other_value in auto_value:
                # 候補の重複を排除
                continue
            auto_value.append(other_value)

    return auto_value


def get_resource_auto_correct_candidates(app, label, query, ckan_addr, ckan_apikey):
    """指定されたCKANから自動補完の入力候補を取得する

        Arguments:
          label: オートコンプリートの対象項目
          query: カタログ検索のクエリ
          ckan_addr: CKANアドレス
          ckan_apikey: CKANapikey

        Returns:
         Dict:
           status: 検索結果
           candidates: オートコンプリート候補
    """

    result = {
        'status': 'error',
        'candidates': []
    }

    ckan_api = connect_ckan(ckan_apikey, ckan_addr)

    datasets = ckan_api.action.resource_search(query=query)

    for catalog in datasets['results']:
        if not catalog[label]:
            # 空値は候補から排除
            continue
        if catalog[label] in result['candidates']:
            # 候補の重複を排除
            continue
        result['candidates'].append(catalog[label])
    result['status'] = 'success'
    # app.logger.warning('get_resource_auto_correct_candidates')
    # app.logger.warning(result)

    return result


def search_auto_correct_resource(app, data, organization, release_ckan_apikey, release_ckan_addr,
                                 detail_ckan_apikey, detail_ckan_addr):
    """CKANから概要情報フィールドの自動補完の入力候補を検索する

        Arguments:
            data: 検索元データ
            organization: カタログに紐づく組織データ
            release_ckan_apikey: 横断CKAN用ユーザパスワード
            release_ckan_addr: 横断用登録先CKANアドレス
    """
    result = {
        'message': 'error',
        'candidates': []
    }
    release_res = {
        'candidates': [],
        'status': ''
    }
    detail_res = {
        'candidates': [],
        'status': ''
    }
    candidates = []

    label = data['search_key']
    keyword = data['search_value']
    # 特殊文字をエスケープ
    for item in QUERY_ESCAPE_REPLACE:
        keyword = keyword.replace(item['word'], item['replace'])
    query = label + ':' + keyword
    # app.logger.warning('query')
    # app.logger.warning(query)

    try:
        # 横断検索用CKANからオートコンプリート候補を取得する
        if release_ckan_apikey and release_ckan_addr:
            release_res = get_resource_auto_correct_candidates(
                app, label, query, release_ckan_addr, release_ckan_apikey)

    except NotAuthorized:
        app.logger.error(traceback.format_exc())
        app.logger.warning('リソースオートコンプリート 横断検索用CKAN 認証エラー')
        raise CatalogToolException(
            'search_auto_correct_resource_release_NotAuthorized', 500)
    except NotFound:
        app.logger.error(traceback.format_exc())
        app.logger.warning('リソースオートコンプリート 横断検索用CKAN 検索エラー')
        raise CatalogToolException(
            'search_auto_correct_resource_release_NotFound', 500)
    except ValidationError:
        app.logger.error(traceback.format_exc())
        app.logger.warning('リソースオートコンプリート 横断検索用CKAN 変数エラー')
        raise CatalogToolException(
            'search_auto_correct_resource_release_ValidationError', 500)
    except CKANAPIError:
        app.logger.error(traceback.format_exc())
        app.logger.warning('リソースオートコンプリート 横断検索用CKAN APIエラー')
        raise CatalogToolException(
            'search_auto_correct_resource_release_CKANAPIError', 500)
    except ServerIncompatibleError:
        app.logger.error(traceback.format_exc())
        app.logger.warning('リソースオートコンプリート 横断検索用CKAN 互換性エラー')
        raise CatalogToolException(
            'search_auto_correct_resource_release_ServerIncompatibleError', 500)
    except AttributeError:
        app.logger.error(traceback.format_exc())
        app.logger.warning('リソースオートコンプリート 横断検索用CKAN 属性エラー')
        raise CatalogToolException(
            'search_auto_correct_resource_release_AttributeError', 500)
    except Exception:
        app.logger.error(traceback.format_exc())
        app.logger.warning('リソースオートコンプリート 横断検索用CKAN 例外')
        raise CatalogToolException(
            'search_auto_correct_resource_release_Exception', 500)

    try:
        # 詳細検索用CKANからオートコンプリート候補を取得する
        if detail_ckan_apikey and detail_ckan_addr:
            detail_res = get_resource_auto_correct_candidates(
                app, label, query, detail_ckan_addr, detail_ckan_apikey)

    except NotAuthorized:
        app.logger.error(traceback.format_exc())
        app.logger.warning('リソースオートコンプリート 詳細検索用CKAN 認証エラー')
        raise CatalogToolException(
            'search_auto_correct_resource_detail_NotAuthorized', 500)
    except NotFound:
        app.logger.error(traceback.format_exc())
        app.logger.warning('リソースオートコンプリート 詳細検索用CKAN 検索エラー')
        raise CatalogToolException(
            'search_auto_correct_resource_detail_NotFound', 500)
    except ValidationError:
        app.logger.error(traceback.format_exc())
        app.logger.warning('リソースオートコンプリート 詳細検索用CKAN 変数エラー')
        raise CatalogToolException(
            'search_auto_correct_resource_detail_ValidationError', 500)
    except CKANAPIError:
        app.logger.error(traceback.format_exc())
        app.logger.warning('リソースオートコンプリート 詳細検索用CKAN APIエラー')
        raise CatalogToolException(
            'search_auto_correct_resource_detail_CKANAPIError', 500)
    except ServerIncompatibleError:
        app.logger.error(traceback.format_exc())
        app.logger.warning('リソースオートコンプリート 詳細検索用CKAN 互換性エラー')
        raise CatalogToolException(
            'search_auto_correct_resource_detail_ServerIncompatibleError', 500)
    except AttributeError:
        app.logger.error(traceback.format_exc())
        app.logger.warning('リソースオートコンプリート 詳細検索用CKAN 属性エラー')
        raise CatalogToolException(
            'search_auto_correct_resource_detail_AttributeError', 500)
    except Exception:
        app.logger.error(traceback.format_exc())
        app.logger.warning('リソースオートコンプリート 詳細検索用CKAN 例外')
        raise CatalogToolException(
            'search_auto_correct_resource_detail_Exception', 500)

    # 各CKANから取得したオートコンプリート候補を結合し、重複を削除
    release_res['candidates'].extend(detail_res['candidates'])
    candidates = copy.deepcopy(release_res['candidates'])
    result['candidates'] = list(set(candidates))

    result['message'] = 'success'
    app.logger.warning('result')
    app.logger.warning(result)

    return result


def get_catalog_auto_correct_candidates(app, label, query, organization, ckan_addr, ckan_apikey):
    """指定されたCKANから自動補完の入力候補を取得する

        Arguments:
          label: オートコンプリートの対象項目
          query: カタログ検索のクエリ
          organization: 組織情報（カタログ検索時に使用）
          ckan_addr: CKANアドレス
          ckan_apikey: CKANapikey

        Returns:
         Dict:
           status: 検索結果
           candidates: オートコンプリート候補
    """

    catalogs = []
    result = {
        'status': 'error',
        'candidates': []
    }

    ckan_api = connect_ckan(ckan_apikey, ckan_addr)

    if not organization:
        # 組織フィルタ―なし
        datasets = ckan_api.action.package_search(q=query)
        for __result in datasets['results']:
            catalogs.append(__result)

    else:
        # 組織フィルターあり
        for __org in organization:
            filter = 'organization:' + __org
            datasets = ckan_api.action.package_search(q=query, fq=filter)
            if not datasets['results']:
                continue
            for __result in datasets['results']:
                catalogs.append(__result)

    if label in {'title', 'notes', 'url'}:
        # extras以外
        for __catalog in catalogs:
            if not __catalog[label]:
                # 空値は候補から排除
                continue
            if __catalog[label] in result['candidates']:
                # 候補の重複を排除
                continue
            result['candidates'].append(__catalog[label])
    else:
        # extras
        if label in WITH_OTHER_FIELDS:
            # 自由欄の値を取得
            result['candidates'] = extra_other(catalogs, label)

        elif label in WITH_OTHER_FIELDS_DATE:
            # データの有効期間と利用ライセンスの期限の自由欄の値を取得
            result['candidates'] = date_extra_other(catalogs, label)

        else:
            for __catalog in catalogs:
                for extra in __catalog['extras']:
                    if not extra['key'] == label:
                        continue
                    if not extra['value']:
                        # 空値は候補から排除
                        continue
                    if extra['value'] in result['candidates']:
                        # 候補の重複を排除
                        continue
                    result['candidates'].append(extra['value'])

    result['status'] = 'success'

    return result


def search_auto_correct_catalog(app, data, organization, release_ckan_apikey, release_ckan_addr,
                                detail_ckan_apikey, detail_ckan_addr):
    """CKANから自動補完の入力候補を検索する

        Arguments:
            data: 検索元データ
            organization: カタログに紐づく組織データ
            release_ckan_apikey: 横断検索用CKANapikey
            release_ckan_addr: 横断検索用CKANアドレス
            detail_ckan_apikey: 詳細検索用CKANapikey
            detail_ckan_addr: 詳細検索用CKANアドレス

        Returns:
          Dict:
            message: オートコンプリート検索結果
            candidates: オートコンプリート候補
    """
    result = {
        'message': 'error',
        'candidates': []
    }
    release_res = {
        'candidates': [],
        'status': ''
    }
    detail_res = {
        'candidates': [],
        'status': ''
    }

    candidates = []
    release_res['candidates'] = []
    detail_res['candidates'] = []
    label = data['search_key']
    keyword = data['search_value']

    # 検索クエリの作成
    # 特殊文字をエスケープ
    for item in QUERY_ESCAPE_REPLACE:
        keyword = keyword.replace(item['word'], item['replace'])
    query = label + ':*' + keyword + '*'
    app.logger.warning('query')
    app.logger.warning(query)

    try:
        # 横断検索用CKANからオートコンプリートの候補を取得
        if release_ckan_apikey and release_ckan_addr:
            release_res = get_catalog_auto_correct_candidates(
                app, label, query, organization, release_ckan_addr, release_ckan_apikey)

    except NotAuthorized:
        app.logger.error(traceback.format_exc())
        app.logger.warning('カタログオートコンプリート 横断検索用CKAN 認証エラー')
        raise CatalogToolException(
            'search_auto_correct_catalog_release_NotAuthorized', 500)
    except NotFound:
        app.logger.error(traceback.format_exc())
        app.logger.warning('カタログオートコンプリート 横断検索用CKAN 検索エラー')
        raise CatalogToolException(
            'search_auto_correct_catalog_release_NotFound', 500)
    except ValidationError:
        app.logger.error(traceback.format_exc())
        app.logger.warning('カタログオートコンプリート 横断検索用CKAN 変数エラー')
        raise CatalogToolException(
            'search_auto_correct_catalog_release_ValidationError', 500)
    except CKANAPIError:
        app.logger.error(traceback.format_exc())
        app.logger.warning('カタログオートコンプリート 横断検索用CKAN APIエラー')
        raise CatalogToolException(
            'search_auto_correct_catalog_release_CKANAPIError', 500)
    except ServerIncompatibleError:
        app.logger.error(traceback.format_exc())
        app.logger.warning('カタログオートコンプリート 横断検索用CKAN 互換性エラー')
        raise CatalogToolException(
            'search_auto_correct_catalog_release_ServerIncompatibleError', 500)
    except AttributeError:
        app.logger.error(traceback.format_exc())
        app.logger.warning('カタログオートコンプリート 横断検索用CKAN 属性エラー')
        raise CatalogToolException(
            'search_auto_correct_catalog_release_AttributeError', 500)
    except Exception:
        app.logger.error(traceback.format_exc())
        app.logger.warning('カタログオートコンプリート 横断検索用CKAN 例外')
        raise CatalogToolException(
            'search_auto_correct_catalog_release_Exception', 500)

    try:
        # 詳細検索用CKANからオートコンプリートの候補を取得
        if detail_ckan_apikey and detail_ckan_addr:
            detail_res = get_catalog_auto_correct_candidates(
                app, label, query, organization, detail_ckan_addr, detail_ckan_apikey)

    except NotAuthorized:
        app.logger.error(traceback.format_exc())
        app.logger.warning('カタログオートコンプリート 詳細検索用CKAN 認証エラー')
        raise CatalogToolException(
            'search_auto_correct_catalog_detail_NotAuthorized', 500)
    except NotFound:
        app.logger.error(traceback.format_exc())
        app.logger.warning('カタログオートコンプリート 詳細検索用CKAN 検索エラー')
        raise CatalogToolException(
            'search_auto_correct_catalog_detail_NotFound', 500)
    except ValidationError:
        app.logger.error(traceback.format_exc())
        app.logger.warning('カタログオートコンプリート 詳細検索用CKAN 変数エラー')
        raise CatalogToolException(
            'search_auto_correct_catalog_detail_ValidationError', 500)
    except CKANAPIError:
        app.logger.error(traceback.format_exc())
        app.logger.warning('カタログオートコンプリート 詳細検索用CKAN APIエラー')
        raise CatalogToolException(
            'search_auto_correct_catalog_detail_CKANAPIError', 500)
    except ServerIncompatibleError:
        app.logger.error(traceback.format_exc())
        app.logger.warning('カタログオートコンプリート 詳細検索用CKAN 互換性エラー')
        raise CatalogToolException(
            'search_auto_correct_catalog_detail_ServerIncompatibleError', 500)
    except AttributeError:
        app.logger.error(traceback.format_exc())
        app.logger.warning('カタログオートコンプリート 詳細検索用CKAN 属性エラー')
        raise CatalogToolException(
            'search_auto_correct_catalog_detail_AttributeError', 500)
    except Exception:
        app.logger.error(traceback.format_exc())
        app.logger.warning('カタログオートコンプリート 詳細検索用CKAN 例外')
        raise CatalogToolException(
            'search_auto_correct_catalog_detail_Exception', 500)

    # 各CKANから取得したオートコンプリート候補を結合し、重複を削除
    release_res['candidates'].extend(detail_res['candidates'])
    candidates = copy.deepcopy(release_res['candidates'])
    result['candidates'] = list(set(candidates))

    result['message'] = 'success'
    app.logger.warning('result')
    app.logger.warning(result)

    return result
