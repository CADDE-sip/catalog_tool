<script setup>
import { config } from'boot/config'
import { ref, reactive, watch, onMounted } from 'vue'
import { useStore } from '../stores/store'
import { useRouter } from 'vue-router'
import axios from 'axios'
import DeleteDialog from '../components/dialog/DeleteDialog.vue'
import OperationConfirmDialog from '../components/dialog/OperationConfirmDialog.vue'
import DatasetConfirm from '../components/DatasetConfirm.vue'
import CompleteDialog from '../components/dialog/CompleteDialog.vue'

const store = useStore()
const router = useRouter()

// 自由欄の先頭と末尾の文字位置
const FIRST_OTHER = 4
const LAST_OTHER = -1

const tmpCatalogData = ''
const periodUnit = [
    {
      label: '日',
      value: 'day'
    },
    {
      label: '週',
      value: 'week'
    },
    {
      label: '月',
      value: 'month'
    },
    {
      label: '年',
      value: 'year'
    }
]
const selected = ref([])
const attr = reactive({
  showResult: false,
  displayData: [],
  btnDisable: false,
  noCatalogSelected: true,
  inputUrlDisable: true,
  inputKeywordDisable: false,
  confirmDialog: {
    isDisplay: false,
    type: '',
    catalogTitle: '',
    message: '',
    options: {}
  },
  deleteDialog: {
    pageName: '',
    isDisplay: false,
    type:'',
    options: {}
  },
  completeDialog: {
    isDisplay: false,
    message: '',
    errorFlg: false
  },
  getData: [],
  inputCkanUrl: '',
  inputKeyword: '*:*',
  searchResultColumns: [],
  serchCkanType: '',
  displayReleaseNote: false,
  displayDetailNote: false,
  tableHeader: ''
})

// 確認画面表示フラグ
var isShowCatalogInfo = ref(false)
const datasetConfirm = ref()

// onMounted
onMounted(function(){
  console.log('-- Search.vue onMounted --')
  // 検索先CKANのデフォルト値を設定
  if (store.loginInfo.releaseCkanAddr && store.loginInfo.detailCkanAddr) {
    attr.serchCkanType = 'bothCkan'
  }
})

// method
// データ検索機能
function btnActionSearch() {
  const dataForSearch = {
    url: attr.inputCkanUrl,
    keyword: attr.inputKeyword
  }
  attr.displayReleaseNote = false
  attr.displayDetailNote = false
  // 横断検索用CKANまたは詳細検索用CKANのどちらかのみが存在する場合は、検索先CKANを内部で指定
  if (!store.loginInfo.detailCkanAddr) {
    attr.serchCkanType = 'releaseCkan'
  }else if (!store.loginInfo.releaseCkanAddr) {
    attr.serchCkanType = 'detailCkan'
  }
  if(attr.serchCkanType === 'releaseCkan'){// 横断検索用CKAN
    searchReleaseCkan(dataForSearch)
  }else if(attr.serchCkanType === 'detailCkan'){// 詳細検索用CKAN
    searchDetailCkan(dataForSearch)
  }else if(attr.serchCkanType === 'bothCkan'){//横断・詳細検索用CKAN
    searchBothCkan(dataForSearch)
  }
}

// 横断検索用CKAN
function searchReleaseCkan(dataForSearch){
  attr.displayData = []
  attr.showResult = false
  attr.searchResultColumns =[
    { name: 'releaseTitle', align: 'left', label: '横断検索用CKAN', field: 'releaseTitle', sortable: true, classes:'underline' },
    { name: 'releaseLastUpdate', align: 'left', label: '最終更新日', field: 'releaseLastUpdate', sortable: true },
    { name: 'releaseRegister', align: 'center', label: '', field: 'releaseRegister', sortable: false },
    { name: 'releaseEdit', align: 'center', label: '', field: 'releaseEdit', sortable: false },
    { name: 'releaseDelete', align: 'center', label: '', field: 'releaseDelete', sortable: false }
  ]
  axios.post(config.apiPrefix + '/datacatalog/release/search', dataForSearch)
    .then(response => {
      console.log(response)
      attr.getData = response.data.datasets
      attr.tableHeader = '横断検索用CKAN検索結果一覧'
      attr.showResult = true
      attr.displayReleaseNote = true
      for (var i = 0; i < attr.getData.length; i++) {
        attr.displayData.push({
          searchCkanType: attr.serchCkanType,
          releaseTitle: attr.getData[i].release.title,
          releaseLastUpdate: attr.getData[i].release.metadata_modified.slice(0, 10).replace(/-/g, '/'),
          releaseId: attr.getData[i].release.id,
          releaseCkanDataName: attr.getData[i].release.name,
          detailId: attr.getData[i].detail.id,
          detailTitle: attr.getData[i].detail.title,
          detailCkanDataName: attr.getData[i].detail.name,
          // 主キー設定
          uniqueId: attr.getData[i].release.id
        })
      }
    })
    .catch(err => {
      console.log('error message:', err.response.data.message)
      attr.completeDialog.isDisplay = true
      attr.completeDialog.message = err.response.data.message || '横断検索カタログ検索に失敗しました。\n管理者に問い合わせてください。'
      attr.completeDialog.errorFlg = true
    })
}

// 詳細検索用CKAN
function searchDetailCkan(dataForSearch){
  attr.displayData = []
  attr.showResult = false
  attr.searchResultColumns =[
    { name: 'detailTitle', align: 'left', label: '詳細検索用CKAN', field: 'detailTitle', sortable: true, classes:'underline' },
    { name: 'detailLastUpdate', align: 'left', label: '最終更新日', field: 'detailLastUpdate', sortable: true },
    { name: 'detailRegister', align: 'center', label: '', field: 'detailRegister', sortable: false }, 
    { name: 'detailEdit', align: 'center', label: '', field: 'detailEdit', sortable: false },
    { name: 'detailDelete', align: 'center', label: '', field: 'detailDelete', sortable: false }
  ]
  axios.post(config.apiPrefix + '/datacatalog/detail/search', dataForSearch)
    .then(response => {
      console.log(response)
      attr.getData = response.data.datasets
      attr.tableHeader = '詳細検索用CKAN検索結果一覧'
      attr.showResult = true
      attr.displayDetailNote = true
      for (var i = 0; i < attr.getData.length; i++) {
        attr.displayData.push({
          searchCkanType: attr.serchCkanType,
          detailTitle: attr.getData[i].detail.title,
          detailLastUpdate: attr.getData[i].detail.metadata_modified.slice(0, 10).replace(/-/g, '/'),
          detailId: attr.getData[i].detail.id,
          detailCkanDataName: attr.getData[i].detail.name,
          releaseId: attr.getData[i].release.id,
          releaseTitle: attr.getData[i].release.title,
          releaseCkanDataName: attr.getData[i].release.name,
          // 主キー設定
          uniqueId: attr.getData[i].detail.id
        })
      }
    })
    .catch(err => {
      console.log('error message:', err.response.data.message)
      attr.completeDialog.isDisplay = true
      attr.completeDialog.message = err.response.data.message || '詳細検索カタログ検索に失敗しました。\n管理者に問い合わせてください。'
      attr.completeDialog.errorFlg = true
    })
}

// 横断・詳細検索用CKAN
function searchBothCkan(dataForSearch){
  attr.displayData = []
  attr.showResult = false
  attr.searchResultColumns =[
    { name: 'releaseTitle', align: 'left', label: '横断検索用CKAN', field: 'releaseTitle', sortable: true, classes:'underline' },
    { name: 'releaseLastUpdate', align: 'left', label: '最終更新日', field: 'releaseLastUpdate', sortable: true },
    { name: 'releaseRegister', align: 'center', label: '', field: 'releaseRegister', sortable: false },
    { name: 'releaseEdit', align: 'center', label: '', field: 'releaseEdit', sortable: false },
    { name: 'releaseDelete', align: 'center', label: '', field: 'releaseDelete', sortable: false },
    { name: 'detailTitle', align: 'left', label: '詳細検索用CKAN', field: 'detailTitle', sortable: true, classes:'underline',
    style: {borderLeft: '3px solid #1976d2'}, headerStyle: {borderLeft: '3px solid #1976d2'} },
    { name: 'detailLastUpdate', align: 'left', label: '最終更新日', field: 'detailLastUpdate', sortable: true },
    { name: 'detailRegister', align: 'center', label: '', field: 'detailRegister', sortable: false }, 
    { name: 'detailEdit', align: 'center', label: '', field: 'detailEdit', sortable: false },
    { name: 'detailDelete', align: 'center', label: '', field: 'detailDelete', sortable: false }
  ]
  axios.post(config.apiPrefix + '/datacatalog/search', dataForSearch)
    .then(response => {
      console.log(response)
      attr.getData = response.data.datasets
      attr.tableHeader = '横断・詳細検索用CKAN検索結果一覧'
      attr.showResult = true
      for (var i = 0; i < attr.getData.length; i++) {
        if (attr.getData[i].release.title && attr.getData[i].detail.title) {
          // 横断・詳細検索カタログで紐づき関係あり
          attr.displayData.push({
            searchCkanType: attr.serchCkanType,
            releaseTitle: attr.getData[i].release.title,
            releaseLastUpdate: attr.getData[i].release.metadata_modified.slice(0, 10).replace(/-/g, '/'),
            releaseId: attr.getData[i].release.id,
            releaseCkanDataName: attr.getData[i].release.name,
            // ユニークな値を横断検索カタログ「登録」ボタンカラムに設定
            detailTitle: attr.getData[i].detail.title,
            detailLastUpdate: attr.getData[i].detail.metadata_modified.slice(0, 10).replace(/-/g, '/'),
            detailCkanDataName: attr.getData[i].detail.name,
            detailId: attr.getData[i].detail.id,
            uniqueId: attr.getData[i].release.id
          })
        } else if (attr.getData[i].release.title) {
          // 横断検索カタログのみ
          attr.displayData.push({
            searchCkanType: attr.serchCkanType,
            releaseTitle: attr.getData[i].release.title,
            releaseLastUpdate: attr.getData[i].release.metadata_modified.slice(0, 10).replace(/-/g, '/'),
            releaseId: attr.getData[i].release.id,
            releaseCkanDataName: attr.getData[i].release.name,
            // 主キー設定
            uniqueId: attr.getData[i].release.id
          })
        } else {
          // 詳細検索カタログのみ
          attr.displayData.push({
            detailTitle: attr.getData[i].detail.title,
            detailLastUpdate: attr.getData[i].detail.metadata_modified.slice(0, 10).replace(/-/g, '/'),
            detailCkanDataName: attr.getData[i].detail.name,
            detailId: attr.getData[i].detail.id,
            // 主キー設定
            uniqueId: attr.getData[i].detail.id
          })
        }
      }
  })
  .catch(err => {
    console.log('error message:', err.response.data.message)
    attr.completeDialog.isDisplay = true
    attr.completeDialog.message = err.response.data.message || '横断検索カタログ・詳細検索カタログ検索に失敗しました。\n管理者に問い合わせてください。'
    attr.completeDialog.errorFlg = true
  })
}

// 複製または編集ボタン押下時、複製データをカタログ作成画面に反映
function setCatalogData(data, ckanType, selectedMode) {
  var i = 0
  tmpCatalogData = ''
  var isBothCatalog = false
  // 選択したデータが横断・詳細カタログどちらも保有
  if (data.detailId && data.releaseId) isBothCatalog = true
  store.updateMode({ mode: selectedMode, ckanType: ckanType, isBothCatalog: isBothCatalog })
  store.updateCkanName({ releaseCkanDataName: data.releaseCkanDataName, detailCkanDataName: data.detailCkanDataName })
  
  // 選択された行の横断カタログと詳細カタログを取得
  var releaseData = ''
  var detailData = ''
  for (i = 0; i < attr.getData.length; i++) {
     if (attr.getData[i].release.id === data.releaseId) {
       releaseData = attr.getData[i].release
      if(selectedMode === 'detail-link-release_duplicate'){
        detailData = attr.getData[i].release // 下書き用に、横断カタログデータを取得
      }
    }
    if (data.detailId && attr.getData[i].detail.id === data.detailId) {
      detailData = attr.getData[i].detail
      if(selectedMode === 'release-link-detail_duplicate'){
        releaseData = attr.getData[i].detail // 下書き用に、詳細カタログデータを取得
      }
    }
  }

  // 複製・編集対象の横断または詳細カタログと、対になる詳細または横断カタログを取得
  var usedCatalogData = ''
  var stockCatalogData = ''  
  if (selectedMode === 'detail_duplicate' || selectedMode === 'release_duplicate' || selectedMode === 'both_duplicate') {// 複製
    if(ckanType === 'release'){
      usedCatalogData = releaseData
    }else{
      usedCatalogData = detailData
    }
  } else if(selectedMode === 'edit' || selectedMode === 'detail-link-release_duplicate' || selectedMode === 'release-link-detail_duplicate'){// 編集、または紐づくカタログ登録
    if (ckanType === 'release') {
      usedCatalogData = releaseData
      stockCatalogData = detailData
    } else {
      usedCatalogData = detailData
      stockCatalogData = releaseData
    }
  }
  setServerData(usedCatalogData, 'updateAutoSetValue')
  setDatasetinfoData(usedCatalogData, 'state')
  setDatajacketData(usedCatalogData, 'state', selectedMode)
  setDatasetoptionalinfoData(usedCatalogData, 'state')
  setUsertermsData(usedCatalogData, 'state')
  if (stockCatalogData) {
    setServerData(stockCatalogData, 'updateAutoSetValueAnother')
    setDatasetinfoData(stockCatalogData, 'another')
    setDatajacketData(stockCatalogData, 'another', selectedMode)
    setDatasetoptionalinfoData(stockCatalogData, 'another')
    setUsertermsData(stockCatalogData, 'another')
  }
  // storeにバックアップデータを作成
  store.backup()
  router.push('/register')
}

// 確認用ダイアログ表示
// data : 選択された行のデータ
// dialogType : OperationConfirmDialogのtype
function showConfirmDialog(data, dialogType){
  let options = {}
  switch(dialogType){
  case 'create-catalog-detail-link-release':
  case 'create-catalog-release-from-release':
  case 'create-catalog-detail-from-release':
  case 'create-catalog-both-from-release':
  case 'edit-catalog-release':
    options.catalogTitle = data.row.releaseTitle
    break
  case 'create-catalog-release-link-detail':
  case 'create-catalog-release-from-detail':
  case 'create-catalog-detail-from-detail':
  case 'create-catalog-both-from-detail':
  case 'edit-catalog-detail':
    options.catalogTitle = data.row.detailTitle
    break
  default:
    return;
  }
  options.detailId  = data.row.detailId
  options.releaseId = data.row.releaseId
  options.releaseCkanDataName = data.row.releaseCkanDataName
  options.detailCkanDataName  = data.row.detailCkanDataName

  attr.confirmDialog.options = options
  attr.confirmDialog.type = dialogType
  attr.confirmDialog.isDisplay = true
}

// 複製および編集操作確認ダイアログで、決定ボタン押下時の動作
// [in] dialogInfo : OperationConfirmDialog.vueのdialogInfo
function onOperationConfirm (dialogInfo) {
  let data = {}
  switch(dialogInfo.type){
  case 'create-catalog-detail-link-release': //１．横断カタログと紐づく詳細カタログ作成
    data.releaseId           = dialogInfo.options.releaseId
    data.releaseCkanDataName = dialogInfo.options.releaseCkanDataName
    data.detailId            = null
    data.detailCkanDataName  = dialogInfo.options.detailCkanDataName
    // 実行モード情報を「紐づく詳細カタログ作成」に更新
    setCatalogData(data, 'detail', 'detail-link-release_duplicate')
    break;
  case 'create-catalog-release-from-release': //２．横断カタログの情報を元に、新規で横断カタログ作成
    data.releaseId           = dialogInfo.options.releaseId
    data.releaseCkanDataName = dialogInfo.options.releaseCkanDataName
    data.detailId            = null
    data.detailCkanDataName  = ''
    // 実行モード情報を「横断カタログ作成」に更新
    setCatalogData(data, 'release', 'release_duplicate')
    break;
  case 'create-catalog-detail-from-release': //３．横断カタログの情報を元に、新規で詳細カタログ作成
    data.releaseId           = dialogInfo.options.releaseId
    data.releaseCkanDataName = dialogInfo.options.releaseCkanDataName
    data.detailId            = null
    data.detailCkanDataName  = dialogInfo.options.detailCkanDataName
    // 実行モード情報を「詳細カタログ作成」に更新
    setCatalogData(data, 'release', 'detail_duplicate')
    break;
  case 'create-catalog-both-from-release' : //４．横断カタログの情報を元に、新規で横断カタログと詳細カタログを作成
    data.releaseId           = dialogInfo.options.releaseId
    data.releaseCkanDataName = dialogInfo.options.releaseCkanDataName
    data.detailId            = null
    data.detailCkanDataName  = dialogInfo.options.detailCkanDataName
    // 実行モード情報を「横断・詳細カタログ作成」に更新
    setCatalogData(data, 'release', 'both_duplicate')
    break;
  case 'create-catalog-release-link-detail': //５．詳細カタログと紐づく横断カタログ作成
    data.releaseId           = null
    data.releaseCkanDataName = dialogInfo.options.releaseDataName
    data.detailId            = dialogInfo.options.detailId
    data.detailCkanDataName  = dialogInfo.options.detailCkanDataName
    // 実行モード情報を「紐づく横断カタログ作成」に更新
    setCatalogData(data, 'release', 'release-link-detail_duplicate')
    break;
  case 'create-catalog-release-from-detail': //６．詳細カタログの情報を元に、新規で横断カタログ作成
    data.releaseId           = null
    data.releaseCkanDataName = dialogInfo.options.releaseDataName
    data.detailId            = dialogInfo.options.detailId
    data.detailCkanDataName  = dialogInfo.options.detailCkanDataName
    // 実行モード情報を「横断カタログ作成」に更新
    setCatalogData(data, 'detail', 'release_duplicate')
    break;
  case 'create-catalog-detail-from-detail': //７．詳細カタログの情報を元に、新規で詳細カタログ作成
    data.releaseId           = null
    data.releaseCkanDataName = dialogInfo.options.releaseDataName
    data.detailId            = dialogInfo.options.detailId
    data.detailCkanDataName  = dialogInfo.options.detailCkanDataName
    // 実行モード情報を「詳細カタログ作成」に更新
    setCatalogData(data, 'detail', 'detail_duplicate')
    break;
  case 'create-catalog-both-from-detail' : //８．詳細カタログの情報を元に、新規で横断カタログと詳細カタログを作成
    data.releaseId           = null
    data.releaseCkanDataName = dialogInfo.options.releaseDataName
    data.detailId            = dialogInfo.options.detailId
    data.detailCkanDataName  = dialogInfo.options.detailCkanDataName
    // 実行モード情報を「横断・詳細カタログ作成」に更新
    setCatalogData(data, 'detail', 'both_duplicate')
    break;
  case 'edit-catalog-release' : //横断カタログ編集
    data.releaseId           = dialogInfo.options.releaseId
    data.releaseCkanDataName = dialogInfo.options.releaseCkanDataName
    data.detailId            = dialogInfo.options.detailId || ''
    data.detailCkanDataName  = dialogInfo.options.detailCkanDataName || ''
    setCatalogData(data, 'release', 'edit')
    break;
  case 'edit-catalog-detail' : //詳細カタログ編集
    data.releaseId           = dialogInfo.options.releaseId || ''
    data.releaseCkanDataName = dialogInfo.options.releaseCkanDataName || ''
    data.detailId            = dialogInfo.options.detailId
    data.detailCkanDataName  = dialogInfo.options.detailCkanDataName
    setCatalogData(data, 'detail', 'edit')
    break;
  }
}

function getExtraValue(data, key) {
  // extraデータ取得機能
  for (var i = 0; i < data.extras.length; i++) {
    if (data.extras[i].key === key) {
      return data.extras[i].value
    }
  }
  return ''
}

function getExtraArrayValue(data, key) {
  // extra配列データ取得機能
  var value = getExtraValue(data, key)
  if (value === '') {
    return []
  } else {
    return value.split(',')
  }
}

// オブジェクトフィールドをストア値用に整形
function formObjectField(ckanValue, itemListLabel) {
  if (!ckanValue) {
    return ''
  }
  for (var key of store.itemList[itemListLabel]) {
    switch (itemListLabel) {
      case 'accessRights':
        if (key.label === ckanValue) {
          return { label: key.label, value: key.value }
        }
        break
      default:
        if (key.value === ckanValue) {
          return { label: key.label, value: key.value }
        }
        break
    }
  }
  return ''
}

// Webサーバの自動設定値のコミット
function setServerData(catalogData, commitTitle) {
  var registedIssued = getExtraValue(catalogData, 'issued')
  var registedIdentifier = getExtraValue(catalogData, 'identifier')
  var registedDatasetUrl = getExtraValue(catalogData, 'dataset_url')
  const commitTitleToActionFunction = {
    'updateAutoSetValue' : store.updateAutoSetValue,
    'updateAutoSetValueAnother' : store.updateAutoSetValueAnother,
  }
  let actionFunction = commitTitleToActionFunction[commitTitle]
  if(actionFunction){
    actionFunction({
      issued: registedIssued,
      identifier: registedIdentifier,
      datasetUrl: registedDatasetUrl
    })
  }
}

// データセット情報の登録値コミット
function setDatasetinfoData(catalogData, storeType) {
  var registedDatasetIdForDetail = getExtraValue(catalogData, 'caddec_dataset_id_for_detail')
  var registedRegistOrg = { label: catalogData.organization.name, value: catalogData.organization.name }
  var tmpPublisherId = getExtraValue(catalogData, 'caddec_provider_id')
  if (!tmpPublisherId) {
    var registedPublisherId = { label: 'non_provider', value: '' }
  } else {
    registedPublisherId = { label: tmpPublisherId, value: tmpPublisherId }
  }
  var registedPublisher = getExtraValue(catalogData, 'publisher_name')
  var registedPublisherUrl = getExtraValue(catalogData, 'publisher_uri')
  var registedCreator = getExtraValue(catalogData, 'creator_name')
  var registedCreatorUrl = getExtraValue(catalogData, 'creator_url')
  var registedContactPoint = getExtraValue(catalogData, 'contact_name')
  var registedContactPointUrl = getExtraValue(catalogData, 'contact_url')
  store.updateDatasetinfo({
      catalogTitle: catalogData.title,
      registOrg: registedRegistOrg,
      catalogDescription: catalogData.notes,
      datasetDescriptionUrl: catalogData.url,
      datasetIdForDetail: registedDatasetIdForDetail,
      publisherId: registedPublisherId,
      publisher: registedPublisher,
      publisherUri: registedPublisherUrl,
      creator: registedCreator,
      creatorUrl: registedCreatorUrl,
      contactPoint: registedContactPoint,
      contactPointUrl: registedContactPointUrl,
      storeType: storeType
    })
}

// NGSIデータモデル整形
function formatNgsiDataModel(dataModel) {
  var tmpDataModel = JSON.parse(dataModel)
  var dataModelList = []
  for (var attribute in tmpDataModel.attrs) {
    var ret = {}
    ret = {
      attribute: attribute,
      description: tmpDataModel.attrs[attribute].description,
      dataType: tmpDataModel.attrs[attribute].type,
      example: tmpDataModel.attrs[attribute].value,
      metadata: []
    }
    for (var name in tmpDataModel.attrs[attribute].metadata) {
      ret.metadata.push({
        metadataName: name,
        dataType: tmpDataModel.attrs[attribute].metadata[name].type,
        example: tmpDataModel.attrs[attribute].metadata[name].value,
        description: tmpDataModel.attrs[attribute].metadata[name].description
      })
    }
    dataModelList.push(ret)
  }
  return dataModelList
}

// データ概要情報の登録値コミット
function setDatajacketData(catalogData, storeType, selectedMode) {
  var i = 0
  var j = 0
  var key = ''
  var registedFiledataDetails = []
  for (i = 0; i < catalogData.resources.length; i++) {
    var tmpFiledataDetails = {}
    // 契約確認の要否
    var contractRequired = {
      label: catalogData.resources[i].caddec_contract_required,
      value: catalogData.resources[i].caddec_contract_required
    }
    // コネクタ利用の要否
    var connectRequired = {
      label: catalogData.resources[i].caddec_required,
      value: catalogData.resources[i].caddec_required
    }
    // 配信の名称
    var registedName = catalogData.resources[i].name || ''
    // 配信の説明
    var registedDescription = catalogData.resources[i].description || ''
    // 配信の情報提供ページURL
    var registedExplainUrl = catalogData.resources[i].explain_url || ''
    // 配信のダウンロードURL
    var registedDownloadUrl = catalogData.resources[i].url || ''
    // 配信のバイトサイズ
    var registedSize = catalogData.resources[i].size || ''
    // 配信のメディアタイプ
    var registedMimetype = ''
    for (key of store.itemList.mimetype) {
      if (catalogData.resources[i].mime_type === key.value) {
        registedMimetype = { label: key.label, value: key.value }
      }
    }
    // 配信のファイル形式
    var registedFormat = catalogData.resources[i].format || ''
    // 配信の圧縮形式
    var registedCompressFormat = ''
    var registedCompressFormatOther = ''
    if (catalogData.resources[i].compress_format) {
      if (catalogData.resources[i].compress_format.startsWith('その他')) {
        registedCompressFormat = { label: 'その他（自由記述）', value: 'その他' }
        registedCompressFormatOther = catalogData.resources[i].compress_format.slice(FIRST_OTHER, LAST_OTHER)
      } else {
        for (key of store.itemList.compressFormat) {
          if (catalogData.resources[i].compress_format === key.value) {
            registedCompressFormat = { label: key.label, value: key.value }
          }
        }
      }
    }
    // 配信のパッケージ形式
    var registedPackageFormat = ''
    var registedPackageFormatOther = ''
    if (catalogData.resources[i].package_format) {
      if (catalogData.resources[i].package_format.startsWith('その他')) {
        registedPackageFormat = { label: 'その他（自由記述）', value: 'その他' }
        registedPackageFormatOther = catalogData.resources[i].package_format.slice(FIRST_OTHER, LAST_OTHER)
      } else {
        for (key of store.itemList.packageFormat) {
          if (catalogData.resources[i].package_format === key.value) {
            registedPackageFormat = { label: key.label, value: key.value }
          }
        }
      }
    }
    // スキーマ
    var registedSchema = catalogData.resources[i].schema || ''
    // スキーマタイプ
    var registedSchemaType = ''
    for (key of store.itemList.schemaType) {
      if (catalogData.resources[i].schema_type === key.value) {
        registedSchemaType = { label: key.label, value: key.value }
      }
    }
    // NGSIデータ種別
    var registedNgsiEntityType = catalogData.resources[i].ngsi_entity_type || ''
    // NGSIテナント
    var registedNgsiTenant = catalogData.resources[i].ngsi_tenant || ''
    // NGSIサービスパス
    var registedNgsiServicePath = catalogData.resources[i].ngsi_service_path || ''
    // NGSIデータモデル
    if (catalogData.resources[i].ngsi_data_model && catalogData.resources[i].ngsi_data_model.length) {
      var registedNgsiDataModel = formatNgsiDataModel(catalogData.resources[i].ngsi_data_model)
    } else {
      registedNgsiDataModel = []
    }
    // 来歴登録の有無
    if (catalogData.resources[i].caddec_resource_id_for_provenance && selectedMode === 'edit') {
      var registedResourceIdForProvenance = catalogData.resources[i].caddec_resource_id_for_provenance
      var registedGetResourceIdForProvenanceLabel = '来歴登録を行わない'
      var registedGetResourceIdForProvenanceValue = 'no'
    } else {
      registedResourceIdForProvenance = ''
      registedGetResourceIdForProvenanceLabel = '来歴登録を行わない'
      registedGetResourceIdForProvenanceValue = 'no'
    }
    // 前段イベント識別子
    var registedPreviousEventId = catalogData.resources[i].previousEventId || ''
    // データサービスのタイトル
    var registedDataServiceTitle = catalogData.resources[i].data_service_title || ''
    // データサービスのエンドポイント
    var registedDataServiceEndpointUrl = catalogData.resources[i].data_service_endpoint_url || ''
    // データサービスのエンドポイントの定義
    var registedDataServiceEndpointDescription = catalogData.resources[i].data_service_endpoint_description || ''
    // リソース提供手段の識別子
    tmpFiledataDetails.resourceType = catalogData.resources[i].caddec_resource_type
    if (catalogData.resources[i].caddec_resource_type) {
      for (j = 0; j < store.itemList.caddecResourceType.length; j++) {
        if (tmpFiledataDetails.resourceType === store.itemList.caddecResourceType[j].value) {
          var resourceTypeLabel = store.itemList.caddecResourceType[j].label
          var resourceTypeValue = store.itemList.caddecResourceType[j].value
        }
      }
    }
    // 配信のライセンス
    var registedResourceLicenseTitle = catalogData.resources[i].license_title || ''
    // 配信のライセンス(URL)
    var registedResourceLicenseUrl = catalogData.resources[i].license_url || ''
    // 配信の発行日
    var registedResourceIssued = ''
    if (store.selectedMode.mode === 'edit' && catalogData.resources[i].issued) {
      registedResourceIssued = catalogData.resources[i].issued
    }
    // 配信のID
    var registedId = ''
    if (selectedMode == 'edit' && catalogData.resources[i].id) {
      registedId = catalogData.resources[i].id
    }
    registedFiledataDetails.push({
      filename: registedName,
      description: registedDescription,
      downloadUrl: registedDownloadUrl,
      explainurl: registedExplainUrl,
      size: registedSize,
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
      resourceType: {
        label: resourceTypeLabel,
        value: resourceTypeValue
      },
      licensetitle: registedResourceLicenseTitle,
      licenseurl: registedResourceLicenseUrl,
      issued: registedResourceIssued,
      id: registedId
    })
  }
  store.updateFiledataDetails({
      filedataDetails: registedFiledataDetails,
      storeType: storeType
    })
}

// データセット情報（任意）登録値コミット
function setDatasetoptionalinfoData(catalogData, storeType) {
  var i = 0
  var j = 0
  var val = ''
  // データセットの主分類
  var themes = getExtraArrayValue(catalogData, 'theme')
  var registedSelectThemes = []
  for (val of themes) {
    registedSelectThemes.push(val)
  }
  // データセットのキーワード
  var registedSelectTags = []
  if (catalogData.tags) {
    for (i = 0; i < catalogData.tags.length; i++) {
      registedSelectTags.push(catalogData.tags[i].display_name)
    }
  }
  // データセットの情報を記述する言語
  var tmpSelectLanguage = []
  tmpSelectLanguage = getExtraArrayValue(catalogData, 'language')
  var registedSelectLanguage = []
  var optLanguages = store.itemList.language
  if (tmpSelectLanguage && tmpSelectLanguage !== []) {
    for (i = 0; i < tmpSelectLanguage.length; i++) {
      for (j = 0; j < optLanguages.length; j++) {
        if (optLanguages[j].value === tmpSelectLanguage[i]) {
          registedSelectLanguage.push({ label: optLanguages[j].label, value: optLanguages[j].value })
        }
      }
    }
  }
  // データセットの提供頻度
  var tmpFrequency = getExtraValue(catalogData, 'frequency')
  var registedFrequency = ''
  if (tmpFrequency) {
    for (i = 0; i < store.itemList.frequency.length; i++) {
      if (store.itemList.frequency[i].value === tmpFrequency) {
        registedFrequency = { label: store.itemList.frequency[i].label, value: store.itemList.frequency[i].value }
        break
      }
    }
  }
  // データセットの対象地域
  var registedSpatialUrl = getExtraValue(catalogData, 'spatial_url')
  var registedSpatialName = getExtraValue(catalogData, 'spatial_text')
  var registedSpatial = getExtraValue(catalogData, 'spatial')
  // データセットの対象期間
  var registedStart = getExtraValue(catalogData, 'temporal_start')
  var registedEnd = getExtraValue(catalogData, 'temporal_end')
  // 語彙
  var registedVocabulary = getExtraValue(catalogData, 'vocabulary')
  // 用語
  var registedTerm = getExtraValue(catalogData, 'term')
  store.updateDatasetOptionalInfoParameters({
      selectThemes: registedSelectThemes,
      selectTags: registedSelectTags,
      vocabulary: registedVocabulary,
      term: registedTerm,
      selectLanguage: registedSelectLanguage,
      frequency: registedFrequency,
      spatialUrl: registedSpatialUrl,
      spatialName: registedSpatialName,
      spatial: registedSpatial,
      start: registedStart,
      end: registedEnd,
      storeType: storeType
    })
}

// 利用条件の登録値コミット
function setUsertermsData(catalogData, storeType) {
  var i = 0
  var j = 0
  // データセット・配信のライセンス（説明）
  var registedLicenseId = ''
  if (catalogData.license_id) {
    for (i = 0; i < store.ckanItemList.licenseId.length; i++) {
      if (store.ckanItemList.licenseId[i].value === catalogData.license_id) {
        registedLicenseId = { label: store.ckanItemList.licenseId[i].label, value: store.ckanItemList.licenseId[i].value }
      }
    }
  }
  // データセット・配信のライセンス
  var registedLicenseUrl = catalogData.license_url || ''
  // データセット・配信の権利表明
  var registedUsrRight = getExtraValue(catalogData, 'rights')
  // データセット・配信のアクセス権（説明）
  var tmpAccessRights = getExtraValue(catalogData, 'access_rights')
  var registedAccessRights = formObjectField(tmpAccessRights, 'accessRights')
  // データセット・配信のアクセス権
  var registedAccessRightsUrl = getExtraValue(catalogData, 'access_rights_url')
  // データセット・配信に関する権利情報URL
  var registedHaspolicyUrl = getExtraValue(catalogData, 'haspolicy_url')
  // データセットを生成した活動
  var registedProvWasGeneratedByUrl = getExtraValue(catalogData, 'prov_was_generated_by_url')
  // データセット・配信が準拠する標準URL
  var registedConformsTo = getExtraValue(catalogData, 'conforms_to')
  // 契約形態
  var tmpContractType = getExtraValue(catalogData, 'trading_policy_contract_type')
  var registedContractType = formObjectField(tmpContractType, 'tradingPolicyContractType')
  // 秘密保持義務
  var tmpSecrecy = getExtraValue(catalogData, 'trading_policy_nda')
  var registedSecrecy = formObjectField(tmpSecrecy, 'tradingPolicyNda')
  // 利用用途
  var tmpUseApplication = getExtraArrayValue(catalogData, 'trading_policy_use_application')
  var registedUseApplication = []
  var registedUseApplicationOther = ''
  if (tmpUseApplication && tmpUseApplication !== []) {
    for (i = 0; i < tmpUseApplication.length; i++) {
      if (tmpUseApplication[i].startsWith('その他')) {
        registedUseApplication.push({ label: 'その他', value: tmpUseApplication[i] })
        registedUseApplicationOther = tmpUseApplication[i].slice(FIRST_OTHER, LAST_OTHER)
        continue
      }
      for (j = 0; j < store.itemList.tradingPolicyUseApplication.length; j++) {
        if (store.itemList.tradingPolicyUseApplication[j].value === tmpUseApplication[i]) {
          registedUseApplication.push({ label: store.itemList.tradingPolicyUseApplication[j].label, value: store.itemList.tradingPolicyUseApplication[j].value })
        }
      }
    }
  }
  // 開示範囲
  var tmpScopeOfDisclosure = getExtraValue(catalogData, 'scope_of_disclosure')
  var registedScopeOfDisclosureOther = ''
  var registedScopeOfDisclosure = ''
  if (tmpScopeOfDisclosure) {
    if (tmpScopeOfDisclosure.startsWith('その他')) {
      registedScopeOfDisclosure = { label: 'その他', value: tmpScopeOfDisclosure }
      registedScopeOfDisclosureOther = tmpScopeOfDisclosure.slice(FIRST_OTHER, LAST_OTHER)
    } else {
      registedScopeOfDisclosure = { label: tmpScopeOfDisclosure, value: tmpScopeOfDisclosure }
    }
  }
  // データ活用地域
  var tmpPermissionResion = getExtraArrayValue(catalogData, 'terms_of_use_permissible_region')
  var registedPermissionResion = []
  var registedPermissionResionOther = ''
  if (tmpPermissionResion && tmpPermissionResion !== []) {
    for (i = 0; i < tmpPermissionResion.length; i++) {
      if (tmpPermissionResion[i].startsWith('その他')) {
        registedPermissionResion.push({ label: 'その他', value: 'その他' })
        registedPermissionResionOther = tmpPermissionResion[i].slice(FIRST_OTHER, LAST_OTHER)
        continue
      }
      for (j = 0; j < store.itemList.termsOfUsePermissibleRegion.length; j++) {
        if (store.itemList.termsOfUsePermissibleRegion[j].value === tmpPermissionResion[i]) {
          registedPermissionResion.push({ label: store.itemList.termsOfUsePermissibleRegion[j].label, value: store.itemList.termsOfUsePermissibleRegion[j].value })
        }
      }
    }
  }
  // 利用に関する注意事項
  var registedNotices = getExtraValue(catalogData, 'terms_of_use_notices')
  // パーソナルデータの類別
  var tmpPersonalData = getExtraValue(catalogData, 'privacy_policy_contains_personal_data')
  var registedPersonalData = ''
  var registedPersonalDataOther = ''
  if (tmpPersonalData) {
    if (tmpPersonalData.startsWith('その他')) {
      registedPersonalData = { label: 'その他', value: tmpPersonalData }
      registedPersonalDataOther = tmpPersonalData.slice(FIRST_OTHER, LAST_OTHER)
    } else {
      registedPersonalData = { label: tmpPersonalData, value: tmpPersonalData }
    }
  }
  // データの有効期間
  var tmpDataEffectivePeriod = getExtraValue(catalogData, 'data_effective_period')
  var registedDataEffectivePeriodSelectTerms = ''
  var registedStartDate = ''
  var registedEndDate = ''
  var registedDataEffectivePeriodFreeField = ''
  if (tmpDataEffectivePeriod) {
    tmpDataEffectivePeriod = JSON.parse(tmpDataEffectivePeriod)
    if (tmpDataEffectivePeriod[0].dataEffectivePeriodType && tmpDataEffectivePeriod[0].dataEffectivePeriodType === 'startEndDate') {
      registedDataEffectivePeriodSelectTerms = { label: '開始日・終了日', value: 'date' }
      registedStartDate = tmpDataEffectivePeriod[0].date.startDate
      registedEndDate = tmpDataEffectivePeriod[0].date.endDate
      registedDataEffectivePeriodFreeField = ''
    } else if (tmpDataEffectivePeriod[0].dataEffectivePeriodType && tmpDataEffectivePeriod[0].dataEffectivePeriodType === 'note') {
      registedDataEffectivePeriodSelectTerms = { label: '自由記述', value: 'note' }
      registedDataEffectivePeriodFreeField = tmpDataEffectivePeriod[0].note
      registedStartDate = ''
      registedEndDate = ''
    }
  }
  // 利用ライセンスの期限
  var tmpUsageLicensePeriod = getExtraValue(catalogData, 'usage_license_period')
  var registedUsageLicensePeriodSelectTerms = ''
  var registedDeadline = ''
  var registedPeriod = ''
  var registedUnit = ''
  var registedUsageLicensePeriodFreeField = ''
  if (tmpUsageLicensePeriod) {
    tmpUsageLicensePeriod = JSON.parse(tmpUsageLicensePeriod)
    if (tmpUsageLicensePeriod[0].usageLicensePeriodType === 'endDate') {
      registedUsageLicensePeriodSelectTerms = { label: '期限', value: 'endDate' }
      registedDeadline = tmpUsageLicensePeriod[0].endDate
      registedPeriod = ''
      registedUnit = ''
      registedUsageLicensePeriodFreeField = ''
    } else if (tmpUsageLicensePeriod[0].usageLicensePeriodType === 'period') {
      registedUsageLicensePeriodSelectTerms = { label: '期間', value: 'value' }
      registedDeadline = ''
      registedUsageLicensePeriodFreeField = ''
      registedPeriod = tmpUsageLicensePeriod[0].period.value
      var tmpUnit = tmpUsageLicensePeriod[0].period.unit
      for (i = 0; i < periodUnit.length; i++) {
        if (tmpUnit === periodUnit[i].value) {
          registedUnit = { label: periodUnit[i].label, value: periodUnit[i].value }
          break
        }
      }
    } else if (tmpUsageLicensePeriod[0].usageLicensePeriodType === 'note') {
      registedUsageLicensePeriodSelectTerms = { label: '自由記述', value: 'note' }
      registedUsageLicensePeriodFreeField = tmpUsageLicensePeriod[0].note
      registedDeadline = ''
      registedPeriod = ''
      registedUnit = ''
    }
  }
  // 有償無償
  var tmpFee = getExtraValue(catalogData, 'fee')
  var registedFee = formObjectField(tmpFee, 'fee')
  // 販売情報
  var registedSalesInfoUrl = getExtraValue(catalogData, 'sales_info_url')
  // 価格帯
  var registedPriceRange = getExtraValue(catalogData, 'pricing_price_range')
  // データ販売に関わる特記事項
  var registedNoticesOfPrice = getExtraValue(catalogData, 'pricing_notices_of_price')
  // 明示された保証
  var tmpExpressWarranty = getExtraValue(catalogData, 'warranty_express_warranty')
  var registedExpressWarranty = ''
  var registedexpressWarrantyOther = ''
  if (tmpExpressWarranty) {
    if (tmpExpressWarranty.startsWith('その他')) {
      registedExpressWarranty = { label: 'その他', value: tmpExpressWarranty }
      registedexpressWarrantyOther = tmpExpressWarranty.slice(FIRST_OTHER, LAST_OTHER)
    } else {
      registedExpressWarranty = { label: tmpExpressWarranty, value: tmpExpressWarranty }
    }
  }
  // 準拠法の対象国
  var tmpLeagalCompliance = getExtraArrayValue(catalogData, 'warranty_leagal_compliance')
  var registedLeagalCompliance = []
  var registedLeagalComplianceOther = ''
  if (tmpLeagalCompliance && tmpLeagalCompliance !== []) {
    for (i = 0; i < tmpLeagalCompliance.length; i++) {
      if (tmpLeagalCompliance[i].startsWith('その他')) {
        registedLeagalCompliance.push({ label: 'その他', value: tmpLeagalCompliance[i] })
        registedLeagalComplianceOther = tmpLeagalCompliance[i].slice(FIRST_OTHER, LAST_OTHER)
        continue
      }
      for (j = 0; j < store.itemList.warrantyLegalCompliance.length; j++) {
        if (store.itemList.warrantyLegalCompliance[j].value === tmpLeagalCompliance[i]) {
          registedLeagalCompliance.push({ label: store.itemList.warrantyLegalCompliance[j].label, value: store.itemList.warrantyLegalCompliance[j].value })
        }
      }
    }
  }
  store.updateUserTerms({
      termName: registedLicenseId,
      termNameUrl: registedLicenseUrl,
      usrRight: registedUsrRight,
      accessRights: registedAccessRights,
      accessRightsUrl: registedAccessRightsUrl,
      haspolicyUrl: registedHaspolicyUrl,
      provWasGeneratedByUrl: registedProvWasGeneratedByUrl,
      conformsTo: registedConformsTo,
      contractType: registedContractType,
      secrecy: registedSecrecy,
      useApplication: registedUseApplication,
      useApplicationOther: registedUseApplicationOther,
      scopeOfDisclosure: registedScopeOfDisclosure,
      scopeOfDisclosureOther: registedScopeOfDisclosureOther,
      permissionResion: registedPermissionResion,
      permissionResionOther: registedPermissionResionOther,
      notices: registedNotices,
      personalData: registedPersonalData,
      personalDataOther: registedPersonalDataOther,
      dataEffectivePeriodSelectTerms: registedDataEffectivePeriodSelectTerms,
      startDate: registedStartDate,
      endDate: registedEndDate,
      dataEffectivePeriodFreefield: registedDataEffectivePeriodFreeField,
      usageLicensePeriodSelectTerms: registedUsageLicensePeriodSelectTerms,
      deadline: registedDeadline,
      period: registedPeriod,
      unit: registedUnit,
      usageLicensePeriodFreefield: registedUsageLicensePeriodFreeField,
      fee: registedFee,
      salesInfoUrl: registedSalesInfoUrl,
      priceRange: registedPriceRange,
      noticesOfPrice: registedNoticesOfPrice,
      expressWarranty: registedExpressWarranty,
      expressWarrantyOther: registedexpressWarrantyOther,
      leagalCompliance: registedLeagalCompliance,
      leagalComplianceOther: registedLeagalComplianceOther,
      storeType: storeType
    })
}

function deleteSelectedRows() {
  var i = 0
  var deleteCatalogList = {
    release: [],
    detail: []
  }
  for (i = 0; i < selected.value.length; i++) {
    if (selected.value[i].releaseId && attr.serchCkanType !== 'detailCkan') {
      // 検索先CKANに横断検索用CKANを指定した場合は、横断検索カタログは削除しない
      deleteCatalogList.release.push(selected.value[i].releaseId)
    }
    if (selected.value[i].detailId && attr.serchCkanType !== 'releaseCkan') {
      // 検索先CKANに横断検索用CKANを指定した場合は、詳細検索カタログは削除しない
      deleteCatalogList.detail.push(selected.value[i].detailId)
    }
  }
  axios.request({ method: 'delete', url: config.apiPrefix + '/datacatalog', data: deleteCatalogList })
    .then(async res => {
      // 検索結果の再表示
      btnActionSearch()
      selected.value = []
      attr.deleteDialog.isDisplay = false
    })
    .catch(err => {
      console.log('error message:', err.response.data.message)
      attr.completeDialog.isDisplay = true
      attr.completeDialog.message = err.response.data.message || 'カタログ削除に失敗しました。\n管理者に問い合わせてください。'
      attr.completeDialog.errorFlg = true
    })
}

// データ一括削除確認ダイアログ表示
function btnConfirmSelectedDelete() {
  let options = {}
  if (store.loginInfo.releaseCkanAddr && store.loginInfo.detailCkanAddr && attr.serchCkanType==='releaseCkan') {
    attr.deleteDialog.options = 'deleteWarningRelease'
  } else if (store.loginInfo.releaseCkanAddr && store.loginInfo.detailCkanAddr && attr.serchCkanType==='detailCkan') {
    attr.deleteDialog.options = 'deleteWarningDetail'
  } else {
    attr.deleteDialog.options = 'noDeleteWarning'
  }
  attr.deleteDialog.isDisplay = true
  attr.deleteDialog.pageName = 'searchSelectedDelete'
}

// データ削除確認用ダイアログ表示
function btnConfirmOneDelete(data, catalogType) {
  let options = {}
  switch(catalogType){
  case 'release'://横断
  case 'release_both'://横断に紐づく詳細
    options.catalogName = data.row.releaseTitle
    break
  case 'detail'://詳細
  case 'detail_both'://詳細に紐づく横断
    options.catalogName = data.row.detailTitle
    break
  default:
    console.log('catalogTypeが不正でした:' + catalogType)
    return;
  }
  options.releaseId = data.row.releaseId
  options.detailId  = data.row.detailId

  attr.deleteDialog.options = options
  attr.deleteDialog.pageName = 'searchOneDelete'  
  attr.deleteDialog.type = catalogType
  attr.deleteDialog.isDisplay = true
}

function deleteRow(data) {
  console.log('- deleteRow:カタログ削除 -')
  console.log(data)

  var deleteCatalogList = {
    release: [],
    detail: []
  }
  switch(data.type){
  case 'release'://横断
    deleteCatalogList.release.push(data.options.releaseId)
    break
  case 'detail'://詳細
    deleteCatalogList.detail.push(data.options.detailId)
    break
  case 'release_both'://横断に紐づく詳細
  case 'detail_both'://詳細に紐づく横断
    deleteCatalogList.release.push(data.options.releaseId)
    deleteCatalogList.detail.push(data.options.detailId)
   break
  default:
    console.log('data.typeが不正でした:' + data.type)
    return;
  }

  axios.request({ method: 'delete', url: config.apiPrefix + '/datacatalog', data: deleteCatalogList })
    .then(async res => {
      // 検索結果の再表示
      btnActionSearch()
      attr.deleteDialog.isDisplay = false
    })
    .catch(err => {
      console.log('error message:', err.response.data.message)
      attr.completeDialog.isDisplay = true
      attr.completeDialog.message = err.response.data.message || 'カタログ削除に失敗しました。\n管理者に問い合わせてください。'
      attr.completeDialog.errorFlg = true
    })
}

function showCatalogInfo(data, ckanType){
  store.copyLicenseToFiledataDetails()
  isShowCatalogInfo.value = true

  var releaseData = ''
  var detailData = ''
  // 選択された行の横断カタログと詳細カタログを取得
  for (var i = 0; i < attr.getData.length; i++) {
    if (attr.getData[i].release.id === data.row.releaseId) {
      releaseData = attr.getData[i].release
    }
    if (data.row.detailId && attr.getData[i].detail.id === data.row.detailId) {
      detailData = attr.getData[i].detail
    }
  }
  // 複製・編集対象の横断または詳細カタログと、対になる詳細または横断カタログを取得
  var usedCatalogData = ''
  if(ckanType === 'release'){
    usedCatalogData = releaseData
  }else{
    usedCatalogData = detailData
  }
  setServerData(usedCatalogData, 'updateAutoSetValue')
  setDatasetinfoData(usedCatalogData, 'state')
  setDatajacketData(usedCatalogData, 'state')
  setDatasetoptionalinfoData(usedCatalogData, 'state')
  setUsertermsData(usedCatalogData, 'state')
}

//watch
watch(() => attr.inputCkanUrl,
  (newVal, oldVal) => {
  // 入力されたURLデータ監視機能
  // URLデータとキーワードデータが入力済みなら検索ボタン押下可能にする
  if (newVal !== '' && newVal !== null) {
    attr.inputKeywordDisable = true
    attr.btnDisable = false
  } else {
    attr.inputKeywordDisable = false
    attr.btnDisable = true
  }
})

watch(() => attr.inputKeyword,
  (newVal, oldVal) => {
  // 入力されたキーワードデータ監視機能
  // キーワードデータが入力済みなら検索ボタン押下可能にする
  if (newVal !== '' && newVal !== null) {
    attr.inputUrlDisable = true
    attr.btnDisable = false
  } else {
    attr.inputUrlDisable = false
    attr.btnDisable = true
  }
})

watch(() => selected.value,
  (newVal) => {
  if (newVal.length) {
    attr.noCatalogSelected = false
  } else {
    attr.noCatalogSelected = true
  }
})

</script>

<template>
  <div class="col-12 q-layout-padding flex justify-center content-center">
    <div v-if="isShowCatalogInfo" class="fit">
      <DatasetConfirm  />
      <q-footer elevated>
        <q-toolbar class="justify-start">
          <q-btn flat color="white" icon="reply_all" @click="isShowCatalogInfo = false" label="検索結果一覧に戻る" />
        </q-toolbar>
      </q-footer>
    </div>
    <q-card v-else class="q-card-background-white" style="width: 100%;">
      <q-card-section>
        <div class="q-pa-md column justify-center items-center" style="width: 100%;">
          <q-list no-border style="width: 95%;">
            <q-item v-if="store.loginInfo.releaseCkanAddr && store.loginInfo.detailCkanAddr">
              <q-item-section class="col-3 flex items-start justify-center">
                <q-item-label><label>検索先CKAN</label></q-item-label>
              </q-item-section>
              <q-item-section  class="col-9">
                <div class="row justify-between">
                  <q-radio
                    v-model="attr.serchCkanType"
                    val="releaseCkan"
                    label="横断検索用CKAN"
                    color="light-blue-10"
                  />
                  <q-radio
                    v-model="attr.serchCkanType"
                    val="detailCkan"
                    label="詳細検索用CKAN"
                    color="light-blue-10"
                  />
                  <q-radio
                    v-model="attr.serchCkanType"
                    val="bothCkan"
                    label="横断・詳細検索用CKAN"
                    color="light-blue-10"
                  />
                </div>
              </q-item-section>
            </q-item>
            <q-item>
              <q-item-section class="col-3 flex items-start justify-center">
                <q-item-label><label>CKANデータURL(id)検索</label></q-item-label>
              </q-item-section>
              <q-item-section  class="col-9">
                <q-input square outlined
                  v-model="attr.inputCkanUrl"
                  :disable="attr.inputUrlDisable"
                  placeholder ="idからデータを指定"
                  dense = true
                />
              </q-item-section>
            </q-item>
            <q-item>
              <q-item-section class="col-3 flex items-start justify-center">
                <q-item-label><label>キーワード検索</label></q-item-label>
              </q-item-section>
              <q-item-section class="col-7 clear-margin">
                <q-input square outlined
                  v-model="attr.inputKeyword"
                  :disable="attr.inputKeywordDisable"
                  placeholder ="キーワードからデータを検索して指定"
                  dense = true
                />
              </q-item-section>
              <q-item-section class="col-2 clear-margin">
                <q-btn
                  style="margin-left: 10px;"
                  color="light-blue-10"
                  label="検索"
                  :disable="attr.btnDisable"
                  @click = "btnActionSearch()"
                />
              </q-item-section>
            </q-item>
          </q-list>
          <br>
          <div v-if="attr.showResult===true" class="q-mt-lg clear-margin" style="width: 100%;">
            <q-table
              :rows="attr.displayData"
              :columns="attr.searchResultColumns"
              selection="multiple"
              row-key="uniqueId"
              v-model:selected="selected"
              separator="cell"
              class="searchTable"
            >
              <template v-slot:top>
                <div class="q-table__title text-weight-bolder full-width row justify-between">
                  <div class="row items-center">
                    <font size="5" color="#1d468f">{{attr.tableHeader}}</font>
                    <div class="note-msg" v-if="attr.displayReleaseNote">（紐づく詳細カタログを持つ横断カタログには星マークがついています。）</div>
                    <div class="note-msg" v-if="attr.displayDetailNote">（紐づく横断カタログを持つ詳細カタログには星マークがついています。）</div>
                  </div>
                  <q-btn
                  style="width: 12%;"
                  outline
                  color="red"
                  :disable="attr.noCatalogSelected"
                  icon="delete"
                  label="削除"
                  @click="btnConfirmSelectedDelete()"
                  />
                </div>
              </template>
              <template v-slot:body-cell-releaseTitle="props">
                <q-td :props="props">
                  <!-- 詳細カタログが紐づいている場合、★を付与する -->
                  <q-icon v-if="props.row.searchCkanType === 'releaseCkan' && typeof props.row.detailTitle !== 'undefined'" name="grade" color="red" style="font-size: 17px;" />                  
                  <span @click="showCatalogInfo(props,'release')">{{props.row.releaseTitle}}</span>
                </q-td>
              </template>
              <template v-slot:body-cell-detailTitle="props">
                <q-td :props="props">
                  <!-- 横断カタログが紐づいている場合、★を付与する -->
                  <q-icon v-if="props.row.searchCkanType === 'detailCkan' && typeof props.row.releaseTitle !== 'undefined'" name="grade" color="red" style="font-size: 17px;" />
                  <span @click="showCatalogInfo(props,'detail')">{{props.row.detailTitle}}</span>
                </q-td>
              </template>
              <!-- 横断検索用CKAN 複製ボタン -->
              <template v-slot:body-cell-releaseRegister="props">
                <q-td class="btn-cell">
                  <div v-if="props.row.releaseTitle">
                    <q-btn-dropdown outline color="primary" class="full-width" label="複製" field="releaseRegister">
                      <q-list>
                        <!-- １．横断カタログと紐づく詳細カタログ作成 -->
                        <!-- 紐づく詳細カタログが既に登録されている場合は非表示 -->
                        <!-- ログインしているCKANが横断検索用CKANのみの場合は非表示 -->
                        <q-item clickable v-close-popup v-if="!props.row.detailTitle && store.loginInfo.detailCkanAddr" @click="showConfirmDialog(props, 'create-catalog-detail-link-release')">
                          <q-item-section>
                            <q-item-label class="menu-item">横断カタログと紐づく詳細カタログ作成</q-item-label>
                          </q-item-section>
                        </q-item>
                        <!-- ２．横断カタログの情報を元に、新規で横断カタログ作成 -->
                        <q-item clickable v-close-popup @click="showConfirmDialog(props, 'create-catalog-release-from-release')" >
                          <q-item-section>
                            <q-item-label class="menu-item">新規で横断カタログ作成</q-item-label>
                          </q-item-section>
                        </q-item>
                        <!-- ３．横断カタログの情報を元に、新規で詳細カタログ作成 -->
                        <!-- ログインしているCKANが横断検索用CKANのみの場合は非表示 -->
                        <q-item clickable v-close-popup v-if="store.loginInfo.detailCkanAddr" @click="showConfirmDialog(props, 'create-catalog-detail-from-release')">
                          <q-item-section>
                            <q-item-label class="menu-item">新規で詳細カタログ作成</q-item-label>
                          </q-item-section>
                        </q-item>
                        <!-- ４．横断カタログの情報を元に、新規で横断カタログと詳細カタログを作成 -->
                        <!-- ログインしているCKANが横断検索用CKANのみの場合は非表示 -->
                        <q-item clickable v-close-popup v-if="store.loginInfo.detailCkanAddr" @click="showConfirmDialog(props, 'create-catalog-both-from-release')">
                          <q-item-section>
                            <q-item-label class="menu-item">新規で横断カタログと詳細カタログ作成</q-item-label>
                          </q-item-section>
                        </q-item>
                      </q-list>
                    </q-btn-dropdown>
                  </div>
                </q-td>
              </template>
              <template v-slot:body-cell-releaseEdit="props">
                <q-td class="btn-cell">
                  <div v-if="props.row.releaseTitle">
                    <q-btn-dropdown outline color="secondary" class="full-width" label="編集" field="releaseEdit">
                      <q-list>
                        <q-item clickable v-close-popup @click="showConfirmDialog(props, 'edit-catalog-release')">
                          <q-item-section>
                            <q-item-label class="menu-item">横断カタログ編集</q-item-label>
                          </q-item-section>
                        </q-item>
                      </q-list>
                    </q-btn-dropdown>
                  </div>
                </q-td>
              </template>
              <template v-slot:body-cell-releaseDelete="props">
                <q-td class="btn-cell">
                  <div v-if="props.row.releaseTitle">
                    <q-btn-dropdown outline color="red" class="full-width" label="削除" field="releaseDelete">
                      <q-list>
                        <q-item clickable v-close-popup>
                          <q-item-section>
                            <q-item-label class="menu-item" @click="btnConfirmOneDelete(props, 'release')">横断カタログ削除</q-item-label>
                          </q-item-section>
                        </q-item>
                        <!-- 紐づく詳細カタログが登録済みの場合に表示 -->
                        <q-item clickable v-close-popup v-if="props.row.detailTitle" @click="btnConfirmOneDelete(props, 'release_both')">
                          <q-item-section>
                            <q-item-label class="menu-item">横断カタログと横断カタログに紐づく詳細カタログ削除</q-item-label>
                          </q-item-section>
                        </q-item>
                      </q-list>
                    </q-btn-dropdown>
                  </div>
                </q-td>
              </template>
              <!-- 詳細検索用CKAN ボタン -->
              <template v-slot:body-cell-detailRegister="props">
                <q-td class="btn-cell">
                  <div v-if="props.row.detailTitle">
                    <q-btn-dropdown outline color="primary" class="full-width" label="複製" field="detailRegister">
                      <q-list>
                        <!-- ５．詳細カタログと紐づく横断カタログ作成 -->
                        <!-- 紐づく横断カタログが既に登録されている場合もしくは非表示 -->
                        <!-- ログインしているCKANが詳細検索用CKANのみの場合は非表示 -->
                        <q-item clickable v-close-popup v-if="!props.row.releaseTitle && store.loginInfo.releaseCkanAddr" @click="showConfirmDialog(props, 'create-catalog-release-link-detail')">
                          <q-item-section>
                            <q-item-label class="menu-item">詳細カタログと紐づく横断カタログ作成</q-item-label>
                          </q-item-section>
                        </q-item>
                        <!-- ６．詳細カタログの情報を元に、新規で横断カタログ作成 -->
                        <!-- ログインしているCKANが詳細検索用CKANのみの場合は非表示 -->
                        <q-item clickable v-close-popup v-if="store.loginInfo.releaseCkanAddr && store.loginInfo.releaseCkanAddr" @click="showConfirmDialog(props, 'create-catalog-release-from-detail')" >
                          <q-item-section>
                            <q-item-label class="menu-item">新規で横断カタログ作成</q-item-label>
                          </q-item-section>
                        </q-item>
                        <!-- ７．詳細カタログの情報を元に、新規で詳細カタログ作成 -->
                        <q-item clickable v-close-popup @click="showConfirmDialog(props, 'create-catalog-detail-from-detail')">
                          <q-item-section>
                            <q-item-label class="menu-item">新規で詳細カタログ作成</q-item-label>
                          </q-item-section>
                        </q-item>
                        <!-- ８．詳細カタログの情報を元に、新規で横断カタログと詳細カタログを作成 -->
                        <!-- ログインしているCKANが詳細検索用CKANのみの場合は非表示 -->
                        <q-item clickable v-close-popup v-if="store.loginInfo.releaseCkanAddr" @click="showConfirmDialog(props, 'create-catalog-both-from-detail')">
                          <q-item-section>
                            <q-item-label class="menu-item">新規で横断カタログと詳細カタログ作成</q-item-label>
                          </q-item-section>
                        </q-item>
                      </q-list>
                    </q-btn-dropdown>
                  </div>
                </q-td>
              </template>
              <template v-slot:body-cell-detailEdit="props">
                <q-td class="btn-cell">
                  <div v-if="props.row.detailTitle">
                    <q-btn-dropdown outline color="secondary" class="full-width" label="編集" field="detailEdit">
                      <q-list>
                        <q-item clickable v-close-popup @click="showConfirmDialog(props, 'edit-catalog-detail')">
                          <q-item-section>
                            <q-item-label class="menu-item">詳細カタログ編集</q-item-label>
                          </q-item-section>
                        </q-item>
                      </q-list>
                    </q-btn-dropdown>
                  </div>
                </q-td>
              </template>
              <template v-slot:body-cell-detailDelete="props">
                <q-td class="btn-cell">
                  <div v-if="props.row.detailTitle">
                    <q-btn-dropdown outline color="red" class="full-width" label="削除" field="detailDelete">
                      <q-list>
                        <q-item clickable v-close-popup>
                          <q-item-section>
                            <q-item-label class="menu-item" @click="btnConfirmOneDelete(props, 'detail')">詳細カタログ削除</q-item-label>
                          </q-item-section>
                        </q-item>
                        <!-- 紐づく詳細カタログが登録済みの場合に表示 -->
                        <q-item clickable v-close-popup v-if="props.row.releaseTitle" @click="btnConfirmOneDelete(props, 'detail_both')" >
                          <q-item-section>
                            <q-item-label class="menu-item">詳細カタログと詳細カタログに紐づく横断カタログ削除</q-item-label>
                          </q-item-section>
                        </q-item>
                      </q-list>
                    </q-btn-dropdown>
                  </div>
                </q-td>
              </template>
            </q-table>
          </div>
          <!-- 削除ダイアログ -->
          <DeleteDialog
            v-bind:dialogInfo="attr.deleteDialog"
            @delete-one-catalog-data="deleteRow"
            @delete-selected-catalog-data="deleteSelectedRows"
            @close-dialog="attr.deleteDialog.isDisplay = false"
          />

          <!-- アクション確認ダイアログ -->
          <OperationConfirmDialog
            v-bind:dialogInfo="attr.confirmDialog"
            @confirm="onOperationConfirm"
            @close-dialog="attr.confirmDialog.isDisplay = false"
          />

          <!-- 完了ダイアログ -->
          <CompleteDialog 
            v-bind:dialogInfo="attr.completeDialog"
            @close-dialog="attr.completeDialog.isDisplay = false, attr.deleteDialog.isDisplay = false"
          />

        </div>
      </q-card-section>
    </q-card>
  </div>
</template>

<style lang="scss">
.btn-cell{
  width: 5%;
}

.clear-margin{
  margin: 0;
}

.add-star:before{
  content: "★";
  color:#f00000;
}

.menu-item{
  font-size: 13px;
  padding: 0px 5px;
}

.note-msg{
  font-size: 12px;
  color: #1976d2;
}

.searchTable .q-table__top, .searchTable .q-table__bottom, .searchTable thead tr:first-child th{
  background-color: rgba(25, 118, 210, 0.1)
}

.underline{
  cursor: pointer;
}

.underline :not(i){
  color: #1976d2;
  text-decoration: underline #1976d2;
}
</style>
