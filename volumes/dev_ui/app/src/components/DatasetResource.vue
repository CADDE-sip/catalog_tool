<script setup>
import { reactive , ref, watch, onMounted, defineExpose } from 'vue'
import { config } from'boot/config'
import axios from 'axios'
import { useStore } from '../stores/store'
import CompleteDialog from './dialog/CompleteDialog.vue'

const store = useStore();

// 配信のダウンロードURLの最大文字数
const DOWNLOAD_URL_MAX_VALUE = 255
// 配信のバイトサイズの最大桁数
const SIZE_MAX_VALUE = 9223372036854775807
// 入力項目エラー文言（無効値）
const ERROR_MESSAGE_INVALID = {
  downloadUrl: '配信のダウンロードURLは255文字以内で入力してください。',
  size: '配信のバイトサイズは"9223372036854775807"以下の数字で入力してください。'
}
// データモデルエラー文言
const ERROR_MESSAGE_DATAMODEL = {
  empty: '属性名は入力必須項目です。入力をお願いします。',
  duplicate: '属性名が重複しています。同じ属性名は登録できません。'
}
// メタデータエラー文言
const ERROR_MESSAGE_METADATA = {
  empty: 'メタデータ名は入力必須項目です。入力をお願いします。',
  duplicate: 'メタデータ名が重複しています。同じメタデータ名は登録できません。'
}

const TEMPLATE_KEYMAP = {
  caddecResourceType: 'resourceType',
  explainUrl: 'explainurl',
  filename: 'filename',
  description: 'description',
  size: 'size',
  mimeType: 'mimetype',
  format: 'format',
  compressFormat: 'compressFormat',
  packageFormat: 'packageFormat',
  schema: 'schema',
  schemaType: 'schemaType',
  dataServiceTitle: 'dataServiceTitle',
  dataServiceEndpointUrl: 'dataServiceEndpointUrl',
  dataServiceEndpointDescription: 'dataServiceEndpointDescription'
}

const TEMPLATE_TYPE_KEYMAP = {
  resourceType: 'object',
  filename: 'string',
  description: 'string',
  explainUrl: 'string',
  size: 'string',
  mimetype: 'object',
  format: 'string',
  compressFormat: 'object',
  packageFormat: 'object',
  schema: 'string',
  schemaType: 'object',
  dataServiceTitle: 'string',
  dataServiceEndpointUrl: 'string',
  dataServiceEndpointDescription: 'string'
}

const AUTOCORRECT_KEYMAP = {
  inputSupportUrl: 'url',
  filename: 'name',
  downloadUrl: 'url'
}

const localFileUrl = ref('api/v1/catalog/tool/localuploads')
const filedataDetails = reactive(store.filedataDetails)
const detail = ref(0)
const errorMessageInputRequired = ref('【入力必須項目】')
const errorFlagList = reactive({
  state: false,
  flagList: {
    contract: true,
    connect: true,
    resourceType: true,
    downloadUrl: true,
  }
})

// 完了ダイアログ
const completeDialog = reactive({
  isDisplay: false,
  message: '',
  errorFlg: false
})

const errorCheckMessage = reactive([])
const urlResponse = ref('')
const showUploader = ref(false)
const localFileData = ref([])
const fieldMessage = reactive({
  updateData: '',
  previousEventIdError: ''
})
const updateDataMessage = ref('')
const previousEventIdErrorMessage = ref('')
const expanded = reactive({
  inputSupportType: '',
  caddecResourceType: '',
  filename: '',
  description: '',
  downloadUrl: '',
  explainUrl: '',
  size: '',
  mimeType: '',
  format: '',
  compressFormat: '',
  packageFormat: '',
  schema: '',
  schemaType: '',
  ngsiEntityType: '',
  ngsiTenant: '',
  ngsiServicePath: '',
  ngsiDataModel: '',
  getResourceIDForProvenance: '',
  caddecResourceIdForProvenance: '',
  previousEventId: '',
  dataServiceTitle: '',
  dataServiceEndpointUrl: '',
  dataServiceEndpointDescription: ''
})

// 非表示設定
const hideFlgs = reactive({
  caddecResourceIdForProvenance: '',
  compressFormat: '',
  dataServiceEndpointDescription: '',
  dataServiceEndpointUrl: '',
  dataServiceTitle: '',
  description: '',
  explainUrl: '',
  filename: '',
  format: '',
  getResourceIDForProvenance: '',
  mimeType: '',
  ngsiDataModel: '',
  ngsiEntityType: '',
  ngsiServicePath: '',
  ngsiTenant: '',
  packageFormat: '',
  previousEventId: '',
  schema: '',
  schemaType: '',
  size: ''
})

const templateFlg = reactive(store.itemDisplayFlg)
const autoCorrect = reactive({
  inputSupportUrl: [],
  filename: [],
  downloadUrl: []
})
// データモデルテーブルカラム
const dataModelColumns = reactive([
  { name: 'attribute', label: '属性名', field: 'attribute', align: 'left', style: 'max-width: 60px' },
  { name: 'dataType', label: 'データ型', field: 'dataType', align: 'left', style: 'max-width: 60px' },
  { name: 'example', label: '参考値', field: 'example', align: 'left', style: 'max-width: 120px' },
  { name: 'description', label: '説明', field: 'description', align: 'left', style: 'max-width: 200px' },
  { name: 'metadata', label: '', field: 'metadata', align: 'left' },
  { name: 'deleteRow', label: '', field: 'deleteRow', align: 'left' }
])
// データモデル取得ボタン活性非活性フラグ
const inActiveGetDataModelBtn = ref(true)
// データモデルエラーメッセージ
const dataModelErrorMessage = ref('')
// メタデータテーブルカラム
const metadataColumns = reactive([
  { name: 'metadataName', label: 'メタデータ名', field: 'metadataName', align: 'left', style: 'max-width: 60px' },
  { name: 'dataType', label: 'データ型', field: 'dataType', align: 'left', style: 'max-width: 60px' },
  { name: 'example', label: '参考値', field: 'example', align: 'left', style: 'max-width: 120px' },
  { name: 'description', label: '説明', field: 'description', align: 'left', style: 'max-width: 200px' },
  { name: 'deleteRow', label: '', field: 'deleteRow', align: 'left' }
])
// メタデータ入力ダイアログ表示フラグ
const showMetadataDialog = ref(false)
// メタデータ入力ダイアログでの表示情報
const metaAttribute = ref('')
const metaDescription = ref('')
const metadataList = ref([])
// データモデルエラー情報
const errorDataModel = reactive({
  message: []
})
// メタデータエラー情報
const errorMetadata = reactive({
  status: false,
  message: []
})
// 前段イベント識別子検索ダイアログ表示フラグ
const showPreviousEventIdList = ref(false)
// 前段イベント識別子検索結果テーブルローディングフラグ
const tableLoading = ref(false)
// 前段イベント識別子検索結果テーブルカラム
const columns = reactive([
  { name: 'providerId', label: 'データ提供者ID', field: 'providerId', align: 'left' },
  { name: 'userId', label: 'CADDEユーザID', field: 'userId', align: 'left' },
  { name: 'timestamp', label: 'タイムスタンプ', field: 'timestamp', align: 'left' },
  { name: 'eventId', label: 'イベント識別子', field: 'eventId', align: 'left' }
])
// 前段イベント識別子検索結果格納配列
const resultData = ref([])
// 入力支援機能使用フラグ
const useInputSupport = ref(false)
const showUseInputSupportButton = ref(true)

// *****************
// onMounted
// *****************
onMounted(function(){
  console.log('-- DatasetResource.vue onMounted --')
  topScroll()
  if (store.selectedMode.mode === 'template' && !filedataDetails.length) {
    var templateFiledataDetails = store.template.filedataDetails[0] ? JSON.parse(JSON.stringify(store.template.filedataDetails[0])) : {}
    var isTemplate = false
    if (Object.keys(templateFiledataDetails).length) {
      isTemplate = true
    }
    filedataDetails.push({
      filename: templateFiledataDetails.filename || '',
      resourceType: {
        label: isTemplate ? templateFiledataDetails.resourceType.label : '',
        value: isTemplate ? templateFiledataDetails.resourceType.value : ''
      },
      dataname: templateFiledataDetails.dataname || '',
      description: templateFiledataDetails.description || '',
      downloadUrl: templateFiledataDetails.downloadUrl || '',
      explainurl: templateFiledataDetails.explainurl || '',
      size: templateFiledataDetails.size || '',
      mimetype: templateFiledataDetails.mimetype || '',
      format: templateFiledataDetails.format || '',
      compressFormat: templateFiledataDetails.compressFormat || '',
      compressFormatOther: templateFiledataDetails.compressFormatOthre || '',
      packageFormat: templateFiledataDetails.packageFormat || '',
      packageFormatOther: templateFiledataDetails.packageFormatOther || '',
      schema: templateFiledataDetails.schema || '',
      schemaType: templateFiledataDetails.schemaType || '',
      ngsiEntityType: templateFiledataDetails.ngsiEntityType || '',
      ngsiTenant: templateFiledataDetails.ngsiTenant || '',
      ngsiServicePath: templateFiledataDetails.ngsiServicePath || '',
      ngsiDataModel: templateFiledataDetails.ngsiDataModel || '',
      contractRequired: isTemplate ? templateFiledataDetails.contractRequired : '要求しない',
      connectRequired: isTemplate ? templateFiledataDetails.contractRequired : '要求する',
      licenseurl: templateFiledataDetails.licenseurl || '',
      getResourceIDForProvenance: {
        label: isTemplate ? templateFiledataDetails.getResourceIDForProvenance.label : '来歴登録を行わない',
        value: isTemplate ? templateFiledataDetails.getResourceIDForProvenance.value : 'no'
      },
      previousEventId: templateFiledataDetails.previousEventId || '',
      dataServiceTitle: templateFiledataDetails.dataServiceTitle || '',
      dataServiceEndpointUrl: templateFiledataDetails.dataServiceEndpointUrl || '',
      dataServiceEndpointDescription: templateFiledataDetails.dataServiceEndpointDescription || '',
      urlForProvenance: templateFiledataDetails.urlForProvenance || '',
      caddeUserId: templateFiledataDetails.caddeUserId || '',
      name: 0,
      label: '配信1',
      displayFlgObj: {
        downloadUrl: true,
        ngsiEntityType: true,
        ngsiTenant: true,
        ngsiServicePath: true,
        ngsiDataModel: true,
      },
      file: '',
      errorFlgObj: {
        resourceType: false,
        downloadUrl: false,
        explainurl: false,
        filename: false,
        description: false,
        size: false,
        mimetype: false,
        format: false,
        schema: false,
        schemaType: false,
        ngsiDataModel: false,
        contract: false,
        connect: false
      },
      errorMessageObj: {
        resourceType: '',
        downloadUrl: '',
        explainurl: '',
        filename: '',
        description: '',
        size: '',
        mimetype: '',
        format: '',
        schema: '',
        schemaType: '',
        ngsiDataModel: '',
        contract: '',
        connect: ''
      },
      freeFieldColumn: {
        compressFormat: false,
        packageFormat: false
      }
    })
  }
})

if (filedataDetails.length) {
  for (var cnt = 0; cnt < filedataDetails.length; cnt++) {
    filedataDetails[cnt].inputSupportResourceType = 
    filedataDetails[cnt].inputSupportUrl = ''
    filedataDetails[cnt].name = cnt
    filedataDetails[cnt].label = '配信' + String(cnt + 1)
    filedataDetails[cnt].errorFlgObj = {}
    filedataDetails[cnt].errorMessageObj = {}
    filedataDetails[cnt].displayFlgObj = {
      downloadUrl: true,
      ngsiEntityType: true,
      ngsiTenant: true,
      ngsiServicePath: true,
      ngsiDataModel: true
    }
    var resourceType = filedataDetails[cnt].resourceType.value
    var displayFlg = filedataDetails[cnt].displayFlgObj
    if (resourceType) {
      switch (resourceType) {
        case 'file/http':
        case 'file/ftp':
          displayFlg.downloadUrl = true
          displayFlg.explainUrl = true
          displayFlg.ngsiEntityType = false
          displayFlg.ngsiTenant = false
          displayFlg.ngsiServicePath = false
          displayFlg.ngsiDataModel = false
          break
        case 'api/ngsi':
          displayFlg.downloadUrl = true
          displayFlg.explainUrl = true
          displayFlg.ngsiEntityType = true
          displayFlg.ngsiTenant = true
          displayFlg.ngsiServicePath = true
          displayFlg.ngsiDataModel = true
          break
      }
    }
    // 自由欄表示非表示設定
    filedataDetails[cnt].freeFieldColumn = {}
    if (filedataDetails[cnt].compressFormatOther) {
      filedataDetails[cnt].freeFieldColumn.compressFormat = true
    } else {
      filedataDetails[cnt].freeFieldColumn.compressFormat = false
    }
    if (filedataDetails[cnt].packageFormatOther) {
      filedataDetails[cnt].freeFieldColumn.packageFormat = true
    } else {
      filedataDetails[cnt].freeFieldColumn.packageFormat = false
    }

    // 「契約確認の要否」
    if (!filedataDetails[cnt].contractRequired){
      filedataDetails[cnt].contractRequired = '要求しない'
    }
    // 「コネクタ利用の要否」
    if (!filedataDetails[cnt].connectRequired) {
      filedataDetails[cnt].connectRequired = '要求する'
    }
  }
}

for (var fileNum = 0; fileNum < filedataDetails.length; fileNum++) {
  if (!filedataDetails[fileNum].contractRequired) {
    filedataDetails[fileNum].errorFlgObj.contract = true
  }
  if (!filedataDetails[fileNum].connectRequired) {
    filedataDetails[fileNum].errorFlgObj.connect = true
  }
}

// 折り畳み表示設定
if (store.selectedMode.mode === 'template') {
  // テンプレート編集時は折り畳み表示を無効化
  for (var key in expanded) {
    expanded[key] = true
  }

  // テンプレート編集時は非表示を無効化
  for (var key in hideFlgs) {
    hideFlgs[key] = true
  }
} else {
  // テンプレート編集時以外はテンプレートファイルに基づき表示方法を設定
  for (key in expanded) {
    expanded[key] = store.itemDisplayFlg[key] !== 'fold'
  }

  for (var key in hideFlgs) {
    hideFlgs[key] = store.itemDisplayFlg[key] !== 'hide'
  }
}

// *****************
// Methods
// *****************

checkFiledataDetails()

// デフォルト自動補完候補取得
function defaultAutoCorrect() {
  // 配信の取得先URL
  axios
    .post(config.apiPrefix + '/resource/autocorrect', { label: 'url', value: filedataDetails[0].inputSupportUrl })
    .then((response) => {
      autoCorrect.inputSupportUrl = response.data.candidates
    })
    .catch(err => {
      autoCorrect.inputSupportUrl = []
      console.log('error message:', err.response.data.message)
    })
  // 配信の名称
  axios
    .post(config.apiPrefix + '/resource/autocorrect', { label: 'name', value: filedataDetails[0].filename })
    .then((response) => {
      autoCorrect.filename = response.data.candidates
    })
    .catch(err => {
      autoCorrect.filename = []
      console.log('error message:', err.response.data.message)
    })
  // 配信のダウンロードURL
  axios
    .post(config.apiPrefix + '/resource/autocorrect', { label: 'url', value: filedataDetails[0].downloadUrl })
    .then((response) => {
      autoCorrect.downloadUrl = response.data.candidates
    })
    .catch(err => {
      autoCorrect.downloadUrl = []
      console.log('error message:', err.response.data.message)
    })
}

// 自動補完候補取得
function filterFn(val, update, abort, field) {
  setTimeout(() => {
    update(() => {
      for (var ckanLabel in AUTOCORRECT_KEYMAP) {
        // カタログのフィールド名に紐づくCKAN変数名を取得
        if (field === ckanLabel) {
          var key = AUTOCORRECT_KEYMAP[ckanLabel]
        }
      }
      var req = {
        label: key,
        value: val
      }
      // 自動補完候補検索API実行
      axios
        .post(config.apiPrefix + '/resource/autocorrect', req)
        .then((response) => {
          const needle = val.toLowerCase()
          var autoOption = response.data.candidates.filter(v => v.toLowerCase().indexOf(needle) > -1)
          autoCorrect[field] = autoOption
        })
        .catch(err => {
          autoCorrect[field] = []
          console.log('error message:', err.response.data.message)
        })
    })
  }, 100)
}

// 自動補完フィールドの入力値をv-modelに設定
function setModel(val, index, field) {
  index[field] = val
  if (field === 'downloadUrl' && !index.resourceName) {
    // データ名フィールドが空の場合、配信のダウンロードURLの入力値を反映
    index.resourceName = val
  }
}

// 入力値有無判定機能
function isEmpty(value) {
  var result = {
    status: '',
    message: ''
  }
  if (value) {
    result.status = false
    result.message = ''
    return result
  } else {
    result.status = true
    result.message = '【入力必須項目】'
    return result
  }
}

// 入力値有効判定機能
function isValid(value, max, label) {
  var res = {
    isError: false,
    message: ''
  }
  if (value && value > max) {
    res.isError = true
    if (label === 'size') {
      res.message = '【無効な値】'
    } else if (label === 'downloadUrl') {
      res.message = '【文字数オーバー】'
　　}
  }
  return res
}

// 登録データ追加機能
function btnAddData() {
  var templateFiledataDetails = store.template.filedataDetails[0]
  var isTemplate = !!templateFiledataDetails
  filedataDetails.push({
    filename: isTemplate ? templateFiledataDetails.filename : store.catalogTitle,
    resourceType: {
      label: isTemplate ? templateFiledataDetails.resourceType.label : '',
      value: isTemplate ? templateFiledataDetails.resourceType.value : ''
    },
    dataname: isTemplate ? templateFiledataDetails.dataname : '',
    description: isTemplate ? templateFiledataDetails.description : '',
    downloadUrl: isTemplate ? templateFiledataDetails.downloadUrl : '',
    explainurl: isTemplate ? templateFiledataDetails.explainurl : '',
    size: isTemplate ? templateFiledataDetails.size : '',
    mimetype: isTemplate ? templateFiledataDetails.mimetype : '',
    format: isTemplate ? templateFiledataDetails.format : '',
    compressFormat: isTemplate ? templateFiledataDetails.compressFormat : '',
    compressFormatOther: isTemplate ? templateFiledataDetails.compressFormatOther : '',
    packageFormat: isTemplate ? templateFiledataDetails.packageFormat : '',
    packageFormatOther: isTemplate ? templateFiledataDetails.packageFormatOther : '',
    schema: isTemplate ? templateFiledataDetails.schema : '',
    schemaType: isTemplate ? templateFiledataDetails.schemaType : '',
    ngsiEntityType: isTemplate ? templateFiledataDetails.ngsiEntityType : '',
    ngsiTenant: isTemplate ? templateFiledataDetails.ngsiTenant : '',
    ngsiServicePath: isTemplate ? templateFiledataDetails.ngsiServicePath : '',
    ngsiDataModel: isTemplate ?  JSON.parse(JSON.stringify(templateFiledataDetails.ngsiDataModel)) : [],
    contractRequired: isTemplate ? templateFiledataDetails.contractRequired : '要求しない',
    connectRequired: isTemplate ? templateFiledataDetails.contractRequired : '要求する',
    licenseurl: isTemplate ? templateFiledataDetails.licenseurl : '',
    getResourceIDForProvenance: {
      label: isTemplate ? templateFiledataDetails.getResourceIDForProvenance.label : '来歴登録を行わない',
      value: isTemplate ? templateFiledataDetails.getResourceIDForProvenance.value : 'no'
    },
    resourceIDForProvenance: '',
    previousEventId: isTemplate ? templateFiledataDetails.previousEventId : '',
    dataServiceTitle: isTemplate ? templateFiledataDetails.dataServiceTitle : '',
    dataServiceEndpointUrl: isTemplate ? templateFiledataDetails.dataServiceEndpointUrl : '',
    dataServiceEndpointDescription: isTemplate ? templateFiledataDetails.dataServiceEndpointDescription : '',
    urlForProvenance: isTemplate ? templateFiledataDetails.urlForProvenance : '',
    caddeUserId: isTemplate ? templateFiledataDetails.caddeUserId : '',
    name: filedataDetails.length,
    label: '配信' + String(filedataDetails.length + 1),
    inputSupportResourceType: '',
    inputSupportNgsiTenant: '',
    inputSupportNgsiServicePath: '',
    inputSupportUrl: '',
    displayFlgObj: {
      downloadUrl: true,
      ngsiEntityType: true,
      ngsiTenant: true,
      ngsiServicePath: true,
      ngsiDataModel: true
    },
    file: '',
    errorFlgObj: {
      downloadUrl: false,
      explainurl: false,
      filename: false,
      description: false,
      size: false,
      mimetype: false,
      format: false,
      compressFormat: false,
      compressFormatOther: false,
      packageFormat: false,
      packageFormatOther: false,
      schema: false,
      schemaType: false,
      ngsiDataModel: false,
      contract: false,
      connect: false,
      dataServiceTitle: false,
      dataServiceEndpointUrl: false,
      dataServiceEndpointDescription: false
    },
    errorMessageObj: {
      resourceType: '',
      downloadUrl: '',
      explainurl: '',
      filename: '',
      description: '',
      size: '',
      mimetype: '',
      format: '',
      compressFormat: '',
      compressFormatOther: '',
      packageFormat: '',
      packageFormatOther: '',
      schema: '',
      schemaType: '',
      ngsiDataModel: '',
      contract: '',
      connect: '',
      dataServiceTitle: '',
      dataServiceEndpointUrl: '',
      dataServiceEndpointDescription: ''
    },
    freeFieldColumn: {
      compressFormat: false,
      packageFormat: false
    }
  })
  errorFlagList.flagList.noContract = false
  errorFlagList.flagList.noConnect = false
  defaultAutoCorrect()
}

// 登録データ削除機能
function btnRemoveData(fileNum) {
  filedataDetails.splice(fileNum, 1)
  for (var i = 0; i < filedataDetails.length; i++) {
    filedataDetails[i].name = i
    filedataDetails[i].label = '配信' + String(i + 1)
  }
  updateDataMessage.value = ''
}

// データ提供法別登録機能
function updateData(inputSupportType, dataurl, detail) {
  updateDataMessage.value = ''
  if (inputSupportType === 'file/http' && dataurl !== '') {
    showUploader.value = false
    updateHttpData(detail)
  } else if (inputSupportType === 'file/ftp' && dataurl !== '') {
    showUploader.value = false
    updateFtpData(detail)
  } else if (inputSupportType === 'api/ngsi' && dataurl !== '') {
    showUploader.value = false
    updateNgsiData(detail)
  } else if (inputSupportType === 'local') {
    showUploader.value = true
  }
}

// HTTPデータ取得機能
function updateHttpData(filedata, autoUploadFlg = false) {
  updateDataMessage.value = '処理中です。暫くお待ちください...'
  filedata.inputSupportIsRequestSuccess = false
  filedata.getResourceIDForProvenance.value = 'no'
  axios.get(config.apiPrefix + '/resource' + '/http' + '/' + filedata.inputSupportUrl)
    .then(async res => {
      updateDataMessage.value = ''
      urlResponse.value = res
      urlUpdateFileSet(filedata, autoUploadFlg)
      // 配信の取得に成功した場合は、配信情報の入力のフィールドに値を反映する
      filedata.resourceType.value = filedata.inputSupportResourceType
      filedata.downloadUrl = filedata.inputSupportUrl
      filedata.inputSupportIsRequestSuccess = true
    })
    .catch(err => {
      updateDataMessage.value = ''
      console.log('error message:', err.response.data.message)
      completeDialog.isDisplay = true
      completeDialog.message = err.response.data.message || '配信の取得に失敗しました。\n管理者に問い合わせてください。'
      completeDialog.errorFlg = true
    })
}

// FTPデータ取得機能
function updateFtpData(filedata, autoUploadFlg = false) {
  updateDataMessage.value = '処理中です。暫くお待ちください...'
  filedata.inputSupportIsRequestSuccess = false
  filedata.getResourceIDForProvenance.value = 'no'
  axios.get(config.apiPrefix + '/resource' + '/ftp' + '/' + filedata.inputSupportUrl)
    .then(async res => {
      updateDataMessage.value = ''
      urlResponse.value = res
      urlUpdateFileSet(filedata, autoUploadFlg)
      // 配信の取得に成功した場合は、配信情報の入力のフィールドに値を反映する
      filedata.resourceType.value = filedata.inputSupportResourceType
      filedata.downloadUrl = filedata.inputSupportUrl
      filedata.inputSupportIsRequestSuccess = true
    })
    .catch(err => {
      updateDataMessage.value = ''
      console.log('error message:', err.response.data.message)
      completeDialog.isDisplay = true
      completeDialog.message = err.response.data.message || '配信の取得に失敗しました。\n管理者に問い合わせてください。'
      completeDialog.errorFlg = true
    })
}

// NGSIデータ取得機能
function updateNgsiData(filedata, autoUploadFlg = false) {
  updateDataMessage.value = '処理中です。暫くお待ちください...'
  filedata.inputSupportIsRequestSuccess = false
  filedata.getResourceIDForProvenance.value = 'no'
  var ngsiInfo = {
    url: filedata.inputSupportUrl,
    tenant: filedata.inputSupportNgsiTenant || '',
    service_path: filedata.inputSupportNgsiServicePath || ''
  }
  axios.post(config.apiPrefix + '/ngsidata', ngsiInfo)
    .then(async res => {
      updateDataMessage.value = ''
      urlResponse.value = res
      urlUpdateFileSet(filedata, autoUploadFlg)
      // 配信の取得に成功した場合は、配信情報の入力のフィールドに値を反映する
      filedata.resourceType.value = filedata.inputSupportResourceType
      filedata.downloadUrl = filedata.inputSupportUrl
      filedata.ngsiTenant = filedata.inputSupportNgsiTenant
      filedata.ngsiServicePath = filedata.inputSupportNgsiServicePath
      filedata.inputSupportIsRequestSuccess = true
    })
    .catch(err => {
      updateDataMessage.value = ''
      console.log('error message:', err.response.data.message)
      completeDialog.isDisplay = true
      completeDialog.message = err.response.data.message || '配信の取得に失敗しました。\n管理者に問い合わせてください。'
      completeDialog.errorFlg = true
    })
}

// メディアタイプの自動入力値判別
function validMimetype(autoValue) {
  var urlMimeType = ''
  for (var key of store.itemList.mimetype) {
    if (autoValue !== key.label) {
      continue
    }
    urlMimeType = {
      label: key.label,
      value: key.value
    }
  }
  return urlMimeType
}

// ファイル情報更新機能
function urlUpdateFileSet(filedata, autoUploadFlg) {
  var urlMimeType = validMimetype(urlResponse.value.data.mime_type)
  var urlSize = ''
  var urlFileformat = ''
  console.log('ファイル情報更新機能')
  console.log(urlResponse)
  if (urlResponse.value !== [] && urlResponse.value !== null) {
    urlSize = urlResponse.value.data.file_size
    urlFileformat = urlResponse.value.data.format
  }
  if (autoUploadFlg) {
    filedata.dataname = urlResponse.value.data.dataname
    store.updateOneFiledataDetails({
        label: filedata.label,
        dataname: filedata.dataname
      }
    )
  } else {
    filedata.description = filedata.description || urlResponse.value.data.data_list
    // filedata.description = urlResponse.value.data.data_list
    filedata.urlSetFlg = true
    filedata.dataname = urlResponse.value.data.dataname
    filedata.size = urlSize
    filedata.mimetype = urlMimeType ?  JSON.parse(JSON.stringify(urlMimeType)) : ''
    filedata.format = urlFileformat
  }
}

// 選択ファイル削除機能
function removeFileList(file) {
  getFileList = getFileList.filter(item => item !== file.name)
  fileDetails = fileDetails.filter(function (element, index, array) {
    return (element.filename && element.filename !== file.name)
  })
}

// ファイルアップデート開始処理
function updateStart(filedata){
  filedata.inputSupportIsRequestSuccess = false
  filedata.getResourceIDForProvenance.value = 'no'
}

// 選択ファイルアップロード機能
async function updateFinish(filedata) {
  filedata.size = localFileData.value.size
  const formData = new FormData()
  formData.append('file', localFileData.value)
  var vars = await uploadFiles(formData)
  filedata.inputSupportIsRequestSuccess = true
  filedata.description = filedata.description || vars.vars
  filedata.format = vars.format
  filedata.dataname = vars.dataname
  var checkedMimetype = validMimetype(vars.mimetype)
  filedata.mimetype = checkedMimetype ?  JSON.parse(JSON.stringify(checkedMimetype)) : ''
}

// 選択データの情報取得機能
async function uploadFiles(formData) {
  var ret = {
    vars: [],
    format: '',
    mimetype: ''
  }
  try {
    const res = await axios.post(config.apiPrefix + '/uploads', formData)
      const items = res.data
    if (items.var_list) {
      ret.vars = items.data_list
      ret.format = items.format
      ret.mimetype = items.mimetype
      ret.dataname = items.dataname
    } else {
      ret.vars = ''
      ret.format = items.format
      ret.mimetype = items.mimetype
      ret.dataname = items.dataname
    }
    return ret
  } catch (err) {
    console.log('error message:', err.response.data.message)
    completeDialog.isDisplay = true
    completeDialog.message = err.response.data.message || '配信の取得に失敗しました。\n管理者に問い合わせてください。'
    completeDialog.errorFlg = true
  }
}

// 選択ファイルアップロード機能
async function uploadFactory(file) {
  localFileData.value = file[0]
  return new Promise((resolve, reject) => {
    resolve(file)
  })
}

function topScroll() {
  window.scrollTo(0, 0)
}

// データモデル行追加機能
function addDataModel(filedataDetails) {
  filedataDetails.ngsiDataModel = filedataDetails.ngsiDataModel || []
   filedataDetails.ngsiDataModel.push({
    attribute: '',
    dataType: '',
    example: '',
    description: '',
    metadata: []
  })
}

// データモデル行削除
function deleteDatamModel(row, filedataDetails) {
  filedataDetails.ngsiDataModel.splice(row.pageIndex, 1)
}

// データモデル取得
function getNgsiDataModel(downloadUrl, ngsiTenant, ngsiServicePath, ngsiEntityType, filedataDetails) {
  tableLoading.value = true
  dataModelErrorMessage.value = ''
  var params = {
    url: downloadUrl,
    tenant: ngsiTenant,
    service_path: ngsiServicePath,
    entity_type: ngsiEntityType
  }
  filedataDetails.ngsiDataModel = []
  axios
    .post(config.apiPrefix + '/ngsidatamodel', params)
    .then((response) => {
      tableLoading.value = false
      for (var val of response.data.data_model) {
        filedataDetails.ngsiDataModel.push(val)
      }
    })
    .catch(err => {
      tableLoading.value = false
      console.log('error message:', err.response.data.message)
      completeDialog.isDisplay = true
      completeDialog.message = err.response.data.message || 'NGSIデータモデルの取得に失敗しました。\n管理者に問い合わせてください。'
      completeDialog.errorFlg = true
    })
}

// メタデータ表示機能
function showMetadata(props) {
  showMetadataDialog.value = true
  metaAttribute.value = props.row.attribute
  metaDescription.value = props.row.description
  metadataList.value = props.row.metadata
}

// メタデータ行追加機能
function addMetadata(row) {
  row.push({
    metadataName: '',
    dataType: '',
    example: '',
    description: ''
  })
}

// メタデータ行削除機能
function deleteMetadata(row, metadata) {
  metadata.splice(row.pageIndex, 1)
}

// 前段イベント識別子検索機能
function searchPreviousEventId(resourceUrlForProvenance, caddeUserId) {
  showPreviousEventIdList.value = true
  tableLoading.value = true
  resultData.value = []
  axios.post(config.apiPrefix + '/previouseventid', { resource_url: resourceUrlForProvenance, user_id: caddeUserId, provider_id: store.publisherId.label })
    .then(async res => {
      tableLoading.value = false
      var previousEvents = res.data.result
      for (var i = 0; i < previousEvents.length; i++) {
        resultData.value.push({
          providerId: previousEvents[i].provider_id,
          timestamp: previousEvents[i].timestamp,
          eventId: previousEvents[i].event_id,
          userId: previousEvents[i].user_id
        })
      }
    })
    .catch(err => {
      tableLoading.value = false
      console.log('error message:', err.response.data.message)
      previousEventIdErrorMessage.value = err.response.data.message || '前段イベント識別子の検索に失敗しました。管理者に問い合わせてください。'
    })
}

// 前段イベント識別子選択
function rowClick(evt, row, index) {
  filedataDetails[detail.value].previousEventId = row.eventId
  showPreviousEventIdList.value = false
}

// データサービスフィールドのテンプレート値自動設定
function templateDataService(val, filedataDetails, field) {
  if (!filedataDetails[field]) {
    filedataDetails[field] = val
  }
}

// パラメータ更新機能
function commitStore() {
  var registedFiledataDetails = []
  if (filedataDetails.length) {
    for (var i = 0; i < filedataDetails.length; i++) {
      // 入力支援フィールド
      // 配信の取得方法
      var registedInputSupportResourceType = filedataDetails[i].inputSupportResourceType || ''
      // 配信の取得先URL
      var registedInputSupportUrl = filedataDetails[i].inputSupportUrl || ''
      // NGSIテナント
      var registedInputSupportNgsiTenant = filedataDetails[i].inputSupportNgsiTenant || ''
      // NGSIサービスパス
      var registedInputSupportNgsiServicePath = filedataDetails[i].inputSupportNgsiServicePath || ''
      // 配信の取得の成功
      var registedInputSupportIsRequestSuccess = filedataDetails[i].inputSupportIsRequestSuccess || false

      // 配信の入力情報フィールド
      // リソース提供手段の識別子
      if (filedataDetails[i].resourceType.value) {
        if (filedataDetails[i].resourceType.value === 'file/http') {
          var registedResourceTypeLabel = 'ファイル提供(HTTP)'
          var registedResourceTypeValue = 'file/http'
        } else if (filedataDetails[i].resourceType.value === 'file/ftp') {
          registedResourceTypeLabel = 'ファイル提供(FTP)'
          registedResourceTypeValue = 'file/ftp'
        } else if (filedataDetails[i].resourceType.value === 'api/ngsi') {
          registedResourceTypeLabel = 'API提供(NGSI API)'
          registedResourceTypeValue = 'api/ngsi'
        } else {
          registedResourceTypeLabel = ''
          registedResourceTypeValue = ''
        }
      }
      // 配信のダウンロードURL
      var registedDownloadUrl = filedataDetails[i].downloadUrl || ''
      // 配信の情報提供ページURL
      var registedExplainUrl = filedataDetails[i].explainurl || ''
      // 配信の名称
      var registedFilename = filedataDetails[i].filename || ''
      // 配信の説明
      var registedDescription = filedataDetails[i].description || ''
      // 配信のバイトサイズ
      var registedSize = filedataDetails[i].size || ''
      // ファイルのカラム名
      var registedColumnName = filedataDetails[i].columnName || ''
      // 配信のメディアタイプ
      var registedMimetype = filedataDetails[i].mimetype || ''
      // 配信のファイル形式
      var registedFormat = filedataDetails[i].format || ''
      // 配信の圧縮形式
      var registedCompressFormat = filedataDetails[i].compressFormat || ''
      // 配信の圧縮形式（自由記述）
      var registedCompressFormatOther = filedataDetails[i].compressFormatOther || ''
      // 配信のパッケージ形式
      var registedPackageFormat = filedataDetails[i].packageFormat || ''
      // 配信のパッケージ形式（自由記述）
      var registedPackageFormatOther = filedataDetails[i].packageFormatOther || ''
      // スキーマ
      var registedSchema = filedataDetails[i].schema || ''
      // スキーマタイプ
      var registedSchemaType = filedataDetails[i].schemaType || ''
      // NGSIデータ種別
      var registedNgsiEntityType = filedataDetails[i].ngsiEntityType || ''
      // NGSIテナント
      var registedNgsiTenant = filedataDetails[i].ngsiTenant || ''
      // NGSIサービスパス
      var registedNgsiServicePath = filedataDetails[i].ngsiServicePath || ''
      // NGSIデータモデル
      var registedNgsiDataModel = filedataDetails[i].ngsiDataModel || []
      // 契約確認の要否
      var contractRequired = filedataDetails[i].contractRequired
      // コネクタ利用の要否
      var connectRequired = filedataDetails[i].connectRequired
      // 来歴登録の有無
      if (filedataDetails[i].getResourceIDForProvenance.value) {
        if (filedataDetails[i].getResourceIDForProvenance.value === 'yes') {
          var registedGetResourceIDForProvenanceLabel = '来歴登録を行う'
          var registedGetResourceIDForProvenanceValue = filedataDetails[i].getResourceIDForProvenance.value
        } else {
          registedGetResourceIDForProvenanceLabel = '来歴登録を行わない'
          registedGetResourceIDForProvenanceValue = filedataDetails[i].getResourceIDForProvenance.value
        }
      } else {
        registedGetResourceIDForProvenanceLabel = '来歴登録を行わない'
        registedGetResourceIDForProvenanceValue = 'no'
      }
      // 交換実績記録用リソースID
      var registedResourceIdForProvenance = filedataDetails[i].resourceIDForProvenance || ''
      // 前段イベント識別子
      var registedPreviousEventId = filedataDetails[i].previousEventId || ''
      // 来歴登録済みの配信のダウンロードURL
      var registedUrlForProvenance = filedataDetails[i].urlForProvenance || ''
      // 来歴登録済みのCADDEユーザID
      var registedCaddeUserId = filedataDetails[i].caddeUserId || ''
      // データサービスのタイトル
      var registedDataServiceTitle = filedataDetails[i].dataServiceTitle || ''
      // データサービスのエンドポイント
      var registedDataServiceEndpointUrl = filedataDetails[i].dataServiceEndpointUrl || ''
      // データサービスのエンドポイントの定義
      var registedDataServiceEndpointDescription = filedataDetails[i].dataServiceEndpointDescription || ''

      // 配信のラベル（画面タブの表示値）
      var registedLabel = filedataDetails[i].label || ''
      // 配信リソース名（リソース取得・保存時にwebサーバから付与）
      var registedDataName = filedataDetails[i].dataname || ''
      // 配信のライセンス
      var registedResourceLicenseTitle = filedataDetails[i].license_title || ''
      // 配信のライセンス（URL)
      var registedResourceLicenseUrl = filedataDetails[i].licenseurl || ''
      // 配信の発行日
      var registedIssued = filedataDetails[i].issued || ''
      // 配信のID
      var registedId = filedataDetails[i].id || ''

      registedFiledataDetails.push({
        inputSupportResourceType: registedInputSupportResourceType,
        inputSupportUrl: registedInputSupportUrl,
        inputSupportIsRequestSuccess: registedInputSupportIsRequestSuccess,
        inputSupportNgsiTenant: registedInputSupportNgsiTenant,
        inputSupportNgsiServicePath: registedInputSupportNgsiServicePath,
        resourceType: {
          label: registedResourceTypeLabel,
          value: registedResourceTypeValue
        },
        downloadUrl: registedDownloadUrl,
        explainurl: registedExplainUrl,
        filename: registedFilename,
        description: registedDescription,
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
          label: registedGetResourceIDForProvenanceLabel,
          value: registedGetResourceIDForProvenanceValue
        },
        resourceIDForProvenance: registedResourceIdForProvenance,
        previousEventId: registedPreviousEventId,
        urlForProvenance: registedUrlForProvenance,
        caddeUserId: registedCaddeUserId,
        dataServiceTitle: registedDataServiceTitle,
        dataServiceEndpointUrl: registedDataServiceEndpointUrl,
        dataServiceEndpointDescription: registedDataServiceEndpointDescription,
        label: registedLabel,
        dataname: registedDataName,
        licensetitle: registedResourceLicenseTitle,
        licenseurl: registedResourceLicenseUrl,
        issued: registedIssued,
        id: registedId,
      })
    }
  }
  console.log('registedFiledataDetails')
  console.log(registedFiledataDetails)
  store.updateFiledataDetails({
      filedataDetails: registedFiledataDetails,
      storeType: 'state'
    }
  )
  console.log('store.filedataDetails')
  console.log(store.filedataDetails)
}

// エラーフラグの管理機能
function checkErrorAllFields() {
  var noError = true
  errorCheckMessage.splice(0)
  const errorMessageDic = {
    resourceType: 'リソース提供手段の識別子は入力必須項目です。入力をお願いします。',
    downloadUrl: '配信のダウンロードURLは入力必須項目です。入力をお願いします。',
    explainurl: '配信の情報提供ページURLは入力必須項目です。入力をお願いします。',
    filename: '配信の名称は入力必須項目です。入力を今お願いします。',
    description: '配信の説明は入力必須項目です。入力をお願いします。',
    size: '配信のバイトサイズは入力必須項目です。入力をお願いします。',
    mimetype: '配信のメディアタイプは入力必須項目です。入力をお願いします。',
    format: '配信のファイル形式は入力必須項目です。入力をお願いします。',
    compressFormat: '配信の圧縮形式は入力必須項目です。入力をお願いします。',
    compressFormatOther: '配信の圧縮形式の自由欄に使用禁止文字が含まれています。',
    packageFormat: '配信のパッケージ形式は入力必須項目です。入力をお願いします。',
    packageFormatOther: '配信のパッケージ形式の自由欄に使用禁止文字が含まれています。',
    schema: 'スキーマは入力必須項目です。入力をお願いします。',
    schemaType: 'スキーマタイプは入力必須項目です。入力をお願いします。',
    ngsiDataModel: 'NGSIデータモデルの属性名は入力必須項目です。入力をお願いします。',
    dataServiceTitle: 'データサービスのタイトルは入力必須項目です。入力をお願いします。',
    dataServiceEndpointUrl: 'データサービスのエンドポイントは入力必須項目です。入力をお願いします。',
    dataServiceEndpointDescription: 'データサービスのエンドポイントの定義は入力必須項目です。入力をお願いします。',
    contract: '契約確認の要否は入力必須項目です。入力をお願いします。',
    connect: 'コネクタ利用の要否は入力必須項目です。入力をお願いします。'
  }

  // filedataDetailsのerrorFlgObjがtrueであれば、該当エラーメッセージと対応するデータ名を設定する
  // すべてのerrorFlgObjがfalseであれば次ページへ遷移する
  for (var i = 0; i < filedataDetails.length; i++) {
    for (var label in filedataDetails[i].errorFlgObj) {
      if (!filedataDetails[i].errorFlgObj[label]) {
        continue
      }
      switch (label) {
        case 'size':
          if (!filedataDetails[i][label]) {
            if (templateFlg[label] === 'mandatory') {
              var errorMessage = '配信' + (i + 1) + '：' + errorMessageDic[label]
              errorCheckMessage.push(errorMessage)
              noError = false
            }
          } else if (filedataDetails[i][label] > SIZE_MAX_VALUE) {
            errorMessage = '配信' + (i + 1) + '：' + ERROR_MESSAGE_INVALID[label]
            errorCheckMessage.push(errorMessage)
            noError = false
          }
          break
        case 'ngsiDataModel':
          var isEmptyAttribute = false
          var isDuplicateAttribute = false
          for (var j = 0; j < filedataDetails[i].ngsiDataModel.length; j++) {
            if (!filedataDetails[i].ngsiDataModel[j].attribute) {
              // 入力有無確認
              isEmptyAttribute = true
            }
            for (var k = 0; k < filedataDetails[i].ngsiDataModel.length; k++) {
              if (j !== k && filedataDetails[i].ngsiDataModel[j].attribute === filedataDetails[i].ngsiDataModel[k].attribute) {
                // 重複確認
                isDuplicateAttribute = true
              }
            }
          }
          if (isEmptyAttribute) {
            errorMessage = '配信' + (i + 1) + '：' + ERROR_MESSAGE_DATAMODEL.empty
            errorCheckMessage.push(errorMessage)
            noError = false
          }
          if (isDuplicateAttribute) {
            errorMessage = '配信' + (i + 1) + '：' + ERROR_MESSAGE_DATAMODEL.duplicate
            errorCheckMessage.push(errorMessage)
            noError = false
          }
          break
        case 'resourceType':
          if (store.selectedMode.mode !== 'template') {
            errorMessage = '配信' + (i + 1) + '：' + errorMessageDic[label]
            errorCheckMessage.push(errorMessage)
            noError = false
          }
          break
        case 'downloadUrl':
          console.log('配信のダウンロードURL', filedataDetails[i][label])
          if (store.selectedMode.mode !== 'template' && !filedataDetails[i][label]) {
            console.log('配信のダウンロードURL未入力')
            errorMessage = '配信' + (i + 1) + '：' + errorMessageDic[label]
            errorCheckMessage.push(errorMessage)
            noError = false
          } else if (filedataDetails[i][label].length > DOWNLOAD_URL_MAX_VALUE) {
            console.log('配信のダウンロードURL文字数オーバー')
            errorMessage = '配信' + (i + 1) + '：' + ERROR_MESSAGE_INVALID[label]
            errorCheckMessage.push(errorMessage)
            noError = false   
          }
          break
        default:
          console.log('未入力')
          errorMessage = '配信' + (i + 1) + '：' + errorMessageDic[label]
          errorCheckMessage.push(errorMessage)
          noError = false
          break
      }
    }
  }
  return noError
}

function clearResourceType(detail) {
  detail.resourceType.value = ''
}

function checkFiledataDetails () {
  var i = 0
  var j = 0
  var k = 0
  for (i = 0; i < filedataDetails.length; i++) {
    // 配信の取得方法のチェック
    if (filedataDetails[i].inputSupportResourceType) {
      updateDataMessage.value = ''
    }
    // リソース提供手段の識別子のチェック
    switch (filedataDetails[i].resourceType.value) {
      case 'file/http':
      case 'file/ftp':
        filedataDetails[i].displayFlgObj.downloadUrl = true
        filedataDetails[i].displayFlgObj.explainUrl = true
        filedataDetails[i].displayFlgObj.ngsiEntityType = false
        filedataDetails[i].displayFlgObj.ngsiTenant = false
        filedataDetails[i].displayFlgObj.ngsiServicePath = false
        filedataDetails[i].displayFlgObj.ngsiDataModel = false
        filedataDetails[i].ngsiEntityType = ''
        filedataDetails[i].ngsiTenant = ''
        filedataDetails[i].ngsiServicePath = ''
        filedataDetails[i].ngsiDataModel = ''
        break
      case 'api/ngsi':
        filedataDetails[i].displayFlgObj.downloadUrl = true
        filedataDetails[i].displayFlgObj.explainUrl = true
        filedataDetails[i].displayFlgObj.ngsiEntityType = true
        filedataDetails[i].displayFlgObj.ngsiTenant = true
        filedataDetails[i].displayFlgObj.ngsiServicePath = true
        filedataDetails[i].displayFlgObj.ngsiDataModel = true
        break
      default:
        filedataDetails[i].displayFlgObj.downloadUrl = true
        filedataDetails[i].displayFlgObj.explainUrl = true
        filedataDetails[i].displayFlgObj.ngsiEntityType = false
        filedataDetails[i].displayFlgObj.ngsiTenant = false
        filedataDetails[i].displayFlgObj.ngsiServicePath = false
        filedataDetails[i].displayFlgObj.ngsiDataModel = false
        filedataDetails[i].ngsiEntityType = ''
        filedataDetails[i].ngsiTenant = ''
        filedataDetails[i].ngsiServicePath = ''
        filedataDetails[i].ngsiDataModel = ''
    }
   
    // 配信のダウンロードURLのチェック
    if (filedataDetails[i].downloadUrl) {
      var errorObjDownloadUrl = isValid(filedataDetails[i].downloadUrl.length, DOWNLOAD_URL_MAX_VALUE, 'downloadUrl')
      filedataDetails[i].errorFlgObj.downloadUrl = errorObjDownloadUrl.isError
      filedataDetails[i].errorMessageObj.downloadUrl = errorObjDownloadUrl.message
    } else {
      if (store.selectedMode.mode !== 'template') {
        filedataDetails[i].errorFlgObj.downloadUrl = true
        filedataDetails[i].errorMessageObj.downloadUrl = '【入力必須項目】'
      }
    }
    // バイトサイズのチェック
    if (filedataDetails[i].size) {
      var errorObjSize = isValid(filedataDetails[i].size, SIZE_MAX_VALUE, 'size')
      filedataDetails[i].errorFlgObj.size = errorObjSize.isError
      filedataDetails[i].errorMessageObj.size = errorObjSize.message
    }
    // 配信の圧縮形式の自由欄表示・非表示制御
    if (filedataDetails[i].compressFormat.value && filedataDetails[i].compressFormat.value === 'その他') {
      filedataDetails[i].freeFieldColumn.compressFormat = true
    } else {
      filedataDetails[i].freeFieldColumn.compressFormat = false
      filedataDetails[i].compressFormatOther = ''
    }
    // リソース提供手段の識別子のチェック確認
    if (filedataDetails[i].resourceType.value) {
      filedataDetails[i].errorFlgObj.resourceType = false
    } else {
      var errorObjResourceType = isEmpty(filedataDetails[i].resourceType.value)
      filedataDetails[i].errorFlgObj.resourceType = true
      filedataDetails[i].errorMessageObj.resourceType = errorObjResourceType.message
    }
    // 配信のパッケージ形式の自由欄表示・非表示制御
    if (filedataDetails[i].packageFormat.value && filedataDetails[i].packageFormat.value === 'その他') {
      filedataDetails[i].freeFieldColumn.packageFormat = true
    } else {
      filedataDetails[i].freeFieldColumn.packageFormat = false
      filedataDetails[i].packageFormatOther = ''
    }
    // 使用禁止文字の有無確認
    if (filedataDetails[i].compressFormatOther.match(',')) {
      filedataDetails[i].errorFlgObj.compressFormatOther = true
      filedataDetails[i].errorMessageObj.compressFormatOther = '使用禁止文字が含まれています。'
    } else {
      filedataDetails[i].errorFlgObj.compressFormatOther = false
      filedataDetails[i].errorMessageObj.compressFormatOther = ''
    }
    if (filedataDetails[i].packageFormatOther.match(',')) {
      filedataDetails[i].errorFlgObj.packageFormatOther = true
      filedataDetails[i].errorMessageObj.packageFormatOther = '使用禁止文字が含まれています。'
    } else {
      filedataDetails[i].errorFlgObj.packageFormatOther = false
      filedataDetails[i].errorMessageObj.packageFormatOther = ''
    }
    // NGSIデータモデルの属性名の入力値確認
    if (!filedataDetails[i].ngsiDataModel.length) {
      filedataDetails[i].errorFlgObj.ngsiDataModel = false
    } else {
      var isEmptyAttribute = false
      var isDuplicateAttribute = false
      errorDataModel.message = []
      for (j = 0; j < filedataDetails[i].ngsiDataModel.length; j++) {
        if (!filedataDetails[i].ngsiDataModel[j].attribute) {
          // 入力有無確認
          isEmptyAttribute = true
        }
        for (k = 0; k < filedataDetails[i].ngsiDataModel.length; k++) {
          if (j !== k && filedataDetails[i].ngsiDataModel[j].attribute === filedataDetails[i].ngsiDataModel[k].attribute) {
            // 重複確認
            isDuplicateAttribute = true
          }
        }
      }
      if (isEmptyAttribute) {
        filedataDetails[i].errorFlgObj.ngsiDataModel = true
        errorDataModel.message.push(ERROR_MESSAGE_DATAMODEL.empty)
      }
      if (isDuplicateAttribute) {
        filedataDetails[i].errorFlgObj.ngsiDataModel = true
        errorDataModel.message.push(ERROR_MESSAGE_DATAMODEL.duplicate)
      }
    }
    // NGSIデータモデルのメタデータ名の入力値確認
    errorMetadata.status = false
    errorMetadata.message = []
    var isEmptyMetadata = false
    var isDuplicateMetadata = false
    for (j = 0; j < filedataDetails[i].ngsiDataModel.length; j++) {
      for (var cnt = 0; cnt < filedataDetails[i].ngsiDataModel[j].metadata.length; cnt++) {
        if (!filedataDetails[i].ngsiDataModel[j].metadata[cnt].metadataName) {
          // 入力有無確認
          errorMetadata.status = true
          isEmptyMetadata = true
        }
        for (var cnt2 = 0; cnt2 < filedataDetails[i].ngsiDataModel[j].metadata.length; cnt2++) {
          if (cnt !== cnt2 && filedataDetails[i].ngsiDataModel[j].metadata[cnt].metadataName === filedataDetails[i].ngsiDataModel[j].metadata[cnt2].metadataName) {
            // 重複確認
            errorMetadata.status = true
            isDuplicateMetadata = true
          }
        }
      }
    }
    if (isEmptyMetadata) {
      errorMetadata.message.push(ERROR_MESSAGE_METADATA.empty)
    }
    if (isDuplicateMetadata) {
      errorMetadata.message.push(ERROR_MESSAGE_METADATA.duplicate)
    }
    // NGSIデータモデルの取得ボタンの活性状態管理
    if (filedataDetails[i].ngsiEntityType && filedataDetails[i].downloadUrl) {
      inActiveGetDataModelBtn.value = false
    } else {
      inActiveGetDataModelBtn.value = true
    }
    if (store.selectedMode.mode === 'template') {
      break
    }
    // 入力必須フィールドの設定
    for (var label in templateFlg) {
      if (!(label in TEMPLATE_KEYMAP)) {
        continue
      }
      if (templateFlg[label] !== 'mandatory') {
        continue
      }
      var filedataDetailsKey = TEMPLATE_KEYMAP[label]
      var checkValue = filedataDetails[i][filedataDetailsKey]
      if (TEMPLATE_TYPE_KEYMAP[filedataDetailsKey] === 'object') {
        checkValue = filedataDetails[i][filedataDetailsKey].value || ''
      }
      errorOdj = isEmpty(checkValue)
      filedataDetails[i].errorFlgObj[filedataDetailsKey] = errorOdj.status
      filedataDetails[i].errorMessageObj[filedataDetailsKey] = errorOdj.message
    }

    // 来歴登録の有無が非表示になった場合、「来歴登録を行わない」に切り替え「交換実績記録用リソースID・前段イベント識別子」も非表示とする
    if(!(filedataDetails[i].resourceType.value && filedataDetails[i].downloadUrl && filedataDetails[i].inputSupportIsRequestSuccess)){
      filedataDetails[i].getResourceIDForProvenance.label = '来歴登録を行わない'
      filedataDetails[i].getResourceIDForProvenance.value = 'no'
    }
  }
}

defineExpose({
  checkErrorAllFields,
  commitStore
})

// *****************
// Watch
// *****************
watch(filedataDetails, checkFiledataDetails)

</script>

<template>
  <div class="dataset-resource">
    <div v-if="store.selectedMode.mode !== 'template'">
      <q-card class="q-ma-sm q-card-background-white">
        <q-card-section>
          <div>
            <font size='5' color='#1d468f'> データの概要情報</font>
          </div>
          <br>
          <div>
            データセットとして登録する
            <div class="cp_tooltip">配信
              <span class="cp_tooltiptext">
                <b>【配信】</b><br>
                &emsp; 配信するデータのことであり各種存在。（例えば、EXCEL、CSVの形式のテキストデータ、センサのログデータ等。）
              </span>
            </div>
            を追加する場合、配信追加ボタンを押し、データ概要情報を記載してください。<br>
            配信削除ボタンを押すと、選択しているタブの配信が削除されます。<br>
            データの概要情報を登録しない場合は、次へボタンを押してください。<br><br>
          </div>
          <div class="row q-gutter-lg">
            <q-btn
              label="配信追加"
              color="light-blue-10"
              class="q-px-lg q-py-xs"
              @click="btnAddData"
            />
            <q-btn
              label="配信削除"
              color="light-blue-10"
              class="q-px-lg q-py-xs"
              @click="btnRemoveData(detail)"
            />
          </div>
        </q-card-section>
      </q-card>
      <q-card class="q-ma-sm q-card-background-white">
        <q-card-section>
          <q-item>
            <q-item-label>
              <div style="padding-right: 25px">
                <p><font size="3" color="#1d468f">登録配信数: </font></p>
              </div>
            </q-item-label>
            <q-item-section>
              <div>
                <p><font size="3">  {{filedataDetails.length}} </font></p>
              </div>
            </q-item-section>
          </q-item>
        </q-card-section>
      </q-card>
      <q-tabs
        v-model="detail"
        inline-label
        shrink
        stretch
        class="bg-grey-3 text-black shadow-2"
        active-color="primary"
        align="justify"
        dense
      >
        <q-tab v-for="detail in filedataDetails" :key="detail.name" v-bind="detail"></q-tab>
      </q-tabs>
      <q-separator></q-separator>
      <q-tab-panels v-model="detail">
        <q-tab-panel v-for="detail in filedataDetails" :name=detail.name :key="detail.name">
          <div class="q-my-sm">
            <q-card 
              class="bg-blue-1 card-outline"
              square
              border
            >
              <q-card-section vertical>
                <q-item>
                  <q-item-section style="max-width: 1000px">
                    <font size="5" color="#1d468f">入力支援</font><br>
                    <p>入力支援機能を使用して配信の取得をすることで、配信情報の自動入力が可能となります。<br>
                    来歴登録のためには、配信の取得が必須となります。<br>
                    入力支援にある項目は配信の取得のためにのみ使用され、データセットには登録されません。<br>
                    <font color="#c10015"><b>配信の取得に成功すると、以下の項目が自動入力されます。</b></font><br>
                    ・リソース提供手段の識別子（配信の取得方法に「ファイル提供(ローカル)」を選択した場合は除く）<br>
                    ・配信のダウンロードURL（配信の取得方法に「ファイル提供(ローカル)」を選択した場合は除く）<br>
                    ・配信の説明（対応ファイル形式：json、csv、xls、xlsx）<br>
                    ・配信のバイトサイズ<br>
                    ・配信のメディアタイプ（配信のメディアタイプの選択肢と一致する場合）<br>
                    ・配信のファイル形式<br>
                    ・NGSIデータ種別（配信の取得方法に「API提供(NGSI)」を選択した場合）<br>
                    ・NGSIテナント（配信の取得方法に「API提供(NGSI)」を選択した場合）<br>
                    ・NGSIサービスパス（配信の取得方法に「API提供(NGSI)」を選択した場合）
                    </p>
                    <div v-if="showUseInputSupportButton">
                      <q-btn
                        label="入力支援機能を使用する"
                        color="light-blue-10"
                        style="max-width: 250px"
                        @click="useInputSupport = true, showUseInputSupportButton = false"
                      />
                    </div>
                    <div v-if="useInputSupport" class="q-pa-md">
                      <font size="4" color="#1d468f">配信の取得方法</font>
                      <p>この配信の取得方法を選択してください。</p>
                      <q-radio
                        v-model="detail.inputSupportResourceType"
                        val="file/http"
                        label="ファイル提供(HTTP)"
                        style="margin-left: 28px"
                        color="light-blue-10"
                      />
                      <q-radio
                        v-model="detail.inputSupportResourceType"
                        val="file/ftp"
                        label="ファイル提供(FTP)"
                        style="margin-left: 16px"
                        color="light-blue-10"
                      />
                      <q-radio
                        v-model="detail.inputSupportResourceType"
                        val="api/ngsi"
                        label="API提供(NGSI API)"
                        style="margin-left: 16px"
                        color="light-blue-10"
                      />
                      <q-radio
                        v-model="detail.inputSupportResourceType"
                        val="local"
                        label="ファイル提供(ローカル)"
                        style="margin-left: 16px"
                        color="light-blue-10"
                      />
                    </div>
                    <div v-if="detail.inputSupportResourceType == 'api/ngsi'">
                      <div class="q-pa-md">
                        <font size="4" color="#1d468f">NGSIテナント</font>
                        <br>
                        この配信のテナントを入力してください。<br>
                        <div class="row">
                          <q-item-section style="max-width: 700px">
                            <q-input
                              v-model="detail.inputSupportNgsiTenant"
                              placeholder="例：tenant1"
                            />
                          </q-item-section>
                        </div>
                      </div>
                      <div class="q-pa-md">
                        <font size="4" color="#1d468f">NGSIサービスパス</font>
                        <br>
                        この配信のサービスパスを入力してください。<br>
                        <div class="row">
                          <q-item-section style="max-width: 700px">
                            <q-input
                              v-model="detail.inputSupportNgsiServicePath"
                              placeholder="例：/service"
                            />
                          </q-item-section>
                        </div>
                      </div>
                    </div>
                    <div v-if="detail.inputSupportResourceType !== 'local' && detail.inputSupportResourceType !== '' && useInputSupport">
                      <div class="q-pa-md">
                        <font size="4" color="#1d468f">配信の取得先URL</font>
                        <p>
                        この配信の取得先URLを入力してください。<br>
                        取得ボタンを押下すると、入力したURL先の配信を取得します。<br>
                        </p>
                        <div class="row">
                          <q-item-section style="max-width: 700px">
                            <q-select
                              v-model="detail.inputSupportUrl"
                              placeholder="例：http://example.com/download/data.csv"
                              use-input
                              hide-selected
                              fill-input
                              input-debounce="0"
                              :options="autoCorrect.inputSupportUrl"
                              @filter="(val, update, abort) => { filterFn(detail.inputSupportUrl, update, abort, 'inputSupportUrl') }"
                              @input-value="(val) => { setModel(val, detail, 'inputSupportUrl') }"
                              hide-dropdown-icon
                            />
                          </q-item-section>
                          <q-item-section style="max-width: 400px">
                            <q-btn
                              label="取得"
                              color="light-blue-10"
                              style="max-width: 100px"
                              @click="updateData(detail.inputSupportResourceType, detail.inputSupportUrl, detail)"
                            />
                          </q-item-section>
                        </div>
                        <div>
                          <font size="3" color="#FF0000">{{updateDataMessage}}</font>
                        </div>
                      </div>
                    </div>
                    <div v-if="detail.inputSupportResourceType === 'local'">
                      <div class="q-pa-md">
                        <font size="4" color="#1d468f">配信のアップロード</font>
                        <p>下記に表示されているアップローダから配信のアップロードを行ってください。<br>
                          アップローダの右上のプラスボタンからアップロードするファイルを選択し、<br>
                          雲アイコンのボタンを押下することで、配信の取得が実行されます。<br>
                        </p>
                        <div class="row">
                          <q-item-section style="max-width: 700px">
                            <q-uploader
                              label="選択したファイルサイズ"
                              style="width: 400px"
                              auto-expand
                              :url="localFileUrl"
                              @remove:cancel="removeFileList"
                              @start="updateStart(detail)"
                              @finish="updateFinish(detail)"
                              :factory="uploadFactory"
                              :max-files="1"
                            />
                          </q-item-section>
                        </div>
                      </div>
                    </div>
                  </q-item-section>
                </q-item>
              </q-card-section>
            </q-card>
          </div>
          <div class="q-my-sm">
            <q-card class="q-card-background-white">
              <q-card-section vertical>
                <q-item>
                  <q-item-section style="max-width: 1000px;">
                    <font size="5" color="#1d468f">配信情報の入力</font>
                    <div class="q-pa-md">
                      <font size="4" color="#1d468f">リソース提供手段の識別子</font>
                      <q-btn
                        color="grey"
                        round
                        flat
                        dense
                        :icon="expanded.caddecResourceType ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                        @click="expanded.caddecResourceType = !expanded.caddecResourceType"
                      />
                      <q-slide-transition>
                        <div v-show="expanded.caddecResourceType">
                          <p>
                            <font size="2" color="orange"><b>入力支援機能対象項目</b></font><br>
                            この配信のリソース提供手段の識別子を選択してください。<br>
                            CKAN変数名：resources:caddec_resource_type
                          </p>
                          <div v-if="detail.errorFlgObj.resourceType">
                            <font size="2" color="#c10015">{{ detail.errorMessageObj.resourceType }}</font>
                          </div>
                          <q-radio
                            v-model="detail.resourceType.value"
                            val="file/http"
                            label="ファイル提供(HTTP)"
                            style="margin-left: 28px"
                            color="light-blue-10"
                          />
                          <q-radio
                            v-model="detail.resourceType.value"
                            val="file/ftp"
                            label="ファイル提供(FTP)"
                            style="margin-left: 16px"
                            color="light-blue-10"
                          />
                          <q-radio
                            v-model="detail.resourceType.value"
                            val="api/ngsi"
                            label="API提供(NGSI API)"
                            style="margin-left: 16px"
                            color="light-blue-10"
                          />
                        </div>
                        <p>{{ errorMessageInputRequired.value }}</p>
                      </q-slide-transition>
                    </div>
                    <div>
                      <div class="q-pa-md">
                        <font size="4" color="#1d468f">配信のダウンロードURL</font>
                        <q-btn
                          color="grey"
                          round
                          flat
                          dense
                          :icon="expanded.downloadUrl ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                          @click="expanded.downloadUrl = !expanded.downloadUrl"
                        />
                        <q-slide-transition>
                          <div v-show="expanded.downloadUrl">
                            <p>
                              <font size="2" color="orange"><b>入力支援機能対象項目</b></font><br>
                              この配信を直接ダウンロードできるURLを入力してください。<br>
                              CKAN変数名：resources:url
                            </p>
                            <q-item-section>
                              <q-select
                                v-model="detail.downloadUrl"
                                use-input
                                placeholder="例：http://example.com/download/data.csv"
                                hide-selected
                                fill-input
                                input-debounce="0"
                                :options="autoCorrect.downloadUrl"
                                @filter="(val, update, abort) => { filterFn(detail.downloadUrl, update, abort, 'downloadUrl') }"
                                @input-value="(val) => { setModel(val, detail, 'downloadUrl') }"
                                hide-dropdown-icon
                                counter
                                :error="detail.errorFlgObj.downloadUrl"
                                :error-message="detail.errorMessageObj.downloadUrl"
                              />
                            </q-item-section>
                          </div>
                        </q-slide-transition>
                      </div>
                    </div>
                    <div>
                      <div class="q-pa-md" v-show="hideFlgs.explainUrl">
                        <font size="4" color="#1d468f">配信の情報提供ページURL</font>
                        <q-btn
                          color="grey"
                          round
                          flat
                          dense
                          :icon="expanded.explainUrl ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                          @click="expanded.explainUrl = !expanded.explainUrl"
                        />
                        <q-slide-transition>
                          <div v-show="expanded.explainUrl">
                            <p>
                            この配信に関する情報として、提供されるデータセットの入手方法等が示された説明が記載されたページのURLを入力してください。<br>
                            CKAN変数：resources:explain_url
                            </p>
                            <q-input
                              v-model="detail.explainurl"
                              placeholder="例：http://example.com/explain/data.csv"
                              :error="detail.errorFlgObj.explainurl"
                              :error-message="detail.errorMessageObj.explainurl"
                            />
                          </div>
                        </q-slide-transition>
                      </div>
                    </div>
                    <div class="q-pa-md" v-show="hideFlgs.filename">
                      <font size="4" color="#1d468f">配信の名称</font>
                      <q-btn
                        color="grey"
                        round
                        flat
                        dense
                        :icon="expanded.filename ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                        @click="expanded.filename = !expanded.filename"
                      />
                      <q-slide-transition>
                        <div v-show="expanded.filename">
                          <p>この配信をひと言で言い表すタイトルを入力してください。<br>
                              CKAN変数名：resources:name</p>
                          <q-select
                            v-model="detail.filename"
                            placeholder="例: olympic2020_place.csv"
                            use-input
                            hide-selected
                            fill-input
                            input-debounce="0"
                            :options="autoCorrect.filename"
                            @filter="(val, update, abort) => { filterFn(detail.filename, update, abort, 'filename') }"
                            @input-value="(val) => { setModel(val, detail, 'filename') }"
                            :error="detail.errorFlgObj.filename"
                            :error-message="detail.errorMessageObj.filename"
                            hide-dropdown-icon
                          />
                        </div>
                      </q-slide-transition>
                    </div>
                    <div class="q-pa-md" v-show="hideFlgs.description">
                      <font size="4" color="#1d468f">配信の説明</font>
                      <q-btn
                        color="grey"
                        round
                        flat
                        dense
                        :icon="expanded.description ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                        @click="expanded.description = !expanded.description"
                      />
                      <q-slide-transition>
                        <div v-show="expanded.description">
                          <p>
                            <font size="2" color="orange"><b>入力支援機能対象項目</b></font><br>
                            この配信のデータ内容、形式(CSVファイル, API等)などの説明を入力してください。<br>
                            CKAN変数名：resources:description
                          </p>
                          <q-input
                            v-model="detail.description"
                            type="textarea"
                            autogrow
                            placeholder="例: 東京オリンピックの各会場の名称、住所、電話番号、会場の緯度・経度から構成されているデータです。CSV形式のファイルで配信します。"
                            :error="detail.errorFlgObj.description"
                            :error-message="detail.errorMessageObj.description"
                          />
                        </div>
                      </q-slide-transition>
                    </div>
                    <div class="q-pa-md" v-show="hideFlgs.size">
                      <font size="4" color="#1d468f">配信のバイトサイズ</font>
                      <q-btn
                        color="grey"
                        round
                        flat
                        dense
                        :icon="expanded.size ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                        @click="expanded.size = !expanded.size"
                      />
                      <q-slide-transition>
                        <div v-show="expanded.size">
                          <p>
                            <font size="2" color="orange"><b>入力支援機能対象項目</b></font><br>
                            この配信のバイトサイズ（単位Byte）を入力してください。<br>
                            CKAN変数名：resources:size
                          </p>
                          <q-input
                            v-model="detail.size"
                            placeholder="例: 1024"
                            suffix="Byte"
                            hide-underline
                            class="input-item"
                            :error="detail.errorFlgObj.size"
                            :error-message="detail.errorMessageObj.size"
                            type="number"
                          />
                        </div>
                      </q-slide-transition>
                    </div>
                    <div v-if="detail.name === 0 && detail.format === 'csv'">
                      <div class="q-pa-md">
                        <font size="4" color="#1d468f">ファイルのカラム名</font>
                        <p>csvファイル内に存在する時刻に関するカラム名を入力してください。<br>
                          入力した値で「データセットの対象期間」自動入力機能を実行します。<br>
                          なお、このフィールドはデータ1の配信のファイル形式がcsvの場合のみ表示されます。</p>
                        <q-input
                          v-model="detail.columnName"
                          placeholder="例: 開始時刻"
                          hide-underline
                        />
                      </div>
                    </div>
                    <div class="q-pa-md" v-show="hideFlgs.mimeType">
                      <font size="4" color="#1d468f">配信のメディアタイプ</font>
                      <q-btn
                        color="grey"
                        round
                        flat
                        dense
                        :icon="expanded.mimeType ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                        @click="expanded.mimeType = !expanded.mimeType"
                      />
                      <q-slide-transition>
                        <div v-show="expanded.mimeType">
                          <p>
                            <font size="2" color="orange"><b>入力支援機能対象項目</b></font><br>
                            この配信のメディアタイプを選択してください。<br>
                            CKAN変数名：resources:mime_type
                          </p>
                          <q-select
                            v-model="detail.mimetype"
                            class="input-item"
                            :options="store.itemList.mimetype"
                            clearable
                            @clear="detail.mimetype=''"
                            :error="detail.errorFlgObj.mimetype"
                            :error-message="detail.errorMessageObj.mimetype"
                          />
                        </div>
                      </q-slide-transition>
                    </div>
                    <div class="q-pa-md" v-show="hideFlgs.format">
                      <font size="4" color="#1d468f">配信のファイル形式</font>
                      <q-btn
                        color="grey"
                        round
                        flat
                        dense
                        :icon="expanded.format ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                        @click="expanded.format = !expanded.format"
                      />
                      <q-slide-transition>
                        <div v-show="expanded.format">
                          <p>
                            <font size="2" color="orange"><b>入力支援機能対象項目</b></font><br>
                            この配信のファイル形式(拡張子)を入力してください。<br>
                            CKAN変数名：resources:format
                          </p>
                          <q-input
                            v-model="detail.format"
                            placeholder="例：csv"
                            hide-underline
                            :error="detail.errorFlgObj.format"
                            :error-message="detail.errorMessageObj.format"
                          />
                        </div>
                      </q-slide-transition>
                    </div>
                    <div class="q-pa-md" v-show="hideFlgs.compressFormat">
                      <font size="4" color="#1d468f">配信の圧縮形式</font>
                      <q-btn
                        color="grey"
                        round
                        flat
                        dense
                        :icon="expanded.compressFormat ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                        @click="expanded.compressFormat = !expanded.compressFormat"
                      />
                      <q-slide-transition>
                        <div v-show="expanded.compressFormat">
                          <p>この配信が圧縮ファイルの場合、その圧縮形式を選択してください。<br>
                              CKAN変数名：resources:compress_format
                          </p>
                          <q-select
                            filter
                            v-model="detail.compressFormat"
                            class="input-item"
                            :options="store.itemList.compressFormat"
                            clearable
                            @clear="detail.compressFormat=''"
                            :error="detail.errorFlgObj.compressFormat"
                            :error-message="detail.errorMessageObj.compressFormat"
                          />
                          <br>
                          <q-input
                            v-show="detail.freeFieldColumn.compressFormat"
                            label="自由欄"
                            class="free-column"
                            v-model="detail.compressFormatOther"
                            hint=" , (カンマ)は使用できません。"
                            :error="detail.errorFlgObj.compressFormatOther"
                            :error-message="detail.errorMessageObj.compressFormatOther"
                          />
                        </div>
                      </q-slide-transition>
                    </div>
                    <div class="q-pa-md" v-show="hideFlgs.packageFormat">
                      <font size="4" color="#1d468f">配信のパッケージ形式</font>
                      <q-btn
                        color="grey"
                        round
                        flat
                        dense
                        :icon="expanded.packageFormat ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                        @click="expanded.packageFormat = !expanded.packageFormat"
                      />
                      <q-slide-transition>
                        <div v-show="expanded.packageFormat">
                        <p>この配信がパッケージ化されたファイルの場合、そのパッケージ形式を選択してください。<br>
                            CKAN変数名：resources:package_format
                        </p>
                        <q-select
                          filter
                          v-model="detail.packageFormat"
                          class="input-item"
                          :options="store.itemList.packageFormat"
                          clearable
                          @clear="detail.packageFormat=''"
                          :error="detail.errorFlgObj.packageFormat"
                          :error-message="detail.errorMessageObj.packageFormat"
                        />
                        <br>
                        <q-input
                          v-show="detail.freeFieldColumn.packageFormat"
                          label="自由欄"
                          class="free-column"
                          v-model="detail.packageFormatOther"
                          hint=" , (カンマ)は使用できません。"
                          :error="detail.errorFlgObj.packageFormatOther"
                          :error-message="detail.errorMessageObj.packageFormatOther"
                        />
                        </div>
                      </q-slide-transition>
                    </div>
                    <div class="q-pa-md" v-show="hideFlgs.schema">
                      <font size="4" color="#1d468f">スキーマ</font>
                      <q-btn
                        color="grey"
                        round
                        flat
                        dense
                        :icon="expanded.schema ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                        @click="expanded.schema = !expanded.schema"
                      />
                      <q-slide-transition>
                        <div v-show="expanded.schema">
                          <p>この配信が利用しているスキーマ定義のURLを入力してください。<br>
                              CKAN変数名：resources:schema
                          </p>
                          <q-input
                            v-model="detail.schema"
                            placeholder="例: https://schema.org/Restaurant"
                            :error="detail.errorFlgObj.schema"
                            :error-message="detail.errorMessageObj.schema"
                          />
                        </div>
                      </q-slide-transition>
                    </div>
                    <div class="q-pa-md" v-show="hideFlgs.schemaType">
                      <font size="4" color="#1d468f">スキーマタイプ</font>
                      <q-btn
                        color="grey"
                        round
                        flat
                        dense
                        :icon="expanded.schemaType ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                        @click="expanded.schemaType = !expanded.schemaType"
                      />
                      <q-slide-transition>
                        <div v-show="expanded.schemaType">
                          <p>この配信が利用しているスキーマ定義のタイプを選択してください。<br>
                              CKAN変数名：resources:schema_type
                          </p>
                          <q-select
                            filter
                            v-model="detail.schemaType"
                            class="input-item"
                            :options="store.itemList.schemaType"
                            clearable
                            @clear="detail.schemaType=''"
                            :error="detail.errorFlgObj.schemaType"
                            :error-message="detail.errorMessageObj.schemaType"
                          />
                        </div>
                      </q-slide-transition>
                    </div>

                    <div v-if="detail.displayFlgObj.ngsiEntityType" v-show="hideFlgs.ngsiEntityType">
                      <div class="q-pa-md">
                        <font size="4" color="#1d468f">NGSIデータ種別</font>
                        <q-btn
                          color="grey"
                          round
                          flat
                          dense
                          :icon="expanded.ngsiEntityType ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                          @click="expanded.ngsiEntityType = !expanded.ngsiEntityType"
                        />
                        <q-slide-transition>
                          <div v-show="expanded.ngsiEntityType">
                            <p>
                              <font size="2" color="orange"><b>入力支援機能対象項目</b></font><br>
                              この配信のデータ種別を入力してください。<br>
                              CKAN変数名：resources:ngsi_entity_type
                            </p>
                            <q-input
                              v-model="detail.ngsiEntityType"
                              placeholder="例: event"
                            />
                          </div>
                        </q-slide-transition>
                      </div>
                    </div>
                    <div v-if="detail.displayFlgObj.ngsiTenant" v-show="hideFlgs.ngsiTenant">
                      <div class="q-pa-md">
                        <font size="4" color="#1d468f">NGSIテナント</font>
                        <q-btn
                          color="grey"
                          round
                          flat
                          dense
                          :icon="expanded.ngsiTenant ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                          @click="expanded.ngsiTenant = !expanded.ngsiTenant"
                        />
                        <q-slide-transition>
                          <div v-show="expanded.ngsiTenant">
                            <p>
                              <font size="2" color="orange"><b>入力支援機能対象項目</b></font><br>
                              この配信のテナントを入力してください。<br>
                              CKAN変数名：resources:ngsi_tenant
                            </p>
                            <q-input
                              v-model="detail.ngsiTenant"
                              placeholder="例: tenant1"
                            />
                          </div>
                        </q-slide-transition>
                      </div>
                    </div>
                    <div v-if="detail.displayFlgObj.ngsiServicePath" v-show="hideFlgs.ngsiServicePath">
                      <div class="q-pa-md">
                        <font size="4" color="#1d468f">NGSIサービスパス</font>
                        <q-btn
                          color="grey"
                          round
                          flat
                          dense
                          :icon="expanded.ngsiServicePath ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                          @click="expanded.ngsiServicePath = !expanded.ngsiServicePath"
                        />
                        <q-slide-transition>
                          <div v-show="expanded.ngsiServicePath">
                            <p>
                              <font size="2" color="orange"><b>入力支援機能対象項目</b></font><br>
                              この配信のサービスパスを入力してください。<br>
                              CKAN変数名：resources:ngsi_service_path
                            </p>
                            <q-input
                              v-model="detail.ngsiServicePath"
                              placeholder="例: /service1"
                            />
                          </div>
                        </q-slide-transition>
                      </div>
                    </div>
                    <div v-if="detail.displayFlgObj.ngsiDataModel" v-show="hideFlgs.ngsiDataModel">
                      <div class="q-pa-md">
                        <font size="4" color="#1d468f">NGSIデータモデル</font>
                        <q-btn
                          color="grey"
                          round
                          flat
                          dense
                          :icon="expanded.ngsiDataModel ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                          @click="expanded.ngsiDataModel = !expanded.ngsiDataModel"
                        />
                        <q-slide-transition>
                          <div v-show="expanded.ngsiDataModel">
                            <div>この配信のデータモデルを入力してください。<br>
                              配信のダウンロードURLとNGSIデータ種別を入力している場合、
                              <div class="cp_tooltip">取得ボタンを押下することでデータモデルが自動入力
                                <span class="cp_tooltiptext">
                                  <b>【データモデルの取得について】</b><br>
                                    &emsp; 下記に入力した値からデータモデルを取得します。<br>
                                    &emsp; ・配信のダウンロードURL（必須）<br>
                                    &emsp; ・NGSIデータ種別（必須）<br>
                                    &emsp; ・NGSIデータテナント<br>
                                    &emsp; ・NGSIデータサービスパス
                                </span>
                              </div>
                              されます。<br>
                              手動でデータモデルを追加する場合は行追加ボタンを押下してください。<br>
                              テーブルの値を編集する場合は、対象の値を押下することで値を直接入力することが可能です。<br>
                              Metadataボタンを押下すると、該当行のデータモデルのMetadataを確認、編集することが可能です。<br>
                              CKAN変数名：resources:ngsi_data_model
                            </div>
                            <q-table
                              style="max-height: 400px"
                              :rows="detail.ngsiDataModel"
                              :columns="dataModelColumns"
                              row-key="attribute"
                              virtual-scroll
                              v-bind:pagination="pagination"
                              :rows-per-page-options="[0]"
                              :loading="tableLoading"
                              :no-data-label="dataModelErrorMessage"
                            >
                              <template v-slot:top>
                                <div>
                                  <q-btn
                                    color="light-blue-10"
                                    label="行追加"
                                    @click="addDataModel(detail)"
                                  />
                                </div>
                              </template>

                              <template v-slot:body="props">
                                <q-tr :props="props">
                                  <q-td key="attribute" :props="props">
                                    <div class="indent-cell">
                                      {{ props.row.attribute }}
                                    </div>
                                    <q-popup-edit v-model="props.row.attribute">
                                      <q-input v-model="props.row.attribute" :rules="[val => !!val || '入力必須項目']" dense autofocus />
                                    </q-popup-edit>
                                  </q-td>
                                  <q-td key="dataType" :props="props">
                                    <div class="indent-cell">
                                      {{ props.row.dataType }}
                                    </div>
                                    <q-popup-edit v-model="props.row.dataType">
                                      <q-input v-model="props.row.dataType" dense autofocus />
                                    </q-popup-edit>
                                  </q-td>
                                  <q-td key="example" :props="props">
                                    <div class="indent-cell">
                                      {{ props.row.example }}
                                    </div>
                                    <q-popup-edit v-model="props.row.example">
                                      <q-input v-model="props.row.example" dense autofocus />
                                    </q-popup-edit>
                                  </q-td>
                                  <q-td key="description" :props="props">
                                    <div class="indent-cell">
                                      {{ props.row.description }}
                                    </div>
                                    <q-popup-edit v-model="props.row.description">
                                      <q-input v-model="props.row.description" dense autofocus />
                                    </q-popup-edit>
                                  </q-td>
                                  <q-td key="metadata" style="width:5px">
                                    <q-btn color="primary" class="full-width" label="Metadata" field='metadata' @click="showMetadata(props)"></q-btn>
                                  </q-td>
                                  <q-td key="deleteRow" :props="props" style="width:5px">
                                    <q-btn color="red-6" class="full-width" label="行削除" field='deleteRow' @click="deleteDatamModel(props, detail)"></q-btn>
                                  </q-td>
                                </q-tr>
                              </template>

                              <template v-slot:no-data="{ message }">
                                <div v-if="dataModelErrorMessage">
                                  <div class="text-red">
                                    <q-icon size="2em" name="warning" />
                                    {{ dataModelErrorMessage }}
                                  </div>
                                </div>
                                <div v-else>
                                  <q-icon size="2em" name="warning" />
                                  {{ message }}
                                </div>
                              </template>

                            </q-table>
                            <div v-if="detail.errorFlgObj.ngsiDataModel" class="q-pt-lg">
                              <div v-for="message in errorDataModel.message" :key="message">
                                <font color="red">{{ message }}</font>
                              </div>
                            </div>
                            <div class="q-pt-lg">
                              <q-btn
                                color="light-blue-10"
                                label="取得"
                                :disable="inActiveGetDataModelBtn"
                                @click="getNgsiDataModel(detail.downloadUrl, detail.ngsiTenant, detail.ngsiServicePath, detail.ngsiEntityType, detail)"
                              />
                            </div>
                          </div>
                        </q-slide-transition>
                      </div>
                    </div>

                    <div class="q-pa-md">
                      <font size="4" color="#1d468f">契約確認の要否</font>
                      <p>CADDEコネクタがデータセットまたは配信を利用するために契約の確認を要するか否かを選択してください。<br>
                          CKAN変数名：resources:caddec_contract_required
                      </p>
                      <br>
                      <q-select
                        filter
                        class="input-item"
                        v-model="detail.contractRequired"
                        :options="store.itemList.caddecContractRequired"
                        :error="detail.errorFlgObj.contract"
                        :error-message="detail.errorMessageObj.contract"
                      />
                    </div>
                    <div class="q-pa-md">
                      <font size="4" color="#1d468f">コネクタ利用の要否</font>
                      <p>データ利用者が配信を取得するためにコネクタを利用する必要があるか否かを選択してください。<br>
                          CKAN変数名：resources:caddec_required
                      </p>
                      <br>
                      <q-select
                        filter
                        class="input-item"
                        v-model="detail.connectRequired"
                        :options="store.itemList.caddecRequired"
                        :error="detail.errorFlgObj.connect"
                        :error-message="detail.errorMessageObj.connect"
                      />
                    </div>
                    <div class="q-pa-md" v-if="detail.resourceType.value && detail.downloadUrl && detail.inputSupportIsRequestSuccess" v-show="hideFlgs.getResourceIDForProvenance">
                      <font size="4" color="#1d468f">来歴登録の有無</font>
                      <q-btn
                        color="grey"
                        round
                        flat
                        dense
                        :icon="expanded.getResourceIDForProvenance ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                        @click="expanded.getResourceIDForProvenance = !expanded.getResourceIDForProvenance"
                      />
                      <q-slide-transition>
                        <div v-show="expanded.getResourceIDForProvenance">
                          <p>この配信に対して来歴登録を行うか否かを選択してください。<br>
                          この項目はデータセットには登録されません。</p>
                          <q-radio
                            v-model="detail.getResourceIDForProvenance.value"
                            val="yes"
                            label="来歴登録を行う"
                            style="margin-left: 28px"
                            color="light-blue-10"
                          />
                          <q-radio
                            v-model="detail.getResourceIDForProvenance.value"
                            val="no"
                            label="来歴登録を行わない"
                            style="margin-left: 28px"
                            color="light-blue-10"
                          />
                        </div>
                      </q-slide-transition>
                    </div>
                    <!-- <div class="q-pa-md" v-if="detail.resourceType.value" v-show="hideFlgs.caddecResourceIdForProvenance"> -->
                    <!-- <div class="q-pa-md" v-if="detail.getResourceIDForProvenance.value === 'yes' || (store.selectedMode.mode === 'edit' && expanded.caddecResourceIdForProvenance && expanded.caddecResourceIdForProvenance.value !== undfined)" v-show="hideFlgs.caddecResourceIdForProvenance"> -->
                    <!-- 交換実績記録用リソースIDフィールドは常時表示する(テンプレートで非表示の場合を除く) -->
                    <div class="q-pa-md" v-show="hideFlgs.caddecResourceIdForProvenance">
                      <font size="4" color="#1d468f">交換実績記録用リソースID</font>
                      <q-btn
                        color="grey"
                        round
                        flat
                        dense
                        :icon="expanded.caddecResourceIdForProvenance ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                        @click="expanded.caddecResourceIdForProvenance = !expanded.caddecResourceIdForProvenance"
                      />
                      <q-slide-transition>
                        <div v-show="expanded.caddecResourceIdForProvenance">
                          <p>入力不可。編集モードで交換実績記録用リソースIDが設定されている場合、交換実績記録用リソースIDが表示されます。<br>
                              CKAN変数名：resources:caddec_resource_id_for_provenance
                          </p>
                          <div v-if="detail.resourceIDForProvenance">
                            <q-input
                              disable
                              v-model="detail.resourceIDForProvenance"
                            />
                          </div>
                          <div v-else>
                            <q-input
                              disable
                              placeholder="None"
                            />
                          </div>
                        </div>
                      </q-slide-transition>
                    </div>
                    <!-- 来歴登録の有無で「来歴登録を行う」を選択された場合、表示する -->
                    <!-- <div v-if="detail.resourceType.value" v-show="hideFlgs.previousEventId"> -->
                    <div v-if="detail.getResourceIDForProvenance.value === 'yes'" v-show="hideFlgs.previousEventId">
                      <div class="q-pa-md">
                        <font size="4" color="#1d468f">前段イベント識別子</font>
                        <q-btn
                          color="grey"
                          round
                          flat
                          dense
                          :icon="expanded.previousEventId ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                          @click="expanded.previousEventId = !expanded.previousEventId"
                        />
                        <q-slide-transition>
                          <div v-show="expanded.previousEventId">
                            <p>前段イベント識別子を入力してください。<br>
                              前段イベント識別子が不明な場合は、検索ボタンを押下することで前段イベント識別子の候補を取得することができます。<br>
                              表示された候補の中から登録する前段イベント識別子を選択してください。<br>
                              検索ボタン押下前に、来歴登録済みのリソースUR、CADDEユーザIDを入力することで検索結果を絞り込むことも可能です。<br>
                              なお、検索時に使用するリソースURLとCADDEユーザIDは、データセットには登録されません。<br>
                              CKAN変数名：resources:previous_event_id
                            </p>
                            <div class="row q-pb-md">
                              <q-list no-border class="col-12">
                                <q-item style="padding-left: 0;">
                                  <q-item-section class="col-11">
                                    <q-input
                                      v-model="detail.previousEventId"
                                    />
                                  </q-item-section>
                                  <q-item-section  class="col-1" style="max-width: 80px;">
                                    <q-btn
                                      label="検索"
                                      color="light-blue-10"
                                      @click="searchPreviousEventId(detail.urlForProvenance, detail.caddeUserId)"
                                    />
                                  </q-item-section>
                                </q-item>
                              </q-list>
                            </div>
                            <div style="width: 700px;">
                              <span slot:name="label"><font size="3" color="#1d468f">来歴登録済みの配信のダウンロードURL</font></span>
                              <q-input
                                v-model="detail.urlForProvenance"
                              />
                              <br>
                              <span slot:name="label"><font size="3" color="#1d468f">来歴登録済みのCADDEユーザID</font></span>
                              <q-input
                                v-model="detail.caddeUserId"
                              />
                              <br>
                            </div>
                          </div>
                        </q-slide-transition>
                      </div>
                    </div>
                    <div class="q-pa-md" v-show="hideFlgs.dataServiceTitle">
                      <font size="4" color="#1d468f">データサービスのタイトル</font>
                      <q-btn
                        color="grey"
                        round
                        flat
                        dense
                        :icon="expanded.dataServiceTitle ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                        @click="expanded.dataServiceTitle = !expanded.dataServiceTitle"
                      />
                      <q-slide-transition>
                        <div v-show="expanded.dataServiceTitle">
                          <div>この
                             <div class="cp_tooltip">データサービス
                               <span class="cp_tooltiptext">
                                 <b>【データサービス】</b><br>
                                 &emsp; データサービスは、データセットに対し、選択、抽出、組み合わせ、処理、または変換の操作を提供します。<br>
                                 &emsp; 例えば、データ配信サービスにより、データセットやサブセットの配信を選択しダウンロードすることができます。<br>
                                 &emsp; データ発見サービスにより、クライアントは適切なデータセットを見つけることができます。
                               </span>
                             </div>
                             を言い表すタイトルを入力してください。<br>
                             CKAN変数名：resources:data_service_title<br><br>
                          </div>
                          <q-input
                            v-model="detail.dataServiceTitle"
                            :error="detail.errorFlgObj.dataServiceTitle"
                            :error-message="detail.errorMessageObj.dataServiceTitle"
                            hide-underline
                          />
                        </div>
                      </q-slide-transition>
                    </div>
                    <div class="q-pa-md" v-show="hideFlgs.dataServiceEndpointUrl">
                      <font size="4" color="#1d468f">データサービスのエンドポイント</font>
                      <q-btn
                        color="grey"
                        round
                        flat
                        dense
                        :icon="expanded.dataServiceEndpointUrl ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                        @click="expanded.dataServiceEndpointUrl = !expanded.dataServiceEndpointUrl"
                      />
                      <q-slide-transition>
                        <div v-show="expanded.dataServiceEndpointUrl">
                          <p>このデータサービスの主要なエンドポイントとなるURLを入力してください。<br>
                              CKAN変数名：resources:data_service_endpoint_url
                          </p>
                          <q-input
                            v-model="detail.dataServiceEndpointUrl"
                            :error="detail.errorFlgObj.dataServiceEndpointUrl"
                            :error-message="detail.errorMessageObj.dataServiceEndpointUrl"
                            hide-underline
                          />
                        </div>
                      </q-slide-transition>
                    </div>
                    <div class="q-pa-md" v-show="hideFlgs.dataServiceEndpointDescription">
                      <font size="4" color="#1d468f">データサービスのエンドポイントの定義</font>
                      <q-btn
                        color="grey"
                        round
                        flat
                        dense
                        :icon="expanded.dataServiceEndpointDescription ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                        @click="expanded.dataServiceEndpointDescription = !expanded.dataServiceEndpointDescription"
                      />
                      <q-slide-transition>
                        <div v-show="expanded.dataServiceEndpointDescription">
                          <p>このデータサービスのエンドポイントの定義を入力してください。<br>
                              CKAN変数名：resources:data_service_endpoint_description
                          </p>
                          <q-input
                            v-model="detail.dataServiceEndpointDescription"
                            :error="detail.errorFlgObj.dataServiceEndpointDescription"
                            :error-message="detail.errorMessageObj.dataServiceEndpointDescription"
                            hide-underline
                          />
                        </div>
                      </q-slide-transition>
                    </div>
                  </q-item-section>
                </q-item>
              </q-card-section>
            </q-card>
          </div>
        </q-tab-panel>
      </q-tab-panels>
      <div v-for="message in errorCheckMessage" :key="message">
        <font size="3" color="#FF0000">{{message}}</font>
      </div>
    </div>
    <div v-else>
      <div v-for="detail in filedataDetails" :key="detail.name" v-bind="detail">
        <q-card class="q-ma-sm q-card-background-white">
          <q-card-section>
            <div class="q-pa-md">
              <font size="4" color="#1d468f">リソース提供手段の識別子</font>
              <q-btn
                color="grey"
                round
                flat
                dense
                :icon="expanded.caddecResourceType ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                @click="expanded.caddecResourceType = !expanded.caddecResourceType"
              />
              <q-slide-transition>
                <div v-show="expanded.caddecResourceType">
                  <p>この配信のリソース提供手段の識別子を選択してください。<br>
                     CKAN変数名：resources:caddec_resource_type
                  </p>
                  <q-radio
                    v-model="detail.resourceType.value"
                    val="file/http"
                    label="ファイル提供(HTTP)"
                    style="margin-left: 28px"
                    color="light-blue-10"
                  />
                  <q-radio
                    v-model="detail.resourceType.value"
                    val="file/ftp"
                    label="ファイル提供(FTP)"
                    style="margin-left: 16px"
                    color="light-blue-10"
                  />
                  <q-radio
                    v-model="detail.resourceType.value"
                    val="api/ngsi"
                    label="API提供(NGSI API)"
                    style="margin-left: 16px"
                    color="light-blue-10"
                  />
                  <q-btn
                    outline
                    label="クリア"
                    color="primary"
                    style="margin-left: 50px"
                    @click="clearResourceType(detail)"
                  />
                </div>
              </q-slide-transition>
            </div>
            <div>
              <div class="q-pa-md">
                <font size="4" color="#1d468f">配信のダウンロードURL</font>
                <q-btn
                  color="grey"
                  round
                  flat
                  dense
                  :icon="expanded.downloadUrl ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                  @click="expanded.downloadUrl = !expanded.downloadUrl"
                />
                <q-slide-transition>
                  <div v-show="expanded.downloadUrl">
                    <p>
                    この配信を直接ダウンロードできるURLを入力してください。<br>
                    CKAN変数名：resources:url
                    </p>
                    <q-item-section>
                      <q-select
                        v-model="detail.downloadUrl"
                        use-input
                        placeholder="例：http://example.com/download/data.csv"
                        hide-selected
                        fill-input
                        input-debounce="0"
                        :options="autoCorrect.downloadUrl"
                        @filter="(val, update, abort) => { filterFn(detail.downloadUrl, update, abort, 'downloadUrl') }"
                        @input-value="(val) => { setModel(val, detail, 'downloadUrl') }"
                        hide-dropdown-icon
                        counter
                        :error="detail.errorFlgObj.downloadUrl"
                        :error-message="detail.errorMessageObj.downloadUrl"
                      />
                    </q-item-section>
                  </div>
                </q-slide-transition>
              </div>
            </div>
            <div>
              <div class="q-pa-md" v-show="hideFlgs.explainUrl">
                <font size="4" color="#1d468f">配信の情報提供ページURL</font>
                <q-btn
                  color="grey"
                  round
                  flat
                  dense
                  :icon="expanded.explainUrl ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                  @click="expanded.explainUrl = !expanded.explainUrl"
                />
                <q-slide-transition>
                  <div v-show="expanded.explainUrl">
                    <p>
                    この配信に関する情報として、提供されるデータセットの入手方法等が示された説明が記載されたページのURLを入力してください。<br>
                    CKAN変数：resources:explain_url
                    </p>
                    <q-input
                      v-model="detail.explainurl"
                      placeholder="例：http://example.com/explain/data.csv"
                    />
                  </div>
                </q-slide-transition>
              </div>
            </div>
            <div class="q-pa-md" v-show="hideFlgs.filename">
              <font size="4" color="#1d468f">配信の名称</font>
              <q-btn
                color="grey"
                round
                flat
                dense
                :icon="expanded.filename ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                @click="expanded.filename = !expanded.filename"
              />
              <q-slide-transition>
                <div v-show="expanded.filename">
                  <p>この配信をひと言で言い表すタイトルを入力してください。<br>
                     CKAN変数名：resources:name</p>
                  <q-select
                    v-model="detail.filename"
                    placeholder="例: olympic2020_place.csv"
                    use-input
                    hide-selected
                    fill-input
                    input-debounce="0"
                    :options="autoCorrect.filename"
                    @filter="(val, update, abort) => { filterFn(detail.filename, update, abort, 'filename') }"
                    @input-value="(val) => { setModel(val, detail, 'filename') }"
                    hide-dropdown-icon
                    @blur="templateDataService(detail.filename, detail, 'dataServiceTitle')"
                  />
                </div>
              </q-slide-transition>
            </div>
            <div class="q-pa-md" v-show="hideFlgs.description">
              <font size="4" color="#1d468f">配信の説明</font>
              <q-btn
                color="grey"
                round
                flat
                dense
                :icon="expanded.description ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                @click="expanded.description = !expanded.description"
              />
              <q-slide-transition>
                <div v-show="expanded.description">
                  <p>この配信のデータ内容、形式(CSVファイル, API等)などの説明を入力してください。<br>
                     CKAN変数名：resources:description
                  </p>
                  <q-input
                    v-model="detail.description"
                    type="textarea"
                    autogrow
                    placeholder="例: 東京オリンピックの各会場の名称、住所、電話番号、会場の緯度・経度から構成されているデータです。CSV形式のファイルで配信します。"
                  />
                </div>
              </q-slide-transition>
            </div>
            <div class="q-pa-md" v-show="hideFlgs.size">
              <font size="4" color="#1d468f">配信のバイトサイズ</font>
              <q-btn
                color="grey"
                round
                flat
                dense
                :icon="expanded.size ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                @click="expanded.size = !expanded.size"
              />
              <q-slide-transition>
                <div v-show="expanded.size">
                  <p>この配信のバイトサイズ（単位Byte）を入力してください。<br>
                     CKAN変数名：resources:size
                  </p>
                  <q-input
                    v-model="detail.size"
                    placeholder="例: 1024"
                    suffix="Byte"
                    hide-underline
                    class="input-item"
                    :error="detail.errorFlgObj.size"
                    :error-message="detail.errorMessageObj.size"
                    type="number"
                  />
                </div>
              </q-slide-transition>
            </div>
            <div class="q-pa-md" v-show="hideFlgs.mimeType">
              <font size="4" color="#1d468f">配信のメディアタイプ</font>
              <q-btn
                color="grey"
                round
                flat
                dense
                :icon="expanded.mimeType ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                @click="expanded.mimeType = !expanded.mimeType"
              />
              <q-slide-transition>
                <div v-show="expanded.mimeType">
                  <p>この配信のメディア・タイプを選択してください。<br>
                     CKAN変数名：resources:mime_type
                  </p>
                  <q-select
                    v-model="detail.mimetype"
                    class="input-item"
                    :options="store.itemList.mimetype"
                    clearable
                    @clear="detail.mimetype=''"
                  />
                </div>
              </q-slide-transition>
            </div>
            <div class="q-pa-md" v-show="hideFlgs.format">
              <font size="4" color="#1d468f">配信のファイル形式</font>
              <q-btn
                color="grey"
                round
                flat
                dense
                :icon="expanded.format ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                @click="expanded.format = !expanded.format"
              />
              <q-slide-transition>
                <div v-show="expanded.format">
                  <p>この配信のファイル形式(拡張子)を入力してください。<br>
                     CKAN変数名：resources:format
                  </p>
                  <q-input
                    v-model="detail.format"
                    placeholder="例: csv"
                    hide-underline
                  />
                </div>
              </q-slide-transition>
            </div>
            <div class="q-pa-md" v-show="hideFlgs.compressFormat">
              <font size="4" color="#1d468f">配信の圧縮形式</font>
              <q-btn
                color="grey"
                round
                flat
                dense
                :icon="expanded.compressFormat ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                @click="expanded.compressFormat = !expanded.compressFormat"
              />
              <q-slide-transition>
                <div v-show="expanded.compressFormat">
                  <p>この配信が圧縮ファイルの場合、その圧縮形式を選択してください。<br>
                     CKAN変数名：resources:compress_format
                  </p>
                  <q-select
                    filter
                    v-model="detail.compressFormat"
                    class="input-item"
                    :options="store.itemList.compressFormat"
                    clearable
                    @clear="detail.compressFormat=''"
                    :error="detail.errorFlgObj.compressFormat"
                    :error-message="detail.errorMessageObj.compressFormat"
                  />
                  <br>
                  <q-input
                    v-show="detail.freeFieldColumn.compressFormat"
                    label="自由欄"
                    class="free-column"
                    v-model="detail.compressFormatOther"
                    hint=" , (カンマ)は使用できません。"
                    :error="detail.errorFlgObj.compressFormatOther"
                    :error-message="detail.errorMessageObj.compressFormatOther"
                  />
                </div>
              </q-slide-transition>
            </div>
            <div class="q-pa-md" v-show="hideFlgs.packageFormat">
              <font size="4" color="#1d468f">配信のパッケージ形式</font>
              <q-btn
                color="grey"
                round
                flat
                dense
                :icon="expanded.packageFormat ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                @click="expanded.packageFormat = !expanded.packageFormat"
              />
              <q-slide-transition>
                <div v-show="expanded.packageFormat">
                  <p>この配信がパッケージかされたファイルの場合、そのパッケージ形式を選択してください。<br>
                     CKAN変数名：resources:package_format
                  </p>
                  <q-select
                    filter
                    v-model="detail.packageFormat"
                    class="input-item"
                    :options="store.itemList.packageFormat"
                    clearable
                    @clear="detail.packageFormat=''"
                    :error="detail.errorFlgObj.packageFormat"
                    :error-message="detail.errorMessageObj.packageFormat"
                  />
                  <br>
                  <q-input
                    v-show="detail.freeFieldColumn.packageFormat"
                    label="自由欄"
                    class="free-column"
                    v-model="detail.packageFormatOther"
                    hint=" , (カンマ)は使用できません。"
                    :error="detail.errorFlgObj.packageFormatOther"
                    :error-message="detail.errorMessageObj.packageFormatOther"
                  />
                </div>
              </q-slide-transition>
            </div>
            <div class="q-pa-md" v-show="hideFlgs.schema">
              <font size="4" color="#1d468f">スキーマ</font>
              <q-btn
                color="grey"
                round
                flat
                dense
                :icon="expanded.schema ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                @click="expanded.schema = !expanded.schema"
              />
              <q-slide-transition>
                <div v-show="expanded.schema">
                  <p>この配信が利用しているスキーマ定義のURLを入力してください。<br>
                     CKAN変数名：resources:schema
                  </p>
                  <q-input
                    v-model="detail.schema"
                    placeholder="例: https://schema.org/Restaurant"
                  />
                </div>
              </q-slide-transition>
            </div>
            <div class="q-pa-md" v-show="hideFlgs.schemaType">
              <font size="4" color="#1d468f">スキーマタイプ</font>
              <q-btn
                color="grey"
                round
                flat
                dense
                :icon="expanded.schemaType ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                @click="expanded.schemaType = !expanded.schemaType"
              />
              <q-slide-transition>
                <div v-show="expanded.schemaType">
                  <p>この配信が利用しているスキーマ定義のタイプを選択してください。<br>
                     CKAN変数名：resources:schema_type
                  </p>
                  <q-select
                    filter
                    v-model="detail.schemaType"
                    class="input-item"
                    :options="store.itemList.schemaType"
                    clearable
                    @clear="detail.schemaType=''"
                  />
                </div>
              </q-slide-transition>
            </div>
            <div v-if="detail.displayFlgObj.ngsiEntityType" class="q-pa-md" v-show="hideFlgs.ngsiEntityType">
              <font size="4" color="#1d468f">NGSIデータ種別</font>
              <q-btn
                color="grey"
                round
                flat
                dense
                :icon="expanded.ngsiEntityType ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                @click="expanded.ngsiEntityType = !expanded.ngsiEntityType"
              />
              <q-slide-transition>
                <div v-show="expanded.ngsiEntityType">
                  <p>この配信のデータ種別を入力してください。<br>
                     CKAN変数名：resources:ngsi_entity_type
                  </p>
                  <q-input
                    v-model="detail.ngsiEntityType"
                    placeholder="例: event"
                  />
                </div>
              </q-slide-transition>
            </div>
            <div v-if="detail.displayFlgObj.ngsiTenant" class="q-pa-md" v-show="hideFlgs.ngsiTenant">
              <font size="4" color="#1d468f">NGSIテナント</font>
              <q-btn
                color="grey"
                round
                flat
                dense
                :icon="expanded.ngsiTenant ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                @click="expanded.ngsiTenant = !expanded.ngsiTenant"
              />
              <q-slide-transition>
                <div v-show="expanded.ngsiTenant">
                  <p>この配信のテナントを入力してください。<br>
                     CKAN変数名：resources:ngsi_tenant
                  </p>
                  <q-input
                    v-model="detail.ngsiTenant"
                    placeholder="例: tenant1"
                  />
                </div>
              </q-slide-transition>
            </div>
            <div v-if="detail.displayFlgObj.ngsiServicePath" class="q-pa-md" v-show="hideFlgs.ngsiServicePath">
              <font size="4" color="#1d468f">NGSIサービスパス</font>
              <q-btn
                color="grey"
                round
                flat
                dense
                :icon="expanded.ngsiServicePath ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                @click="expanded.ngsiServicePath = !expanded.ngsiServicePath"
              />
              <q-slide-transition>
                <div v-show="expanded.ngsiServicePath">
                  <p>この配信のサービスパスを入力してください。<br>
                     CKAN変数名：resources:ngsi_service_path
                  </p>
                  <q-input
                    v-model="detail.ngsiServicePath"
                    placeholder="例: /service1"
                  />
                </div>
              </q-slide-transition>
            </div>
            <div v-if="detail.displayFlgObj.ngsiDataModel" class="q-pa-md" v-show="hideFlgs.ngsiDataModel">
              <font size="4" color="#1d468f">NGSIデータモデル</font>
              <q-btn
                color="grey"
                round
                flat
                dense
                :icon="expanded.ngsiDataModel ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                @click="expanded.ngsiDataModel = !expanded.ngsiDataModel"
              />
              <q-slide-transition>
                <div v-show="expanded.ngsiDataModel">
                  <div>この配信のデータモデルを入力してください。<br>
                     配信のダウンロードURLとNGSIデータ種別を入力している場合、
                     <div class="cp_tooltip">取得ボタンを押下することでデータモデルが自動入力
                       <span class="cp_tooltiptext">
                         <b>【データモデルの取得について】</b><br>
                           &emsp; 下記に入力した値からデータモデルを取得します。<br>
                           &emsp; ・配信のダウンロードURL（必須）<br>
                           &emsp; ・NGSIデータ種別（必須）<br>
                           &emsp; ・NGSIデータテナント<br>
                           &emsp; ・NGSIデータサービスパス
                       </span>
                     </div>
                     されます。<br>
                     手動でデータモデルを追加する場合は行追加ボタンを押下してください。<br>
                     テーブルの値を編集する場合は、対象の値を押下することで値を直接入力することが可能です。<br>
                     Metadataボタンを押下すると、該当行のデータモデルのMetadataを確認、編集することが可能です。<br>
                     CKAN変数名：resources:ngsi_data_model
                  </div>
                  <q-table
                    style="max-height: 400px"
                    :rows="detail.ngsiDataModel"
                    :columns="dataModelColumns"
                    row-key="attribute"
                    virtual-scroll
                    v-bind:pagination="pagination"
                    :rows-per-page-options="[0]"
                    :loading=tableLoading
                    :no-data-label="dataModelErrorMessage"
                  >
                    <template v-slot:top>
                      <div>
                        <q-btn
                          color="light-blue-10"
                          label="行追加"
                          @click="addDataModel(detail)"
                        />
                      </div>
                    </template>
                    <template v-slot:body="props">
                      <q-tr :props="props">
                        <q-td key="attribute" :props="props">
                          <div class="indent-cell">
                            {{ props.row.attribute }}
                          </div>
                          <q-popup-edit v-model="props.row.attribute">
                            <q-input v-model="props.row.attribute" :rules="[val => !!val || '入力必須項目']" dense autofocus />
                          </q-popup-edit>
                        </q-td>
                        <q-td key="dataType" :props="props">
                          <div class="indent-cell">
                            {{ props.row.dataType }}
                          </div>
                          <q-popup-edit v-model="props.row.dataType">
                            <q-input v-model="props.row.dataType" dense autofocus />
                          </q-popup-edit>
                        </q-td>
                        <q-td key="example" :props="props">
                          <div class="indent-cell">
                            {{ props.row.example }}
                          </div>
                          <q-popup-edit v-model="props.row.example">
                            <q-input v-model="props.row.example" dense autofocus />
                          </q-popup-edit>
                        </q-td>
                        <q-td key="description" :props="props">
                          <div class="indent-cell">
                            {{ props.row.description }}
                          </div>
                          <q-popup-edit v-model="props.row.description">
                            <q-input v-model="props.row.description" dense autofocus />
                          </q-popup-edit>
                        </q-td>
                        <q-td key="metadata" style="width:5px">
                          <q-btn color="primary" class="full-width" label="Metadata" field='metadata' @click="showMetadata(props)"></q-btn>
                        </q-td>
                        <q-td key="deleteRow" :props="props" style="width:5px">
                          <q-btn color="red-6" class="full-width" label="行削除" field='deleteRow' @click="deleteDatamModel(props, detail)"></q-btn>
                        </q-td>
                      </q-tr>
                    </template>
                    <template v-slot:no-data="{ message }">
                      <div v-if="dataModelErrorMessage">
                        <div class="text-red">
                          <q-icon size="2em" name="warning" />
                          {{ dataModelErrorMessage }}
                        </div>
                      </div>
                      <div v-else>
                        <q-icon size="2em" name="warning" />
                        {{ message }}
                      </div>
                    </template>
                  </q-table>
                  <div v-if="detail.errorFlgObj.ngsiDataModel" class="q-pt-lg">
                    <div v-for="message in errorDataModel.message" :key="message">
                      <font color="red">{{ message }}</font>
                    </div>
                  </div>
                  <div class="q-pt-lg">
                    <q-btn
                      color="light-blue-10"
                      label="取得"
                      :disable="inActiveGetDataModelBtn"
                      @click="getNgsiDataModel(detail.downloadUrl, detail.ngsiTenant, detail.ngsiServicePath, detail.ngsiEntityType, detail)"
                    />
                  </div>
                </div>
              </q-slide-transition>
            </div>
            <div class="q-pa-md">
              <font size="4" color="#1d468f">契約確認の要否</font>
              <p>CADDEコネクタがデータセットまたは配信を利用するために契約の確認を要するか否かを選択してください。<br>
                 CKAN変数名：resources:caddec_contract_required
              </p>
              <br>
              <q-select
                filter
                class="input-item"
                v-model="detail.contractRequired"
                :options="store.itemList.caddecContractRequired"
              />
            </div>
            <div class="q-pa-md">
              <font size="4" color="#1d468f">コネクタ利用の要否</font>
              <p>データ利用者が配信を取得するためにコネクタを利用する必要があるか否かを選択してください。<br>
                 CKAN変数名：resources:caddec_required
              </p>
              <br>
              <q-select
                filter
                class="input-item"
                v-model="detail.connectRequired"
                :options="store.itemList.caddecRequired"
              />
            </div>
            <div class="q-pa-md" v-if="detail.resourceType.value" v-show="hideFlgs.getResourceIDForProvenance">
              <font size="4" color="#1d468f">来歴登録の有無</font>
              <q-btn
                color="grey"
                round
                flat
                dense
                :icon="expanded.caddecResourceIdForProvenance ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                @click="expanded.caddecResourceIdForProvenance = !expanded.caddecResourceIdForProvenance"
              />
              <q-slide-transition>
                <div v-show="expanded.caddecResourceIdForProvenance">
                  <p>
                    この配信に対して来歴登録を行うか否かを選択してください。<br>
                    この項目はデータセットには登録されません。
                  </p>
                  <q-radio
                    v-model="detail.getResourceIDForProvenance.value"
                    disable
                    val="yes"
                    label="来歴登録を行う"
                    style="margin-left: 28px"
                    color="light-blue-10"
                  />
                  <q-radio
                    disable
                    v-model="detail.getResourceIDForProvenance.value"
                    val="no"
                    label="来歴登録を行わない"
                    style="margin-left: 28px"
                    color="light-blue-10"
                  />
                </div>
              </q-slide-transition>
            </div>
            <div class="q-pa-md" v-if="detail.resourceType.value" v-show="hideFlgs.caddecResourceIdForProvenance">
              <font size="4" color="#1d468f">交換実績記録用リソースID</font>
              <q-btn
                color="grey"
                round
                flat
                dense
                :icon="expanded.caddecResourceIdForProvenance ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                @click="expanded.caddecResourceIdForProvenance = !expanded.caddecResourceIdForProvenance"
              />
              <q-slide-transition>
                <div v-show="expanded.caddecResourceIdForProvenance">
                  <p>入力不可。編集モードで交換実績記録用リソースIDが設定されている場合、交換実績記録用リソースIDが表示されます。<br>
                     CKAN変数名：resources:caddec_resource_id_for_provenance
                  </p>
                  <div v-if="detail.resourceIDForProvenance">
                    <q-input
                      disable
                      v-model="detail.resourceIDForProvenance"
                    />
                  </div>
                  <div v-else>
                    <q-input
                      disable
                      placeholder="None"
                    />
                  </div>
                </div>
              </q-slide-transition>
            </div>
            <div v-if="detail.resourceType.value" v-show="hideFlgs.previousEventId">
              <div class="q-pa-md">
                <font size="4" color="#1d468f">前段イベント識別子</font>
                <q-btn
                  color="grey"
                  round
                  flat
                  dense
                  :icon="expanded.previousEventId ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                  @click="expanded.previousEventId = !expanded.previousEventId"
                />
                <q-slide-transition>
                  <div v-show="expanded.previousEventId">
                    <p>前段イベント識別子を入力してください。<br>
                       前段イベント識別子が不明な場合はデータ名、データ利用者コネクタIDを入力後、検索ボタンを押し、<br>
                       候補の中から登録する前段イベント識別子を選択してください。<br>
                       なお、データ名とCADDEユーザIDは前段イベント識別子の検索にのみ使用され、データセットには登録されません。<br>
                       CKAN変数名：resources:previous_event_id<br>
                      <span style="color: red;">本項目はテンプレート編集時は入力（選択）できません。</span>
                    </p>                    
                    <div class="row q-pb-md">
                      <q-list no-border class="col-12">
                        <q-item style="padding-left: 0;">
                          <q-item-section class="col-11">
                            <q-input
                              disable
                              v-model="detail.previousEventId"
                            />
                          </q-item-section>
                          <q-item-section  class="col-1" style="max-width: 80px;">
                            <q-btn
                              disable
                              label="検索"
                              color="light-blue-10"
                              @click="searchPreviousEventId(detail.urlForProvenance, detail.caddeUserId)"
                            />
                          </q-item-section>
                        </q-item>
                      </q-list>
                    </div>
                    <div style="width: 700px;">
                      <span slot: name="label"><font size="3" color="#1d468f">来歴登録済みの配信のダウンロードURL</font></span>
                      <q-input
                        v-model="detail.urlForProvenance"
                      />
                      <br>
                      <span slot: name="label"><font size="3" color="#1d468f">来歴登録済みのCADDEユーザID</font></span>
                      <q-input
                        v-model="detail.caddeUserId"
                      />
                      <br>
                    </div>
                  </div>
                </q-slide-transition>
              </div>
            </div>
            <div class="q-pa-md" v-show="hideFlgs.dataServiceTitle">
              <font size="4" color="#1d468f">データサービスのタイトル</font>
              <q-btn
                color="grey"
                round
                flat
                dense
                :icon="expanded.dataServiceTitle ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                @click="expanded.dataServiceTitle = !expanded.dataServiceTitle"
              />
              <q-slide-transition>
                <div v-show="expanded.dataServiceTitle">
                  <p>このデータサービスを言い表すタイトルを入力してください。<br>
                     未設定の場合、配信の名称の値が自動入力されます。<br>
                     CKAN変数名：resources:data_service_title
                  </p>
                  <q-input
                    v-model="detail.dataServiceTitle"
                    :error="detail.errorFlgObj.filename"
                    :error-message="detail.errorMessageObj.filename"
                    hide-underline
                  />
                </div>
              </q-slide-transition>
            </div>
            <div class="q-pa-md" v-show="hideFlgs.dataServiceEndpointUrl">
              <font size="4" color="#1d468f">データサービスのエンドポイント</font>
              <q-btn
                color="grey"
                round
                flat
                dense
                :icon="expanded.dataServiceEndpointUrl ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                @click="expanded.dataServiceEndpointUrl = !expanded.dataServiceEndpointUrl"
              />
              <q-slide-transition>
                <div v-show="expanded.dataServiceEndpointUrl">
                  <p>このデータサービスの主要なエンドポイントとなるURLを入力してください。<br>
                     未設定の場合、配信のダウンロードURLの値が自動入力されます。<br>
                     CKAN変数名：resources:data_service_endpoint_url
                  </p>
                  <q-input
                    v-model="detail.dataServiceEndpointUrl"
                    :error="detail.errorFlgObj.filename"
                    :error-message="detail.errorMessageObj.filename"
                    hide-underline
                  />
                </div>
              </q-slide-transition>
            </div>
            <div class="q-pa-md" v-show="hideFlgs.dataServiceEndpointDescription">
              <font size="4" color="#1d468f">データサービスのエンドポイントの定義</font>
              <q-btn
                color="grey"
                round
                flat
                dense
                :icon="expanded.dataServiceEndpointDescription ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                @click="expanded.dataServiceEndpointDescription = !expanded.dataServiceEndpointDescription"
              />
              <q-slide-transition>
                <div v-show="expanded.dataServiceEndpointDescription">
                  <p>このデータサービスのエンドポイントの定義を入力してください。<br>
                     CKAN変数名：resources:data_service_endpoint_description
                  </p>
                  <q-input
                    v-model="detail.dataServiceEndpointDescription"
                    :error="detail.errorFlgObj.filename"
                    :error-message="detail.errorMessageObj.filename"
                    hide-underline
                  />
                </div>
              </q-slide-transition>
            </div>
          </q-card-section>
        </q-card>
      </div>
      <div v-for="message in errorCheckMessage" :key="message">
        <font size="3" color="#FF0000">{{message}}</font>
      </div>
    </div>

    <!-- 前段イベント識別子検索結果ダイアログ -->
    <q-dialog transition-show="scale" transition-hide="scale" full-width v-model="showPreviousEventIdList">
      <q-card :content-css="{minWidth: '80vw', minHeight: '80vh'}" color="light-blue-1">
        <div style="padding: 50px">
          <div class="q-display-1 q-mb-md"><font color="#1d468f">検索結果一覧</font></div>
          <q-table
            :rows="resultData"
            :columns="columns"
            row-key="timestamp"
            :loading=tableLoading
            @row-click="rowClick"
          >
            <q-tr
              slot:name="body"
              v-slot="props"
              :props="props"
              class="cursor-pointer"
            >
              <q-td v-for="col in props.cols" :key="col.name" :props="props">
                {{ col.value }}
              </q-td>
            </q-tr>
          </q-table>
          <div align="left">
            <font size="3" color="#FF0000">{{previousEventIdErrorMessage}}</font>
          </div>
          <p />
          <div align="right">
            <q-btn
              color="light-blue-10"
              label="閉じる"
              @click="showPreviousEventIdList = false, fieldMessage.previousEventIdError = ''"
            />
          </div>
        </div>
      </q-card>
    </q-dialog>

    <!-- メタデータ入力ダイアログ -->
    <q-dialog transition-show="scale" transition-hide="scale" full-width v-model="showMetadataDialog" persistent>
      <q-card :content-css="{minWidth: '80vw', minHeight: '80vh'}" color="light-blue-1">
        <div style="padding: 50px">
          <div class="q-display-1"><font color="#1d468f">Metadata</font></div>
          <font>属性名：{{ metaAttribute }}</font><br>
          <font>説明：{{ metaDescription }}</font>
          <p />
          <q-table
            style="max-height: 400px"
            :rows="metadataList"
            :columns="metadataColumns"
            row-key="metadataName"
            virtual-scroll
            v-bind:pagination="pagination"
            :rows-per-page-options="[0]"
          >
            <template v-slot:top>
              <q-btn
                color="light-blue-10"
                label="行追加"
                @click="addMetadata(metadataList)"
              />
            </template>

            <template v-slot:body="props">
              <q-tr :props="props">
                <q-td key="metadataName" :props="props">
                  <div class="indent-cell">
                    {{ props.row.metadataName }}
                  </div>
                  <q-popup-edit v-model="props.row.metadataName">
                    <q-input v-model="props.row.metadataName" :rules="[val => !!val || '入力必須項目']" dense autofocus />
                  </q-popup-edit>
                </q-td>
                <q-td key="dataType" :props="props">
                  <div class="indent-cell">
                    {{ props.row.dataType }}
                  </div>
                  <q-popup-edit v-model="props.row.dataType">
                    <q-input v-model="props.row.dataType" dense autofocus />
                  </q-popup-edit>
                </q-td>
                <q-td key="example" :props="props">
                  <div class="indent-cell">
                    {{ props.row.example }}
                  </div>
                  <q-popup-edit v-model="props.row.example">
                    <q-input v-model="props.row.example" dense autofocus />
                  </q-popup-edit>
                </q-td>
                <q-td key="description" :props="props">
                  <div class="indent-cell">
                    {{ props.row.description }}
                  </div>
                  <q-popup-edit v-model="props.row.description">
                    <q-input v-model="props.row.description" dense autofocus />
                  </q-popup-edit>
                </q-td>
                <q-td key="deleteRow" :props="props" style="width:5px">
                  <q-btn color="red-6" class="full-width" label="行削除" field='deleteRow' @click="deleteMetadata(props, metadataList)"></q-btn>
                </q-td>
              </q-tr>
            </template>
          </q-table>
          <p />
          <div v-if="errorMetadata.status" class="q-pt-lg">
            <div v-for="message in errorMetadata.message" :key="message">
              <font color="red">{{ message }}</font>
            </div>
          </div>
          <div align="right">
            <q-btn
              color="light-blue-10"
              label="閉じる"
              @click="showMetadataDialog = errorMetadata.status"
            />
          </div>
        </div>
      </q-card>
    </q-dialog>

  <!-- 完了ダイアログ -->
  <CompleteDialog
    v-bind:dialogInfo="completeDialog"
    @close-dialog="completeDialog.isDisplay = false"
  />

  </div>
</template>

<style lang="scss">
.cp_tooltip{
  position: relative;
  display: inline-block;
  cursor: pointer;
  background: linear-gradient(transparent 90%, #add8e6 60%);
}

.cp_tooltip .cp_tooltiptext{
  position: absolute;
  z-index: 1;
  bottom: 100%;
  left: 0;
  visibility: hidden;
  width: auto;
  white-space: nowrap;
  padding: 0.3em 0.5em;
  transition: opacity 1s;
  text-align: left;
  opacity: 0;
  color: #ffffff;
  border-radius: 6px;
  background-color: #6495ed;
}

.indent-cell{
  max-width: 360px;
  white-space: normal;
  overflow-wrap: break-word;
}

.cp_tooltip{
  position: relative;
  display: inline-block;
  cursor: pointer;
  background: linear-gradient(transparent 90%, #add8e6 60%);
}

.cp_tooltip .cp_tooltiptext{
  position: absolute;
  z-index: 1;
  bottom: 100%;
  left: 0;
  visibility: hidden;
  width: auto;
  white-space: nowrap;
  padding: 0.3em 0.5em;
  transition: opacity 1s;
  text-align: left;
  opacity: 0;
  color: #ffffff;
  border-radius: 6px;
  background-color: #6495ed;
}

.dataset-resource .input-item{
  width: 400px;
}

.free-column{
  width: 800px;
  padding-left:20px;
}

.card-outline{
  border: 1px solid black;
}
</style>
