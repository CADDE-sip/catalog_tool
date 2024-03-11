<script setup>
import { reactive , ref, onMounted, watch, computed } from 'vue'
import { useStore } from 'stores/store'

const store = useStore();

const KEYMAP = {
  theme: 'selectThemes',
  tags: 'selectTags',
  language: 'selectLanguage',
  useApplication: 'useApplication',
  scopeOfDisclosure: 'scopeOfDisclosure',
  permissionResion: 'permissionResion',
  personalData: 'personalData',
  expressWarranty: 'expressWarranty',
  leagalCompliance: 'leagalCompliance'
}

// 横断カタログ編集反映オプション
const editReleaseOption = reactive([
  {
    label: '横断カタログに反映する',
    value: true
  },
  {
    label: '横断カタログに反映しない',
    value: false
  }
])

// 詳細カタログ編集反映オプション
const editDetailOption = reactive([
  {
    label: '詳細カタログに反映する',
    value: true
  },
  {
    label: '詳細カタログに反映しない',
    value: false
  }
])

// テンプレート表示形式オプション
const TEMPLATE_DISPLAY_TYPE_MANDATORY = reactive({
    label: '必須入力表示',
    value: 'mandatory'
})

const TEMPLATE_DISPLAY_TYPE_OPTIONAL = reactive({
    label: '任意入力表示（展開）',
    value: 'optional'
})

const TEMPLATE_DISPLAY_TYPE_FOLD = reactive({
    label: '任意入力表示（折り畳み）',
    value: 'fold'
})

const TEMPLATE_DISPLAY_TYPE_HIDE = reactive({
    label: '非表示（選択した場合、カタログに登録されません）',
    value: 'hide'
})

// 概要情報入力データ
const tableData = ref([])

// 概要情報テーブルカラム
const columns = reactive([
  { name: 'index', align: 'left', label: '#', field: 'index', sortable: true },
  { name: 'filename', align: 'center', label: '配信の名称', field: 'filename', sortable: true },
  { name: 'description', align: 'center', label: '配信の説明', field: 'description' },
  { name: 'resourceType', align: 'center', label: 'リソース提供手段の識別子', field: row => row.resourceType.label },
  { name: 'downloadUrl', align: 'center', label: '配信のダウンロードURL', field: 'downloadUrl' },
  { name: 'explainurl', align: 'center', label: '配信の情報提供ページURL', field: 'explainurl' },
  { name: 'size', align: 'center', label: '配信のバイトサイズ', field: 'size' },
  { name: 'mimetype', align: 'center', label: '配信のメディアタイプ', field: row => row.mimetype.label },
  { name: 'format', align: 'center', label: '配信のファイル形式', field: 'format' },
  { name: 'compressFormat', align: 'center', label: '配信の圧縮形式', field: row => row.compressFormat.label },
  { name: 'packageFormat', align: 'center', label: '配信のパッケージ形式', field: row => row.packageFormat.label },
  { name: 'schema', align: 'center', label: 'スキーマ', field: 'schema' },
  { name: 'schemaType', align: 'center', label: 'スキーマタイプ', field: row => row.schemaType.label },
  { name: 'ngsiEntityType', align: 'center', label: 'NGSIデータ種別', field: 'ngsiEntityType' },
  { name: 'ngsiTenant', align: 'center', label: 'NGSIテナント', field: 'ngsiTenant' },
  { name: 'ngsiServicePath', align: 'center', label: 'NGSIサービスパス', field: 'ngsiServicePath' },
  { name: 'ngsiDataModel', align: 'center', label: 'NGSIデータモデル', field: row => row.ngsiDataModel.length ? 'あり' : 'なし' },
  { name: 'contractRequired', align: 'center', label: '契約確認の要否', field: row => row.contractRequired.label },
  { name: 'connectRequired', align: 'center', label: 'コネクタ利用の要否', field: row => row.connectRequired.label },
  { name: 'getResourceIDForProvenance', align: 'center', label: '来歴登録の有無', field: row => row.getResourceIDForProvenance.label },
  { name: 'resourceIDForProvenance', align: 'center', label: '交換実績記録用リソースID', field: 'resourceIDForProvenance' },
  { name: 'previousEventId', align: 'center', label: '前段イベント識別子', field: 'previousEventId' },
  { name: 'dataServiceTitle', align: 'center', label: 'データサービスのタイトル', field: 'dataServiceTitle' },
  { name: 'dataServiceEndpointUrl', align: 'center', label: 'データサービスのエンドポイント', field: 'dataServiceEndpointUrl' },
  { name: 'dataServiceEndpointDescription', align: 'center', label: 'データサービスのエンドポイントの定義', field: 'dataServiceEndpointDescription' }
])

// 概要情報テーブルカラムの表示カラム一覧
const datajacketVisibleColumns = computed(() => {
  var visibleColumns = []

  visibleColumns.push('index')
  if (store.itemDisplayFlg['filename'] !== 'hide') visibleColumns.push('filename')
  if (store.itemDisplayFlg['description'] !== 'hide') visibleColumns.push('description')
  visibleColumns.push('resourceType')
  visibleColumns.push('downloadUrl')
  if (store.itemDisplayFlg['explainUrl'] !== 'hide') visibleColumns.push('explainurl')
  if (store.itemDisplayFlg['size'] !== 'hide') visibleColumns.push('size')
  if (store.itemDisplayFlg['mimeType'] !== 'hide') visibleColumns.push('mimetype')
  if (store.itemDisplayFlg['format'] !== 'hide') visibleColumns.push('format')
  if (store.itemDisplayFlg['compressFormat'] !== 'hide') visibleColumns.push('compressFormat')
  if (store.itemDisplayFlg['packageFormat'] !== 'hide') visibleColumns.push('packageFormat')
  if (store.itemDisplayFlg['schema'] !== 'hide') visibleColumns.push('schema')
  if (store.itemDisplayFlg['schemaType'] !== 'hide') visibleColumns.push('schemaType')
  if (store.itemDisplayFlg['ngsiEntityType'] !== 'hide') visibleColumns.push('ngsiEntityType')
  if (store.itemDisplayFlg['ngsiTenant'] !== 'hide') visibleColumns.push('ngsiTenant')
  if (store.itemDisplayFlg['ngsiServicePath'] !== 'hide') visibleColumns.push('ngsiServicePath')
  if (store.itemDisplayFlg['ngsiDataModel'] !== 'hide') visibleColumns.push('ngsiDataModel')
  visibleColumns.push('contractRequired')
  visibleColumns.push('connectRequired')
  if (store.itemDisplayFlg['getResourceIDForProvenance'] !== 'hide') visibleColumns.push('getResourceIDForProvenance')
  if (store.itemDisplayFlg['caddecResourceIdForProvenance'] !== 'hide') visibleColumns.push('resourceIDForProvenance')
  if (store.itemDisplayFlg['previousEventId'] !== 'hide') visibleColumns.push('previousEventId')
  if (store.itemDisplayFlg['dataServiceTitle'] !== 'hide') visibleColumns.push('dataServiceTitle')
  if (store.itemDisplayFlg['dataServiceEndpointUrl'] !== 'hide') visibleColumns.push('dataServiceEndpointUrl')
  if (store.itemDisplayFlg['dataServiceEndpointDescription'] !== 'hide') visibleColumns.push('dataServiceEndpointDescription')

  return visibleColumns
});

// データモデル入力データ
const dataModelList = ref([])

// データモデルテーブルカラム
const dataModelColumns = reactive([
  { name: 'attribute', label: '属性名', field: 'attribute', align: 'center' },
  { name: 'dataType', label: 'データ型', field: 'dataType', align: 'center' },
  { name: 'example', label: '参考値', field: 'example', align: 'center' },
  { name: 'description', label: '説明', field: 'description', align: 'center' },
  { name: 'metadata', label: 'メタデータ', field: row => row.metadata.length ? 'あり' : 'なし', align: 'center' }
])

// メタデータ入力データ
const metadataList = ref([])
const metaAttribute = ref('')
const metaDescription = ref('')

// メタデータテーブルダイアログ表示非表示フラグ
const showMetadataDialog = ref(false)

// メタデータテーブルカラム
const metadataColumns = reactive([
  { name: 'metadataName', label: 'メタデータ名', field: 'metadataName', align: 'center' },
  { name: 'dataType', label: 'データ型', field: 'dataType', align: 'center' },
  { name: 'example', label: '参考値', field: 'example', align: 'center' },
  { name: 'description', label: '説明', field: 'description', align: 'center' }
])

// 「データの有効期間」の表示フィールド
const displayFieldDataEffectivePeriod = ref('')

// 「利用ライセンスの期限」の表示フィールド
const displayFieldUsageLicensePeriod = ref('')

// 赤字表示フラグ
const redCharFlg = reactive({
  theme: false,
  tags: false,
  language: false,
  useApplication: false,
  scopeOfDisclosure: false,
  permissionResion: false,
  personalData: '',
  expressWarranty: '',
  leagalCompliance: false
})

// 確認画面での表示値
const displayValue = reactive({
  compressFormat: '',
  packageFormat: '',
  theme: '',
  tags: '',
  language: '',
  useApplication: '',
  scopeOfDisclosure: '',
  permissionResion: '',
  personalData: '',
  period: '',
  expressWarranty: '',
  leagalCompliance: ''
})

// フィールドの表示形式
const displayType = reactive({
  url: {},
  caddecDatasetIdForDetail: {},
  publisherName: {},
  publisherUri: {},
  creatorName: {},
  creatorUrl: {},
  contactName: {},
  contactUrl: {},
  filename: {},
  description: {},
  downloadUrl: {},
  explainUrl: {},
  size: {},
  mimeType: {},
  format: {},
  compressFormat: {},
  packageFormat: {},
  schema: {},
  schemaType: {},
  ngsiEntityType: {},
  ngsiTenant: {},
  ngsiServicePath: {},
  ngsiDataModel: {},
  getResourceIDForProvenance: {},
  dataServiceTitle: {},
  dataServiceEndpointUrl: {},
  dataServiceEndpointDescription: {},
  theme: {},
  tags: {},
  vocabulary: {},
  term: {},
  language: {},
  frequency: {},
  spatial: {},
  temporal: {},
  licenseTitle: {},
  licenseUrl: {},
  rights: {},
  accessRights: {},
  accessRightsUrl: {},
  haspolicyUrl: {},
  provWasGeneratedByUrl: {},
  conformsTo: {},
  tradingPolicyContractType: {},
  tradingPolicyNda: {},
  tradingPolicyUseApplication: {},
  scopeOfDisclosure: {},
  termsOfUsePermissibleRegion: {},
  termsOfUseNotices: {},
  privacyPolicyContainsPersonalData: {},
  dataEffectivePeriod: {},
  usageLicensePeriod: {},
  fee: {},
  salesInfoUrl: {},
  pricingPriceRange: {},
  pricingNoticesOfPrice: {},
  warrantyExpressWarranty: {},
  warrantyLegalCompliance: {}
})

// 必須以外選択できない項目に使用
const mandatoryItem = ref('必須入力表示')

// 編集反映フラグ
const editFlg = reactive({
  title: '',
  notes: '',
  url: '',
  registOrg: '',
  caddecProviderId: '',
  publisherName: '',
  publisherUri: '',
  creatorName: '',
  creatorUrl: '',
  contactName: '',
  contactUrl: '',
  resources: '',
  theme: '',
  tags: '',
  vocabulary: '',
  term: '',
  language: '',
  frequency: '',
  spatial: '',
  temporal: '',
  license: '',
  rights: '',
  accessRights: '',
  haspolicyUrl: '',
  provWasGeneratedByUrl: '',
  conformsTo: '',
  tradingPolicyContractType: '',
  tradingPolicyNda: '',
  tradingPolicyUseApplication: '',
  scopeOfDisclosure: '',
  termsOfUsePermissibleRegion: '',
  termsOfUseNotices: '',
  privacyPolicyContainsPersonalData: '',
  dataEffectivePeriod: '',
  usageLicensePeriod: '',
  fee: '',
  salesInfoUrl: '',
  pricingPriceRange: '',
  pricingNoticesOfPrice: '',
  warrantyExpressWarranty: '',
  warrantyLegalCompliance: ''
})

// created
setDisplayValueFiledataDetails()
createTableData()
createDataModelTableData()
defaultEditCopy()
setTemplateDisplayDefault()
setDisplayValue()
setDisplayValuePeriod()
checkRedCharacter()
checkDisplayFieldDataEffectivePeriod()
checkDisplayFieldUsageLicensePeriod()

// mounted
onMounted(function(){
  console.log('-- DatasetConfirm.vue onMounted --')
  console.log(store.selectedMode.mode)
  topScroll()
})

// データセット・配信のライセンスの表示設定切り替え
watch(() => displayType.licenseTitle,
  (newReg, oldReg) => {
    displayType.licenseUrl = newReg
})

// データセット・配信のアクセス権の表示設定切り替え
watch(() => displayType.accessRights,
  (newReg, oldReg) => {
    displayType.accessRightsUrl = newReg
})

// 有償無償
watch(() => displayType.fee,
  (newReg, oldReg) => {
    // 有償無償を非表示した場合、「データ販売に関わる特記事項・価格帯・販売情報」も非表示とする
    if(newReg.value === 'hide'){
      displayType.salesInfoUrl = newReg
      displayType.pricingPriceRange = newReg
      displayType.pricingNoticesOfPrice = newReg
    }
})


// 確認画面のプルダウン（テンプレート表示）の初期値を設定
function setTemplateDisplayDefault() {
  if (store.selectedMode.mode !== 'template') {
    return
  }
  for (var field in displayType) {
    for (var storeLabel in store.itemDisplayFlg) {
      if (field !== storeLabel) {
        continue
      }
      if (store.itemDisplayFlg[storeLabel]) {
        if (store.itemDisplayFlg[storeLabel] === 'mandatory') {
          // displayType[field] = { label: '必須', value: 'mandatory' }
          displayType[field] = TEMPLATE_DISPLAY_TYPE_MANDATORY
        } else if (store.itemDisplayFlg[storeLabel] === 'fold') {
          // displayType[field] = { label: '折り畳み', value: 'fold' }
          displayType[field] = TEMPLATE_DISPLAY_TYPE_FOLD
        } else if (store.itemDisplayFlg[storeLabel] === 'hide') {
          // displayType[field] = { label: '非表示', value: 'hide' }
          displayType[field] = TEMPLATE_DISPLAY_TYPE_HIDE
        }else {
          // displayType[field] = { label: 'オプション', value: 'optional' }
          displayType[field] = TEMPLATE_DISPLAY_TYPE_OPTIONAL
        }
      } else {
        // displayType[field] = { label: 'オプション', value: 'optional' }
        displayType[field] = TEMPLATE_DISPLAY_TYPE_OPTIONAL
      }
    }
  }
}

// カタログ編集の反映有無フラグのデフォルト値設定
function defaultEditCopy() {
  if (!store.selectedMode.isBothCatalog) return
  if (store.selectedMode.mode === 'edit') {
    if (store.selectedMode.ckanType === 'release') {
      var defaultEditOption = { label: '詳細カタログに反映しない', value: false }
    } else {
      defaultEditOption = { label: '横断カタログに反映しない', value: false }
    }
    for (var col in editFlg) {
      editFlg[col] = defaultEditOption
    }
  }
}

// 画面最上部移動
function topScroll() {
  window.scrollTo(0, 0)
}

// 確認画面での表示値設定
function setDisplayValue() {
  for (var field in displayValue) {
    for (var key in KEYMAP) {
      if (field !== key) {
        continue
      }
      var param = KEYMAP[key]
      var tmpList = []
      var otherField = ''
      var i = 0
      switch (field) {
        case 'theme':
        case 'tags':
          if (store[param].length) {
            displayValue[field] = store[param].join(', ')
          }
          break
        case 'language':
          for (i = 0; i < store[param].length; i++) {
            if (store[param][i].label) {
              tmpList.push(store[param][i].label)
            }
          }
          displayValue[field] = tmpList.join(', ')
          break
        case 'scopeOfDisclosure':
        case 'personalData':
        case 'expressWarranty':
          otherField = String(param) + 'Other'
          if (store[otherField]) {
            displayValue[field] = '自由欄：' + store[otherField]
          } else {
            if (store[param].label) {
              displayValue[field] = store[param].label
            }
          }
          break
        case 'useApplication':
        case 'permissionResion':
        case 'leagalCompliance':
          otherField = String(param) + 'Other'
          for (i = 0; i < store[param].length; i++) {
            if (store[param][i].label) {
              if (store[param][i].label === 'その他' && store[otherField]) {
                tmpList.push('自由欄：' + store[otherField])
                continue
              }
              if (store[param][i].value) {
                tmpList.push(store[param][i].label)
              }
            }
          }
          displayValue[field] = tmpList.join(', ')
          break
      }
    }
  }
}

// 概要情報の確認画面での表示値設定
function setDisplayValueFiledataDetails() {
  console.log('setDisplayValueFiledataDetails')
  for (var i = 0; i < store.filedataDetails.length; i++) {
    for (var fieldName in store.filedataDetails[i]) {
      if (fieldName !== 'compressFormat' && fieldName !== 'packageFormat') {
        continue
      }
      var otherFieldName = fieldName + 'Other'
      var displayValue = fieldName + 'DisplayValue'
      if (store.filedataDetails[i][otherFieldName]) {
        store.filedataDetails[i][displayValue] = '自由欄：' + store.filedataDetails[i][otherFieldName]
      } else {
        store.filedataDetails[i][displayValue] = store.filedataDetails[i][fieldName].label || ''
      }
    }
  }
}

// 「利用ライセンスの期限」の確認画面での表示値設定（※期間を選択）
function setDisplayValuePeriod() {
  displayValue.period = ''
  // 期間が未選択
  if (store.usageLicensePeriod.selectTerms.value !== 'value') return
  // 期間(整数)と期間(単位)が未入力
  if (!store.usageLicensePeriod.period && !store.usageLicensePeriod.unit) return
  displayValue.period = store.usageLicensePeriod.period + store.usageLicensePeriod.unit.label
}

// 赤字対象のモード判定
function checkRedCharacterMode(currentMode) {
  // 登録値更新時に確認画面で赤字表示をするモード
  const MODE_FOR_RED_CHARACTER = [
    'edit',
    'release_duplicate',
    'detail_duplicate',
    'both_duplicate',
    'release-link-detail_duplicate',
    'detail-link-release_duplicate'
  ]
  for (var mode of MODE_FOR_RED_CHARACTER) {
    if (currentMode === mode) {
      return true
    }
  }
  return false
}

// 赤字表示判定
function checkRedCharacter() {
  for (var field in redCharFlg) {
    if (!checkRedCharacterMode(store.selectedMode.mode)) {
      // カタログ複製または編集時以外は黒字表示
      redCharFlg[field] = false
      continue
    }
    for (var key in KEYMAP) {
      if (field !== key) {
        continue
      }
      var param = KEYMAP[key]
      switch (field) {
        case 'theme':
        case 'tags':
          redCharFlg[field] = checkEditArrayValue(param)
          break
        case 'language':
          redCharFlg[field] = checkEditLanguageValue(param)
          break
        case 'scopeOfDisclosure':
        case 'personalData':
        case 'expressWarranty':
          redCharFlg[field] = checkEditValueWithOther(param)
          break
        case 'useApplication':
        case 'permissionResion':
        case 'leagalCompliance':
          redCharFlg[field] = checkEditArrayValueWithOther(param)
          break
      }
    }
  }
}

// 配列フィールドの編集有無判定
function checkEditArrayValue(param) {
  var i = 0
  var j = 0
  if (store[param].length !== store.hold[param].length) {
    return true
  }
  for (i = 0; i < store[param].length; i++) {
    var match = false
    for (j = 0; j < store.hold[param].length; j++) {
      if (store[param][i] !== store.hold[param][j]) {
        continue
      }
      match = true
      break
    }
    if (!match) {
      return true
    }
  }
  return false
}

// 「情報を記述する言語」の編集有無判定
function checkEditLanguageValue(param) {
  if (store[param].length !== store.hold[param].length) {
    // 選択値の数が異なる
    return true
  }
  for (var i = 0; i < store.selectLanguage.length; i++) {
    var match = false
    for (var j = 0; j < store.hold[param].length; j++) {
      if (store[param][i].label !== store.hold[param][j].label) {
        continue
      }
      match = true
      break
    }
    if (!match) {
      // holdの中にstateと一致する要素がなかった
      return true
    }
  }
  return false
}

// 自由記述ありフィールドの編集有無判定
function checkEditValueWithOther(param) {
  var otherField = String(param) + 'Other'
  if (store[param].label !== store.hold[param].label) {
    // 選択値が異なる
    return true
  }
  if (store[otherField] !== store.hold[otherField]) {
    // 自由欄の記述内容が異なる
    return true
  }
  return false
}

// 自由記述あり配列フィールドの編集有無判定
function checkEditArrayValueWithOther(param) {
  var otherField = String(param) + 'Other'
  if (store[param].length !== store.hold[param].length) {
    return true
  }
  for (var i = 0; i < store[param].length; i++) {
    var match = false
    for (var j = 0; j < store.hold[param].length; j++) {
      if (store[param][i].label !== store.hold[param][j].label) {
        continue
      }
      if (store[param][i].value !== store.hold[param][j].value) {
        continue
      }
      match = true
      break
    }
    if (!match) {
      // holdの中にstateと一致する要素がなかった
      return true
    }
  }
  if (store[otherField] !== store.hold[otherField]) {
    // 自由欄の記述内容が異なる
    return true
  }
  return false
}

// 「データの有効期間」表示・非表示の制御
function checkDisplayFieldDataEffectivePeriod() {
  displayFieldDataEffectivePeriod.value = 'none'
  if (store.dataEffectivePeriod.selectTerms.value === 'date') {
    displayFieldDataEffectivePeriod.value = 'date'
  }
  if (store.dataEffectivePeriod.selectTerms.value === 'note') {
    displayFieldDataEffectivePeriod.value = 'freefield'
  }
}

// 「利用ライセンスの期限」表示・非表示の制御
function checkDisplayFieldUsageLicensePeriod() {
  displayFieldUsageLicensePeriod.value = 'none'
  if (store.usageLicensePeriod.selectTerms.value === 'endDate') {
    displayFieldUsageLicensePeriod.value = 'deadline'
  }
  if (store.usageLicensePeriod.selectTerms.value === 'value') {
    displayFieldUsageLicensePeriod.value = 'period'
  }
  if (store.usageLicensePeriod.selectTerms.value === 'note') {
    displayFieldUsageLicensePeriod.value = 'freefield'
  }
}

// データ概要情報：データ情報のテーブルに表示するデータを作成
function createTableData() {
  tableData.value = []
  for (var i = 0; i < store.filedataDetails.length; i++) {
    var dataObj = {}
    dataObj.index = i + 1
    var filedataDetails = store.filedataDetails[i]

    for (const key in filedataDetails) {
      dataObj[key] = filedataDetails[key]
    }

    // 複製または編集時の赤字表示設定
    // if (store.selectedMode.mode !== 'new_release_register' && store.selectedMode.mode !== 'new_detail_register' && store.selectedMode.mode !== 'new_both_register' && store.selectedMode.mode !== 'template') {
    if (checkRedCharacterMode(store.selectedMode.mode)) {
      if (store.filedataDetails.length !== store.hold.filedataDetails.length) {
        for (const key in filedataDetails) {
          dataObj['pre' + key] = ''
        }
      } else {
        var prefiledataDetails = store.hold.filedataDetails[i]
        for (const key in filedataDetails) {
          if (prefiledataDetails[key]) {
            dataObj['pre' + key] = prefiledataDetails[key]
          } else {
            dataObj['pre' + key] = ''
          }
        }
      }
    } else {
      for (const key in filedataDetails) {
        dataObj['pre' + key] = filedataDetails[key]
      }
    }
    tableData.value.push(dataObj)
  }
}

// データ概要情報：データモデルテーブルに表示するデータを作成
function createDataModelTableData() {
  var i = 0
  dataModelList.value = []
  for (i = 0; i < store.filedataDetails.length; i++) {
    if (!store.filedataDetails[i].ngsiDataModel.length) {
      continue
    }
    var dataModel = {
      index: '',
      ngsiDataModel: []
    }
    dataModel.index = '#' + String(i + 1)
    dataModel.ngsiDataModel = store.filedataDetails[i].ngsiDataModel
    dataModelList.value.push(dataModel)
  }
}

// データセット情報の登録データ生成
function createDataDatasetInfoForRegister(storeType) {
  var dataCreatorInfomation = [
    {
      label: 'caddec_dataset_id_for_detail',
      value: storeType.datasetIdForDetail
    },
    {
      label: 'caddec_provider_id',
      value: storeType.publisherId.value
    },
    {
      label: 'publisher_name',
      value: storeType.publisher
    },
    {
      label: 'publisher_uri',
      value: storeType.publisherUri
    },
    {
      label: 'creator_name',
      value: storeType.creator
    },
    {
      label: 'creator_url',
      value: storeType.creatorUrl
    },
    {
      label: 'contact_name',
      value: storeType.contactPoint
    },
    {
      label: 'contact_url',
      value: storeType.contactPointUrl
    }
  ]
  return dataCreatorInfomation
}

// データセット情報の編集データ生成
function createDataDatasetInfoForEdit() {
  var dataCreatorInfomation = [
    {
      label: 'caddec_dataset_id_for_detail',
      value: store.another.datasetIdForDetail
    },
    {
      label: 'caddec_provider_id',
      value: editFlg.caddecProviderId.value ? store.publisherId.value : store.another.publisherId.value
    },
    {
      label: 'publisher_name',
      value: editFlg.publisherName.value ? store.publisher : store.another.publisher
    },
    {
      label: 'publisher_uri',
      value: editFlg.publisherUri.value ? store.publisherUri : store.another.publisherUri
    },
    {
      label: 'creator_name',
      value: editFlg.creatorName.value ? store.creator : store.another.creator
    },
    {
      label: 'creator_url',
      value: editFlg.creatorUrl.value ? store.creatorUrl : store.another.creatorUrl
    },
    {
      label: 'contact_name',
      value: editFlg.contactName.value ? store.contactPoint : store.another.contactPoint
    },
    {
      label: 'contact_url',
      value: editFlg.contactUrl.value ? store.contactPointUrl : store.another.contactPointUrl
    }
  ]
  return dataCreatorInfomation
}

// 「データセットの情報を記述する言語」のCKANへの登録値(value)取得
function getLanguageValue(storeType) {
  var langValueList = []
  for (var selCnt = 0; selCnt < storeType.selectLanguage.length; selCnt++) {
    if (storeType.selectLanguage[selCnt].value) {
      langValueList.push(storeType.selectLanguage[selCnt].value)
    }
  }
  return langValueList
}

// データ概要情報：メタデータテーブルに表示するデータを作成
function createMetadataTable(dataModel) {
  showMetadataDialog.value = true
  metaAttribute.value = dataModel.attribute
  metaDescription.value = dataModel.description
  metadataList.value = dataModel.metadata
}

// 利用条件で設定した配信情報を概要情報に設定
function copyUsertermsDataToDatajacket(storeType, selectedMode) {
  for (var i = 0; i < storeType.filedataDetails.length; i++) {
    if (selectedMode === 'edit') {
      if (editFlg.license) {
        storeType.filedataDetails[i].licensetitle = store.termName.label || ''
        storeType.filedataDetails[i].licenseurl = store.termNameUrl
      } else {
        storeType.filedataDetails[i].licensetitle = store.another.termName.label || ''
        storeType.filedataDetails[i].licenseurl = store.another.termNameUrl
      }
      storeType.filedataDetails[i].usrRight = editFlg.rights.value ? store.usrRight : store.another.usrRight
      if (editFlg.accessRights) {
        storeType.filedataDetails[i].accessRights = store.accessRights.label || ''
        storeType.filedataDetails[i].accessRightsUrl = store.accessRightsUrl
      } else {
        storeType.filedataDetails[i].accessRights = store.another.accessRights.label || ''
        storeType.filedataDetails[i].accessRightsUrl = store.another.accessRightsUrl
      }
      storeType.filedataDetails[i].haspolicyUrl = editFlg.haspolicyUrl.value ? store.haspolicyUrl : store.another.haspolicyUrl
      storeType.filedataDetails[i].conformsTo = editFlg.conformsTo.value ? store.conformsTo : store.another.conformsTo
    } else {
      storeType.filedataDetails[i].licensetitle = storeType.termName.label || ''
      storeType.filedataDetails[i].licenseurl = storeType.termNameUrl
      storeType.filedataDetails[i].usrRight = storeType.usrRight
      storeType.filedataDetails[i].accessRights = storeType.accessRights.label || ''
      storeType.filedataDetails[i].accessRightsUrl = storeType.accessRightsUrl
      storeType.filedataDetails[i].haspolicyUrl = storeType.haspolicyUrl
      storeType.filedataDetails[i].conformsTo = storeType.conformsTo
    }
  }
}

// 概要情報の登録データ生成
function createDatajacketForCkan(storeType, selectedMode) {
  copyUsertermsDataToDatajacket(storeType, selectedMode)
  for (var i = 0; i < storeType.filedataDetails.length; i++) {
    for (var field in storeType.filedataDetails[i]) {
      if (field !== 'compressFormat' && field !== 'packageFormat') {
        continue
      }
      // 自由記述フィールドをCKAN登録用に整形
      var otherFieldName = field + 'Other'
      if (!storeType.filedataDetails[i][otherFieldName]) {
        continue
      }
      storeType.filedataDetails[i][field].value = 'その他(' + storeType.filedataDetails[i][otherFieldName] + ')'
    }
  }
  return storeType.filedataDetails
}

// データセット情報(任意)の登録データ生成
function createDatasetoptionalForRegister(storeType) {
  var datasetoptional = [
    {
      label: 'vocabulary',
      value: storeType.vocabulary
    },
    {
      label: 'term',
      value: storeType.term
    },
    {
      label: 'language',
      value: getLanguageValue(storeType)
    },
    {
      label: 'frequency',
      value: storeType.frequency.value
    },
    {
      label: 'spatial_url',
      value: storeType.geonames.spatialUrl
    },
    {
      label: 'spatial_text',
      value: storeType.geonames.spatialName
    },
    {
      label: 'spatial',
      value: storeType.geonames.spatial
    },
    {
      label: 'temporal_start',
      value: storeType.dataCalender.start
    },
    {
      label: 'temporal_end',
      value: storeType.dataCalender.end
    }
  ]
  return datasetoptional
}

// データセット情報(任意)の編集データ生成
function createDatasetoptionalForEdit() {
  var datasetoptional = [
    {
      label: 'vocabulary',
      value: editFlg.vocabulary.value ? store.vocabulary : store.another.vocabulary
    },
    {
      label: 'term',
      value: editFlg.term.value ? store.term : store.another.term
    },
    {
      label: 'language',
      value: editFlg.language.value ? getLanguageValue(store) : getLanguageValue(store.another)
    },
    {
      label: 'frequency',
      value: editFlg.frequency.value ? store.frequency.value : store.another.frequency.value
    },
    {
      label: 'spatial_url',
      value: editFlg.spatial.value ? store.geonames.spatialUrl : store.another.geonames.spatialUrl
    },
    {
      label: 'spatial_text',
      value: editFlg.spatial.value ? store.geonames.spatialName : store.another.geonames.spatialName
    },
    {
      label: 'spatial',
      value: editFlg.spatial.value ? store.geonames.spatial : store.another.geonames.spatial
    },
    {
      label: 'temporal_start',
      value: editFlg.temporal.value ? store.dataCalender.start : store.another.dataCalender.start
    },
    {
      label: 'temporal_end',
      value: editFlg.temporal.value ? store.dataCalender.end : store.another.dataCalender.end
    }
  ]
  return datasetoptional
}

// 自由記述ありフィールドのCKAN登録値取得
function ckanValueWithOther(storeType, field) {
  var registerValue = ''
  var othreField = String(field) + 'Other'
  if (storeType[othreField]) {
    registerValue = 'その他(' + storeType[othreField] + ')'
  } else {
    if (storeType[field].value) {
      registerValue = storeType[field].value
    }
  }
  return registerValue
}

// 自由記述あり配列フィールドのCKAN登録値取得
function ckanValueArrayWithOther(storeType, field) {
  var valueList = []
  var othreField = String(field) + 'Other'
  for (var selCnt = 0; selCnt < storeType[field].length; selCnt++) {
    if (storeType[field][selCnt].label) {
      if (storeType[field][selCnt].label === 'その他' && storeType[othreField]) {
        valueList.push('その他(' + storeType[othreField] + ')')
        continue
      }
      valueList.push(storeType[field][selCnt].value)
    }
  }
  return valueList
}

// 利用条件の登録データ生成
function createUserTermsForRegister(storeType) {
  var userTerms = [
    {
      label: 'rights',
      value: storeType.usrRight
    },
    {
      label: 'access_rights',
      value: storeType.accessRights.label
    },
    {
      label: 'access_rights_url',
      value: storeType.accessRightsUrl
    },
    {
      label: 'haspolicy_url',
      value: storeType.haspolicyUrl
    },
    {
      label: 'prov_was_generated_by_url',
      value: storeType.provWasGeneratedByUrl
    },
    {
      label: 'conforms_to',
      value: storeType.conformsTo
    },
    {
      label: 'trading_policy_contract_type',
      value: storeType.contractType.value
    },
    {
      label: 'trading_policy_nda',
      value: storeType.secrecy.value
    },
    {
      label: 'trading_policy_use_application',
      value: ckanValueArrayWithOther(storeType, 'useApplication')
    },
    {
      label: 'scope_of_disclosure',
      value: ckanValueWithOther(storeType, 'scopeOfDisclosure')
    },
    {
      label: 'terms_of_use_permissible_region',
      value: ckanValueArrayWithOther(storeType, 'permissionResion')
    },
    {
      label: 'terms_of_use_notices',
      value: storeType.notices
    },
    {
      label: 'privacy_policy_contains_personal_data',
      value: ckanValueWithOther(storeType, 'personalData')
    },
    {
      label: 'fee',
      value: storeType.fee.value
    },
    {
      label: 'sales_info_url',
      value: storeType.salesInfoUrl
    },
    {
      label: 'pricing_price_range',
      value: storeType.priceRange
    },
    {
      label: 'pricing_notices_of_price',
      value: storeType.noticesOfPrice
    },
    {
      label: 'warranty_express_warranty',
      value: ckanValueWithOther(storeType, 'expressWarranty')
    },
    {
      label: 'warranty_leagal_compliance',
      value: ckanValueArrayWithOther(storeType, 'leagalCompliance')
    }
  ]
  return userTerms
}

// 利用条件の編集データ生成
function createUserTermsForEdit() {
  var userTerms = [
    {
      label: 'rights',
      value: editFlg.rights.value ? store.usrRight : store.another.usrRight
    },
    {
      label: 'access_rights',
      value: editFlg.accessRights.value ? store.accessRights.label : store.another.accessRights.label
    },
    {
      label: 'access_rights_url',
      value: editFlg.accessRights.value ? store.accessRightsUrl : store.another.accessRightsUrl
    },
    {
      label: 'haspolicy_url',
      value: editFlg.haspolicyUrl.value ? store.haspolicyUrl : store.another.haspolicyUrl
    },
    {
      label: 'prov_was_generated_by_url',
      value: editFlg.provWasGeneratedByUrl.value ? store.provWasGeneratedByUrl : store.another.provWasGeneratedByUrl
    },
    {
      label: 'conforms_to',
      value: editFlg.conformsTo.value ? store.conformsTo : store.another.conformsTo
    },
    {
      label: 'trading_policy_contract_type',
      value: editFlg.tradingPolicyContractType.value ? store.contractType.value : store.another.contractType.value
    },
    {
      label: 'trading_policy_nda',
      value: editFlg.tradingPolicyNda.value ? store.secrecy.value : store.another.secrecy.value
    },
    {
      label: 'trading_policy_use_application',
      value: editFlg.tradingPolicyUseApplication.value ? ckanValueArrayWithOther(store, 'useApplication') : ckanValueArrayWithOther(store.another, 'useApplication')
    },
    {
      label: 'scope_of_disclosure',
      value: editFlg.scopeOfDisclosure.value ? ckanValueWithOther(store, 'scopeOfDisclosure') : ckanValueWithOther(store.another, 'scopeOfDisclosure')
    },
    {
      label: 'terms_of_use_permissible_region',
      value: editFlg.termsOfUsePermissibleRegion.value ? ckanValueArrayWithOther(store, 'permissionResion') : ckanValueArrayWithOther(store.another, 'permissionResion')
    },
    {
      label: 'terms_of_use_notices',
      value: editFlg.termsOfUseNotices.value ? store.notices : store.another.notices
    },
    {
      label: 'privacy_policy_contains_personal_data',
      value: editFlg.privacyPolicyContainsPersonalData.value ? ckanValueWithOther(store, 'personalData') : ckanValueWithOther(store.another, 'personalData')
    },
    {
      label: 'fee',
      value: editFlg.fee.value ? store.fee.value : store.another.fee.value
    },
    {
      label: 'sales_info_url',
      value: editFlg.salesInfoUrl.value ? store.salesInfoUrl : store.another.salesInfoUrl
    },
    {
      label: 'pricing_price_range',
      value: editFlg.pricingPriceRange.value ? store.priceRange : store.another.priceRange
    },
    {
      label: 'pricing_notices_of_price',
      value: editFlg.pricingNoticesOfPrice.value ? store.noticesOfPrice : store.another.noticesOfPrice
    },
    {
      label: 'warranty_express_warranty',
      value: editFlg.warrantyExpressWarranty.value ? ckanValueWithOther(store, 'expressWarranty') : ckanValueWithOther(store.another, 'expressWarranty')
    },
    {
      label: 'warranty_leagal_compliance',
      value: editFlg.warrantyLegalCompliance.value ? ckanValueArrayWithOther(store, 'leagalCompliance') : ckanValueArrayWithOther(store.another, 'leagalCompliance')
    }
  ]
  return userTerms
}

// 「データの有効期間」のCKAN登録値を取得
function getDataEffectivePeriod(storeType) {
  var dataEffectivePeriod = ''
  var dataEffectivePeriodMap = []
  if (storeType.dataEffectivePeriod.selectTerms !== [] && storeType.dataEffectivePeriod.selectTerms !== null) {
    if (storeType.dataEffectivePeriod.selectTerms.value === 'date') {
      dataEffectivePeriodMap.push({
        dataEffectivePeriodType: 'startEndDate',
        date: {
          startDate: store.dataEffectivePeriod.startDate,
          endDate: store.dataEffectivePeriod.endDate
        }
      })
    } else if (storeType.dataEffectivePeriod.selectTerms.value === 'note') {
      dataEffectivePeriodMap.push({
        dataEffectivePeriodType: 'note',
        note: store.dataEffectivePeriod.freefield
      })
    }
    var jsonData = JSON.stringify(dataEffectivePeriodMap)
    dataEffectivePeriod = JSON.parse(jsonData)
  }
  return dataEffectivePeriod
}

// 「利用ライセンスの期限」のCKAN登録値を取得
function getUsageLicensePeriod(storeType) {
  var usageLicensePeriod = ''
  var usageLicensePeriodMap = []
  if (storeType.usageLicensePeriod.selectTerms !== [] && storeType.usageLicensePeriod.selectTerms !== null) {
    if (storeType.usageLicensePeriod.selectTerms.value === 'endDate') {
      usageLicensePeriodMap.push({
        usageLicensePeriodType: 'endDate',
        endDate: storeType.usageLicensePeriod.deadline
      })
    } else if (storeType.usageLicensePeriod.selectTerms.value === 'value') {
      usageLicensePeriodMap.push({
        usageLicensePeriodType: 'period',
        period: {
          referenceDate: 'purchasedDay',
          value: storeType.usageLicensePeriod.period,
          unit: storeType.usageLicensePeriod.unit.value
        }
      })
    } else if (storeType.usageLicensePeriod.selectTerms.value === 'note') {
      usageLicensePeriodMap.push({
        usageLicensePeriodType: 'note',
        note: storeType.usageLicensePeriod.freefield
      })
    }
    var jsonData = JSON.stringify(usageLicensePeriodMap)
    usageLicensePeriod = JSON.parse(jsonData)
  }
  return usageLicensePeriod
}

// 「利用期間」の登録データ生成
function createUserTermsJsonForRegister(storeType) {
  var userTermsJson = [
    {
      label: 'data_effective_period',
      value: getDataEffectivePeriod(storeType)
    },
    {
      label: 'usage_license_period',
      value: getUsageLicensePeriod(storeType)
    }
  ]
  return userTermsJson
}

// 「利用期間」の編集データ生成
function createUserTermsJsonForEdit() {
  var userTermsJson = [
    {
      label: 'data_effective_period',
      value: editFlg.dataEffectivePeriod.value ? getDataEffectivePeriod(store) : getDataEffectivePeriod(store.another)
    },
    {
      label: 'usage_license_period',
      value: editFlg.usageLicensePeriod.value ? getUsageLicensePeriod(store) : getUsageLicensePeriod(store.another)
    }
  ]
  return userTermsJson
}

// カタログ登録・編集APIリクエストのdata_creatorフィールドを表示・非表示フラグでフィルタ
function filterDataCreatorDisplayOptions(dataCreator, displayOptions){
  // カタログ登録・編集APIのlabel : 表示・非表示フラグリストのフィールド 対応表
  const mapDatasetInfoDisplay = {
    caddec_dataset_id_for_detail: 'caddecDatasetIdForDetail',
    // caddec_provider_idは対応する表示・非表示フラグリストのフィールドなし
    publisher_name: 'publisherName',
    publisher_uri: 'publisherUri',
    creator_name: 'creatorName',
    creator_url: 'creatorUrl',
    contact_name: 'contactName',
    contact_url: 'contactUrl',
  }

  // 非表示設定された項目をフィルタ
  var filteredDataCreatorList = []
  for (var i = 0; i < dataCreator.length; i++) {
    var field = dataCreator[i].label
    if(field in mapDatasetInfoDisplay){
        var displayField = mapDatasetInfoDisplay[field]
        if(displayOptions[displayField] === 'hide'){
          continue
        }
    }
    filteredDataCreatorList.push(dataCreator[i])
  }

  return filteredDataCreatorList
}

// カタログ登録・編集APIリクエストのdatasetoptionalフィールドを表示・非表示フラグでフィルタ
function filterDatasetOptionalDisplayOptions(datasetoptional, displayOptions){
  // カタログ登録・編集APIのlabel : 表示・非表示フラグリストのフィールド 対応表
  const mapDatasetoptionalDisplay = {
    vocabulary: 'vocabulary',
    term: 'term',
    language: 'language',
    frequency: 'frequency',
    spatial_url: 'spatial',
    spatial_text: 'spatial',
    spatial: 'spatial',
    temporal_start: 'temporal',
    temporal_end: 'temporal',
  }

  // 非表示設定された項目をフィルタ
  var filteredDatasetoptionalList = []
  for (var i = 0; i < datasetoptional.length; i++) {
    var field = datasetoptional[i].label
    if(field in mapDatasetoptionalDisplay){    
        var displayField = mapDatasetoptionalDisplay[field]
        if(displayOptions[displayField] === 'hide'){
          continue
        }
    }
    filteredDatasetoptionalList.push(datasetoptional[i])
  }

  return filteredDatasetoptionalList
}

// カタログ登録・編集APIリクエストのfiledata_detailsフィールドを表示・非表示フラグでフィルタ
function filterFiledataDetailsDisplayOptions(filedataDetails, displayOptions){
  // カタログ登録・編集APIのフィールド : 表示・非表示フラグリストのフィールド 対応表
  const mapDatajacketDisplay = {
    accessRights: 'accessRights',
    accessRightsUrl: 'accessRights',
    compressFormat: 'compressFormat',
    compressFormatDisplayValue: 'compressFormat',
    compressFormatOther: 'compressFormat',
    conformsTo: 'conformsTo',
    dataServiceEndpointDescription: 'dataServiceEndpointDescription',
    dataServiceEndpointUrl: 'dataServiceEndpointUrl',
    dataServiceTitle: 'dataServiceTitle',
    explainurl: 'explainUrl',
    description: 'description',
    filename: 'filename',
    format: 'format',
    getResourceIDForProvenance: 'getResourceIDForProvenance',
    haspolicyUrl: 'haspolicyUrl',
    licensetitle: 'licenseTitle',
    licenseurl: 'licenseUrl',
    mimetype: 'mimeType',
    ngsiDataModel: 'ngsiDataModel',
    ngsiEntityType: 'ngsiEntityType',
    ngsiServicePath: 'ngsiServicePath',
    ngsiTenant: 'ngsiTenant',
    packageFormat: 'packageFormat',
    packageFormatDisplayValue: 'packageFormat',
    packageFormatOther: 'packageFormat',
    previousEventId: 'previousEventId',
    resourceIDForProvenance: 'caddecResourceIdForProvenance',
    schema: 'schema',
    schemaType: 'schemaType',
    size: 'size',
    usrRight: 'rights',//配信の権利表明
  }

  // 非表示設定された項目をフィルタ
  var filteredFiledataDetailList = []
  for (var i = 0; i < filedataDetails.length; i++) {
    var filteredFiledataDetail = {}
    for (var field in filedataDetails[i]) {
      if(field in mapDatajacketDisplay){
          var displayField = mapDatajacketDisplay[field]
          if(displayOptions[displayField] === 'hide'){
            continue
          }
      }
      filteredFiledataDetail[field] = filedataDetails[i][field]
    }
    filteredFiledataDetailList.push(filteredFiledataDetail)
  }

  return filteredFiledataDetailList
}

// カタログ登録・編集APIリクエストのuser_termsフィールドを表示・非表示フラグでフィルタ
function filterUserTermsDisplayOptions(userTerms, displayOptions){
  // カタログ登録・編集APIのフィールド : 表示・非表示フラグリストのフィールド 対応表
  const mapUserTermsDisplay = {
    rights: 'rights',
    access_rights: 'accessRights',
    access_rights_url: 'accessRightsUrl',
    haspolicy_url: 'haspolicyUrl',
    prov_was_generated_by_url: 'provWasGeneratedByUrl',
    conforms_to: 'conformsTo',
    trading_policy_contract_type: 'tradingPolicyContractType',
    trading_policy_nda: 'tradingPolicyNda',
    trading_policy_use_application: 'tradingPolicyUseApplication',
    scope_of_disclosure: 'scopeOfDisclosure',
    terms_of_use_permissible_region: 'termsOfUsePermissibleRegion',
    terms_of_use_notices: 'termsOfUseNotices',
    privacy_policy_contains_personal_data: 'privacyPolicyContainsPersonalData',
    fee: 'fee',
    sales_info_url: 'salesInfoUrl',
    pricing_price_range: 'pricingPriceRange',
    pricing_notices_of_price: 'pricingNoticesOfPrice',
    warranty_express_warranty: 'warrantyExpressWarranty',
    warranty_leagal_compliance: 'warrantyLegalCompliance',
  }

  var filteredUserTermslList = []
  for (var i = 0; i < userTerms.length; i++) {
    var field = userTerms[i].label
    if(field in mapUserTermsDisplay){
        var displayField = mapUserTermsDisplay[field]
        if(displayOptions[displayField] === 'hide'){
          continue
        }
    }
    filteredUserTermslList.push(userTerms[i])
  }

  return filteredUserTermslList
}

// カタログ登録・編集APIリクエストのuser_terms_jsonフィールドを表示・非表示フラグでフィルタ
function filterUserTermsJsonDisplayOptions(userTermsJson, displayOptions){
  // カタログ登録・編集APIのlabel : 表示・非表示フラグリストのフィールド 対応表
  const mapUserTermsJsonDisplay = {
    data_effective_period: 'dataEffectivePeriod',
    usage_license_period: 'usageLicensePeriod',
  }

  var filteredUserTermsJsonList = []
  for (var i = 0; i < userTermsJson.length; i++) {
    var field = userTermsJson[i].label
    if(field in mapUserTermsJsonDisplay){
        var displayField = mapUserTermsJsonDisplay[field]
        if(displayOptions[displayField] === 'hide'){
          continue
        }
    }
    filteredUserTermsJsonList.push(userTermsJson[i])
  }

  return filteredUserTermsJsonList
}

// カタログ登録・編集APIリクエストのデータを表示・非表示フラグでフィルタ
function filterCatalogData(catalogData, displayOptions) {
  // カタログ登録・編集APIのフィールド : 表示・非表示フラグリストのフィールド 対応表
  const mapCatalogDataDisplay = {
    dataset_class: 'theme',
    dataset_description_url: 'url',
    dataset_key: 'tags',
  }

  // 非表示設定された項目をフィルタ
  var filteredCatalogData = {}
  for (var field in catalogData){
    if(field in mapCatalogDataDisplay){
      var displayField = mapCatalogDataDisplay[field]
      if(displayOptions[displayField] === 'hide'){
        continue
      }
    }
    filteredCatalogData[field] = catalogData[field]
  }

  // 関数で対応するフィールドをフィルタ
  if("data_creator" in catalogData){
    filteredCatalogData["data_creator"] = filterDataCreatorDisplayOptions(catalogData["data_creator"], displayOptions)
  }
  if("datasetoptional" in catalogData){
    filteredCatalogData["datasetoptional"] = filterDatasetOptionalDisplayOptions(catalogData["datasetoptional"], displayOptions)
  }
  if("filedata_details" in catalogData){
    filteredCatalogData["filedata_details"] = filterFiledataDetailsDisplayOptions(catalogData["filedata_details"], displayOptions)
  }
  if("user_terms" in catalogData){
    filteredCatalogData["user_terms"] = filterUserTermsDisplayOptions(catalogData["user_terms"], displayOptions)
  }
  if("user_terms_json" in catalogData){
    filteredCatalogData["user_terms_json"] = filterUserTermsJsonDisplayOptions(catalogData["user_terms_json"], displayOptions)
  }

  return filteredCatalogData
}

// カタログパラメータ整形
function formatCatalogParameter() {
  var pkg = {
    regist_org: store.registOrg.value,
    dataset_description_url: store.datasetDescriptionUrl,
    catalogTitle: store.catalogTitle,
    catalogDescription: store.catalogDescription,
    data_creator: createDataDatasetInfoForRegister(store),
    dataset_class: store.selectThemes,
    dataset_key: store.selectTags,
    datasetoptional: createDatasetoptionalForRegister(store),
    filedata_details: createDatajacketForCkan(store, 'register'),
    user_terms: createUserTermsForRegister(store),
    user_terms_json: createUserTermsJsonForRegister(store),
    data_terms: store.termName.value,
    license_title: store.termName.label,
    license_url: store.termNameUrl,
    selected_mode: store.selectedMode.mode,
    ckan_data_name: '',
    issued: store.issued,
    identifier: store.identifier,
    dataset_url: store.datasetUrl
  }
  // return pkg
  return filterCatalogData(pkg, store.itemDisplayFlg)
}

// バックアップデータ整形
function formatBackup() {
  var pkg = {
    regist_org: store.hold.registOrg.value,
    dataset_description_url: store.hold.datasetDescriptionUrl,
    catalogTitle: store.hold.catalogTitle,
    catalogDescription: store.hold.catalogDescription,
    data_creator: createDataDatasetInfoForRegister(store.hold),
    dataset_class: store.hold.selectThemes,
    dataset_key: store.hold.selectTags,
    datasetoptional: createDatasetoptionalForRegister(store.hold),
    filedata_details: createDatajacketForCkan(store.hold, 'register'),
    user_terms: createUserTermsForRegister(store.hold),
    user_terms_json: createUserTermsJsonForRegister(store.hold),
    data_terms: store.hold.termName.value,
    license_title: store.hold.termName.label,
    license_url: store.hold.termNameUrl,
    selected_mode: store.selectedMode.mode,
    ckan_data_name: store.releaseCkanDataName,
    issued: store.issued,
    identifier: store.identifier,
    dataset_url: store.datasetUrl
  }
  // return pkg
  return filterCatalogData(pkg, store.itemDisplayFlg)
}

// 横断カタログと紐づく詳細カタログ、または詳細カタログと紐づく横断カタログ
function formatLinkAnotherData() {
  var anotherData = {
    regist_org: store.another.registOrg.value,
    dataset_description_url: store.another.datasetDescriptionUrl,
    catalogTitle: store.another.catalogTitle,
    catalogDescription: store.another.catalogDescription,
    data_creator: createDataDatasetInfoForEdit(),
    dataset_class: store.another.selectThemes,
    dataset_key: store.another.selectTags,
    datasetoptional: createDatasetoptionalForEdit(),
    filedata_details: createDatajacketForCkan(store.another, 'register'),
    user_terms: createUserTermsForEdit(),
    user_terms_json: createUserTermsJsonForEdit(),
    data_terms: store.another.termName.value,
    license_title: store.another.termName.label,
    license_url: store.another.termNameUrl,
    selected_mode: store.selectedMode.mode,
    ckan_data_name: store.mode === 'detail-link-release_duplicate' ? store.releaseCkanDataName : store.detailCkanDataName,
    issued: store.another.issued,
    identifier: store.another.identifier,
    dataset_url: store.another.datasetUrl
  }
  //return anotherData
  return filterCatalogData(anotherData, store.itemDisplayFlg)
}

// 横断カタログ編集反映データ整形
function formatReleaseEdit() {
  var releaseData = {
    regist_org: editFlg.registOrg.value ? store.registOrg.value : store.another.registOrg.value,
    dataset_description_url: editFlg.url.value ? store.datasetDescriptionUrl : store.another.datasetDescriptionUrl,
    catalogTitle: editFlg.title.value ? store.catalogTitle : store.another.catalogTitle,
    catalogDescription: editFlg.notes.value ? store.catalogDescription : store.another.catalogDescription,
    data_creator: createDataDatasetInfoForEdit(),
    dataset_class: editFlg.theme.value ? store.selectThemes : store.another.selectThemes,
    dataset_key: editFlg.tags.value ? store.selectTags : store.another.selectTags,
    datasetoptional: createDatasetoptionalForEdit(),
    filedata_details: editFlg.resources.value ? createDatajacketForCkan(store, 'edit') : createDatajacketForCkan(store.another, 'edit'),
    user_terms: createUserTermsForEdit(),
    user_terms_json: createUserTermsJsonForEdit(),
    data_terms: editFlg.license.value ? store.termName.value : store.another.termName.value,
    license_title: editFlg.license.value ? store.termName.label : store.another.termName.label,
    license_url: editFlg.license.value ? store.termNameUrl : store.another.termNameUrl,
    selected_mode: store.selectedMode.mode,
    ckan_data_name: store.releaseCkanDataName,
    issued: store.another.issued,
    identifier: store.another.identifier,
    dataset_url: store.another.datasetUrl
  }
  //return releaseData
  return filterCatalogData(releaseData, store.itemDisplayFlg)
}

// 詳細カタログ編集反映データ整形
function formatDetailEdit() {
  var detailData = {
    regist_org: editFlg.registOrg.value ? store.registOrg.value : store.another.registOrg.value,
    dataset_description_url: editFlg.url.value ? store.datasetDescriptionUrl : store.another.datasetDescriptionUrl,
    catalogTitle: editFlg.title.value ? store.catalogTitle : store.another.catalogTitle,
    catalogDescription: editFlg.notes.value ? store.catalogDescription : store.another.catalogDescription,
    data_creator: createDataDatasetInfoForEdit(),
    dataset_class: editFlg.theme.value ? store.selectThemes : store.another.selectThemes,
    dataset_key: editFlg.tags.value ? store.selectTags : store.another.selectTags,
    datasetoptional: createDatasetoptionalForEdit(),
    filedata_details: editFlg.resources.value ? createDatajacketForCkan(store, 'edit') : createDatajacketForCkan(store.another, 'edit'),
    user_terms: createUserTermsForEdit(),
    user_terms_json: createUserTermsJsonForEdit(),
    data_terms: editFlg.license.value ? store.termName.value : store.another.termName.value,
    license_title: editFlg.license.value ? store.termName.label : store.another.termName.label,
    license_url: editFlg.license.value ? store.termNameUrl : store.another.termNameUrl,
    selected_mode: store.selectedMode.mode,
    ckan_data_name: store.detailCkanDataName,
    issued: store.another.issued,
    identifier: store.another.identifier,
    dataset_url: store.another.datasetUrl
  }
  //return detailData
  return filterCatalogData(detailData, store.itemDisplayFlg)
}

// 編集反映フラグのチェック
function checkEditFlg() {
  for (var key in editFlg) {
    if (editFlg[key].value) {
      return true
    }
  }
  return false
}

// テンプレートデータの整形
function formatTemplateData() {
  // データセット情報の表示形式
  var displayDatasetinfo = {
    url: displayType.url.value,
    caddec_dataset_id_for_detail: displayType.caddecDatasetIdForDetail.value,
    publisher_name: displayType.publisherName.value,
    publisher_uri: displayType.publisherUri.value,
    creator_name: displayType.creatorName.value,
    creator_url: displayType.creatorUrl.value,
    contact_name: displayType.contactName.value,
    contact_url: displayType.contactUrl.value
  }

  // 概要情報の表示形式
  var displayDatajacket = {
    filename: displayType.filename.value,
    description: displayType.description.value,
    downloadUrl: displayType.downloadUrl.value,
    explainurl: displayType.explainUrl.value,
    size: displayType.size.value,
    mime_type: displayType.mimeType.value,
    format: displayType.format.value,
    compress_format: displayType.compressFormat.value,
    package_format: displayType.packageFormat.value,
    schema: displayType.schema.value,
    schema_type: displayType.schemaType.value,
    ngsi_entity_type: displayType.ngsiEntityType.value,
    ngsi_tenant: displayType.ngsiTenant.value,
    ngsi_service_path: displayType.ngsiServicePath.value,
    ngsi_data_model: displayType.ngsiDataModel.value,
    // 「来歴登録の有無」の表示形式は交換実績記録用リソースIDと共通とする
    get_resource_id_for_provenance: displayType.getResourceIDForProvenance.value,
    caddec_resource_id_for_provenance: displayType.getResourceIDForProvenance.value,
    // 「前段イベント識別子」の表示形式は交換実績記録用リソースIDと共通とする
    previous_event_id: displayType.getResourceIDForProvenance.value,
    data_service_title: displayType.dataServiceTitle.value,
    data_service_endpoint_url: displayType.dataServiceEndpointUrl.value,
    data_service_endpoint_description: displayType.dataServiceEndpointDescription.value
  }

  // データセット情報(任意)の表示形式
  var displayDatasetoptionalinfo = {
    theme: displayType.theme.value,
    tags: displayType.tags.value,
    language: displayType.language.value,
    vocabulary: displayType.vocabulary.value,
    term: displayType.term.value,
    frequency: displayType.frequency.value,
    spatial: displayType.spatial.value,
    temporal: displayType.temporal.value
  }

  // 利用条件の表示形式
  var displayUserTerms = {
    license_title: displayType.licenseTitle.value,
    license_url: displayType.licenseUrl.value,
    rights: displayType.rights.value,
    access_rights: displayType.accessRights.value,
    access_rights_url: displayType.accessRightsUrl.value,
    haspolicy_url: displayType.haspolicyUrl.value,
    prov_was_generated_by_url: displayType.provWasGeneratedByUrl.value,
    conforms_to: displayType.conformsTo.value,
    trading_policy_contract_type: displayType.tradingPolicyContractType.value,
    trading_policy_nda: displayType.tradingPolicyNda.value,
    trading_policy_use_application: displayType.tradingPolicyUseApplication.value,
    scope_of_disclosure: displayType.scopeOfDisclosure.value,
    terms_of_use_permissible_region: displayType.termsOfUsePermissibleRegion.value,
    terms_of_use_notices: displayType.termsOfUseNotices.value,
    privacy_policy_contains_personal_data: displayType.privacyPolicyContainsPersonalData.value,
    data_effective_period: displayType.dataEffectivePeriod.value,
    usage_license_period: displayType.usageLicensePeriod.value,
    fee: displayType.fee.value,
    sales_info_url: displayType.salesInfoUrl.value,
    pricing_price_range: displayType.pricingPriceRange.value,
    pricing_notices_of_price: displayType.pricingNoticesOfPrice.value,
    warranty_express_warranty: displayType.warrantyExpressWarranty.value,
    warranty_legal_compliance: displayType.warrantyLegalCompliance.value
  }

  // データセットの情報のパラメータ
  var datasetinfoData = {
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

  // データ概要情報のパラメータ
  var datajacketData = store.filedataDetails

  // データセット情報(任意)のパラメータ
  var datasetoptionalinfoData = {
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
  
  // 利用条件のパラメータ
  var usertermsData = {
    // selected_tab: store.selectedTab,
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
  var templateData = {
    catalog_display: {
      datasetinfo: displayDatasetinfo,
      datajacket: displayDatajacket,
      datasetoptionalinfo: displayDatasetoptionalinfo,
      userterms: displayUserTerms
    },
    catalog_value: {
      datasetinfo: datasetinfoData,
      datajacket: datajacketData,
      datasetoptionalinfo: datasetoptionalinfoData,
      userterms: usertermsData
    }
  }
  return templateData
}

defineExpose({
  formatLinkAnotherData,
  formatCatalogParameter,
  formatBackup,
  formatDetailEdit,
  checkEditFlg,
  formatReleaseEdit,
  formatTemplateData
})

</script>

<template>
  <!-- -------------------------------------------------------------------------------------------------- -->
  <!-- カタログ複製時または編集時は更新箇所を赤字表示する                                                 -->
  <!-- ただし、概要情報の配信数が追加または削除された場合は概要情報テーブルの全項目を赤字表示する         -->
  <!-- NGSIデータモデルも赤字表示の対象外とする                                                           -->
  <!-- -------------------------------------------------------------------------------------------------- -->
  <div class="dataset-confirm">
    <q-card class="q-ma-sm q-card-background-white">
      <q-card-section>
        <div class="q-py-sm">
          <font size = '5'>データセット情報</font>
        </div>
        <div class="q-py-sm">
          <font size = '4' color='#1d468f'>データセットのタイトル</font>
          <div class="row justify-start items-end">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'under-line', 'fit', 'indent-item',
              { 'red-color': store.catalogTitle !== store.hold.catalogTitle && checkRedCharacterMode(store.selectedMode.mode)}]">
              {{ store.catalogTitle }}
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.title"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.title"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                disable
                label="表示形式"
                label-color="primary"
                v-model="mandatoryItem"
              />
            </div>
          </div>
        </div>
        <div class="q-py-sm">
          <font size = '4' color='#1d468f'>データセットの説明</font>
          <div class="row justify-start items-end">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'under-line', 'fit', 'indent-item',
              { 'red-color': store.catalogDescription !== store.hold.catalogDescription && checkRedCharacterMode(store.selectedMode.mode)}]">
              {{ store.catalogDescription }}
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.notes"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.notes"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                disable
                label="表示形式"
                label-color="primary"
                v-model="mandatoryItem"
              />
            </div>
          </div>
        </div>
        <div class="q-py-sm" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.url !== 'hide'">
          <font size = '4' color='#1d468f'>データセットの説明ページURL</font>
          <div class="row justify-start items-end">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'under-line', 'fit', 'indent-item',
              { 'red-color': store.datasetDescriptionUrl !== store.hold.datasetDescriptionUrl && checkRedCharacterMode(store.selectedMode.mode)}]">
              {{ store.datasetDescriptionUrl }}
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.url"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.url"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                v-model="displayType.url"
                :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
              />
            </div>
          </div>
        </div>
        <div class="q-py-sm" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.caddecDatasetIdForDetail !== 'hide'">
          <font size = '4' color='#1d468f'>詳細検索用データセットID</font>
          <div class="row justify-start items-end">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'column', 'justify-center', 'under-line',
              { 'red-color': store.datasetIdForDetail !== store.hold.datasetIdForDetail && checkRedCharacterMode(store.selectedMode.mode)}]">
              {{ store.datasetIdForDetail }}
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                v-model="displayType.caddecDatasetIdForDetail"
                :options="[TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD]"
              />
            </div>
          </div>
        </div>
        <div class="q-py-sm">
          <font size = '4' color='#1d468f'>ユーザの属する組織</font>
          <div class="row justify-start items-end">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'column', 'justify-center', 'under-line',
              { 'red-color': store.registOrg.label !== store.hold.registOrg.label && checkRedCharacterMode(store.selectedMode.mode)}]">
              {{ store.registOrg.label }}
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.registOrg"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.registOrg"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                disable
                v-model="mandatoryItem"
              />
            </div>
          </div>
        </div>
        <div class="q-py-sm">
          <font size = '4' color='#1d468f'>提供者ID</font>
          <div class="row justify-start items-end">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'column', 'justify-center', 'under-line',
              { 'red-color': store.publisherId.label !== store.hold.publisherId.label && checkRedCharacterMode(store.selectedMode.mode)}]">
              {{ store.publisherId.label }}
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.caddecProviderId"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.caddecProviderId"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                disable
                v-model="mandatoryItem"
              />
            </div>
          </div>
        </div>
        <div class="q-py-sm" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.publisherUri !== 'hide'">
          <font size = '4' color='#1d468f'>データセットの公開者</font>
          <div class="row justify-start items-end">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'under-line', 'fit', 'indent-item',
              { 'red-color': store.publisherUri !== store.hold.publisherUri && checkRedCharacterMode(store.selectedMode.mode)}]">
              {{ store.publisherUri }}
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.publisherUri"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.publisherUri"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                v-model="displayType.publisherUri"
                :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
              />
            </div>
          </div>
        </div>
        <div class="q-py-sm" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.publisherName !== 'hide'">
          <font size = '4' color='#1d468f'>データセットの公開者（説明）</font>
          <div class="row justify-start items-end">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'under-line', 'fit', 'indent-item',
              { 'red-color': store.publisher !== store.hold.publisher && checkRedCharacterMode(store.selectedMode.mode)}]">
              {{ store.publisher }}
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.publisherName"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.publisherName"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                v-model="displayType.publisherName"
                :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
              />
            </div>
          </div>
        </div>
        <div class="q-py-sm" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.creatorUrl !== 'hide'">
          <font size = '4' color='#1d468f'>データセットの作成者</font>
          <div class="row justify-start items-end">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'under-line', 'fit', 'indent-item',
              { 'red-color': store.creatorUrl !== store.hold.creatorUrl && checkRedCharacterMode(store.selectedMode.mode)}]">
              {{ store.creatorUrl }}
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.creatorUrl"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.creatorUrl"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                v-model="displayType.creatorUrl"
                :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
              />
            </div>
          </div>
        </div>
        <div class="q-py-sm" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.creatorName !== 'hide'">
          <font size = '4' color='#1d468f'>データセットの作成者（説明）</font>
          <div class="row justify-start items-end">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'under-line', 'fit', 'indent-item',
              { 'red-color': store.creator !== store.hold.creator && checkRedCharacterMode(store.selectedMode.mode)}]">
              {{ store.creator }}
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.creatorName"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.creatorName"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                v-model="displayType.creatorName"
                :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
              />
            </div>
          </div>
        </div>
        <div class="q-py-sm" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.contactUrl !== 'hide'">
          <font size = '4' color='#1d468f'>データセットの窓口</font>
          <div class="row justify-start items-end">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'under-line', 'fit', 'indent-item',
              { 'red-color': store.contactPointUrl !== store.hold.contactPointUrl && checkRedCharacterMode(store.selectedMode.mode)}]">
              {{ store.contactPointUrl }}
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.contactUrl"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.contactUrl"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                v-model="displayType.contactUrl"
                :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
              />
            </div>
          </div>
        </div>
        <div class="q-py-sm" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.contactName !== 'hide'">
          <font size = '4' color='#1d468f'>データセットの窓口（説明）</font>
          <div class="row justify-start items-end">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'under-line', 'fit', 'indent-item',
              { 'red-color': store.contactPoint !== store.hold.contactPoint && checkRedCharacterMode(store.selectedMode.mode)}]">
              {{ store.contactPoint }}
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.contactName"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.contactName"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                v-model="displayType.contactName"
                :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
              />
            </div>
          </div>
        </div>
      </q-card-section>
    </q-card>
    <q-card class="q-ma-sm q-card-background-white">
      <q-card-section>
        <div class="q-py-sm">
          <font size= '5'>データ概要情報</font>
        </div>
        <div v-if="store.selectedMode.mode === 'template'">
          <div v-for="(item3, index3) in store.filedataDetails" :key="index3">
            <div class="q-py-sm">
              <font size = '4' color='#1d468f'>リソース提供手段の識別子</font>
              <div class="row justify-start items-end">
                <div class="col-10">
                  <q-input v-model="item3.resourceType.label" readonly />
                </div>
                <div class="col-2">
                  <q-select
                    label="表示形式"
                    label-color="primary"
                    disable
                    v-model="mandatoryItem"
                  />
                </div>
              </div>
            </div>
            <div class="q-py-sm">
              <font size = '4' color='#1d468f'>配信のダウンロードURL</font>
              <div class="row justify-start items-end">
                <div class="col-10">
                  <q-input v-model="item3.downloadUrl" autogrow readonly />
                </div>
                <div class="col-2">
                  <q-select
                    label="表示形式"
                    label-color="primary"
                    disable
                    v-model="mandatoryItem"
                  />
                </div>
              </div>
            </div>
            <div class="q-py-sm">
              <font size = '4' color='#1d468f'>配信の情報提供ページURL</font>
              <div class="row justify-start items-end">
                <div class="col-10">
                  <q-input v-model="item3.explainurl" autogrow readonly />
                </div>
                <div class="col-2">
                  <q-select
                    label="表示形式"
                    label-color="primary"
                    v-model="displayType.explainUrl"
                    :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
                  />
                </div>
              </div>
            </div>
            <div class="q-py-sm">
              <font size = '4' color='#1d468f'>配信の名称</font>
              <div class="row justify-start items-end">
                <div class="col-10">
                  <q-input v-model="item3.filename" autogrow readonly />
                </div>
                <div class="col-2">
                  <q-select
                    label="表示形式"
                    label-color="primary"
                    v-model="displayType.filename"
                    :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
                  />
                </div>
              </div>
            </div>
            <div class="q-py-sm">
              <font size = '4' color='#1d468f'>配信の説明</font>
              <div class="row justify-start items-end">
                <div class="col-10">
                  <q-input v-model="item3.description" autogrow readonly />
                </div>
                <div class="col-2">
                  <q-select
                    label="表示形式"
                    label-color="primary"
                    v-model="displayType.description"
                    :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
                  />
                </div>
              </div>
            </div>
            <div class="q-py-sm">
              <font size = '4' color='#1d468f'>配信のバイトサイズ</font>
              <div class="row justify-start items-end">
                <div class="col-10">
                  <q-input v-model="item3.size" readonly />
                </div>
                <div class="col-2">
                  <q-select
                    label="表示形式"
                    label-color="primary"
                    v-model="displayType.size"
                    :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
                  />
                </div>
              </div>
            </div>
            <div class="q-py-sm">
              <font size = '4' color='#1d468f'>配信のメディアタイプ</font>
              <div class="row justify-start items-end">
                <div class="col-10">
                  <q-input v-model="item3.mimetype.label" readonly />
                </div>
                <div class="col-2">
                  <q-select
                    label="表示形式"
                    label-color="primary"
                    v-model="displayType.mimeType"
                    :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
                  />
                </div>
              </div>
            </div>
            <div class="q-py-sm">
              <font size = '4' color='#1d468f'>配信のファイル形式</font>
              <div class="row justify-start items-end">
                <div class="col-10">
                  <q-input v-model="item3.format" autogrow readonly />
                </div>
                <div class="col-2">
                  <q-select
                    label="表示形式"
                    label-color="primary"
                    v-model="displayType.format"
                    :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
                  />
                </div>
              </div>
            </div>
            <div class="q-py-sm">
              <font size = '4' color='#1d468f'>配信の圧縮形式</font>
              <div class="row justify-start items-end">
                <div class="col-10">
                  <q-input v-model="item3.compressFormatDisplayValue" readonly />
                </div>
                <div class="col-2">
                  <q-select
                    label="表示形式"
                    label-color="primary"
                    v-model="displayType.compressFormat"
                    :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
                  />
                </div>
              </div>
            </div>
            <div class="q-py-sm">
              <font size = '4' color='#1d468f'>配信のパッケージ形式</font>
              <div class="row justify-start items-end">
                <div class="col-10">
                  <q-input v-model="item3.packageFormatDisplayValue" readonly />
                </div>
                <div class="col-2">
                  <q-select
                    label="表示形式"
                    label-color="primary"
                    v-model="displayType.packageFormat"
                    :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
                  />
                </div>
              </div>
            </div>
            <div class="q-py-sm">
              <font size = '4' color='#1d468f'>スキーマ</font>
              <div class="row justify-start items-end">
                <div class="col-10">
                  <q-input v-model="item3.schema" autogrow readonly />
                </div>
                <div class="col-2">
                  <q-select
                    label="表示形式"
                    label-color="primary"
                    v-model="displayType.schema"
                    :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
                  />
                </div>
              </div>
            </div>
            <div class="q-py-sm">
              <font size = '4' color='#1d468f'>スキーマタイプ</font>
              <div class="row justify-start items-end">
                <div class="col-10">
                  <q-input v-model="item3.schemaType.label" readonly />
                </div>
                <div class="col-2">
                  <q-select
                    label="表示形式"
                    label-color="primary"
                    v-model="displayType.schemaType"
                    :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
                  />
                </div>
              </div>
            </div>
            <div class="q-py-sm">
              <font size = '4' color='#1d468f'>NGSIデータ種別</font>
              <div class="row justify-start items-end">
                <div class="col-10">
                  <q-input v-model="item3.ngsiEntityType" autogrow readonly />
                </div>
                <div class="col-2">
                  <q-select
                    label="表示形式"
                    label-color="primary"
                    v-model="displayType.ngsiEntityType"
                    :options="[TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
                  />
                </div>
              </div>
            </div>
            <div class="q-py-sm">
              <font size = '4' color='#1d468f'>NGSIテナント</font>
              <div class="row justify-start items-end">
                <div class="col-10">
                  <q-input v-model="item3.ngsiTenant" autogrow readonly />
                </div>
                <div class="col-2">
                  <q-select
                    label="表示形式"
                    label-color="primary"
                    v-model="displayType.ngsiTenant"
                    :options="[TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
                  />
                </div>
              </div>
            </div>
            <div class="q-py-sm">
              <font size = '4' color='#1d468f'>NGSIサービスパス</font>
              <div class="row justify-start items-end">
                <div class="col-10">
                  <q-input v-model="item3.ngsiServicePath" autogrow readonly />
                </div>
                <div class="col-2">
                  <q-select
                    label="表示形式"
                    label-color="primary"
                    v-model="displayType.ngsiServicePath"
                    :options="[TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
                  />
                </div>
              </div>
            </div>
            <div class="q-py-sm">
              <div class="row justify-start items-center">
                <div class="col-10">
                  <font size = '4' color='#1d468f'>NGSIデータモデル</font>
                </div>
                <div class="col-2">
                  <q-select
                    label="表示形式"
                    label-color="primary"
                    v-model="displayType.ngsiDataModel"
                    :options="[TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
                  />
                </div>
              </div>
              <p />
              <q-table
                :rows="item3.ngsiDataModel"
                :columns="dataModelColumns"
                row-key="attribute"
                :separator="cell"
              >
                <template v-slot:body="props">
                  <q-tr :props="props">
                    <q-td key="attribute" :props="props">
                      {{ props.row.attribute }}
                    </q-td>
                    <q-td key="dataType" :props="props">
                      {{ props.row.dataType }}
                    </q-td>
                    <q-td key="example" :props="props">
                      {{ props.row.example }}
                    </q-td>
                    <q-td key="description" :props="props">
                      {{ props.row.description }}
                    </q-td>
                    <q-td key="metadata" :props="props" class="metadata-btn">
                      <q-btn color="primary" outline class="full-width" :label="props.row.metadata.length ? 'あり' : 'なし'" field='metadata' :disable="!props.row.metadata.length" @click="createMetadataTable(props.row)"></q-btn>
                    </q-td>
                  </q-tr>
                </template>
              </q-table>
            </div>
            <div class="q-py-sm">
              <font size = '4' color='#1d468f'>契約確認の要否</font>
              <div class="row justify-start items-end">
                <div class="col-10">
                  <q-input v-model="item3.contractRequired.label" readonly />
                </div>
                <div class="col-2">
                  <q-select
                    label="表示形式"
                    label-color="primary"
                    disable
                    v-model="mandatoryItem"
                  />
                </div>
              </div>
            </div>
            <div class="q-py-sm">
              <font size = '4' color='#1d468f'>コネクタ利用の要否</font>
              <div class="row justify-start items-end">
                <div class="col-10">
                  <q-input v-model="item3.connectRequired.label" readonly />
                </div>
                <div class="col-2">
                  <q-select
                    label="表示形式"
                    label-color="primary"
                    disable
                    v-model="mandatoryItem"
                  />
                </div>
              </div>
            </div>
            <div class="q-pt-sm">
              <div class="row justify-start items-center">
                <font class="col-10" size = '4' color='#1d468f'>来歴</font>
                <div class="col-2">
                  <q-select
                    label="表示形式"
                    label-color="primary"
                    v-model="displayType.getResourceIDForProvenance"
                    :options="[TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
                  />
                </div>
              </div>
            </div>
            <div v-show="displayType.getResourceIDForProvenance">
              <div class="q-py-sm q-pl-lg">
                <font size = '4' color='#1d468f'>来歴登録の有無</font>
                <div class="row">
                  <div class="col-10">
                    <q-input v-model="item3.getResourceIDForProvenance.label" readonly />
                  </div>
                </div>
              </div>
              <div class="q-py-sm q-pl-lg">
                <font size = '4' color='#1d468f'>交換実績記録用リソースID</font>
                <div class="row">
                  <div class="col-10">
                    <q-input readonly />
                  </div>
                </div>
              </div>
              <div class="q-py-sm q-pl-lg">
                <font size = '4' color='#1d468f'>前段イベント識別子</font>
                <div class="row">
                  <div class="col-10">
                    <q-input v-model="item3.previousEventId" readonly />
                  </div>
                </div>
              </div>
              <div class="q-py-sm q-pl-xl">
                <font size = '4' color='#1d468f'>来歴登録済みの配信のダウンロードURL</font>
                <div class="row">
                  <div class="col-10">
                    <q-input v-model="item3.urlForProvenance" autogrow readonly />
                  </div>
                </div>
              </div>
              <div class="q-py-sm q-pl-xl">
                <font size = '4' color='#1d468f'>来歴登録済みのCADDEユーザID</font>
                <div class="row">
                  <div class="col-10">
                    <q-input v-model="item3.caddeUserId" autogrow readonly />
                  </div>
                </div>
              </div>
            </div>      
            <div class="q-py-sm">
              <font size = '4' color='#1d468f'>データサービスのタイトル</font>
              <div class="row justify-start items-end">
                <div class="col-10">
                  <q-input v-model="item3.dataServiceTitle" autogrow readonly />
                </div>
                <div class="col-2">
                  <q-select
                    label="表示形式"
                    label-color="primary"
                    v-model="displayType.dataServiceTitle"
                    :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
                  />
                </div>
              </div>
            </div>
            <div class="q-py-sm">
              <font size = '4' color='#1d468f'>データサービスのエンドポイント</font>
              <div class="row justify-start items-end">
                <div class="col-10">
                  <q-input v-model="item3.dataServiceEndpointUrl" autogrow readonly />
                </div>
                <div class="col-2">
                  <q-select
                    label="表示形式"
                    label-color="primary"
                    v-model="displayType.dataServiceEndpointUrl"
                    :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
                  />
                </div>
              </div>
            </div>
            <div class="q-py-sm">
              <font size = '4' color='#1d468f'>データサービスのエンドポイントの定義</font>
              <div class="row justify-start items-end">
                <div class="col-10">
                  <q-input v-model="item3.dataServiceEndpointDescription" autogrow readonly />
                </div>
                <div class="col-2">
                  <q-select
                    label="表示形式"
                    label-color="primary"
                    v-model="displayType.dataServiceEndpointDescription"
                    :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-else>
          <div v-if="store.selectedMode.mode === 'edit'" class="col-md-2">
            <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
              <div class="row">
                <div class="col-md-2 offset-md-10">
                  <q-select
                    v-model="editFlg.resources"
                    :options="editDetailOption"
                  />
                </div>
              </div>
            </div>
            <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
              <div class="row">
                <div class="col-md-2 offset-md-10">
                  <q-select
                    v-model="editFlg.resources"
                    :options="editReleaseOption"
                  />
                </div>
              </div>
            </div>
          </div>
          <div class="col-12">
            <q-table
              :rows=tableData
              :columns="columns"
              :visible-columns="datajacketVisibleColumns"
              row-key="index"
              :separator="cell"
              required: true
              class="resourceTable"
            >
              <template v-slot:body-cell-filename="props">
                <q-td :props="props" :class="(props.row.prefilename=='' || props.row.filename!=props.row.prefilename)?'text-red':'text-black'">
                  {{props.row.filename}}
                </q-td>
              </template>
              <template v-slot:body-cell-description="props">
                <q-td :props="props" :class="(props.row.predescription=='' || props.row.description!=props.row.predescription)?'text-red':'text-black'">
                  {{props.row.description}}
                </q-td>
              </template>
              <template v-slot:body-cell-resourceType="props">
                <q-td :props="props" :class="(props.row.preresourceType=='' || props.row.resourceType.label!=props.row.preresourceType.label)?'text-red':'text-black'">
                  {{props.row.resourceType.label}}
                </q-td>
              </template>
              <template v-slot:body-cell-downloadUrl="props">
                <q-td :props="props" :class="(props.row.predownloadUrl=='' || props.row.downloadUrl!=props.row.predownloadUrl)?'text-red':'text-black'">
                  {{props.row.downloadUrl}}
                </q-td>
              </template>
              <template v-slot:body-cell-explainurl="props">
                <q-td :props="props" :class="(props.row.preexplainurl=='' || props.row.explainurl!=props.row.preexplainurl)?'text-red':'text-black'">
                  {{props.row.explainurl}}
                </q-td>
              </template>
              <template v-slot:body-cell-size="props">
                <q-td :props="props" :class="(props.row.presize=='' || props.row.size!=props.row.presize)?'text-red':'text-black'">
                  {{props.row.size}}
                </q-td>
              </template>
              <template v-slot:body-cell-mimetype="props">
                <q-td :props="props" :class="(props.row.premimetype=='' || props.row.mimetype.label!=props.row.premimetype.label)?'text-red':'text-black'">
                  {{props.row.mimetype.label}}
                </q-td>
              </template>
              <template v-slot:body-cell-format="props">
                <q-td :props="props" :class="(props.row.preformat=='' || props.row.format!=props.row.preformat)?'text-red':'text-black'">
                  {{props.row.format}}
                </q-td>
              </template>
              <template v-slot:body-cell-compressFormat="props">
                <q-td
                  :props="props"
                  :class="(props.row.compressFormat=='' ||
                           props.row.compressFormat.label!=props.row.precompressFormat.label ||
                           props.row.compressFormatOther!=props.row.precompressFormatOther)
                           ?'text-red':'text-black'"
                >
                  {{props.row.compressFormatDisplayValue}}
                </q-td>
              </template>
              <template v-slot:body-cell-packageFormat="props">
                <q-td
                  :props="props"
                  :class="(props.row.packageFormat=='' ||
                           props.row.packageFormat.label!=props.row.prepackageFormat.label ||
                           props.row.packageFormatOther!=props.row.prepackageFormatOther)
                           ?'text-red':'text-black'"
                >
                  {{props.row.packageFormatDisplayValue}}
                </q-td>
              </template>
              <template v-slot:body-cell-schema="props">
                <q-td :props="props" :class="(props.row.preschema=='' || props.row.schema!=props.row.preschema)?'text-red':'text-black'">
                  {{props.row.schema}}
                </q-td>
              </template>
              <template v-slot:body-cell-schemaType="props">
                <q-td :props="props" :class="(props.row.preschemaType=='' || props.row.schemaType.label!=props.row.preschemaType.label)?'text-red':'text-black'">
                  {{props.row.schemaType.label}}
                </q-td>
              </template>
              <template v-slot:body-cell-ngsiEntityType="props">
                <q-td :props="props" :class="(props.row.prengsiEntityType=='' || props.row.ngsiEntityType!=props.row.prengsiEntityType)?'text-red':'text-black'">
                  {{props.row.ngsiEntityType}}
                </q-td>
              </template>
              <template v-slot:body-cell-ngsiTenant="props">
                <q-td :props="props" :class="(props.row.prengsiTenant=='' || props.row.ngsiTenant!=props.row.prengsiTenant)?'text-red':'text-black'">
                  {{props.row.ngsiTenant}}
                </q-td>
              </template>
              <template v-slot:body-cell-ngsiServicePath="props">
                <q-td :props="props" :class="(props.row.prengsiServicePath=='' || props.row.ngsiServicePath!=props.row.prengsiServicePath)?'text-red':'text-black'">
                  {{props.row.ngsiServicePath}}
                </q-td>
              </template>
              <template v-slot:body-cell-ngsiDataModel="props">
                <q-td :props="props" :class="(props.row.ngsiDataModel.length!=props.row.prengsiDataModel.length)?'text-red':'text-black'">
                  {{props.row.ngsiDataModel.length ? 'あり' : 'なし'}}
                </q-td>
              </template>
              <template v-slot:body-cell-contractRequired="props">
                <q-td :props="props" :class="(props.row.precontractRequired=='' || props.row.contractRequired.label!=props.row.precontractRequired.label)?'text-red':'text-black'">
                  {{props.row.contractRequired.label}}
                </q-td>
              </template>
              <template v-slot:body-cell-connectRequired="props">
                <q-td :props="props" :class="(props.row.preconnectRequired=='' || props.row.connectRequired.label!=props.row.preconnectRequired.label)?'text-red':'text-black'">
                  {{props.row.connectRequired.label}}
                </q-td>
              </template>
              <template v-slot:body-cell-getResourceIDForProvenance="props">
                <q-td
                  :props="props"
                  :class="(props.row.pregetResourceIDForProvenance=='' ||
                           props.row.getResourceIDForProvenance.label!=props.row.pregetResourceIDForProvenance.label )
                           ?'text-red':'text-black'"
                >
                  {{props.row.getResourceIDForProvenance.label}}
                </q-td>
              </template>
              <template v-slot:body-cell-resourceIDForProvenance="props">
                <q-td :props="props" :class="(props.row.preresourceIDForProvenance=='' || props.row.resourceIDForProvenance!=props.row.preresourceIDForProvenance)?'text-red':'text-black'">
                  {{props.row.resourceIDForProvenance}}
                </q-td>
              </template>
              <template v-slot:body-cell-dataServiceTitle="props">
                <q-td :props="props" :class="(props.row.dataServiceTitle=='' || props.row.dataServiceTitle!=props.row.predataServiceTitle)?'text-red':'text-black'">
                  {{props.row.dataServiceTitle}}
                </q-td>
              </template>
              <template v-slot:body-cell-dataServiceEndpointUrl="props">
                <q-td :props="props" :class="(props.row.dataServiceEndpointUrl=='' || props.row.dataServiceEndpointUrl!=props.row.predataServiceEndpointUrl)?'text-red':'text-black'">
                  {{props.row.dataServiceEndpointUrl}}
                </q-td>
              </template>
              <template v-slot:body-cell-dataServiceEndpointDescription="props">
                <q-td :props="props" :class="(props.row.dataServiceEndpointDescription=='' || props.row.dataServiceEndpointDescription!=props.row.predataServiceEndpointDescription)?'text-red':'text-black'">
                  {{props.row.dataServiceEndpointDescription}}
                </q-td>
              </template>
            </q-table>
          </div>
          <div v-if="dataModelList.length" class="q-pa-md">
            <font size= '4'>NGSIデータモデル</font>
          </div>
          <div v-for="(item4, index4) in dataModelList" :key="index4">
            <div class="col-12 q-py-sm">
              <q-table
                :title="item4.index"
                :rows="item4.ngsiDataModel"
                :columns="dataModelColumns"
                row-key="index"
                :separator="cell"
              >
                <template v-slot:body="props">
                  <q-tr :props="props">
                    <q-td key="attribute" :props="props">
                      {{ props.row.attribute }}
                    </q-td>
                    <q-td key="dataType" :props="props">
                      {{ props.row.dataType }}
                    </q-td>
                    <q-td key="example" :props="props">
                      {{ props.row.example }}
                    </q-td>
                    <q-td key="description" :props="props">
                      {{ props.row.description }}
                    </q-td>
                    <q-td key="metadata" :props="props" class="metadata-btn">
                      <q-btn color="primary" outline class="full-width" :label="props.row.metadata.length ? 'あり' : 'なし'" field='metadata' :disable="!props.row.metadata.length" @click="createMetadataTable(props.row)"></q-btn>
                    </q-td>
                  </q-tr>
                </template>
              </q-table>
            </div>
          </div>
        </div>
      </q-card-section>
    </q-card>
    <q-card class="q-ma-sm q-card-background-white">
      <q-card-section>
        <div class="q-py-sm">
          <font size = '5' v-show="!store.datasetOptionAllHide">データセット情報（任意）</font>
          <font size = '4' v-show="store.datasetOptionAllHide" style="color: #1d468f;">データセット情報（任意）の入力項目はありません</font>          
        </div>
        <div class="q-py-sm" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.theme !== 'hide'">
          <font size = '4' color='#1d468f'>データセットの主分類</font>
          <div class="row justify-start items-end">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'under-line', 'fit', 'indent-item',
              { 'red-color': redCharFlg.theme }]">
              {{ displayValue.theme }}
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.theme"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.theme"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                v-model="displayType.theme"
                :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
              />
            </div>
          </div>
        </div>
        <div class="q-py-sm" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.tags !== 'hide'">
          <font size = '4' color='#1d468f'>データセットのキーワード</font>
          <div class="row justify-start items-end">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'under-line', 'fit', 'indent-item',
              { 'red-color': redCharFlg.tags }]">
              {{ displayValue.tags }}
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.tags"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.tags"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                v-model="displayType.tags"
                :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
              />
            </div>
          </div>
        </div>
        <div class="q-py-sm" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.language !== 'hide'">
          <font size = '4' color='#1d468f'>データセットの情報を記述する言語</font>
          <div class="row justify-start items-end">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'under-line', 'fit', 'indent-item',
              { 'red-color': redCharFlg.language }]">
              {{ displayValue.language }}
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.language"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.language"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                v-model="displayType.language"
                :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
              />
            </div>
          </div>
        </div>
        <div class="q-py-sm" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.vocabulary !== 'hide'">
          <font size = '4' color='#1d468f'>語彙</font>
          <div class="row justify-start items-end">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'under-line', 'fit', 'indent-item',
              { 'red-color': store.vocabulary !== store.hold.vocabulary && checkRedCharacterMode(store.selectedMode.mode)}]">
              {{ store.vocabulary }}
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.vocabulary"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.vocabulary"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                v-model="displayType.vocabulary"
                :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
              />
            </div>
          </div>
        </div>
        <div class="q-py-sm" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.term !== 'hide'">
          <font size = '4' color='#1d468f'>用語</font>
          <div class="row justify-start items-end">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'under-line', 'fit', 'indent-item',
              { 'red-color': store.term !== store.hold.term && checkRedCharacterMode(store.selectedMode.mode)}]">
              {{ store.term }}
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.term"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.term"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                v-model="displayType.term"
                :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
              />
            </div>
          </div>
        </div>
        <div class="q-py-sm" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.frequency !== 'hide'">
          <font size = '4' color='#1d468f'>データセットの提供頻度</font>
          <div class="row justify-start items-end">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'column', 'justify-center', 'under-line',
              { 'red-color': store.frequency !== store.hold.frequency && checkRedCharacterMode(store.selectedMode.mode)}]">
              {{ store.frequency.label }}
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.frequency"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.frequency"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                v-model="displayType.frequency"
                :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
              />
            </div>
          </div>
        </div>
        <div class="q-py-sm" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.spatial !== 'hide'">
          <div class="row justify-start items-center">
            <div class="col-10">
              <font size="4" color="#1d468f">データセットの対象地域</font>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.spatial"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.spatial"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                v-model="displayType.spatial"
                :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
              />
            </div>
          </div>
          <div class="row">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'column', 'justify-center', 'under-line',
              { 'red-color': store.geonames.spatialUrl !== store.hold.geonames.spatialUrl && checkRedCharacterMode(store.selectedMode.mode)}]">
              {{ store.geonames.spatialUrl }}
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'column', 'justify-center', 'under-line',
              { 'red-color': store.geonames.spatialName !== store.hold.geonames.spatialName && checkRedCharacterMode(store.selectedMode.mode)}]">
              {{ store.geonames.spatialName }}
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'column', 'justify-center', 'under-line',
              { 'red-color': store.geonames.spatial !== store.hold.geonames.spatial && checkRedCharacterMode(store.selectedMode.mode)}]">
              {{ store.geonames.spatial }}
              </div>
            </div>
          </div>
        </div>
        <div class="q-py-sm" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.temporal !== 'hide'">
          <div class="row justify-start items-center">
            <div class="col-10">
              <font size="4" color="#1d468f">データセットの対象期間</font>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.temporal"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.temporal"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                v-model="displayType.temporal"
                :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
              />
            </div>
          </div>
          <div class="row">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'column', 'justify-center', 'under-line',
              { 'red-color': store.dataCalender.start !== store.hold.dataCalender.start && checkRedCharacterMode(store.selectedMode.mode)}]">
              {{ store.dataCalender.start }}
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'column', 'justify-center', 'under-line',
              { 'red-color': store.dataCalender.end !== store.hold.dataCalender.end && checkRedCharacterMode(store.selectedMode.mode)}]">
              {{ store.dataCalender.end }}
              </div>
            </div>
          </div>
        </div>
      </q-card-section>
    </q-card>
    <q-card class="q-ma-sm q-card-background-white">
      <q-card-section>
        <div class="q-py-sm">
          <font size = '5' v-show="!store.useTermsAllHide">利用条件</font>
          <font size = '4' v-show="store.useTermsAllHide" style="color: #1d468f;">利用条件の入力項目はありません</font>          
        </div>
        <div class="q-pt-sm" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.licenseTitle !== 'hide'">
          <div class="row justify-start items-center">
            <div class="col-10">
              <font size="4" color="#1d468f">データセット・配信のライセンス</font>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.license"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.license"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                v-model="displayType.licenseTitle"
                :options="[TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
              />
            </div>
          </div>
        </div>
        <div class="q-pb-sm q-pl-md" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.licenseTitle !== 'hide'">
          <font size="4" color="#1d468f">データセット・配信のライセンス（説明）</font>
          <div class="row">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'column', 'justify-center', 'under-line',
              { 'red-color': store.termName.label !== store.hold.termName.label && checkRedCharacterMode(store.selectedMode.mode)}]">
              {{ store.termName.label }}
              </div>
            </div>
          </div>
        </div>
        <div class="q-pb-sm q-pl-md" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.licenseTitle !== 'hide'">
          <font size="4" color="#1d468f">データセット・配信のライセンス</font>
          <div class="row">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'column', 'justify-center', 'under-line',
              { 'red-color': store.termNameUrl !== store.hold.termNameUrl && checkRedCharacterMode(store.selectedMode.mode)}]">
              {{ store.termNameUrl }}
              </div>
            </div>
          </div>
        </div>
        <div class="q-py-sm" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.rights !== 'hide'">
          <font size="4" color="#1d468f">データセット・配信の権利表明</font>
          <div class="row justify-start items-end">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'under-line', 'fit', 'indent-item',
              { 'red-color': store.usrRight !== store.hold.usrRight && checkRedCharacterMode(store.selectedMode.mode)}]">
              {{ store.usrRight }}
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.rights"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.rights"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                v-model="displayType.rights"
                :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
              />
            </div>
          </div>
        </div>
        <div class="q-pt-sm" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.accessRights !== 'hide'">
          <div class="row justify-start items-center">
            <div class="col-10">
              <font size="4" color="#1d468f">データセット・配信のアクセス権</font>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.accessRights"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.accessRights"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                v-model="displayType.accessRights"
                :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
              />
            </div>
          </div>
        </div>
        <div class="q-pb-sm q-pl-md" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.accessRights !== 'hide'">
          <font size="4" color="#1d468f">データセット・配信のアクセス権（説明）</font>
          <div class="row">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'column', 'justify-center', 'under-line',
              { 'red-color': store.accessRights.label && store.accessRights.label !== store.hold.accessRights.label && checkRedCharacterMode(store.selectedMode.mode)}]">
              {{ store.accessRights.label }}
              </div>
            </div>
          </div>
        </div>
        <div class="q-pb-sm q-pl-md" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.accessRights !== 'hide'">
          <font size="4" color="#1d468f">データセット・配信のアクセス権</font>
          <div class="row">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'under-line', 'fit', 'indent-item',
              { 'red-color': store.accessRightsUrl !== store.hold.accessRightsUrl && checkRedCharacterMode(store.selectedMode.mode)}]">
              {{ store.accessRightsUrl }}
              </div>
            </div>
          </div>
        </div>
        <div class="q-py-sm" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.haspolicyUrl !== 'hide'">
          <font size="4" color="#1d468f">データセット・配信に関する権利情報URL</font>
          <div class="row justify-start items-end">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'under-line', 'fit', 'indent-item',
              { 'red-color': store.haspolicyUrl !== store.hold.haspolicyUrl && checkRedCharacterMode(store.selectedMode.mode)}]">
              {{ store.haspolicyUrl }}
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.haspolicyUrl"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.haspolicyUrl"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                v-model="displayType.haspolicyUrl"
                :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
              />
            </div>
          </div>
        </div>
        <div class="q-py-sm" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.provWasGeneratedByUrl !== 'hide'">
          <font size="4" color="#1d468f">データセットを生成した活動</font>
          <div class="row justify-start items-end">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'under-line', 'fit', 'indent-item',
              { 'red-color': store.provWasGeneratedByUrl !== store.hold.provWasGeneratedByUrl && checkRedCharacterMode(store.selectedMode.mode)}]">
              {{ store.provWasGeneratedByUrl }}
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.provWasGeneratedByUrl"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.provWasGeneratedByUrl"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                v-model="displayType.provWasGeneratedByUrl"
                :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
              />
            </div>
          </div>
        </div>
        <div class="q-py-sm" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.conformsTo !== 'hide'">
          <font size="4" color="#1d468f">データセット・配信が準拠する標準URL</font>
          <div class="row justify-start items-end">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'under-line', 'fit', 'indent-item',
              { 'red-color': store.conformsTo !== store.hold.conformsTo && checkRedCharacterMode(store.selectedMode.mode)}]">
              {{ store.conformsTo }}
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.conformsTo"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.conformsTo"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                v-model="displayType.conformsTo"
                :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
              />
            </div>
          </div>
        </div>
        <div class="q-py-md" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.tradingPolicyContractType !== 'hide' || store.itemDisplayFlg.tradingPolicyNda !== 'hide' || store.itemDisplayFlg.tradingPolicyUseApplication !== 'hide' || store.itemDisplayFlg.tradingPolicyUseApplication !== 'hide'">
          <font size="4" color="#1d468f">契約ポリシー</font>
        </div>
        <div class="q-pb-sm q-pl-md" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.tradingPolicyContractType !== 'hide'">
          <font size = '4' color='#1d468f'>契約形態</font>
          <div class="row justify-start items-end">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'column', 'justify-center', 'under-line',
              { 'red-color': store.contractType.label !== store.hold.contractType.label && checkRedCharacterMode(store.selectedMode.mode)}]">
              {{ store.contractType.label }}
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.tradingPolicyContractType"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.tradingPolicyContractType"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                v-model="displayType.tradingPolicyContractType"
                :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
              />
            </div>
          </div>
        </div>
        <div class="q-py-sm q-pl-md" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.tradingPolicyNda !== 'hide'">
          <font size = '4' color='#1d468f'>秘密保持義務</font>
          <div class="row justify-start items-end">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'column', 'justify-center', 'under-line',
              { 'red-color': store.secrecy.label !== store.hold.secrecy.label && checkRedCharacterMode(store.selectedMode.mode)}]">
              {{ store.secrecy.label }}
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.tradingPolicyNda"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.tradingPolicyNda"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                v-model="displayType.tradingPolicyNda"
                :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
              />
            </div>
          </div>
        </div>
        <div class="q-py-sm q-pl-md" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.tradingPolicyUseApplication !== 'hide'">
          <font size = '4' color='#1d468f'>利用用途</font>
          <div class="row justify-start items-end">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'under-line', 'fit', 'indent-item',
              { 'red-color': redCharFlg.useApplication }]">
              {{ displayValue.useApplication }}
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.tradingPolicyUseApplication"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.tradingPolicyUseApplication"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                v-model="displayType.tradingPolicyUseApplication"
                :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
              />
            </div>
          </div>
        </div>
        <div class="q-py-md" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.scopeOfDisclosure !== 'hide' || store.itemDisplayFlg.termsOfUsePermissibleRegion !== 'hide' || store.itemDisplayFlg.termsOfUseNotices !== 'hide'">
          <font size="4" color="#1d468f">データ利用条件</font>
        </div>
        <div class="q-pb-sm q-pl-md" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.scopeOfDisclosure !== 'hide'">
          <font size = '4' color='#1d468f'>開示範囲</font>
          <div class="row justify-start items-end">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'under-line', 'fit', 'indent-item',
              { 'red-color': redCharFlg.scopeOfDisclosure }]">
              {{ displayValue.scopeOfDisclosure }}
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.scopeOfDisclosure"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.scopeOfDisclosure"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                v-model="displayType.scopeOfDisclosure"
                :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
              />
            </div>
          </div>
        </div>
        <div class="q-py-sm q-pl-md" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.termsOfUsePermissibleRegion !== 'hide'">
          <font size = '4' color='#1d468f'>データ活用地域</font>
          <div class="row justify-start items-end">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'under-line', 'fit', 'indent-item',
              { 'red-color': redCharFlg.permissionResion }]">
              {{ displayValue.permissionResion }}
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.termsOfUsePermissibleRegion"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.termsOfUsePermissibleRegion"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                v-model="displayType.termsOfUsePermissibleRegion"
                :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
              />
            </div>
          </div>
        </div>
        <div class="q-py-sm q-pl-md" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.termsOfUseNotices !== 'hide'">
          <font size = '4' color='#1d468f'>利用に関する注意事項</font>
          <div class="row justify-start items-end">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'under-line', 'fit', 'indent-item',
              { 'red-color': store.notices !== store.hold.notices && checkRedCharacterMode(store.selectedMode.mode)}]">
              {{ store.notices }}
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.termsOfUseNotices"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.termsOfUseNotices"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                v-model="displayType.termsOfUseNotices"
                :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
              />
            </div>
          </div>
        </div>
        <div class="q-py-md" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.privacyPolicyContainsPersonalData !== 'hide'">
          <font size="4" color="#1d468f">データ保護要件</font>
        </div>
        <div class="q-pb-sm q-pl-md" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.privacyPolicyContainsPersonalData !== 'hide'">
          <font size = '4' color='#1d468f'>パーソナルデータの類別</font>
          <div class="row justify-start items-end">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'under-line', 'fit', 'indent-item',
              { 'red-color': redCharFlg.personalData }]">
              {{ displayValue.personalData }}
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.privacyPolicyContainsPersonalData"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.privacyPolicyContainsPersonalData"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                v-model="displayType.privacyPolicyContainsPersonalData"
                :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
              />
            </div>
          </div>
        </div>
        <div class="q-py-md" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.dataEffectivePeriod !== 'hide' || store.itemDisplayFlg.usageLicensePeriod !== 'hide'">
          <font size="4" color="#1d468f">利用期間</font>
        </div>
        <div class="q-pb-sm q-pl-md" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.dataEffectivePeriod !== 'hide'">
          <font size="4" color="#1d468f">データの有効期間</font>
          <div class="row justify-start items-end">
            <div class="col-10">
              <div v-if="displayFieldDataEffectivePeriod==='date'">
                <div v-bind:class="[
                'q-field__control', 'q-field__native', 'column', 'justify-center', 'under-line',
                { 'red-color': store.dataEffectivePeriod.startDate !== store.hold.dataEffectivePeriod.startDate && checkRedCharacterMode(store.selectedMode.mode)}]">
                開始日: {{ store.dataEffectivePeriod.startDate }}
                </div>
              </div>
              <div v-if="displayFieldDataEffectivePeriod==='date'">
                <div v-bind:class="[
                'q-field__control', 'q-field__native', 'column', 'justify-center', 'under-line',
                { 'red-color': store.dataEffectivePeriod.endDate !== store.hold.dataEffectivePeriod.endDate && checkRedCharacterMode(store.selectedMode.mode)}]">
                終了日: {{ store.dataEffectivePeriod.endDate }}
                </div>
              </div>
              <div v-if="displayFieldDataEffectivePeriod==='freefield'">
                <div v-bind:class="[
                'q-field__control', 'q-field__native', 'under-line', 'fit', 'indent-item',
                { 'red-color': store.dataEffectivePeriod.freefield !== store.hold.dataEffectivePeriod.freefield && checkRedCharacterMode(store.selectedMode.mode)}]">
                自由欄: {{ store.dataEffectivePeriod.freefield }}
                </div>
              </div>
              <div v-if="displayFieldDataEffectivePeriod==='none'">
                <div v-bind:class="[
                'q-field__control', 'q-field__native', 'column', 'justify-center', 'under-line',
                { 'red-color': store.dataEffectivePeriod.freefield !== store.hold.dataEffectivePeriod.freefield && checkRedCharacterMode(store.selectedMode.mode),
                'grey-color': store.selectedMode.mode === 'edit' === false || store.dataEffectivePeriod.freefield === store.hold.dataEffectivePeriod.freefield}]">
                None
                </div>
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.dataEffectivePeriod"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType==='detail'">
                <q-select
                  v-model="editFlg.dataEffectivePeriod"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode==='template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                v-model="displayType.dataEffectivePeriod"
                :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
              />
            </div>
          </div>
        </div>
        <div class="q-py-sm q-pl-md" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.usageLicensePeriod !== 'hide'">
          <font size="4" color="#1d468f">利用ライセンスの期限</font>
          <div class="row justify-start items-end">
            <div class="col-10">
              <div v-if="displayFieldUsageLicensePeriod==='deadline'">
                <div v-bind:class="[
                'q-field__control', 'q-field__native', 'column', 'justify-center', 'under-line',
                { 'red-color': store.usageLicensePeriod.deadline !== store.hold.usageLicensePeriod.deadline && checkRedCharacterMode(store.selectedMode.mode)}]">
                期限: {{ store.usageLicensePeriod.deadline }}
                </div>
              </div>
              <div v-if="displayFieldUsageLicensePeriod==='period'">
                <div v-bind:class="[
                'q-field__control', 'q-field__native', 'column', 'justify-center', 'under-line',
                { 'red-color': (store.usageLicensePeriod.period !== store.hold.usageLicensePeriod.period && checkRedCharacterMode(store.selectedMode.mode)) ||
                (store.usageLicensePeriod.unit !== store.hold.usageLicensePeriod.unit && store.selectedMode.mode === 'edit')}]">
                期間: {{ displayValue.period }}
                </div>
              </div>
              <div v-if="displayFieldUsageLicensePeriod==='freefield'">
                <div v-bind:class="[
                'q-field__control', 'q-field__native', 'under-line', 'fit', 'indent-item',
                { 'red-color': store.usageLicensePeriod.freefield !== store.hold.usageLicensePeriod.freefield && checkRedCharacterMode(store.selectedMode.mode)}]">
                自由欄: {{ store.usageLicensePeriod.freefield }}
                </div>
              </div>
              <div v-if="displayFieldUsageLicensePeriod==='none'">
                <div v-bind:class="[
                'q-field__control', 'q-field__native', 'column', 'justify-center', 'under-line',
                { 'red-color': store.usageLicensePeriod.freefield !== store.hold.usageLicensePeriod.freefield && checkRedCharacterMode(store.selectedMode.mode),
                'grey-color': store.selectedMode.mode === 'edit' === false || store.usageLicensePeriod.freefield === store.hold.usageLicensePeriod.freefield}]">
                None
                </div>
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.usageLicensePeriod"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.usageLicensePeriod"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                v-model="displayType.usageLicensePeriod"
                :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
              />
            </div>
          </div>
        </div>
        <div class="q-py-md" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.fee !== 'hide'|| store.itemDisplayFlg.salesInfoUrl !== 'hide' || store.itemDisplayFlg.pricingPriceRange !== 'hide' || store.itemDisplayFlg.pricingNoticesOfPrice !== 'hide'">
          <font size="4" color="#1d468f">支払い</font>
        </div>
        <div class="q-pb-sm q-pl-md" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.fee !== 'hide'">
          <font size = '4' color='#1d468f'>有償無償</font>
          <div class="row justify-start items-end">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'column', 'justify-center', 'under-line',
              { 'red-color': store.fee.label !== store.hold.fee.label && checkRedCharacterMode(store.selectedMode.mode)}]">
              {{ store.fee.label }}
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.fee"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.fee"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                v-model="displayType.fee"
                :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
              />
            </div>
          </div>
        </div>
        <div class="q-py-sm q-pl-md" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.salesInfoUrl !== 'hide'">
          <font size = '4' color='#1d468f'>販売情報</font>
          <div class="row justify-start items-end">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'under-line', 'fit', 'indent-item',
              { 'red-color': store.salesInfoUrl !== store.hold.salesInfoUrl && checkRedCharacterMode(store.selectedMode.mode)}]">
              {{ store.salesInfoUrl }}
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.salesInfoUrl"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.salesInfoUrl"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                v-model="displayType.salesInfoUrl"
                :options="[TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
              />
            </div>
          </div>
        </div>
        <div class="q-py-sm q-pl-md" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.pricingPriceRange !== 'hide'">
          <font size = '4' color='#1d468f'>価格帯</font>
          <div class="row justify-start items-end">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'under-line', 'fit', 'indent-item',
              { 'red-color': store.priceRange !== store.hold.priceRange && checkRedCharacterMode(store.selectedMode.mode)}]">
              {{ store.priceRange }}
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.pricingPriceRange"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.pricingPriceRange"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                v-model="displayType.pricingPriceRange"
                :options="[TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
              />
            </div>
          </div>
        </div>
        <div class="q-py-sm q-pl-md" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.pricingNoticesOfPrice !== 'hide'">
          <font size = '4' color='#1d468f'>データ販売に関わる特記事項</font>
          <div class="row justify-start items-end">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'under-line', 'fit', 'indent-item',
              { 'red-color': store.noticesOfPrice !== store.hold.noticesOfPrice && checkRedCharacterMode(store.selectedMode.mode)}]">
              {{ store.noticesOfPrice }}
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.pricingNoticesOfPrice"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.pricingNoticesOfPrice"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                v-model="displayType.pricingNoticesOfPrice"
                :options="[TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
              />
            </div>
          </div>
        </div>
        <div class="q-py-md" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.warrantyExpressWarranty !== 'hide' || store.itemDisplayFlg.warrantyLegalCompliance !== 'hide'">
          <font size="4" color="#1d468f">保証</font>
        </div>
        <div class="q-pb-sm q-pl-md" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.warrantyExpressWarranty !== 'hide'">
          <font size = '4' color='#1d468f'>明示された保証</font>
          <div class="row justify-start items-end">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'under-line', 'fit', 'indent-item',
              { 'red-color': redCharFlg.expressWarranty }]">
              {{ displayValue.expressWarranty }}
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.warrantyExpressWarranty"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.warrantyExpressWarranty"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                v-model="displayType.warrantyExpressWarranty"
                :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
              />
            </div>
          </div>
        </div>
        <div class="q-py-sm q-pl-md" v-show="store.selectedMode.mode === 'template' || store.itemDisplayFlg.warrantyLegalCompliance !== 'hide'">
          <font size = '4' color='#1d468f'>準拠法の対象国</font>
          <div class="row justify-start items-end">
            <div class="col-10">
              <div v-bind:class="[
              'q-field__control', 'q-field__native', 'under-line', 'fit', 'indent-item',
              { 'red-color': redCharFlg.leagalCompliance }]">
              {{ displayValue.leagalCompliance }}
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'edit'" class="col-2">
              <div v-if="store.selectedMode.ckanType === 'release' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.warrantyLegalCompliance"
                  :options="editDetailOption"
                />
              </div>
              <div v-if="store.selectedMode.ckanType === 'detail' && store.selectedMode.isBothCatalog">
                <q-select
                  v-model="editFlg.warrantyLegalCompliance"
                  :options="editReleaseOption"
                />
              </div>
            </div>
            <div v-if="store.selectedMode.mode === 'template'" class="col-2">
              <q-select
                label="表示形式"
                label-color="primary"
                v-model="displayType.warrantyLegalCompliance"
                :options="[TEMPLATE_DISPLAY_TYPE_MANDATORY, TEMPLATE_DISPLAY_TYPE_OPTIONAL, TEMPLATE_DISPLAY_TYPE_FOLD, TEMPLATE_DISPLAY_TYPE_HIDE]"
              />
            </div>
          </div>
        </div>
      </q-card-section>
    </q-card>

    <!-- メタデータダイアログ -->
    <q-dialog transition-show="scale" transition-hide="scale" full-width v-model="showMetadataDialog">
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
            <template v-slot:body="props">
              <q-tr :props="props">
                <q-td key="metadataName" :props="props">
                  {{ props.row.metadataName }}
                </q-td>
                <q-td key="dataType" :props="props">
                  {{ props.row.dataType }}
                </q-td>
                <q-td key="example" :props="props">
                  {{ props.row.example }}
                </q-td>
                <q-td key="description" :props="props">
                  {{ props.row.description }}
                </q-td>
              </q-tr>
            </template>
          </q-table>
          <p />
          <div align="right">
            <q-btn
              color="light-blue-10"
              label="閉じる"
              v-close-popup
            />
          </div>
        </div>
      </q-card>
    </q-dialog>
  </div>
</template>

<style lang="scss">
.q-card-background-white{
  background: white
}

.under-line{
  border-bottom: dashed 1px grey
}

.red-color{
  color: red
}

.grey-color{
  color: grey
}

.metadata-btn{
  width: 5px;
}

.resourceTable .q-table__top, .resourceTable .q-table__bottom, .resourceTable thead tr:first-child th{
  background-color: rgba(25, 118, 210, 0.1)
}

.dataset-confirm .indent-item{
 overflow-wrap: break-word;
}

.dataset-confirm .col-10 .q-field__control{
  min-height: 56px;
}
</style>
