<script setup>
import { useRouter, isNavigationFailure } from 'vue-router'
import { Loading } from 'quasar'
import { onMounted, reactive, onBeforeUnmount } from 'vue'
import { useStore } from '../stores/store'
import CompleteDialog from '../components/dialog/CompleteDialog.vue'
import axios from 'axios'
import { config } from'boot/config'

const store = useStore()
const router = useRouter()

const completeDialog = reactive({
  isDisplay: false,
  message: '',
  errorFlg: false
})

const attr = reactive({
  languageList: []
})

Loading.show()

onMounted(function(){
  console.log('-- loginLoad.vue onMounted --')
  var urlIndex = location.href.indexOf('/#/')
  var catalogToolUrl = location.href.slice(0, urlIndex+3)
  axios.post(config.apiPrefix + '/auth/login', { keycloak_uuid: store.authInfo.keycloakState, auth_code: store.authInfo.keycloakCode, catalog_tool_url: catalogToolUrl })
  .then(res => {
    store.updateUser({
      ckan: res.data.ckan,
      username: res.data.ckan_username,
      caddeUserId: res.data.cadde_user_id,
      caddeUserIdList: res.data.cadde_user_id_list,
      releaseCkanAddr: res.data.release_ckan_addr,
      detailCkanAddr: res.data.detail_ckan_addr,
      sysadmin: res.data.sysadmin
    })
    store.initItemListParams()// 列挙型データの初期化
    store.initCkanItemListParams()// ライセンスリストの初期化
    store.initConfigValue()// 外部サービス・機械学習の使用有無フラグ初期化

    // 言語リスト取得
    axios.get('datalist/languageList.json')
    .then((res) => {
      attr.languageList = res.data

      // 列挙型データの取得・更新
      axios.get('datalist/itemValue.json')
      .then(res => {
        var itemListValue = res.data[0].select_item
        store.updateItemList({
          frequency: getItemListValue(itemListValue, 'frequency'),
          caddecResourceType: getItemListValue(itemListValue, 'caddec_resource_type'),
          caddecContractRequired: getItemListValue(itemListValue, 'caddec_contract_required'),
          caddecRequired: getItemListValue(itemListValue, 'caddec_required'),
          accessRights: getItemListValue(itemListValue, 'access_rights'),
          tradingPolicyContractType: getItemListValue(itemListValue, 'trading_policy_contract_type'),
          tradingPolicyNda: getItemListValue(itemListValue, 'trading_policy_nda'),
          tradingPolicyUseApplication: getItemListValue(itemListValue, 'trading_policy_use_application'),
          scopeOfDisclosure: getItemListValue(itemListValue, 'scope_of_disclosure'),
          termsOfUsePermissibleRegion: getItemListValue(itemListValue, 'terms_of_use_permissible_region'),
          privacyPolicyContainsPersonalData: getItemListValue(itemListValue, 'privacy_policy_contains_personal_data'),
          dataEffectivePeriod: getItemListValue(itemListValue, 'data_effective_period'),
          usageLicensePeriod: getItemListValue(itemListValue, 'usage_license_period'),
          fee: getItemListValue(itemListValue, 'fee'),
          warrantyExpressWarranty: getItemListValue(itemListValue, 'warranty_express_warranty'),
          warrantyLegalCompliance: getItemListValue(itemListValue, 'warranty_legal_compliance'),
          mimetype: getItemListValue(itemListValue, 'mime_type'),
          compressFormat: getItemListValue(itemListValue, 'compress_format'),
          packageFormat: getItemListValue(itemListValue, 'package_format'),
          schemaType: getItemListValue(itemListValue, 'schema_type'),
          language: attr.languageList
        })

        // 外部サービスおよび機械学習使用有無確認
        axios.get(config.apiPrefix + '/config')
        .then(res => {
          store.updateConfigValue({
            geonames: res.data.geonames.use_geonames,
            theme: res.data.machine_learn.theme,
            keyword: res.data.machine_learn.keyword,
            spatial: res.data.machine_learn.spatial,
            temporal: res.data.machine_learn.temporal
          })

          // テンプレート情報の初期化
          store.initField(['template'])
          // テンプレート情報の取得
          axios.get(config.apiPrefix + '/template')
          .then((res) => {
            // 各フィールドの値を画面ごとにコミット
            var itemValue = res.data.template.catalog_value
            commitDatasetinfo(itemValue.datasetinfo, ['state', 'template'])
            // 概要情報はtemplateの値のみコミット
            commitDatajacket(itemValue.datajacket, ['template'])
            commitDatasetoptionalinfo(itemValue.datasetoptionalinfo, ['state', 'template'])
            commitUserterms(itemValue.userterms, ['state', 'template'])
            console.log('LoginLoad.vue テンプレート値コミット後', store.template)

            // ライセンスリスト取得APIの実行
            // ライセンスリスト取得・更新
            var licenseItemList = []
            axios.get(config.apiPrefix + '/licenselist')
            .then(response => {
              var licenseRes = response.data
              for (var i = 0; i < licenseRes.length; i++) {
                licenseItemList.push({
                  label: licenseRes[i].title,
                  value: licenseRes[i].id,
                  url: licenseRes[i].url
                })
              }
              store.updateCkanItemList({ licenseId: licenseItemList })
              axios.get(config.apiPrefix + '/ckaninfo')
              .then(async response => {
                for (var i = 0; i < response.data.length; i++) {
                  if (response.data[i].ckan_type === 'release') {
                    var releaseCkanTitle = response.data[i].title
                    var releaseCkanDescription = response.data[i].description
                    var releaseCkanUrl = response.data[i].url
                    // TO DO CKANから取得したカタログ公開者・カタログ公開者（説明）データの設定
                    // CKANから取得するデータに該当データなし（2021/12/03現在）
                    var releaseCkanPublisher = ''
                    var releaseCkanPublisherExplanation = ''
                  } else if (response.data[i].ckan_type === 'detail') {
                    var detailCkanTitle = response.data[i].title
                    var detailCkanDescription = response.data[i].description
                    var detailCkanUrl = response.data[i].url
                    // TO DO CKANから取得したカタログ公開者・カタログ公開者（説明）データの設定
                    // CKANから取得するデータに該当データなし（2021/12/03現在）
                    var detailCkanPublisher = ''
                    var detailCkanPublisherExplanation = ''
                  }
                }
                store.updateCkanCataloginfo({
                  releaseCkanCatalogTitle: releaseCkanTitle,
                  releaseCkanCatalogDescription: releaseCkanDescription,
                  releaseCkanCatalogUrl: releaseCkanUrl,
                  releaseCkanCatalogPublisher: releaseCkanPublisher,
                  releaseCkanCatalogPublisherExplanation: releaseCkanPublisherExplanation,
                  detailCkanCatalogTitle: detailCkanTitle,
                  detaikCkanCatalogDescription: detailCkanDescription,
                  detailCkanCatalogUrl: detailCkanUrl,
                  detailCkanCatalogPublisher: detailCkanPublisher,
                  detailCkanCatalogPublisherExplanation: detailCkanPublisherExplanation
                })
                // 次画面遷移
                if (store.loginInfo.sysadmin === true) {
                  // [運用管理者ユーザでログイン]ユーザ管理画面へ遷移
                  router.push('/userManager').then(failure => {
                    if (!isNavigationFailure(failure)) {
                      // [運用管理者ユーザでログイン]実行モード情報を「ユーザ管理」に更新
                      store.updateMode({ mode: 'userManagement', ckanType: '', isBothCatalog: false })
                    }
                  })
                } else {
                  // [提供者ユーザでログイン]メニュー選択画面へ遷移
                  router.push('/menuSelect').then(failure => {
                    if (!isNavigationFailure(failure)) {
                      store.updateMode({ mode: 'menuSelect', ckanType: '', isBothCatalog: false })
                    }
                  })
                }
              })
              
              .catch(err => {
                console.log('error message:', err.response.data.message)
                completeDialog.isDisplay = true
                completeDialog.message = err.response.data.message || 'カタログサイト情報取得に失敗しました。\n管理者に問い合わせてください。'
                completeDialog.errorFlg = true
              })
            })
            .catch(err => {
              console.log('error message:', err.response.data.message)
              completeDialog.isDisplay = true
              completeDialog.message = err.response.data.message || 'ライセンスリスト取得に失敗しました。\n管理者に問い合わせてください。'
              completeDialog.errorFlg = true
            })
          })
          .catch(err => {
            console.log('error message:', err.response.data.message)
            completeDialog.isDisplay = true
            completeDialog.message = err.response.data.message || 'テンプレート取得に失敗しました。\n管理者に問い合わせてください。'
            completeDialog.errorFlg = true
          })
        })
        .catch(err => {
          console.log('error message:', err.response.data.message)
          completeDialog.isDisplay = true
          completeDialog.message = err.response.data.message || '外部サービスおよび機械学習使用有無確認に失敗しました。\n管理者に問い合わせてください。'
          completeDialog.errorFlg = true
        })
      })
      .catch(err => {
        console.log('error message:選択肢表示データの取得に失敗しました。\n管理者に問い合わせてください。')
        completeDialog.isDisplay = true
        completeDialog.message = '選択肢表示データの取得に失敗しました。\n管理者に問い合わせてください。'
        completeDialog.errorFlg = true
      })
    })
    .catch(err => {
      console.log('error message: Languageファイルの取得に失敗しました。\n管理者に問い合わせてください。')
      completeDialog.isDisplay = true
      completeDialog.message = 'Languageファイルの取得に失敗しました。\n管理者に問い合わせてください。'
      completeDialog.errorFlg = true
    })
    Loading.hide()
  })
  .catch(err => {
    Loading.hide()
    console.log('error message:', err.response.data.message)
    completeDialog.isDisplay = true
    completeDialog.message = err.response.data.message || '認証ログインに失敗しました。\n管理者に問い合わせてください。'
    completeDialog.errorFlg = true
  })
})

// データセット情報のパラメータ更新（テンプレート）
function commitDatasetinfo (data, storeTypeList) {
  for (var i = 0; i < storeTypeList.length; i++) {
    store.updateDatasetinfo({
        catalogTitle: data.title,
        catalogDescription: data.notes,
        datasetDescriptionUrl: data.url,
        datasetIdForDetail: data.caddec_dataset_id_for_detail,
        registOrg: data.regist_org,
        publisherId: data.caddec_provider_id,
        publisher: data.publisher_name,
        publisherUri: data.publisher_uri,
        creator: data.creator_name,
        creatorUrl: data.creator_url,
        contactPoint: data.contact_name,
        contactPointUrl: data.contact_url,
        storeType: storeTypeList[i]
      })
  }
}

// データ概要情報のパラメータ更新（テンプレート）
function commitDatajacket (data, storeTypeList) {
  console.log('commitDatajacket', data)
  var registedFiledataDetails = []
  if (data.length) {
    for (var i = 0; i < data.length; i++) {
      // 契約確認の要否
      var contractRequired = data[i].contractRequired
      // コネクタ利用の要否
      var connectRequired = data[i].connectRequired
      // 配信の名称
      var registedFilename = data[i].filename || ''
      // 配信リソース名（リソース取得・保存時にwebサーバから付与）
      var registedDataName = data[i].dataname || ''
      // 配信の説明
      var registedDescription = data[i].description || ''
      // 配信の情報提供ページURL
      var registedUrl = data[i].dataurl || ''
      // 配信のダウンロードURL
      var registedDownloadUrl = data[i].downloadUrl || ''
      // 配信の情報配信ページURL
      var registedExplainUrl = data[i].explainurl || ''
      // 配信のバイトサイズ
      var registedSize = data[i].size || ''
      // ファイルのカラム名
      var registedColumnName = data[i].columnName || ''
      // 配信のメディアタイプ
      var registedMimetype = data[i].mimetype || ''
      // 配信のファイル形式
      var registedFormat = data[i].format || ''
      // 配信の圧縮形式
      var registedCompressFormat = data[i].compressFormat || ''
      // 配信の圧縮形式（自由記述）
      var registedCompressFormatOther = data[i].compressFormatOther || ''
      // 配信のパッケージ形式
      var registedPackageFormat = data[i].packageFormat || ''
      // 配信のパッケージ形式（自由記述）
      var registedPackageFormatOther = data[i].packageFormatOther || ''
      // スキーマ
      var registedSchema = data[i].schema || ''
      // スキーマタイプ
      var registedSchemaType = data[i].schemaType || ''
      // NGSIデータ種別
      var registedNgsiEntityType = data[i].ngsiEntityType || ''
      // NGSIテナント
      var registedNgsiTenant = data[i].ngsiTenant || ''
      // NGSIサービスパス
      var registedNgsiServicePath = data[i].ngsiServicePath || ''
      // NGSIデータモデル
      var registedNgsiDataModel = data[i].ngsiDataModel || []
      // 来歴登録の有無
      if (data[i].getResourceIDForProvenance) {
        if (data[i].getResourceIDForProvenance.label && data[i].getResourceIDForProvenance.value) {
          var registedGetResourceIdForProvenanceLabel = data[i].getResourceIDForProvenance.label
          var registedGetResourceIdForProvenanceValue = data[i].getResourceIDForProvenance.value
        } else {
          registedGetResourceIdForProvenanceLabel = ''
          registedGetResourceIdForProvenanceValue = ''
        }
      }
      // 交換実績記録用リソースID
      var registedResourceIdForProvenance = data[i].resourceIDForProvenance || ''
      // 前段イベント識別子
      var registedPreviousEventId = data[i].previousEventId || ''
      // データサービスのタイトル
      var registedDataServiceTitle = data[i].dataServiceTitle || ''
      // データサービスのエンドポイント
      var registedDataServiceEndpointUrl = data[i].dataServiceEndpointUrl || ''
      // データサービスのエンドポイントの定義
      var registedDataServiceEndpointDescription = data[i].dataServiceEndpointDescription || ''
      // 来歴登録済みの配信のダウンロードURL
      var registedUrlForProvenance = data[i].urlForProvenance || ''
      // 来歴登録済みの利用者コネクタID
      var registedCaddeUserId = data[i].caddeUserId || ''
      // リソース提供手段の識別子
      if (data[i].resourceType.value) {
        if (data[i].resourceType.value === 'file/http') {
          var registedResourceTypeLabel = 'ファイル提供(HTTP)'
          var registedResourceTypeValue = 'file/http'
        } else if (data[i].resourceType.value === 'file/ftp') {
          registedResourceTypeLabel = 'ファイル提供(FTP)'
          registedResourceTypeValue = 'file/ftp'
        } else if (data[i].resourceType.value === 'api/ngsi') {
          registedResourceTypeLabel = 'API提供(NGSI API)'
          registedResourceTypeValue = 'api/ngsi'
        } else {
          registedResourceTypeLabel = ''
          registedResourceTypeValue = ''
        }
      }
      // 配信のライセンス
      var registedResourceLicenseTitle = data[i].license_title || ''
      // 配信のライセンス（URL)
      var registedResourceLicenseUrl = data[i].licenseurl || ''
      // 配信の発行日
      var registedIssued = data[i].issued || ''
      // 配信のラベル（画面タブの表示値）
      var registedLabel = data[i].label || ''
      registedFiledataDetails.push({
        label: registedLabel,
        dataname: registedDataName,
        filename: registedFilename,
        description: registedDescription,
        dataurl: registedUrl,
        downloadUrl: registedDownloadUrl,
        explainurl: registedExplainUrl,
        size: registedSize,
        columnName: registedColumnName,
        mimetype: registedMimetype,
        format: registedFormat,
        compressFormat: registedCompressFormat,
        compressFormatOther: registedCompressFormatOther,
        packageFormat: registedPackageFormat,
        packageFormatOther: registedPackageFormatOther,
        schema: registedSchema,
        schemaType: registedSchemaType,
        ngsiEntityType: registedNgsiEntityType,
        ngsiTenant: registedNgsiTenant,
        ngsiServicePath: registedNgsiServicePath,
        ngsiDataModel: registedNgsiDataModel,
        contractRequired: contractRequired,
        connectRequired: connectRequired,
        getResourceIDForProvenance: {
          label: registedGetResourceIdForProvenanceLabel,
          value: registedGetResourceIdForProvenanceValue
        },
        resourceIDForProvenance: registedResourceIdForProvenance,
        previousEventId: registedPreviousEventId,
        dataServiceTitle: registedDataServiceTitle,
        dataServiceEndpointUrl: registedDataServiceEndpointUrl,
        dataServiceEndpointDescription: registedDataServiceEndpointDescription,
        urlForProvenance: registedUrlForProvenance,
        caddeUserId: registedCaddeUserId,
        resourceType: {
          label: registedResourceTypeLabel,
          value: registedResourceTypeValue
        },
        licensetitle: registedResourceLicenseTitle,
        licenseurl: registedResourceLicenseUrl,
        issued: registedIssued
      })
    }
  }
  for (var j = 0; j < storeTypeList.length; j++) {
    store.updateFiledataDetails({
      filedataDetails: registedFiledataDetails,
      storeType: storeTypeList[j]
    })
  }
  console.log('テンプレート取得後のコミット', store.template)
}

// データセット情報(任意)のパラメータ更新（テンプレート）
function commitDatasetoptionalinfo (data, storeTypeList) {
  for (var i = 0; i < storeTypeList.length; i++) {
    store.updateDatasetOptionalInfoParameters({
        selectThemes: data.theme,
        selectTags: data.tags,
        vocabulary: data.vocabulary,
        term: data.term,
        selectLanguage: data.language,
        frequency: data.frequency,
        spatialUrl: data.spatial_url,
        spatialName: data.spatial_text,
        spatial: data.spatial,
        start: data.temporal_start,
        end: data.temporal_end,
        storeType: storeTypeList[i]
      })
  }
}

// 利用条件のパラメータ更新（テンプレート）
function commitUserterms (data, storeTypeList) {
  for (var i = 0; i < storeTypeList.length; i++) {
    store.updateUserTerms({
        selectedTab: data.selected_tab,
        termName: data.license_title,
        termNameUrl: data.license_url,
        usrRight: data.rights,
        accessRights: data.access_rights,
        accessRightsUrl: data.access_rights_url,
        haspolicyUrl: data.haspolicy_url,
        provWasGeneratedByUrl: data.prov_was_generated_by_url,
        conformsTo: data.conforms_to,
        contractType: data.trading_policy_contract_type,
        secrecy: data.trading_policy_nda,
        useApplication: data.trading_policy_use_application,
        useApplicationOther: data.trading_policy_use_application_free,
        scopeOfDisclosure: data.scope_of_disclosure,
        scopeOfDisclosureOther: data.scope_of_disclosure_free,
        permissionResion: data.terms_of_use_permissible_region,
        permissionResionOther: data.terms_of_use_permissible_region_free,
        notices: data.terms_of_use_notices,
        personalData: data.privacy_policy_contains_personal_data,
        personalDataOther: data.privacy_policy_contains_personal_data_free,
        dataEffectivePeriodSelectTerms: data.data_effective_period_term,
        startDate: data.data_effective_period_start,
        endDate: data.data_effective_period_end,
        dataEffectivePeriodFreefield: data.data_effective_period_free,
        usageLicensePeriodSelectTerms: data.usage_license_period_term,
        deadline: data.usage_license_period_deadline,
        period: data.usage_license_period_period,
        unit: data.usage_license_period_unit,
        usageLicensePeriodFreefield: data.usage_license_period_free,
        fee: data.fee,
        salesInfoUrl: data.sales_info_url,
        priceRange: data.pricing_price_range,
        noticesOfPrice: data.pricing_notices_of_price,
        expressWarranty: data.warranty_express_warranty,
        expressWarrantyOther: data.warranty_express_warranty_free,
        leagalCompliance: data.warranty_legal_compliance,
        leagalComplianceOther: data.warranty_legal_compliance_free,
        storeType: storeTypeList[i]
      })
  }
}

// 「選択肢」リストの読込
function getItemListValue (itemValue, keyName) {
  var itemValueMap = []
  var listValueMap = []
  for (var value in itemValue) {
    var ckanKeyName = itemValue[value].ckanKeyName
    if (ckanKeyName === keyName) {
      itemValueMap = itemValue[value].valueMap
      break
    }
  }
  for (var key in itemValueMap) {
    listValueMap.push({ label: itemValueMap[key], value: key })
  }
  var jsonData = JSON.stringify(listValueMap)
  return JSON.parse(jsonData)
}

</script>
<template>
  <div class="col-12 q-layout-padding flex justify-center content-center">
    <q-card class="q-card-background-white" style="max-width: 80%; width: 100%;">
    </q-card>

    <!-- 完了ダイアログ -->
    <CompleteDialog
      v-bind:dialogInfo="completeDialog"
      @close-dialog="router.push('/')"
    />

  </div>
</template>
    
