<script setup>
import { config } from'boot/config'
import { reactive, ref, watch, onMounted, onBeforeUnmount } from 'vue'
import { Loading } from 'quasar'
import axios from 'axios'
import { useStore } from '../stores/store'
import { useRouter, isNavigationFailure } from 'vue-router'

import DatasetInfo from '../components/DatasetInfo.vue'
import DatasetOption from '../components/DatasetOption.vue'
import DatasetResource from '../components/DatasetResource.vue'
import DatasetUseTerms from '../components/DatasetUseTerms.vue'
import DatasetConfirm from '../components/DatasetConfirm.vue'
import Completion from '../components/DatasetRegistComp.vue'
import CompleteDialog from '../components/dialog/CompleteDialog.vue'
import TemporalSaveDialog from '../components/dialog/TemporalSaveDialog.vue'
import { worker } from 'cluster'

const router = useRouter()
const store = useStore()
var step = ref(1)
const attr = reactive({
  tmpSaveDialog: {
    isDisplay: false,
    catalogName: ''
  },
  displayTmpSaveBtn: true,
  completeDialog: {
    isDisplay: false,
    message: '',
    errorFlg: false
  },
  // CKAN登録結果（DatasetRegistComp.vueに受け渡す)
  registerResult: {
    res: '',
    error: ''
  }
})

const datasetInfo = ref()
const datasetResource = ref()
const datasetOption = ref()
const datasetUseTerms = ref()
const datasetConfirm = ref()

// watch
watch(() => store.createNewCatalog,
  (newVal, oldVal) => {
    if (step.value === 1) {
      if (!datasetInfo.value) {
        return
      }
      datasetInfo.value.initDatasetinfo()
    } else {
      step.value = 1
    }
})

watch(() => store.mode,
  (newVal, oldVal) => {
    // modeがtemplateの場合、一時保存ボタンを非表示
    switchDisplayTmpSaveBtn(newVal)
})

watch(() => step.value,
  (newVal, oldVal) => {
    if(newVal == 1){
      // 編集中フラグをセット
      store.isCatalogEditing = true
    }else if(newVal == 6){
      // 編集中フラグをクリア
      store.isCatalogEditing = false
    }
})

onMounted(function(){
  console.log('-- Dataset.vue onMounted --')
  // 編集中フラグをセット
  store.isCatalogEditing = true
  switchDisplayTmpSaveBtn(store.mode)
})

onBeforeUnmount(function(){
  // 編集中フラグをクリア
  store.isCatalogEditing = false
})

// method
// modeによって一時保存ボタンの表示を切り替える
function switchDisplayTmpSaveBtn(mode){
  switch (mode) {
    case 'new_release_register':
    case 'new_detail_register':
    case 'new_both_register':
      attr.displayTmpSaveBtn = true
      break
    default:
      attr.displayTmpSaveBtn = false
  }
}

// データ概要情報画面へ進む
function btnNextToDataJacket() {
  var noError =  datasetInfo.value.checkErrorAllFields()
  if (noError) {
    // エラーフィールドがなければ次ページへ遷移
    step.value = 2
    // エラーフィールドがなければ入力項目をストアに更新
    datasetInfo.value.commitStore()
    return false
  } else {
    return true
  }
}

// データセット情報(任意)画面へ遷移
function btnNextToDatasetOptional() {
  var noError = datasetResource.value.checkErrorAllFields()
  if (noError) {
    // エラーフィールドがなければ次ページへ遷移
    step.value = 3
    // エラーフィールドがなければ入力項目をストアに更新
    datasetResource.value.commitStore()
  }
}

// 利用条件画面へ遷移
function btnNextToUserterms() {
  var noError = datasetOption.value.checkErrorAllFields()
  if (noError) {
    // エラーフィールドがなければ次ページへ遷移
    step.value = 4
    // エラーフィールドがなければ入力項目をストアに更新
    datasetOption.value.commitStore()
  }
}

// 確認画面へ遷移
function btnNextToConfirm() {
  store.copyLicenseToFiledataDetails()
  var noError = datasetUseTerms.value.checkErrorAllFields()
  if (noError) {
    // エラーフィールドがなければ次ページへ遷移
    step.value = 5
    // エラーフィールドがなければ入力項目をストアに更新
    datasetUseTerms.value.commitStore()
  }
}

// データセット情報画面からの一時保存ファイル名取得
// 一時保存確認ポップアップ画面表示
function btnConfirmTemporalSave() {
  if (step.value === 1) {
    datasetInfo.value.commitStore()
  }
  attr.tmpSaveDialog.catalogName = store.catalogTitle
  attr.tmpSaveDialog.isDisplay = true
}

// データ一時保存
function btnTemporalSave(filename) {
  if (step.value === 1) {
    datasetInfo.value.commitStore()
  } else if (step.value === 2) {
    datasetResource.value.commitStore()
  } else if (step.value === 3) {
    datasetOption.value.commitStore()
  } else if (step.value === 4) {
    datasetUseTerms.value.commitStore()
  }
  var tmpFile = {
    tmp_file_name: filename,
    ckan_info: store.mode
  }
  var datasetinfo = {
    title: store.catalogTitle,
    notes: store.catalogDescription,
    url: store.datasetDescriptionUrl,
    caddec_dataset_id_for_detail: store.datasetIdForDetail,
    regist_org: store.registOrg,
    caddec_provider_id: store.publisherId,
    publisher_name: store.publisher,
    publisher_uri: store.publisherUri,
    creator_name: store.creator,
    creator_url: store.creatorUrl,
    contact_name: store.contactPoint,
    contact_url: store.contactPointUrl
  }
  var datajacket = store.filedataDetails
  var datasetoptionalinfo = {
    theme: store.selectThemes,
    tags: store.selectTags,
    language: store.selectLanguage,
    vocabulary: store.vocabulary,
    term: store.term,
    frequency: store.frequency,
    spatial_url: store.geonames.spatialUrl,
    spatial_text: store.geonames.spatialName,
    spatial: store.geonames.spatial,
    temporal_start: store.dataCalender.start,
    temporal_end: store.dataCalender.end
  }
  var userterms = {
    license_title: store.termName,
    license_url: store.termNameUrl,
    rights: store.usrRight,
    access_rights: store.accessRights,
    access_rights_url: store.accessRightsUrl,
    haspolicy_url: store.haspolicyUrl,
    prov_was_generated_by_url: store.provWasGeneratedByUrl,
    conforms_to: store.conformsTo,
    trading_policy_contract_type: store.contractType,
    trading_policy_nda: store.secrecy,
    trading_policy_use_application: store.useApplication,
    trading_policy_use_application_free: store.useApplicationOther,
    scope_of_disclosure: store.scopeOfDisclosure,
    scope_of_disclosure_free: store.scopeOfDisclosureOther,
    terms_of_use_permissible_region: store.permissionResion,
    terms_of_use_permissible_region_free: store.permissionResionOther,
    terms_of_use_notices: store.notices,
    privacy_policy_contains_personal_data: store.personalData,
    privacy_policy_contains_personal_data_free: store.personalDataOther,
    data_effective_period_term: store.dataEffectivePeriod.selectTerms,
    data_effective_period_start: store.dataEffectivePeriod.startDate,
    data_effective_period_end: store.dataEffectivePeriod.endDate,
    data_effective_period_free: store.dataEffectivePeriod.freefield,
    usage_license_period_term: store.usageLicensePeriod.selectTerms,
    usage_license_period_deadline: store.usageLicensePeriod.deadline,
    usage_license_period_period: store.usageLicensePeriod.period,
    usage_license_period_unit: store.usageLicensePeriod.unit,
    usage_license_period_free: store.usageLicensePeriod.freefield,
    fee: store.fee,
    sales_info_url: store.salesInfoUrl,
    pricing_price_range: store.priceRange,
    pricing_notices_of_price: store.noticesOfPrice,
    warranty_express_warranty: store.expressWarranty,
    warranty_express_warranty_free: store.expressWarrantyOther,
    warranty_legal_compliance: store.leagalCompliance,
    warranty_legal_compliance_free: store.leagalComplianceOther
  }
  var dataForUpdate = {
    ckan_data_name: store.ckanDataName,
    issued: store.issued,
    identifier: store.identifier,
    dataset_url: store.datasetUrl
  }
  const saveData = {
    tmpFile: tmpFile,
    datasetinfo: datasetinfo,
    datajacket: datajacket,
    datasetoptionalinfo: datasetoptionalinfo,
    userterms: userterms,
    dataForUpdate: dataForUpdate
  }
  axios
    .put(config.apiPrefix + '/temporal', saveData)
    .then(async res => {
      attr.completeDialog.isDisplay = true
      attr.completeDialog.message = '一時保存に成功しました。'
      attr.completeDialog.errorFlg = false
    })
    .catch(err => {
      console.log('error message:', err.response.data.message)
      attr.completeDialog.isDisplay = true
      attr.completeDialog.message = err.response.data.message || '一時保存に失敗しました。\n管理者に問い合わせてください。'
      attr.completeDialog.errorFlg = true
    })
}

// 画面最上部移動
function topScroll() {
  window.scrollTo(0, 0)
}

// 横断CKAN登録
function registerReleaseCatalog() {
  Loading.show()
  var releaseData = datasetConfirm.value.formatCatalogParameter()
  // TODO:以下の項目の値は空値に設定する。必要なさそうであれば削除
  // 詳細検索カタログと紐づけない場合、以下の項目を空にする
  if(store.mode === 'new_release_register' || store.mode === 'release_duplicate'){
    for(var i = 0; i < releaseData.data_creator.length; i++){
      if(releaseData.data_creator[i].label === 'caddec_dataset_id_for_detail'){
        releaseData.data_creator[i].value = ''
      } 
    }
  }
  releaseData.filedata_details.id = ''
  releaseData.filedata_details.issued = ''
  releaseData.dataset_url = ''
  releaseData.identifier = ''
  releaseData.issued = ''
  // 詳細検索カタログと紐づける場合、anotherからデータを取得
  var detailData = ''
  if(store.mode === 'release-link-detail_duplicate'){
    detailData = datasetConfirm.value.formatLinkAnotherData()
  }
  var registerRequest = {
    release: releaseData,
    detail: detailData
  }
  var registerUrl = '/datacatalog/release/add'
  topScroll()
  registerToCkan(registerRequest, registerUrl)
}

// 詳細CKAN登録
function registerDetailCatalog() {
  Loading.show()
  var detailData = datasetConfirm.value.formatCatalogParameter()
  // TODO:以下の項目の値は空値に設定する。必要なさそうであれば削除
  // 横断検索カタログと紐づけない場合、以下の項目を空にする
  if(store.mode === 'new_detail_register' || store.mode === 'detail_duplicate'){
    for(var i = 0; i < detailData.data_creator.length; i++){
      if(detailData.data_creator[i].label === 'caddec_dataset_id_for_detail'){
        // pkg.data_creator[i].value = ''
        detailData.data_creator[i].value = ''
      } 
    }
  }  
  detailData.filedata_details.id = ''
  detailData.filedata_details.issued = ''
  detailData.dataset_url = ''
  detailData.identifier = ''
  detailData.issued = ''
  // 横断検索カタログと紐づける場合、anotherからデータを取得
  var releaseData = ''
  if(store.mode === 'detail-link-release_duplicate'){
    releaseData = datasetConfirm.value.formatLinkAnotherData()
  }
  var registerRequest = {
    release: releaseData,
    detail: detailData
  }
  var registerUrl = '/datacatalog/detail/add'
  topScroll()
  registerToCkan(registerRequest, registerUrl)
}

// 横断CKAN・詳細CKAN登録
function registerBothCatalog() {
  Loading.show()
  var pkg = datasetConfirm.value.formatCatalogParameter()
  // TODO:以下の項目の値は空値に設定する。必要なさそうであれば削除
  pkg.filedata_details.id = ''
  pkg.filedata_details.issued = ''
  pkg.dataset_url = ''
  pkg.identifier = ''
  pkg.issued = ''
  var registerRequest = {
    release: pkg,
    detail: pkg
  }
  var registerUrl = '/datacatalog/add'
  topScroll()
  registerToCkan(registerRequest, registerUrl)
}

// 横断カタログ編集
function editReleaseCatalog() {
  Loading.show()
  var releaseData = datasetConfirm.value.formatCatalogParameter()
  releaseData.ckan_data_name = store.releaseCkanDataName
  var detailData = datasetConfirm.value.formatDetailEdit()
  if (datasetConfirm.value.checkEditFlg()) {
    // 編集フラグがtrueの項目があれば、詳細カタログを更新する
    var registerUrl = '/datacatalog/edit'
    var registerRequest = {
      release: releaseData,
      detail: detailData
    }
  } else {
    registerUrl = '/datacatalog/release/edit'
    registerRequest = {
      release: releaseData
    }
  }
  topScroll()
  registerToCkan(registerRequest, registerUrl)
}

// 詳細カタログ編集
function editDetailCatalog() {
  Loading.show()
  var detailData = datasetConfirm.value.formatCatalogParameter()
  detailData.ckan_data_name = store.detailCkanDataName
  var releaseData = datasetConfirm.value.formatReleaseEdit()
  if (datasetConfirm.value.checkEditFlg()) {
    // 編集フラグがtrueの項目があれば、横断カタログを更新する
    var registerUrl = '/datacatalog/edit'
    var registerRequest = {
      release: releaseData,
      detail: detailData
    }
  } else {
    registerUrl = '/datacatalog/detail/edit'
    registerRequest = {
      detail: detailData
    }
  }
  topScroll()
  registerToCkan(registerRequest, registerUrl)
}

function registerToCkan(registerInfo, registerUrl) {
  axios
    .put(config.apiPrefix + registerUrl, registerInfo)
    .then(async res => {
      attr.registerResult.res = res.data
      step.value = 6
      Loading.hide()
    })
    .catch(err => {
      Loading.hide()
      console.log('error message:', err.response.data.message)
      attr.registerResult.error = err
      attr.completeDialog.isDisplay = true
      attr.completeDialog.message = err.response.data.message || 'カタログ登録に失敗しました。\n管理者に問い合わせてください。'
      attr.completeDialog.errorFlg = true
    })
}

// DisplayFlgの更新
function itemDisplayFlgStoreCommit(flgValue) {
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
      downloadUrl: flgValue.datajacket.downloadurl,
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
function commitDatasetinfo(data, storeTypeList) {
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
function commitDatajacket(data, storeTypeList) {
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
      // 配信の説明ページURL
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
function commitDatasetoptionalinfo(data, storeTypeList) {
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
function commitUserterms(data, storeTypeList) {
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

// テンプレート取得・設定
function setTemplate() {
  axios.get(config.apiPrefix + '/template')
    .then((response) => {
      // 各フィールドの表示形式コミット
      var itemDisplayValue = response.data.template.catalog_display
      itemDisplayFlgStoreCommit(itemDisplayValue)
      // stateを初期化
      store.initStateParams()
      // 各フィールドの値を画面ごとにコミット
      var itemValue = response.data.template.catalog_value
      commitDatasetinfo(itemValue.datasetinfo, ['state', 'template'])
      commitDatajacket(itemValue.datajacket, ['template'])
      commitDatasetoptionalinfo(itemValue.datasetoptionalinfo, ['state', 'template'])
      commitUserterms(itemValue.userterms, ['state', 'template'])
      // テンプレート登録後、メニュー選択画面に遷移する
      router.push('/menuSelect').then(failure => {
        if (!isNavigationFailure(failure)) {
          store.updateMode({ mode: 'menuSelect', ckanType: '', isBothCatalog: false })
        }
      })
    })
    .catch(err => {
      console.log('error message:', err.response.data.message)
      attr.completeDialog.isDisplay = true
      attr.completeDialog.message = err.response.data.message || 'テンプレート取得に失敗しました。\n管理者に問い合わせてください。'
      attr.completeDialog.errorFlg = true
    })
}

// テンプレート更新
function updateTemplate() {
  var templateCatalog = datasetConfirm.value.formatTemplateData()
  axios
    .put(config.apiPrefix + '/template', templateCatalog)
    .then(async res => {
      if (res.data.status === 'success') {
        // 更新したテンプレートを取得し、store.tempalteを更新
        setTemplate()
      }
    })
    .catch(err => {
      console.log('error message:', err.response.data.message)
      attr.completeDialog.isDisplay = true
      attr.completeDialog.message = err.response.data.message || 'テンプレート更新に失敗しました。\n管理者に問い合わせてください。'
      attr.completeDialog.errorFlg = true
    })
}

// 別カタログを新規作成
function btnCreateAnotherCatalog() {
  store.initStateParams()
  store.updateMode({ mode: store.mode, ckanType: '', isBothCatalog: false })
  step.value = 1
  attr.registerResult = {
    res: '',
    error: ''
  }
}

</script>

<template>
  <div class="col-12">
    <q-layout ref="layout" view="hHh lpR fFf">
      <q-page-container
        color="light-blue-10">
        <q-stepper
          v-model="step"
          header-nav
          ref="stepper"
          color="light-blue-10"
          animated
        >
          <q-step
            :name="1"
            title="データセット情報"
            icon="settings"
            :done="step > 1"
            :header-nav="step > 1"
          >
            <!-- データセット情報 -->
            <DatasetInfo
              ref="datasetInfo"
            />
            <q-stepper-navigation>
              <q-footer>
                <q-toolbar class="justify-end">
                  <q-btn
                    v-if="attr.displayTmpSaveBtn"
                    flat
                    color="white"
                    icon="save_alt"
                    @click="btnConfirmTemporalSave()"
                    label="一時保存"
                    class="col-grow"
                  />
                  <q-btn
                    flat
                    color="white"
                    icon-right="arrow_forward_ios"
                    @click="btnNextToDataJacket()"
                    label="次へ"
                  />
                </q-toolbar>
              </q-footer>
            </q-stepper-navigation>
          </q-step>
          <br>
          <!--                                         -->
          <!--                                         -->
          <q-step
            :name="2"
            title="データ概要情報"
            icon="list_alt"
            :done="step > 2"
            :header-nav="step > 2"
          >
            <!-- データ概要情報 -->
            <DatasetResource
              ref="datasetResource"
            />
            <q-stepper-navigation>
              <q-footer elevated>
                <q-toolbar class="justify-end">
                  <q-btn
                    v-if="attr.displayTmpSaveBtn"
                    flat
                    color="white"
                    icon="save_alt"
                    @click="btnConfirmTemporalSave()"
                    label="一時保存"
                    class="col-grow"
                  />
                  <q-btn
                    flat
                    color="white"
                    icon="arrow_back_ios"
                    @click="datasetResource.commitStore(), step = 1"
                    label="戻る"
                  />
                  <q-btn
                    flat
                    color="white"
                    icon-right="arrow_forward_ios"
                    @click="btnNextToDatasetOptional()"
                    label="次へ"
                  />
                </q-toolbar>
              </q-footer>
            </q-stepper-navigation>
          </q-step>
          <!--                                         -->
          <!--                                         -->
          <q-step
            :name="3"
            title="データセット情報（任意）"
            icon="list_alt"
            :done="step > 3"
            :header-nav="step > 3"
          >
            <!-- データセット情報 (任意)-->
            <DatasetOption
              ref="datasetOption"
            />
            <q-stepper-navigation>
              <q-footer elevated>
                <q-toolbar class="justify-end">
                  <q-btn
                    v-if="attr.displayTmpSaveBtn"
                    flat
                    color="white"
                    icon="save_alt"
                    @click="btnConfirmTemporalSave()"
                    label="一時保存"
                    class="col-grow"
                  />
                  <q-btn
                    flat
                    color="white"
                    icon="arrow_back_ios"
                    @click="datasetOption.commitStore(), step = 2"
                    label="戻る"
                  />
                  <q-btn
                    flat
                    color="white"
                    icon-right="arrow_forward_ios"
                    @click="btnNextToUserterms()"
                    label="次へ"
                  />
                </q-toolbar>
              </q-footer>
            </q-stepper-navigation>
            <br>
            <br>
          </q-step>
          <!--                                         -->
          <!--                                         -->
          <q-step
            :name="4"
            title="利用条件"
            icon="list_alt"
            :done="step > 4"
            :header-nav="step > 4"
          >
            <!-- 利用条件 -->
            <DatasetUseTerms
              ref="datasetUseTerms"
            />
            <q-stepper-navigation>
              <q-footer elevated>
                <q-toolbar class="justify-end">
                  <q-btn
                    v-if="attr.displayTmpSaveBtn"
                    flat
                    color="white"
                    icon="save_alt"
                    @click="btnConfirmTemporalSave()"
                    label="一時保存"
                    class="col-grow"
                  />
                  <q-btn
                    flat
                    color="white"
                    icon="arrow_back_ios"
                    @click="datasetUseTerms.commitStore(), step = 3"
                    label="戻る"
                  />
                  <q-btn
                    flat
                    color="white"
                    icon-right="arrow_forward_ios"
                    @click="btnNextToConfirm()"
                    label="次へ"
                  />
                </q-toolbar>
              </q-footer>
            </q-stepper-navigation>
          </q-step>
          <!--                                         -->
          <!--                                         -->
          <q-step
            :name="5"
            title="確認"
            icon="cloud_upload"
            :done="step > 5"
            :header-nav="step > 5"
          >
            <!-- 確認 -->
            <DatasetConfirm
              ref="datasetConfirm"
            />
            <q-stepper-navigation>
              <q-footer elevated>
                  <q-toolbar class="justify-end">
                    <q-btn
                      v-if="attr.displayTmpSaveBtn"
                      flat
                      color="white"
                      icon="save_alt"
                      @click="btnConfirmTemporalSave()"
                      label="一時保存"
                      class="col-grow"
                    />
                    <div v-if="store.selectedMode.mode === 'new_release_register' || store.selectedMode.mode === 'new_detail_register' || store.selectedMode.mode === 'new_both_register' || store.selectedMode.mode === 'release_duplicate' || store.selectedMode.mode === 'detail_duplicate' || store.selectedMode.mode === 'both_duplicate' || store.selectedMode.mode === 'release-link-detail_duplicate' || store.selectedMode.mode === 'detail-link-release_duplicate'">
                      <q-btn
                        flat
                        color="white"
                        icon="arrow_back_ios"
                        @click="step = 4"
                        label="戻る"
                      />
                      <!-- 横断登録 -->
                      <q-btn
                        v-if="store.selectedMode.mode === 'new_release_register' || store.selectedMode.mode === 'release_duplicate' || store.selectedMode.mode === 'release-link-detail_duplicate'"
                        outline
                        color="white"
                        @click="registerReleaseCatalog()"
                        label="登録"
                      />
                      <!-- 詳細登録 -->
                      <q-btn
                        v-if="store.selectedMode.mode === 'new_detail_register' || store.selectedMode.mode === 'detail_duplicate' || store.selectedMode.mode === 'detail-link-release_duplicate'"
                        outline
                        color="white"
                        @click="registerDetailCatalog()"
                        label="登録"
                      />
                      <!-- 横断・詳細登録 -->
                      <q-btn
                        v-if="store.selectedMode.mode === 'new_both_register' || store.selectedMode.mode === 'both_duplicate'"  
                        outline
                        color="white"
                        @click="registerBothCatalog()"
                        label="登録"
                      />
                    </div>
                    <!-- 編集 -->
                    <div v-if="store.selectedMode.mode === 'edit'">
                      <q-btn
                        flat
                        color="white"
                        icon="arrow_back_ios"
                        @click="step = 4"
                        label="戻る"
                        class="btn-back-edit"
                      />
                      <q-btn
                        v-if="store.selectedMode.ckanType === 'release'"
                        outline
                        color="white"
                        @click="editReleaseCatalog()"
                        label="編集"
                      />
                      <q-btn
                        v-if="store.selectedMode.ckanType === 'detail'"
                        outline
                        color="white"
                        @click="editDetailCatalog()"
                        label="編集"
                      />
                    </div>
                    <div v-if="store.selectedMode.mode === 'template'">
                      <q-btn
                        flat
                        color="white"
                        icon="arrow_back_ios"
                        @click="step = 4"
                        label="戻る"
                        class="btn-back-template"
                      />
                      <q-btn
                        outline
                        color="white"
                        @click="updateTemplate()"
                        label="テンプレート更新"
                      />
                    </div>
                  </q-toolbar>
                </q-footer>
            </q-stepper-navigation>
            <br>
            <br>
          </q-step>
          <q-step
            :name="6"
            title="完了"
            icon="cloud_done"
            :header-nav="step > 6"
          >
            <!-- 完了 -->
            <Completion
              ref="completion"
              :registerResult="attr.registerResult"
            />
            <div v-if="store.selectedMode.mode !== 'edit'">
              <q-stepper-navigation class="row justify-end">
                <q-btn
                  flat
                  @click="btnCreateAnotherCatalog()"
                  color="light-blue-10"
                  label="別のデータセットを引き続き入力"
                />
              </q-stepper-navigation>
            </div>
          </q-step>
        </q-stepper>
      </q-page-container>

      <!-- 一時保存ダイアログ -->
      <TemporalSaveDialog 
        v-bind:dialogInfo="attr.tmpSaveDialog"
        @tmp-save="btnTemporalSave"
        @close-dialog="attr.tmpSaveDialog.isDisplay = false"
      />

      <!-- 完了ダイアログ -->
      <CompleteDialog 
        v-bind:dialogInfo="attr.completeDialog"
        @close-dialog="attr.completeDialog.isDisplay = false, attr.tmpSaveDialog.isDisplay = false"
      />

    </q-layout>
  </div>
</template>

<style lang="scss">
.q-card-background-white{
  background: white;
}

.docs-step-btn .q-btn{
  margin: 5px;
}

.docs-step-btn .btn-fixed-width{
  width: 200px;
}

.docs-step-btn .btn-fixed-bottom-right{
  position: bottom-right;
}
</style>
