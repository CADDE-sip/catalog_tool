<script setup>
import { config } from'boot/config'
import { reactive, ref, onMounted, watch } from 'vue'
import { useStore } from '../stores/store'
import { useRouter } from 'vue-router'
import OperationConfirmDialog from '../components/dialog/OperationConfirmDialog.vue'
import CompleteDialog from '../components/dialog/CompleteDialog.vue'
import axios from 'axios'

const store = useStore()
const router = useRouter()

const INIT_STORE_FIELDS = ['hold', 'another']

const link = ref('')
const confirmDialog = reactive({
    isDisplay: false,
    type: 'confirm-discard',
    options: {}
})

const completeDialog = reactive({
  isDisplay: false,
  message: '',
  errorFlg: false
})

// 画面切り替えでダイアログを表示させる必要があるか判定
function isNeedToShowTransitionConfirmDialog () {
  if (router.currentRoute.value.fullPath !== '/register') {
    return false
  }

  if(store.isCatalogEditing == false){
    return false
  }

  return true
}

// transitionFunctionを呼び出して実行する
// 必要ならその前にOperationConfirmDialogを表示して確認する
function processWithConfirmDialogIfNeeded (transitionFunction) {
  if (isNeedToShowTransitionConfirmDialog()){
    confirmDialog.type = 'confirm-discard'
    confirmDialog.options = {}
    confirmDialog.confirmCallback = transitionFunction
    confirmDialog.cancelCallback = null
    confirmDialog.isDisplay = true
  } else {
    transitionFunction()
  }
}

//カタログ作成
function btnMoveRegistration (registerMode) {
  switch (registerMode) {
    case 'new_release_register':
      link.value = 'releaseRegister'
      break
    case 'new_detail_register':
      link.value = 'detailRegister'
      break
    case 'new_both_register':
      link.value = 'bothRegister'
      break
  }
  if (router.currentRoute.value.fullPath !== '/register') {//カタログ作成以外の画面から遷移する場合
    // 同じ画面への遷移はエラーとなる
    processWithConfirmDialogIfNeeded( () => {
      beforeCatalogCreate().then(res => {
        if(!res) return
        store.updateMode({ mode: registerMode, ckanType: '', isBothCatalog: false })
        router.push('/register')
      })
    } )
  } else {//カタログ作成画面、もしくはテンプレート編集画面から遷移する場合
    // DatasetInfo.vueにいる場合は、該当画面の初期化をする
    // DatasetResource.vue, DatasetOption.vue, DatasetUseTerms.vue, Dataset.vueのいずれかの子コンポーネントにいる場合は、DatasetInfo.vueに遷移
    processWithConfirmDialogIfNeeded( () => {
      beforeCatalogCreate().then(res => {
        if(!res) return
        // 実行モード情報を更新
        store.updateMode({ mode: registerMode, ckanType: '', isBothCatalog: false })
        // 新規カタログ作成フラグをtrueに更新
        var createNewCatalogFlg = store.createNewCatalog !== true
        store.pushCreate({ createNewCatalog: createNewCatalogFlg })
        console.log('- btnMoveRegistration -')
        console.log('createNewCatalogFlg:'+createNewCatalogFlg)
      })
    } )
  }
}

// 複製・編集・削除
function btnMoveSearch () {
  link.value = 'search'
  if (router.currentRoute.value.fullPath !== '/search') {
    // 同じ画面への遷移はエラーとなる
    processWithConfirmDialogIfNeeded( () => {
      // カタログ入力情報の初期化・登録済みカタログ情報の初期化・紐づけ先カタログ情報の初期化
      initStoreFields(INIT_STORE_FIELDS)
      // 実行モード情報を「複製・編集・削除」に更新
      store.updateMode({ mode: 'search', ckanType: '', isBothCatalog: false })
      // 複製・編集・削除画面へ遷移
      router.push('/search')
    } )
  }
}

// 登録再開
function btnMoveRestart () {
  link.value = 'selectDraft'
  if (router.currentRoute.value.fullPath !== '/selectDraft') {
    // 同じ画面への遷移はエラーとなる
    processWithConfirmDialogIfNeeded( () => {
      // カタログ入力情報の初期化・登録済みカタログ情報の初期化・紐づけ先カタログ情報の初期化
      initStoreFields(INIT_STORE_FIELDS)
      // 実行モード情報を「登録再開」に更新
      store.updateMode({ mode: 'selectDraft', ckanType: '', isBothCatalog: false })
      // 登録再開画面へ遷移
      router.push('/selectDraft')
    } )
  }
}

// ユーザ管理
function btnMoveUserList () {
  link.value = 'userManagement'
  if (router.currentRoute.value.fullPath !== '/userManager') {
    // 同じ画面への遷移はエラーとなる
    processWithConfirmDialogIfNeeded( () => {
      // 実行モード情報を「ユーザ管理」に更新
      store.updateMode({ mode: 'userManagement', ckanType: '', isBothCatalog: false })
      // ユーザ管理画面へ遷移
      router.push('/userManager')
    } )
  }
}

// インポート
function btnMoveImport () {
  link.value = 'import'
  if (router.currentRoute.value.fullPath !== '/import') {
    // 同じ画面への遷移はエラーとなる
    processWithConfirmDialogIfNeeded( () => {
      // 実行モード情報を「インポート」に更新
      store.updateMode({ mode: 'import', ckanType: '', isBothCatalog: false })
      // インポート画面へ遷移
      router.push('/import')
    } )
  }
}

// エクスポート
function btnMoveExport () {
  link.value = 'export'
  if (router.currentRoute.value.fullPath !== '/export') {
    // 同じ画面への遷移はエラーとなる
    processWithConfirmDialogIfNeeded( () => {
      // 実行モード情報を「エクスポート」に更新
      store.updateMode({ mode: 'export', ckanType: '', isBothCatalog: false })
      // エクスポート画面へ遷移
      router.push('/export')
    } )
  }
}

// テンプレート編集
function btnMoveTemplate () {
  link.value = 'template'
  processWithConfirmDialogIfNeeded( () => {
    // カタログ入力情報の初期化・登録済みカタログ情報の初期化・紐づけ先カタログ情報の初期化
    beforeCatalogCreate().then(res => {
      if(!res) return
      if (router.currentRoute.value.fullPath !== '/register') {
        store.updateMode({ mode: 'template', ckanType: '', isBothCatalog: false })
        router.push('/register')
      } else {
        // 実行モード情報を「テンプレート編集」に更新
        store.updateMode({ mode: 'template', ckanType: '', isBothCatalog: false })
        // 新規カタログ作成フラグをfalseに更新
        var createNewCatalogFlg = store.createNewCatalog !== true
        store.pushCreate({ createNewCatalog: createNewCatalogFlg })
      }
    })
  })
}

// 確認ダイアログで決定ボタン押下時の処理
function onOperationConfirmDialogConfirm () {
  confirmDialog.isDisplay = false
}

// 確認ダイアログでキャンセルボタン押下時の処理
function onOperationConfirmDialogCancel () {
  confirmDialog.isDisplay = false
}

// テンプレート情報の取得
// テンプレート情報の更新
// 表示形式の更新
async function setTemplate () {
  let res
  try{
    // テンプレートの取得
    res = await axios.get(config.apiPrefix + '/template')
  }catch(err){
    console.log('error message:', err.response.data.message)
    completeDialog.isDisplay = true
    completeDialog.message = err.response.data.message || 'テンプレート取得に失敗しました。\n管理者に問い合わせてください。'
    completeDialog.errorFlg = true
    return false
  }

  if(res.data.status === 'failed') {
    return false
  }

  // 表示形式の更新
  var itemDisplayValue = res.data.template.catalog_display
  itemDisplayFlgStoreCommit(itemDisplayValue)
  // 各フィールドの値を画面ごとにコミット
  var itemValue = res.data.template.catalog_value
  commitDatasetinfo(itemValue.datasetinfo, ['state', 'template'])
  // 概要情報はtemplateの値のみコミット
  commitDatajacket(itemValue.datajacket, ['template'])
  commitDatasetoptionalinfo(itemValue.datasetoptionalinfo, ['state', 'template'])
  commitUserterms(itemValue.userterms, ['state', 'template'])
  return true
}

// DisplayFlgの更新
function itemDisplayFlgStoreCommit (flgValue) {
  store.updateItemDisplayFlg({
      url: flgValue.datasetinfo.url,
      caddecDatasetIdForDetail: flgValue.datasetinfo.caddec_dataset_id_for_detail,
      publisherName: flgValue.datasetinfo.publisher_name,
      publisherUri: flgValue.datasetinfo.publisher_uri,
      creatorName: flgValue.datasetinfo.creator_name,
      creatorUrl: flgValue.datasetinfo.creator_url,
      contactName: flgValue.datasetinfo.contact_name,
      contactUrl: flgValue.datasetinfo.contact_url,
      inputSupportType: flgValue.datajacket.input_support_type,
      caddecResourceType: flgValue.datajacket.caddec_resource_type,
      filename: flgValue.datajacket.filename,
      description: flgValue.datajacket.description,
      downloadUrl: flgValue.datajacket.download_url,
      explainUrl: flgValue.datajacket.explainurl,
      size: flgValue.datajacket.size,
      mimeType: flgValue.datajacket.mime_type,
      format: flgValue.datajacket.format,
      compressFormat: flgValue.datajacket.compress_format,
      packageFormat: flgValue.datajacket.package_format,
      schema: flgValue.datajacket.schema,
      schemaType: flgValue.datajacket.schema_type,
      ngsiEntityType: flgValue.datajacket.ngsi_entity_type,
      ngsiTenant: flgValue.datajacket.ngsi_tenant,
      ngsiServicePath: flgValue.datajacket.ngsi_service_path,
      ngsiDataModel: flgValue.datajacket.ngsi_data_model,
      getResourceIDForProvenance: flgValue.datajacket.get_resource_id_for_provenance,
      caddecResourceIdForProvenance: flgValue.datajacket.caddec_resource_id_for_provenance,
      previousEventId: flgValue.datajacket.previous_event_id,
      dataServiceTitle: flgValue.datajacket.data_service_title,
      dataServiceEndpointUrl: flgValue.datajacket.data_service_endpoint_url,
      dataServiceEndpointDescription: flgValue.datajacket.data_service_endpoint_description,
      theme: flgValue.datasetoptionalinfo.theme,
      tags: flgValue.datasetoptionalinfo.tags,
      language: flgValue.datasetoptionalinfo.language,
      vocabulary: flgValue.datasetoptionalinfo.vocabulary,
      term: flgValue.datasetoptionalinfo.term,
      frequency: flgValue.datasetoptionalinfo.frequency,
      spatial: flgValue.datasetoptionalinfo.spatial,
      temporal: flgValue.datasetoptionalinfo.temporal,
      licenseTitle: flgValue.userterms.license_title,
      licenseUrl: flgValue.userterms.license_url,
      rights: flgValue.userterms.rights,
      accessRights: flgValue.userterms.access_rights,
      accessRightsUrl: flgValue.userterms.access_rights_url,
      haspolicyUrl: flgValue.userterms.haspolicy_url,
      provWasGeneratedByUrl: flgValue.userterms.prov_was_generated_by_url,
      conformsTo: flgValue.userterms.conforms_to,
      tradingPolicyContractType: flgValue.userterms.trading_policy_contract_type,
      tradingPolicyNda: flgValue.userterms.trading_policy_nda,
      tradingPolicyUseApplication: flgValue.userterms.trading_policy_use_application,
      scopeOfDisclosure: flgValue.userterms.scope_of_disclosure,
      termsOfUsePermissibleRegion: flgValue.userterms.terms_of_use_permissible_region,
      termsOfUseNotices: flgValue.userterms.terms_of_use_notices,
      privacyPolicyContainsPersonalData: flgValue.userterms.privacy_policy_contains_personal_data,
      dataEffectivePeriod: flgValue.userterms.data_effective_period,
      usageLicensePeriod: flgValue.userterms.usage_license_period,
      fee: flgValue.userterms.fee,
      salesInfoUrl: flgValue.userterms.sales_info_url,
      pricingPriceRange: flgValue.userterms.pricing_price_range,
      pricingNoticesOfPrice: flgValue.userterms.pricing_notices_of_price,
      warrantyExpressWarranty: flgValue.userterms.warranty_express_warranty,
      warrantyLegalCompliance: flgValue.userterms.warranty_legal_compliance
    })
}

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
      // 来歴登録済みのCADDEユーザID
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
}

// データセット情報(任意)のパラメータ更新（テンプレート）
function commitDatasetoptionalinfo (data, storeTypeList) {
  console.log('- commitDatasetoptionalinfo -')
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

// 全項目の値・選択肢の初期化
async function beforeCatalogCreate ()  {
  // hold：登録済みカタログ情報｜another：紐づけ先カタログ情報｜template：テンプレート情報
  // 登録済みカタログ情報の初期化
  // 紐づけ先カタログ情報の初期化
  // テンプレート情報の初期化（カタログ作成のみ）
  var fieldList = ['hold', 'another', 'template']
  initStoreFields(fieldList)

  // テンプレートの取得・更新・表示形式の更新
  let isSetTemplateSuccess = await setTemplate()
  if(!isSetTemplateSuccess){
    return false
  }
  return true
}

// 初期化処理
function initStoreFields(fieldList){
  // カタログ入力情報の初期化
  store.initStateParams()
  // fieldListに入っている項目の初期化
  store.initField(fieldList)
}

// ********************
// Mounted
// ********************
onMounted(function(){
  // Menuの網掛けボタン設定(keycloakログイン画面からのリダイレクト時)
  if (store.selectedMode.mode === 'userManagement') {
    link.value = 'userManagement'
  } else if (store.selectedMode.mode === 'menuSelect') {
    link.value = ''
  }
})

// ********************
// watch
// ********************
watch(() => store.mode,
  // Menuの網掛けボタン設定
  (newVal) => {
    if (newVal === 'userManagement') {
      link.value = 'userManagement'
    } else if (newVal === 'menuSelect') {
      link.value = ''
    }
  }
)

</script>

<template>
  <div v-if="store.loginInfo.releaseCkanAddr || store.loginInfo.detailCkanAddr">
    <q-list no-border link inset-delimiter>
      <q-item v-if="store.loginInfo.sysadmin">
        <q-item-section>
          <q-expansion-item
            label="管理"
            default-opened
            class="item"
          >
            <q-list no-border link inset-delimiter>
              <q-item
                clickable
                :active="link === 'userManagement'"
                @click="btnMoveUserList()"
                active-class="my-menu-sub-link"
              >
                <q-item-section class="sub-item">ユーザ管理</q-item-section>
              </q-item>
            </q-list>
          </q-expansion-item>
        </q-item-section>
      </q-item>

      <q-item>
        <q-item-section>
          <q-expansion-item
            label="カタログ作成"
            default-opened
            class="item"
            >
            <q-list no-border link inset-delimiter>
              <q-item>
                <q-item-section>
                  <q-expansion-item
                    label="新規登録"
                    default-opened
                    class="sub-item init-reg-title"
                    >
                    <q-list no-border link inset-delimiter>
                      <div v-if="store.loginInfo.releaseCkanAddr">
                        <q-item
                          clickable
                          :active="link === 'releaseRegister'"
                          @click="btnMoveRegistration('new_release_register')"
                          active-class="my-menu-sub-link"
                          dense
                        >
                          <q-item-section class="child-item">横断検索カタログ作成</q-item-section>
                        </q-item>
                      </div>
                      <div v-if="store.loginInfo.detailCkanAddr">
                        <q-item
                          clickable
                          :active="link === 'detailRegister'"
                          @click="btnMoveRegistration('new_detail_register')"
                          active-class="my-menu-sub-link"
                          dense
                        >
                          <q-item-section class="child-item">詳細検索カタログ作成</q-item-section>
                        </q-item>
                      </div>
                      <div v-if="store.loginInfo.releaseCkanAddr && store.loginInfo.detailCkanAddr">
                        <q-item
                          clickable
                          :active="link === 'bothRegister'"
                          @click="btnMoveRegistration('new_both_register')"
                          active-class="my-menu-sub-link"
                          dense
                        >
                          <q-item-section class="child-item">横断・詳細検索カタログ作成</q-item-section>
                        </q-item>
                      </div>
                    </q-list>
                  </q-expansion-item>
                </q-item-section>
              </q-item>
              <q-item>
                <q-item-section>
                  <q-item
                    clickable
                    :active="link === 'selectDraft'"
                    @click="btnMoveRestart()"
                    active-class="my-menu-sub-link"
                  >
                    <q-item-section class="sub-item">登録再開</q-item-section>
                  </q-item>
                </q-item-section>
              </q-item>
              <q-item>
                <q-item-section>
                  <q-item
                    clickable
                    :active="link === 'search'"
                    @click="btnMoveSearch()"
                    active-class="my-menu-sub-link"
                  >
                    <q-item-section class="sub-item">複製・編集・削除</q-item-section>
                  </q-item>
                </q-item-section>
              </q-item>
            </q-list>
          </q-expansion-item>
        </q-item-section>
      </q-item>

      <q-item>
        <q-item-section>
          <q-expansion-item
            label="ユーティリティ"
            default-opened
            class="item"
          >
            <q-list no-border link inset-delimiter>
              <q-item
                clickable
                :active="link === 'import'"
                @click="btnMoveImport()"
                active-class="my-menu-sub-link"
              >
                <q-item-section class="sub-item">インポート</q-item-section>
              </q-item>
              <q-item
                clickable
                :active="link === 'export'"
                @click="btnMoveExport()"
                active-class="my-menu-sub-link"
              >
                <q-item-section class="sub-item">エクスポート</q-item-section>
              </q-item>
            </q-list>
          </q-expansion-item>
        </q-item-section>
      </q-item>

      <q-item>
        <q-item-section>
          <q-expansion-item
            label="設定"
            default-opened
            class="item"
          >
            <q-list no-border link inset-delimiter>
              <q-item
                clickable
                :active="link === 'template'"
                @click="btnMoveTemplate()"
                active-class="my-menu-sub-link"
              >
                <q-item-section class="sub-item">テンプレート編集</q-item-section>
              </q-item>
            </q-list>
          </q-expansion-item>
        </q-item-section>
      </q-item>

    <!-- 確認ダイアログ -->
    </q-list>
    <OperationConfirmDialog
      v-bind:dialogInfo="confirmDialog"
      @confirm="onOperationConfirmDialogConfirm"
      @close-dialog="onOperationConfirmDialogCancel"
    />
    
    <!-- 完了ダイアログ -->
    <CompleteDialog
      v-bind:dialogInfo="completeDialog"
      @close-dialog="completeDialog.isDisplay = false"
    />
  </div>
</template>

<style lang="scss">
.init-reg-title .q-item__label{
  margin-left: 8px;
}

.q-list .q-item {
    padding: 5px 5px;
}

.q-drawer .item .q-item {
    padding: 5px 7px;
}

.item{
  font-size: 14px;
}

.sub-item{
  font-size: 13px;
  margin-left: 7px;
  white-space: nowrap;
}

.child-item{
  font-size: 11px;
  margin-left: 10px;
  white-space: nowrap;
}


.my-menu-sub-link{
  font-size: 13px;
  color: #2650A4;
  background-color: #E8F1FA;
  margin-left: 15px;
}
</style>
