<script setup>
import { config } from'boot/config'
import { reactive, ref, watch, onMounted, computed } from 'vue'
import axios from 'axios'
import { useStore } from '../stores/store'

const store = useStore()

const EMPTY_ERROR_MESSAGE = '【入力必須項目】'
const INVALID_ERROR_MESSAGE = '【無効な値】'

// 必須入力項目エラー文言（未入力）
const ERROR_MESSAGE = {
  usrRight: 'データセット・配信の権利表明は入力必須項目です。入力をお願いします。',
  accessRights: 'データセット・配信のアクセス権（説明）は入力必須項目です。入力をお願いします。',
  accessRightsUrl: 'データセット・配信のアクセス権は入力必須項目です。入力をお願いします。',
  haspolicyUrl: 'データセット・配信に関する権利情報URLは入力必須項目です。入力をお願いします。',
  provWasGeneratedByUrl: 'データセットを生成した活動は入力必須項目です。入力をお願いします。',
  conformsTo: 'データセット・配信が準拠する標準URLは入力必須項目です。入力をお願いします。',
  contractType: '契約形態は入力必須項目です。入力をお願いします。',
  secrecy: '秘密保持義務は入力必須項目です。入力をお願いします。',
  useApplication: '利用用途は入力必須項目です。入力をお願いします。',
  scopeOfDisclosure: '開示範囲は入力必須項目です。入力をお願いします。',
  permissionResion: 'データ活用地域は入力必須項目です。入力をお願いします。',
  notices: '利用に関する注意事項は入力必須項目です。入力をお願いします。',
  personalData: 'パーソナルデータの類別は入力必須項目です。入力をお願いします。',
  dataEffectivePeriod: 'データの有効期間は入力必須項目です。入力をお願いします。',
  usageLicensePeriod: '利用ライセンスの期限は入力必須項目です。入力をお願いします。',
  fee: '有償無償は入力必須項目です。入力をお願いします。',
  expressWarranty: '明示された保証は入力必須項目です。入力をお願いします。',
  leagalCompliance: '準拠法の対象国は入力必須項目です。入力をお願いします。'
}

// 入力項目エラー文言（無効値）
const ERROR_MESSAGE_INVALID = {
  dataEffectivePeriod: 'データの有効期間の終了日が開始日より前に設定されています。',
  invalidStartDateFormat: 'データの有効期間の開始日に無効な値が入力されています。',
  invalidEndDateFormat: 'データの有効期間の終了日に無効な値が入力されています。',
  invalidUsageLicensePeriodDeadline: '利用ライセンスの期限に無効な値が入力されています。'
}

// 入力項目エラー文言（使用禁止文字）
const ERROR_RESERVED_WORD = {
  useApplicationOther: '利用用途の自由欄に使用禁止文字が含まれています。',
  scopeOfDisclosureOther: '開示範囲の自由欄に使用禁止文字が含まれています。',
  permissionResionOther: 'データ活用地域の自由欄に使用禁止文字が含まれています。',
  personalDataOther: 'パーソナルデータの類別の自由欄に使用禁止文字が含まれています。',
  dataEffectivePeriod: 'データの有効期間の自由欄に使用禁止文字が含まれています。',
  usageLicensePeriod: '利用ライセンスの期限の自由欄に使用禁止文字が含まれています。',
  expressWarrantyOther: '明示された保証の自由欄に使用禁止文字が含まれています。',
  leagalComplianceOther: '準拠法の対象国の自由欄に使用禁止文字が含まれています。'
}

// カタログパラメータ名とCKAN変数名の紐づけデータ
const KEYMAP = {
  usrRight: 'rights',
  haspolicyUrl: 'haspolicy_url',
  provWasGeneratedByUrl: 'prov_was_generated_by_url',
  conformsTo: 'conforms_to',
  useApplication: 'trading_policy_use_application',
  scopeOfDisclosure: 'scope_of_disclosure',
  permissionResion: 'terms_of_use_permissible_region',
  personalData: 'privacy_policy_contains_personal_data',
  dataEffectivePeriod: 'data_effective_period',
  usageLicensePeriod: 'usage_license_period',
  salesInfoUrl: 'sales_info_url',
  noticesOfPrice: 'pricing_notices_of_price',
  expressWarranty: 'warranty_express_warranty',
  leagalCompliance: 'warranty_leagal_compliance'
}

const placeholderDate = ref('')

const attr = reactive({
  catalogParameter: {
    usrRight: store.usrRight,
    termName: store.termName,
    termNameUrl: store.termNameUrl,
    accessRights: store.accessRights,
    accessRightsUrl: store.accessRightsUrl,
    haspolicyUrl: store.haspolicyUrl,
    provWasGeneratedByUrl: store.provWasGeneratedByUrl,
    conformsTo: store.conformsTo,
    contractType: store.contractType,
    secrecy: store.secrecy,
    useApplication: store.useApplication,
    useApplicationOther: store.useApplicationOther,
    scopeOfDisclosure: store.scopeOfDisclosure,
    scopeOfDisclosureOther: store.scopeOfDisclosureOther,
    permissionResion: store.permissionResion,
    permissionResionOther: store.permissionResionOther,
    notices: store.notices,
    personalData: store.personalData,
    personalDataOther: store.personalDataOther,
    fee: store.fee,
    priceRange: store.priceRange,
    salesInfoUrl: store.salesInfoUrl,
    noticesOfPrice: store.noticesOfPrice,
    expressWarranty: store.expressWarranty,
    expressWarrantyOther: store.expressWarrantyOther,
    leagalCompliance: store.leagalCompliance,
    leagalComplianceOther: store.leagalComplianceOther,
    dataEffectivePeriod: {
      selectTerms: store.dataEffectivePeriod.selectTerms,
      startDate: store.dataEffectivePeriod.startDate,
      endDate: store.dataEffectivePeriod.endDate,
      freefield: store.dataEffectivePeriod.freefield
    },
    usageLicensePeriod: {
      selectTerms: store.usageLicensePeriod.selectTerms,
      deadline: store.usageLicensePeriod.deadline,
      period: store.usageLicensePeriod.period,
      unit: store.usageLicensePeriod.unit,
      freefield: store.usageLicensePeriod.freefield
    }
  },
  startCalenderFlg: false,
  endCalenderFlg: false,
  periodCalenderFlg: false,
  freeFieldColumn: {
    useApplication: false,
    scopeOfDisclosure: false,
    permissionResion: false,
    personalData: false,
    expressWarranty: false,
    leagalCompliance: false
  },
  dataEffectivePeriodField: {
    date: false,
    freeField: false
  },
  usageLicensePeriodField: {
    deadline: false,
    periodDulation: false,
    freeField: false
  },
  feeField: {
    salesInfoUrl: false,
    priceRange: false,
    noticesOfPrice: false
  },
  periodUnit: [
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
  ],
  errorCheckMessage: [],
  errorMessageReservedWord: '使用禁止文字が含まれています。',
  templateFlg: store.itemDisplayFlg,
  // 自動補完候補
  autoCorrect: {
    usrRight: [],
    haspolicyUrl: [],
    provWasGeneratedByUrl: [],
    conformsTo: [],
    useApplication: [],
    scopeOfDisclosure: [],
    permissionResion: [],
    personalData: [],
    dataEffectivePeriod: [],
    usageLicensePeriod: [],
    salesInfoUrl: [],
    noticesOfPrice: [],
    expressWarranty: [],
    leagalCompliance: []
  }
})

// 折りたたみ表示フラグ
const expanded = reactive({
  licenseTitle: '',
  licenseUrl: '',
  rights: '',
  accessRights: '',
  accessRightsUrl: '',
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

// 非表示フラグ
const hideFlgs = reactive({
  accessRights: '',
  conformsTo: '',
  fee: '',
  haspolicyUrl: '',
  licenseTitle: '',
  pricingNoticesOfPrice: '',
  pricingPriceRange: '',
  privacyPolicyContainsPersonalData: '',
  provWasGeneratedByUrl: '',
  rights: '',
  salesInfoUrl: '',
  termsOfUseNotices: '',
  termsOfUsePermissibleRegion: '',
  scopeOfDisclosure: '',
  tradingPolicyContractType: '',
  tradingPolicyNda: '',
  tradingPolicyUseApplication: '',
  dataEffectivePeriod: '',
  usageLicensePeriod: '',
  warrantyExpressWarranty: '',
  warrantyLegalCompliance: ''
})

// 表示項目がすべて非表示の場合にtrue
const isAllHide = computed( () => {
  // テンプレート編集中はfalse
  if(store.selectedMode.mode === 'template'){
    store.updateUseTermsAllHide(false)
    return false
  }

  for(var key in hideFlgs){
    // 1つでもhideでない項目があったら、falseを返す
    if (store.itemDisplayFlg[key] !== 'hide'){
      store.updateUseTermsAllHide(false)
      return false
    }
  }

  store.updateUseTermsAllHide(true)
  return true
})

// 入力する項目がない場合、表示されるメッセージの背景の高さを調整
const fillHeightClass = computed( () => {
  if(isAllHide.value){
    var parentHeight = document.getElementsByClassName('q-page')[0].offsetHeight;
    var stepHeaderHeight = document.getElementsByClassName('q-stepper__header')[0].offsetHeight;
    //50はフッター部の高さ
    var minHeight = parentHeight - (50 + stepHeaderHeight)

    return {'min-height' : minHeight + 'px'}
  }

  return {}
})

// method
// 自動補完候補取得
function filterFn(val, update, abort, field) {
  setTimeout(() => {
    update(() => {
      for (var ckanLabel in KEYMAP) {
        // カタログのフィールド名に紐づくCKAN変数名を取得
        if (field === ckanLabel) {
          var key = KEYMAP[ckanLabel]
        }
      }
      var req = {
        label: key,
        value: val
      }
      // 自動補完候補検索API実行
      axios
        .post(config.apiPrefix + '/datacatalog/autocorrect', req)
        .then((response) => {
          const needle = val.toLowerCase()
          // 自動補完候補の重複削除
          var autoOption = response.data.candidates.filter(v => v.toLowerCase().indexOf(needle) > -1)
          attr.autoCorrect[field] = autoOption
        })
        .catch(err => {
          attr.autoCorrect[field] = []
          console.log('error message:', err.response.data.message)
        })
    })
  }, 100)
}

// 自動補完フィールドの入力値をv-modelに設定
function setModel(val, field) {
  if (field === 'dataEffectivePeriod' || field === 'usageLicensePeriod') {
    // データセットの有効期間またはライセンスの利用期限
    attr.catalogParameter[field].freefield = val
    return
  }
  attr.catalogParameter[field] = val
}

// 必須フィールドエラー判定
function isError(displayFlg, value, type) {
  if (type === 'startDate') {
    if (value && attr.catalogParameter.dataEffectivePeriod.endDate && (value > attr.catalogParameter.dataEffectivePeriod.endDate)) {
      // 開始日が終了日より後の場合はエラー
      return true
    }
  } else if (type === 'endDate') {
    if (value && attr.catalogParameter.dataEffectivePeriod.startDate && (value < attr.catalogParameter.dataEffectivePeriod.startDate)) {
      // 終了日が開始日より前の場合はエラー
      return true
    }
  }
  if (store.selectedMode.mode === 'template') {
    // テンプレート編集時は、空判定をしない
    return false
  }
  if (displayFlg !== 'mandatory') {
    // 必須入力フィールドではないためエラーにしない
    return false
  }
  if (type === 'list') {
    if (!value.length) {
      // フィールドの配列が空の場合はエラー
      return true
    }
  } else {
    if (!value) {
      // フィールドが空の場合はエラー
      return true
    }
  }
  // 入力値問題なし
  return false
}

// 自由欄カンマ入力判定
function isCommaError(val) {
  if (val.match(/,/)) {
    return true
  }
}

function isValidDateFormat(value) {
  if (!/^-?[0-9]{4}\-(0[1-9]||1[0-2])\-(0[1-9]|[12][0-9]|3[01])$/.test(value)) {
    return false
  }
  if (value.indexOf('02-30') !== -1 || value.indexOf('02-31') !== -1 || value.indexOf('04-31') !== -1 || value.indexOf('06-31') !== -1 || value.indexOf('09-31') !== -1 || value.indexOf('11-31') !== -1) {
    return false
  }
  if (value.indexOf('02-29') !== -1) {
    let year = value.slice(0, 4)
    if ((year % 4 == 0) && (year % 100 != 0) || (year % 400 == 0)) {
      return true
    } else {
      return false
    }
  }
  let date = new Date(value)
  return !isNaN(date.getDate())
}

// エラーメッセージ生成
function errorFieldMessage(value, type) {
  if (type === 'startDate') {
    if (value && attr.catalogParameter.dataEffectivePeriod.endDate && (value > attr.catalogParameter.dataEffectivePeriod.endDate)) {
      // 開始日が終了日より後の場合はエラー
      return INVALID_ERROR_MESSAGE
    }
  } else if (type === 'endDate') {
    if (value && attr.catalogParameter.dataEffectivePeriod.startDate && (value < attr.catalogParameter.dataEffectivePeriod.startDate)) {
      // 終了日が開始日より前の場合はエラー
      return INVALID_ERROR_MESSAGE
    }
  }
  if (store.selectedMode.mode === 'template') {
    // テンプレート編集時は、空判定をしない
    return ''
  }
  if (type === 'list') {
    if (!value.length) {
      // フィールドの配列が空の場合はエラー
      return EMPTY_ERROR_MESSAGE
    }
  } else {
    if (!value) {
      // フィールドが空の場合はエラー
      return EMPTY_ERROR_MESSAGE
    }
  }
}

// データセットのライセンスURLの自動入力
function autoInputTermNameUrl() {
  for (var num = 0; num < store.ckanItemList.licenseId.length; num++) {
    if (store.ckanItemList.licenseId[num].value === attr.catalogParameter.termName.value) {
    // データセットのライセンスに紐づくライセンスURLを入力
      attr.catalogParameter.termNameUrl = store.ckanItemList.licenseId[num].url
      break
    }
  }
}

// データセット・配信のアクセス権の自動入力
function autoInputAccessRightsUrl() {
  for (var num = 0; num < store.itemList.accessRights.length; num++) {
    if (store.itemList.accessRights[num].value === attr.catalogParameter.accessRights.value) {
      attr.catalogParameter.accessRightsUrl = attr.catalogParameter.accessRights.label === 'その他' ? '' : store.itemList.accessRights[num].value
      break
    }
  }
}

function startCalenderClose() {
  attr.catalogParameter.dataEffectivePeriod.startDate = attr.catalogParameter.dataEffectivePeriod.startDate.split('T')[0].replace(/\//g, '-')
  attr.startCalenderFlg = false
}

function endCalenderClose() {
  attr.catalogParameter.dataEffectivePeriod.endDate = attr.catalogParameter.dataEffectivePeriod.endDate.split('T')[0].replace(/\//g, '-')
  attr.endCalenderFlg = false
}

function periodCalenderClose() {
  attr.catalogParameter.usageLicensePeriod.deadline = attr.catalogParameter.usageLicensePeriod.deadline.split('T')[0].replace(/\//g, '-')
  attr.periodCalenderFlg = false
}

function startCalender() {
  attr.startCalenderFlg = true
}

function endCalender() {
  attr.endCalenderFlg = true
}

function periodCalender() {
  attr.periodCalenderFlg = true
}

// 表示フィールドの制御
function showField() {
  const fieldType = {
    useApplication: 'list',
    scopeOfDisclosure: 'object',
    permissionResion: 'list',
    personalData: 'object',
    dataEffectivePeriod: 'object',
    usageLicensePeriod: 'object',
    fee: 'object',
    expressWarranty: 'object',
    leagalCompliance: 'list'
  }
  for (var key in attr.catalogParameter) {
    for (var type in fieldType) {
      if (key !== type) {
        continue
      }
      switch (key) {
        case 'dataEffectivePeriod':
          // データセットの有効期間
          if (attr.catalogParameter[key].selectTerms.value === 'date') {
            // 開始日・終了日を選択
            attr.dataEffectivePeriodField.date = true
            attr.dataEffectivePeriodField.freeField = false
          } else if (attr.catalogParameter.dataEffectivePeriod.selectTerms.value === 'note') {
            // 自由記述を選択
            attr.dataEffectivePeriodField.date = false
            attr.dataEffectivePeriodField.freeField = true
          } else {
            // 未選択
            attr.dataEffectivePeriodField.date = false
            attr.dataEffectivePeriodField.freeField = false
          }
          break
        case 'usageLicensePeriod':
          // 利用ライセンスの期限
          if (attr.catalogParameter[key].selectTerms.value === 'endDate') {
          // 期限を選択
            attr.usageLicensePeriodField.deadline = true
            attr.usageLicensePeriodField.periodDulation = false
            attr.usageLicensePeriodField.freeField = false
          } else if (attr.catalogParameter[key].selectTerms.value === 'value') {
            // 期間を選択
            attr.usageLicensePeriodField.periodDulation = true
            attr.usageLicensePeriodField.deadline = false
            attr.usageLicensePeriodField.freeField = false
          } else if (attr.catalogParameter[key].selectTerms.value === 'note') {
            // 自由記述を選択
            attr.usageLicensePeriodField.freeField = true
            attr.usageLicensePeriodField.deadline = false
            attr.usageLicensePeriodField.periodDulation = false
          } else {
            // 未選択
            attr.usageLicensePeriodField.deadline = false
            attr.usageLicensePeriodField.periodDulation = false
            attr.usageLicensePeriodField.freeField = false
          }
          break
        case 'fee':
          // 有償無償
          if (attr.catalogParameter[key].value === '有償') {
            // 有償を選択
            for (var field in attr.feeField) {
              attr.feeField[field] = true
            }
          } else {
            // 無償を選択
            for (field in attr.feeField) {
              attr.feeField[field] = false
            }
          }
          break
        default:
          if (fieldType[type] === 'list') {
            for (var i = 0; i < attr.catalogParameter[key].length; i++) {
              if (attr.catalogParameter[key][i].label === 'その他') {
                attr.freeFieldColumn[key] = true
                break
              }
            }
          } else {
            // if (attr.catalogParameter[key].value === 'その他') {
            if (attr.catalogParameter[key].label === 'その他') {
              // その他（自由記述）を選択
              attr.freeFieldColumn[key] = true
            } else {
              // その他（自由記述）を未選択
              attr.freeFieldColumn[key] = false
            }
          }
          break
      }
    }
  }
}

function topScroll() {
  window.scrollTo(0, 0)
}

// パラメータ更新
function commitStore() {
  store.updateUserTerms({
      termName: attr.catalogParameter.termName,
      termNameUrl: attr.catalogParameter.termNameUrl,
      usrRight: attr.catalogParameter.usrRight,
      accessRights: attr.catalogParameter.accessRights,
      accessRightsUrl: attr.catalogParameter.accessRightsUrl,
      haspolicyUrl: attr.catalogParameter.haspolicyUrl,
      provWasGeneratedByUrl: attr.catalogParameter.provWasGeneratedByUrl,
      conformsTo: attr.catalogParameter.conformsTo,
      contractType: attr.catalogParameter.contractType,
      secrecy: attr.catalogParameter.secrecy,
      useApplication: attr.catalogParameter.useApplication,
      useApplicationOther: attr.catalogParameter.useApplicationOther,
      scopeOfDisclosure: attr.catalogParameter.scopeOfDisclosure,
      scopeOfDisclosureOther: attr.catalogParameter.scopeOfDisclosureOther,
      permissionResion: attr.catalogParameter.permissionResion,
      permissionResionOther: attr.catalogParameter.permissionResionOther,
      notices: attr.catalogParameter.notices,
      personalData: attr.catalogParameter.personalData,
      personalDataOther: attr.catalogParameter.personalDataOther,
      dataEffectivePeriodSelectTerms: attr.catalogParameter.dataEffectivePeriod.selectTerms,
      startDate: attr.catalogParameter.dataEffectivePeriod.startDate,
      endDate: attr.catalogParameter.dataEffectivePeriod.endDate,
      dataEffectivePeriodFreefield: attr.catalogParameter.dataEffectivePeriod.freefield,
      usageLicensePeriodSelectTerms: attr.catalogParameter.usageLicensePeriod.selectTerms,
      deadline: attr.catalogParameter.usageLicensePeriod.deadline,
      period: attr.catalogParameter.usageLicensePeriod.period,
      unit: attr.catalogParameter.usageLicensePeriod.unit,
      usageLicensePeriodFreefield: attr.catalogParameter.usageLicensePeriod.freefield,
      fee: attr.catalogParameter.fee,
      salesInfoUrl: attr.catalogParameter.salesInfoUrl,
      priceRange: attr.catalogParameter.priceRange,
      noticesOfPrice: attr.catalogParameter.noticesOfPrice,
      expressWarranty: attr.catalogParameter.expressWarranty,
      expressWarrantyOther: attr.catalogParameter.expressWarrantyOther,
      leagalCompliance: attr.catalogParameter.leagalCompliance,
      leagalComplianceOther: attr.catalogParameter.leagalComplianceOther,
      storeType: 'state'
    })
}

// データの有効期間 入力値のクリア
function clearDataEffectivePeriod() {
  attr.catalogParameter.dataEffectivePeriod.selectTerms = ''
  attr.catalogParameter.dataEffectivePeriod.startDate = ''
  attr.catalogParameter.dataEffectivePeriod.endDate = ''
  attr.catalogParameter.dataEffectivePeriod.freefield = ''
}

// 利用ライセンスの期限 入力値のクリア
function clearUsageLicensePeriod() {
  attr.catalogParameter.usageLicensePeriod.selectTerms = ''
  attr.catalogParameter.usageLicensePeriod.deadline = ''
  attr.catalogParameter.usageLicensePeriod.period = ''
  attr.catalogParameter.usageLicensePeriod.unit = ''
  attr.catalogParameter.usageLicensePeriod.freefield = ''
}

// 現在の日付を取得する
function getCurrentDate() {
  var currentData = new Date()
  var year = currentData.getFullYear()
  var month = currentData.getMonth()+1
  var day = currentData.getDate()
  placeholderDate.value = year + "-" + month + "-" + day
}

// エラーフラグの管理機能
function checkErrorAllFields() {
  const checkMandatory = {
    usrRight: attr.templateFlg.rights,
    accessRights: attr.templateFlg.accessRights,
    accessRightsUrl: attr.templateFlg.accessRightsUrl,
    haspolicyUrl: attr.templateFlg.haspolicyUrl,
    provWasGeneratedByUrl: attr.templateFlg.provWasGeneratedByUrl,
    conformsTo: attr.templateFlg.conformsTo,
    contractType: attr.templateFlg.tradingPolicyContractType,
    secrecy: attr.templateFlg.tradingPolicyNda,
    useApplication: attr.templateFlg.tradingPolicyUseApplication,
    scopeOfDisclosure: attr.templateFlg.scopeOfDisclosure,
    permissionResion: attr.templateFlg.termsOfUsePermissibleRegion,
    notices: attr.templateFlg.termsOfUseNotices,
    personalData: attr.templateFlg.privacyPolicyContainsPersonalData,
    dataEffectivePeriod: attr.templateFlg.dataEffectivePeriod,
    usageLicensePeriod: attr.templateFlg.usageLicensePeriod,
    fee: attr.templateFlg.fee,
    expressWarranty: attr.templateFlg.warrantyExpressWarranty,
    leagalCompliance: attr.templateFlg.warrantyLegalCompliance
  }
  const checkOtherField = [
    'useApplicationOther',
    'scopeOfDisclosureOther',
    'permissionResionOther',
    'personalDataOther',
    'dataEffectivePeriod',
    'usageLicensePeriod',
    'expressWarrantyOther',
    'leagalComplianceOther'
  ]
  const dataType = {
    usrRight: 'string',
    accessRights: 'object',
    accessRightsUrl: 'string',
    haspolicyUrl: 'string',
    provWasGeneratedByUrl: 'string',
    conformsTo: 'string',
    contractType: 'object',
    secrecy: 'object',
    useApplication: 'list',
    scopeOfDisclosure: 'object',
    permissionResion: 'list',
    notices: 'string',
    personalData: 'object',
    dataEffectivePeriod: 'object',
    usageLicensePeriod: 'object',
    fee: 'object',
    expressWarranty: 'object',
    leagalCompliance: 'list'
  }
  var noError = true
  attr.errorCheckMessage = []

  // 開始日に無効な値が入力されているかの判定
  if (attr.catalogParameter.dataEffectivePeriod.startDate) {
    if(!isValidDateFormat(attr.catalogParameter.dataEffectivePeriod.startDate)){
      attr.errorCheckMessage.push(ERROR_MESSAGE_INVALID.invalidStartDateFormat)
      noError = false
    }
  }

  // 終了日に無効な値が入力されているかの判定
  if (attr.catalogParameter.dataEffectivePeriod.endDate) {
    if(!isValidDateFormat(attr.catalogParameter.dataEffectivePeriod.endDate)){
      attr.errorCheckMessage.push(ERROR_MESSAGE_INVALID.invalidEndDateFormat)
      noError = false
    }
  }

  // 期限に無効な値が入力されているかの判定
  if (attr.catalogParameter.usageLicensePeriod.deadline) {
    if(!isValidDateFormat(attr.catalogParameter.usageLicensePeriod.deadline)){
      attr.errorCheckMessage.push(ERROR_MESSAGE_INVALID.invalidUsageLicensePeriodDeadline)
      noError = false
    }
  }

  if (attr.catalogParameter.dataEffectivePeriod.startDate && attr.catalogParameter.dataEffectivePeriod.endDate) {
    // データの有効期間の開始日と終了日が入力されている場合は、終了日が開始日より後になっていることを確認
    if (isError(checkMandatory.dataEffectivePeriod, attr.catalogParameter.dataEffectivePeriod.startDate, 'startDate') ||
    isError(checkMandatory.dataEffectivePeriod, attr.catalogParameter.dataEffectivePeriod.endDate, 'endDate')) {
      attr.errorCheckMessage.push(ERROR_MESSAGE_INVALID.dataEffectivePeriod)
      noError = false
    }
  }
  for (var field of checkOtherField) {
    // 自由欄に使用禁止文字（,）が含まれているか判定
    if (field === 'dataEffectivePeriod' || field === 'usageLicensePeriod') {
      if (isCommaError(attr.catalogParameter[field].freefield)) {
        noError = false
        attr.errorCheckMessage.push(ERROR_RESERVED_WORD[field])
      }
    } else {
      if (isCommaError(attr.catalogParameter[field])) {
        noError = false
        attr.errorCheckMessage.push(ERROR_RESERVED_WORD[field])
      }
    }
  }
  if (store.selectedMode.mode === 'template') {
    // テンプレート編集時は空値判定をしない
    return noError
  }
  for (var checkKey in checkMandatory) {
    if (checkMandatory[checkKey] !== 'mandatory') {
      // 必須フィールドではない
      continue
    }
    switch (checkKey) {
      // データの有効期間空値判定
      case 'dataEffectivePeriod':
        if (isError(checkMandatory[checkKey], attr.catalogParameter[checkKey].selectTerms, dataType[checkKey])) {
          attr.errorCheckMessage.push(ERROR_MESSAGE[checkKey])
          noError = false
        } else {
          if (!attr.catalogParameter[checkKey].selectTerms.value || attr.catalogParameter[checkKey].selectTerms.value !== 'date') {
            break
          }
          if (!attr.catalogParameter[checkKey].startDate || !attr.catalogParameter[checkKey].endDate) {
            attr.errorCheckMessage.push(ERROR_MESSAGE[checkKey])
            noError = false
          }
        }
        break
      // 利用ライセンスの期限空値判定
      case 'usageLicensePeriod':
        if (isError(checkMandatory[checkKey], attr.catalogParameter[checkKey].selectTerms, dataType[checkKey])) {
          attr.errorCheckMessage.push(ERROR_MESSAGE[checkKey])
          noError = false
        } else {
          if (attr.catalogParameter[checkKey].selectTerms.value === 'endDate' && !attr.catalogParameter[checkKey].deadline) {
            attr.errorCheckMessage.push(ERROR_MESSAGE[checkKey])
            noError = false
          } else if (attr.catalogParameter[checkKey].selectTerms.value === 'value' && (!attr.catalogParameter[checkKey].period || !attr.catalogParameter[checkKey].unit)) {
            attr.errorCheckMessage.push(ERROR_MESSAGE[checkKey])
            noError = false
          }
        }
        break
      // その他のフィールドの空値判定
      default:
        if (isError(checkMandatory[checkKey], attr.catalogParameter[checkKey], dataType[checkKey])) {
          attr.errorCheckMessage.push(ERROR_MESSAGE[checkKey])
          noError = false
        }
        break
    }
  }
  return noError
}

// mounted
onMounted(function(){
  console.log('-- DatasetUseTerms.vue onMounted --')

  topScroll()
  getCurrentDate()
  showField()
})

// watch
// データセット・配信のライセンス(説明)の監視
watch(() => attr.catalogParameter.termName,
  (newReg, oldReg) => {
  autoInputTermNameUrl()
})

// データセット・配信のアクセス権(説明)の監視
watch(() => attr.catalogParameter.accessRights,
  (newReg, oldReg) => {
  autoInputAccessRightsUrl()
})

// 利用用途の入力値監視
watch(() => attr.catalogParameter.useApplication,
  (newReg, oldReg) => {
  var obj = newReg
  const search = 'その他'
  if (obj !== [] && obj !== null) {
    var objMatch = obj.filter(function (item, index) {
      if (item.value === search) {
        return true
      }
    })
    if (objMatch !== [] && objMatch !== null) {
      if (objMatch.length !== 0) {
        attr.freeFieldColumn.useApplication = true
      } else {
        attr.freeFieldColumn.useApplication = false
        attr.catalogParameter.useApplicationOther = ''
      }
    } else {
      attr.freeFieldColumn.useApplication = false
      attr.catalogParameter.useApplicationOther = ''
    }
  }
})

// 開示範囲の入力値監視
watch(() => attr.catalogParameter.scopeOfDisclosure,
  (newReg, oldReg) => {
  showField()
  if (!attr.freeFieldColumn.scopeOfDisclosure) {
    // 自由記述が選択されていなければ、自由記述フィールドを空にする
    attr.catalogParameter.scopeOfDisclosureOther = ''
  }
})

// データ活用地域の入力値監視
watch(() => attr.catalogParameter.permissionResion,
  (newReg, oldReg) => {
  var obj = newReg
  const search = 'その他'
  if (obj !== [] && obj !== null) {
    var objMatch = obj.filter(function (item, index) {
      if (item.value === search) {
        return true
      }
    })
    if (objMatch !== [] && objMatch !== null) {
      if (objMatch.length !== 0) {
        attr.freeFieldColumn.permissionResion = true
      } else {
        attr.freeFieldColumn.permissionResion = false
        attr.catalogParameter.permissionResionOther = ''
      }
    } else {
      attr.freeFieldColumn.permissionResion = false
      attr.catalogParameter.permissionResionOther = ''
    }
  }
})

// パーソナルデータの類別の入力値監視
watch(() => attr.catalogParameter.personalData,
  (newReg, oldReg) => {
  showField()
  if (!attr.freeFieldColumn.personalData) {
    // 自由記述が選択されていなければ、自由記述フィールドを空にする
    attr.catalogParameter.personalDataOther = ''
  }
})

// データの有効期間入力値監視
watch(() => attr.catalogParameter.dataEffectivePeriod.selectTerms,
  (newReg, oldReg) => {
  // 選択値が変更された場合、開始日・終了日、自由記述フィールドを空にする
  attr.catalogParameter.dataEffectivePeriod.startDate = ''
  attr.catalogParameter.dataEffectivePeriod.endDate = ''
  attr.catalogParameter.dataEffectivePeriod.freefield = ''
  showField()
})

// 利用ライセンスの期限の入力値監視
watch(() => attr.catalogParameter.usageLicensePeriod.selectTerms,
  (newReg, oldReg) => {
  // 選択値が変更された場合、期限、期間、自由記述フィールドを空にする
  attr.catalogParameter.usageLicensePeriod.deadline = ''
  attr.catalogParameter.usageLicensePeriod.period = ''
  attr.catalogParameter.usageLicensePeriod.unit = ''
  attr.catalogParameter.usageLicensePeriod.freefield = ''
  showField()
})

// 有償無償の入力値監視
watch(() => attr.catalogParameter.fee,
  (newReg, oldReg) => {
  // 選択値が変更された場合、販売情報、価格帯、データ販売に関わる特記事項フィールドを空にする
  attr.catalogParameter.salesInfoUrl = ''
  attr.catalogParameter.priceRange = ''
  attr.catalogParameter.noticesOfPrice = ''
  showField()
})

// 明示された保証の入力値監視
watch(() => attr.catalogParameter.expressWarranty,
  (newReg, oldReg) => {
  showField()
  if (!attr.freeFieldColumn.expressWarranty) {
    // 自由記述が選択されていなければ、自由記述フィールドを空にする
    attr.catalogParameter.expressWarrantyOther = ''
  }
})

// 準拠法の対象国の入力値監視
watch(() => attr.catalogParameter.leagalCompliance,
  (newReg, oldReg) => {
  var obj = newReg
  const search = 'その他'
  if (obj !== [] && obj !== null) {
    var objMatch = obj.filter(function (item, index) {
      if (item.value === search) {
        return true
      }
    })
    if (objMatch !== [] && objMatch !== null) {
      if (objMatch.length !== 0) {
        attr.freeFieldColumn.leagalCompliance = true
      } else {
        attr.freeFieldColumn.leagalCompliance = false
        attr.catalogParameter.leagalComplianceOther = ''
      }
    } else {
      attr.freeFieldColumn.leagalCompliance = false
      attr.catalogParameter.leagalComplianceOther = ''
    }
  }
})

// created
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

// 自動補完候補デフォルト設定
// データセット・配信の権利表明
axios
  .post(config.apiPrefix + '/datacatalog/autocorrect', { label: 'rights', value: attr.catalogParameter.usrRight })
  .then((response) => {
    attr.autoCorrect.usrRight = response.data.candidates
  })
  .catch(err => {
    attr.autoCorrect.usrRight = []
    console.log('error message:', err.response.data.message)
  })

// データセット・配信に関する権利情報URL
axios
  .post(config.apiPrefix + '/datacatalog/autocorrect', { label: 'haspolicy_url', value: attr.catalogParameter.provWasGeneratedByUrl })
  .then((response) => {
    attr.autoCorrect.provWasGeneratedByUrl = response.data.candidates
  })
  .catch(err => {
    attr.autoCorrect.provWasGeneratedByUrl = []
    console.log('error message:', err.response.data.message)
  })

// データセットを生成した活動
axios
  .post(config.apiPrefix + '/datacatalog/autocorrect', { label: 'prov_was_generated_by_url', value: attr.catalogParameter.haspolicyUrl })
  .then((response) => {
    attr.autoCorrect.haspolicyUrl = response.data.candidates
  })
  .catch(err => {
    attr.autoCorrect.haspolicyUrl = []
    console.log('error message:', err.response.data.message)
  })

// データセット・配信が準拠する標準URL
axios
  .post(config.apiPrefix + '/datacatalog/autocorrect', { label: 'conforms_to', value: attr.catalogParameter.conformsTo })
  .then((response) => {
    attr.autoCorrect.conformsTo = response.data.candidates
  })
  .catch(err => {
    attr.autoCorrect.conformsTo = []
    console.log('error message:', err.response.data.message)
  })

// 利用用途（自由欄）
axios
  .post(config.apiPrefix + '/datacatalog/autocorrect', { label: 'trading_policy_use_application', value: attr.catalogParameter.useApplicationOther })
  .then((response) => {
    attr.autoCorrect.useApplication = response.data.candidates
  })
  .catch(err => {
    attr.autoCorrect.useApplication = []
    console.log('error message:', err.response.data.message)
  })

// 開示範囲（自由欄）
axios
  .post(config.apiPrefix + '/datacatalog/autocorrect', { label: 'scope_of_disclosure', value: attr.catalogParameter.scopeOfDisclosureOther })
  .then((response) => {
    attr.autoCorrect.scopeOfDisclosure = response.data.candidates
  })
  .catch(err => {
    attr.autoCorrect.scopeOfDisclosure = []
    console.log('error message:', err.response.data.message)
  })

// データ活用地域（自由欄）
axios
  .post(config.apiPrefix + '/datacatalog/autocorrect', { label: 'terms_of_use_permissible_region', value: attr.catalogParameter.permissionResionOther })
  .then((response) => {
    attr.autoCorrect.permissionResion = response.data.candidates
  })
  .catch(err => {
    attr.autoCorrect.permissionResion = []
    console.log('error message:', err.response.data.message)
  })

// パーソナルデータの類別（自由欄）
axios
  .post(config.apiPrefix + '/datacatalog/autocorrect', { label: 'privacy_policy_contains_personal_data', value: attr.catalogParameter.personalDataOther })
  .then((response) => {
    attr.autoCorrect.personalData = response.data.candidates
  })
  .catch(err => {
    attr.autoCorrect.personalData = []
    console.log('error message:', err.response.data.message)
  })

// データの有効期間（自由記述）
axios
  .post(config.apiPrefix + '/datacatalog/autocorrect', { label: 'data_effective_period', value: attr.catalogParameter.dataEffectivePeriod.freefield })
  .then((response) => {
    attr.autoCorrect.dataEffectivePeriod = response.data.candidates
  })
  .catch(err => {
    attr.autoCorrect.dataEffectivePeriod = []
    console.log('error message:', err.response.data.message)
  })

// 利用ライセンスの期限（自由記述）
axios
  .post(config.apiPrefix + '/datacatalog/autocorrect', { label: 'usage_license_period', value: attr.catalogParameter.usageLicensePeriod.freefield })
  .then((response) => {
    attr.autoCorrect.usageLicensePeriod = response.data.candidates
  })
  .catch(err => {
    attr.autoCorrect.usageLicensePeriod = []
    console.log('error message:', err.response.data.message)
  })

// 販売情報
axios
  .post(config.apiPrefix + '/datacatalog/autocorrect', { label: 'sales_info_url', value: attr.catalogParameter.salesInfoUrl })
  .then((response) => {
    attr.autoCorrect.salesInfoUrl = response.data.candidates
  })
  .catch(err => {
    attr.autoCorrect.salesInfoUrl = 
    console.log('error message:', err.response.data.message)
  })

// データ販売に関わる特記事項
axios
  .post(config.apiPrefix + '/datacatalog/autocorrect', { label: 'pricing_notices_of_price', value: attr.catalogParameter.noticesOfPrice })
  .then((response) => {
    attr.autoCorrect.noticesOfPrice = response.data.candidates
  })
  .catch(err => {
    attr.autoCorrect.noticesOfPrice = []
    console.log('error message:', err.response.data.message)
  })

// 明示された保証（自由欄）
axios
  .post(config.apiPrefix + '/datacatalog/autocorrect', { label: 'warranty_express_warranty', value: attr.catalogParameter.expressWarrantyOther })
  .then((response) => {
    attr.autoCorrect.expressWarranty = response.data.candidates
  })
  .catch(err => {
    attr.autoCorrect.expressWarranty = []
    console.log('error message:', err.response.data.message)
  })

// 準拠法の対象国（自由欄）
axios
  .post(config.apiPrefix + '/datacatalog/autocorrect', { label: 'warranty_leagal_compliance', value: attr.catalogParameter.leagalComplianceOther })
  .then((response) => {
    attr.autoCorrect.leagalCompliance = response.data.candidates
  })
  .catch(err => {
    attr.autoCorrect.leagalCompliance = []
    console.log('error message:', err.response.data.message)
  })

defineExpose({
  checkErrorAllFields,
  commitStore
})

</script>

<template>
  <div :style="fillHeightClass" class="dataset-useterms">
    <q-card class="q-ma-sm" v-show="hideFlgs.licenseTitle">
      <q-card-section>
        <font size="5" color="#1d468f">データセット・配信のライセンス</font>
        <br><br>
        このデータセットの利用条件に関するライセンスを選択してください。
        ライセンス（説明）を選択すると対応するライセンスが自動入力されます。
        <br><br>
        <font size="3" color="#1d468d">データセット・配信のライセンス（説明）</font>
        <q-btn
          color="grey"
          round
          flat
          dense
          :icon="expanded.licenseTitle ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
          @click="expanded.licenseTitle = !expanded.licenseTitle"
        />
        <q-slide-transition>
          <div v-show="expanded.licenseTitle">
            <p>CKAN変数名：license_title、resources:license_title</p>
            <q-item>
              <div class="q-gutter-md select-item" style="padding-right: 25px">
                <q-select
                  v-model="attr.catalogParameter.termName"
                  :options="store.ckanItemList.licenseId"
                  clearable
                  @clear="attr.catalogParameter.termName='', attr.catalogParameter.termNameUrl=''"
                />
              </div>
            </q-item>
          </div>
        </q-slide-transition>
        <br>
        <font size="3" color="#1d468d">データセット・配信のライセンス</font>
        <q-btn
          color="grey"
          round
          flat
          dense
          :icon="expanded.licenseUrl ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
          @click="expanded.licenseUrl = !expanded.licenseUrl"
        />
        <q-slide-transition>
          <div v-show="expanded.licenseUrl">
            <p>CKAN変数名：license_url、resources:license_url</p>
            <q-item>
              <q-input
                v-model="attr.catalogParameter.termNameUrl"
                style="width: 1000px;"
                disable
              />
              <br>
            </q-item>
          </div>
        </q-slide-transition>
      </q-card-section>
    </q-card>
    <q-card class="q-ma-sm" v-show="hideFlgs.rights">
      <q-card-section>
        <font size="5" color="#1d468f">データセット・配信の権利表明</font>
        <q-btn
          color="grey"
          round
          flat
          dense
          :icon="expanded.rights ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
          @click="expanded.rights = !expanded.rights"
        />
        <br><br>
        <q-slide-transition>
          <div v-show="expanded.rights">
            ライセンス表示を指定できない場合は、利用規約のURLリンクを記載してください。<br>
            CKAN変数名：extras:rights、resources:rights
            <br>
            <q-select
              v-model="attr.catalogParameter.usrRight"
              use-input
              hide-selected
              fill-input
              input-debounce="0"
              :options="attr.autoCorrect.usrRight"
              @filter="(val, update, abort) => { filterFn(attr.catalogParameter.usrRight, update, abort, 'usrRight') }"
              @input-value="(val) => { setModel(val, 'usrRight') }"
              :error-message="errorFieldMessage(attr.catalogParameter.usrRight, 'string')"
              :error="isError(attr.templateFlg.rights, attr.catalogParameter.usrRight, 'string')"
              hide-dropdown-icon
              class="input-item"
            />
          </div>
        </q-slide-transition>
      </q-card-section>
    </q-card>
    <q-card class="q-ma-sm" v-show="hideFlgs.accessRights">
      <q-card-section>
        <font size="5" color="#1d468f">データセット・配信のアクセス権</font>
        <br><br>
        このデータセット・配信に対して、誰がアクセスできるのかを示す情報を選択してください。<br>
        アクセス権（説明）を選択すると、対応するアクセス権が自動入力されます。<br>
        アクセス権（説明）にその他を選択した場合は、このデータセット・配信に対して、誰がアクセスできるのかを示すURLを入力してください。
        <br><br>
        <font size="3" color="#1d468d">データセット・配信のアクセス権（説明）</font>
        <q-btn
          color="grey"
          round
          flat
          dense
          :icon="expanded.accessRights ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
          @click="expanded.accessRights = !expanded.accessRights"
        />
        <q-slide-transition>
          <div v-show="expanded.accessRights">
            <p>CKAN変数名：extras:access_rights、resources:access_rights</p>
            <q-item>
              <div class="q-gutter-md select-item" style="padding-right: 25px">
                <q-select
                  v-model="attr.catalogParameter.accessRights"
                  :options="store.itemList.accessRights"
                  @input="attr.catalogParameter.accessRightsUrl = attr.catalogParameter.accessRights && attr.catalogParameter.accessRights.value !== 'その他' ? attr.catalogParameter.accessRights.value : ''"
                  clearable
                  @clear="attr.catalogParameter.accessRights='', attr.catalogParameter.accessRightsUrl=''"
                  :error-message="errorFieldMessage(attr.catalogParameter.accessRights, 'object')"
                  :error="isError(attr.templateFlg.accessRights, attr.catalogParameter.accessRights, 'object')"
                />
              </div>
            </q-item>
          </div>
        </q-slide-transition>
        <br>
        <font size="3" color="#1d468d">データセット・配信のアクセス権</font>
        <q-btn
          color="grey"
          round
          flat
          dense
          :icon="expanded.accessRightsUrl ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
          @click="expanded.accessRightsUrl = !expanded.accessRightsUrl"
        />
        <q-slide-transition>
          <div v-show="expanded.accessRightsUrl">
            <p>CKAN変数名：extras:access_rights_url、resources:access_rights_url</p>
            <q-item>
              <q-input
                v-model="attr.catalogParameter.accessRightsUrl"
                style="width: 1000px;"
                :disable="attr.catalogParameter.accessRights &&
                          attr.catalogParameter.accessRights.label &&
                          attr.catalogParameter.accessRights.label!=='その他'"
                :error-message="errorFieldMessage(attr.catalogParameter.accessRightsUrl, 'string')"
                :error="isError(attr.templateFlg.accessRightsUrl, attr.catalogParameter.accessRightsUrl, 'string')"
              />
              <br>
            </q-item>
          </div>
        </q-slide-transition>
      </q-card-section>
    </q-card>
    <q-card class="q-ma-sm" v-show="hideFlgs.haspolicyUrl">
      <q-card-section>
        <font size="5" color="#1d468f">データセット・配信に関する権利情報URL</font>
        <q-btn
          color="grey"
          round
          flat
          dense
          :icon="expanded.haspolicyUrl ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
          @click="expanded.haspolicyUrl = !expanded.haspolicyUrl"
        />
        <br><br>
        <q-slide-transition>
          <div v-show="expanded.haspolicyUrl">
            このデータセットおよび配信に対する権利をODRL言語で記載したURLを入力してください。<br>
            CKAN変数名：extras:haspolicy_url、resources:haspolicy_url
            <br>
            <q-select
              v-model="attr.catalogParameter.haspolicyUrl"
              use-input
              hide-selected
              fill-input
              input-debounce="0"
              :options="attr.autoCorrect.haspolicyUrl"
              @filter="(val, update, abort) => { filterFn(attr.catalogParameter.haspolicyUrl, update, abort, 'haspolicyUrl') }"
              @input-value="(val) => { setModel(val, 'haspolicyUrl') }"
              hide-dropdown-icon
              class="input-item"
              :error-message="errorFieldMessage(attr.catalogParameter.haspolicyUrl, 'string')"
              :error="isError(attr.templateFlg.haspolicyUrl, attr.catalogParameter.haspolicyUrl, 'string')"
            />
          </div>
        </q-slide-transition>
      </q-card-section>
    </q-card>
    <q-card class="q-ma-sm" v-show="hideFlgs.provWasGeneratedByUrl">
      <q-card-section>
        <font size="5" color="#1d468f">データセットを生成した活動</font>
        <q-btn
          color="grey"
          round
          flat
          dense
          :icon="expanded.provWasGeneratedByUrl ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
          @click="expanded.provWasGeneratedByUrl = !expanded.provWasGeneratedByUrl"
        />
        <br><br>
        <q-slide-transition>
          <div v-show="expanded.provWasGeneratedByUrl">
            データセットの作成をもたらした、またはそのためのビジネス・コンテキストを提供する活動を示すURLを入力してください。<br>
            CKAN変数名：extras:prov_was_generated_by_url
            <br>
            <q-select
              v-model="attr.catalogParameter.provWasGeneratedByUrl"
              use-input
              hide-selected
              fill-input
              input-debounce="0"
              :options="attr.autoCorrect.provWasGeneratedByUrl"
              @filter="(val, update, abort) => { filterFn(attr.catalogParameter.provWasGeneratedByUrl, update, abort, 'provWasGeneratedByUrl') }"
              @input-value="(val) => { setModel(val, 'provWasGeneratedByUrl') }"
              hide-dropdown-icon
              class="input-item"
              :error-message="errorFieldMessage(attr.catalogParameter.provWasGeneratedByUrl, 'string')"
              :error="isError(attr.templateFlg.provWasGeneratedByUrl, attr.catalogParameter.provWasGeneratedByUrl, 'string')"
            />
          </div>
        </q-slide-transition>
      </q-card-section>
    </q-card>
    <q-card class="q-ma-sm" v-show="hideFlgs.conformsTo">
      <q-card-section>
        <font size="5" color="#1d468f">データセット・配信が準拠する標準URL</font>
        <q-btn
          color="grey"
          round
          flat
          dense
          :icon="expanded.conformsTo ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
          @click="expanded.conformsTo = !expanded.conformsTo"
        />
        <br><br>
        <q-slide-transition>
          <div v-show="expanded.conformsTo">
            データセットおよび配信が準拠するモデル、スキーマ、オントロジー、ビュー、またはプロファイルを示すURLを入力してください。<br>
            CKAN変数名: extras:conforms_to、resources:conforms_to
            <br>
            <q-select
              v-model="attr.catalogParameter.conformsTo"
              use-input
              hide-selected
              fill-input
              input-debounce="0"
              :options="attr.autoCorrect.conformsTo"
              @filter="(val, update, abort) => { filterFn(attr.catalogParameter.conformsTo, update, abort, 'conformsTo') }"
              @input-value="(val) => { setModel(val, 'conformsTo') }"
              hide-dropdown-icon
              class="input-item"
              :error-message="errorFieldMessage(attr.catalogParameter.conformsTo, 'string')"
              :error="isError(attr.templateFlg.conformsTo, attr.catalogParameter.conformsTo, 'string')"
            />
          </div>
        </q-slide-transition>
      </q-card-section>
    </q-card>
    <q-card class="q-ma-sm" v-show="hideFlgs.tradingPolicyContractType || hideFlgs.tradingPolicyNda || hideFlgs.tradingPolicyUseApplication">
      <q-card-section>
        <font size="5" color="#1d468f">契約ポリシー</font>
        <br>
        データ販売を行うにあたって、あなたが所属する組織では、
        どういった契約ポリシーを持っているかを記載してください。
        <br><br>
        <div v-show="hideFlgs.tradingPolicyContractType">
          <font size="3" color="#1d468d">契約形態</font>
          <q-btn
            color="grey"
            round
            flat
            dense
            :icon="expanded.tradingPolicyContractType ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
            @click="expanded.tradingPolicyContractType = !expanded.tradingPolicyContractType"
          />
          <q-slide-transition>
            <div v-show="expanded.tradingPolicyContractType">
              <p>このデータセットの契約形態を記載してください。<br>
                  CKAN変数名：extras:trading_policy_contract_type
              </p>
              <q-select
                class="select-item"
                v-model="attr.catalogParameter.contractType"
                placeholder="  例： 利用許諾"
                :options="store.itemList.tradingPolicyContractType"
                :error-message="errorFieldMessage(attr.catalogParameter.contractType, 'object')"
                :error="isError(attr.templateFlg.tradingPolicyContractType, attr.catalogParameter.contractType, 'object')"
                >
                <template v-if="attr.catalogParameter.contractType" v-slot:append>
                  <q-icon name="cancel" @click.stop="attr.catalogParameter.contractType = ''" class="cursor-pointer" />
                </template>
              </q-select>
              <br><br>
            </div>
          </q-slide-transition>
        </div>
        <div v-show="hideFlgs.tradingPolicyNda">
          <font size="3" color="#1d468d">秘密保持義務</font>
          <q-btn
            color="grey"
            round
            flat
            dense
            :icon="expanded.tradingPolicyNda ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
            @click="expanded.tradingPolicyNda = !expanded.tradingPolicyNda"
          />
          <q-slide-transition>
            <div v-show="expanded.tradingPolicyNda">
              <p>データの購入者に、秘密保持義務を含む、契約の締結や規約への合意を求めるかを記載してください。<br>
                  CKAN変数名：extras:trading_policy_nda
              </p>
              <q-select
                class="select-item"
                v-model="attr.catalogParameter.secrecy"
                :options="store.itemList.tradingPolicyNda"
                placeholder="  例： 求める"
                :error-message="errorFieldMessage(attr.catalogParameter.secrecy, 'object')"
                :error="isError(attr.templateFlg.tradingPolicyNda, attr.catalogParameter.secrecy, 'object')"
                >
                <template v-if="attr.catalogParameter.secrecy" v-slot:append>
                  <q-icon name="cancel" @click.stop="attr.catalogParameter.secrecy = ''" class="cursor-pointer" />
                </template>
              </q-select>
              <br><br>
            </div>
          </q-slide-transition>
        </div>
        <div v-show="hideFlgs.tradingPolicyUseApplication">
          <font size="3" color="#1d468d">利用用途</font>
          <q-btn
            color="grey"
            round
            flat
            dense
            :icon="expanded.tradingPolicyUseApplication ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
            @click="expanded.tradingPolicyUseApplication = !expanded.tradingPolicyUseApplication"
          />
          <q-slide-transition>
            <div v-show="expanded.tradingPolicyUseApplication">
              <p>どの用途であれば、利用を認めるかを記載してください。<br>
                  CKAN変数名：extras:trading_policy_use_application
              </p>
              <q-select
                use-chips
                multiple
                class="select-item"
                color="light-blue-10"
                v-model="attr.catalogParameter.useApplication"
                :options="store.itemList.tradingPolicyUseApplication"
                placeholder="  例： 制限なし"
                :error-message="errorFieldMessage(attr.catalogParameter.useApplication, 'list')"
                :error="isError(attr.templateFlg.tradingPolicyUseApplication, attr.catalogParameter.useApplication, 'list')"
              />
              <q-select
                v-show="attr.freeFieldColumn.useApplication"
                label="自由欄"
                style="padding-left:20px;"
                class="input-item"
                v-model="attr.catalogParameter.useApplicationOther"
                use-input
                hide-selected
                fill-input
                input-debounce="0"
                :options="attr.autoCorrect.useApplication"
                @filter="(val, update, abort) => { filterFn(attr.catalogParameter.useApplicationOther, update, abort, 'useApplication') }"
                @input-value="(val) => { setModel(val, 'useApplicationOther') }"
                :error="isCommaError(attr.catalogParameter.useApplicationOther)"
                :error-message="attr.errorMessageReservedWord"
                hide-dropdown-icon
                hint=" , (カンマ)は使用できません。"
              />
            </div>
          </q-slide-transition>
        </div>        
      </q-card-section>
    </q-card>
    <q-card class="q-ma-sm" v-show="hideFlgs.scopeOfDisclosure || hideFlgs.termsOfUsePermissibleRegion || hideFlgs.termsOfUseNotices">
      <q-card-section>
        <font size="5" color="#1d468f">データ利用条件</font>
        <br>
        データの利用条件や開示範囲、派生データの利用権など、
        販売しようとしているデータの利用条件を記載してください。<br>
        <br><br>
        <div v-show="hideFlgs.scopeOfDisclosure">
          <font size="3" color="#1d468f">開示範囲</font>
          <q-btn
            color="grey"
            round
            flat
            dense
            :icon="expanded.scopeOfDisclosure ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
            @click="expanded.scopeOfDisclosure = !expanded.scopeOfDisclosure"
          />
          <q-slide-transition>
            <div v-show="expanded.scopeOfDisclosure">
              <p>提供者に前もって知らせなくても、購入者がデータを開示してよい範囲を記載してください。<br>
                  CKAN変数名：extras:scope_of_disclosure
              </p>
              <q-select
                class="select-item"
                v-model="attr.catalogParameter.scopeOfDisclosure"
                :options="store.itemList.scopeOfDisclosure"
                placeholder="  例： 制限なし"
                :error-message="errorFieldMessage(attr.catalogParameter.scopeOfDisclosure, 'object')"
                :error="isError(attr.templateFlg.scopeOfDisclosure, attr.catalogParameter.scopeOfDisclosure, 'object')"
              >
                <template v-if="attr.catalogParameter.scopeOfDisclosure" v-slot:append>
                  <q-icon name="cancel" @click.stop="attr.catalogParameter.scopeOfDisclosure = ''" class="cursor-pointer" />
                </template>
              </q-select>
              <q-select
                v-show="attr.freeFieldColumn.scopeOfDisclosure"
                label="自由欄"
                style="padding-left:20px;"
                class="input-item"
                v-model="attr.catalogParameter.scopeOfDisclosureOther"
                use-input
                hide-selected
                fill-input
                input-debounce="0"
                :options="attr.autoCorrect.scopeOfDisclosure"
                @filter="(val, update, abort) => { filterFn(attr.catalogParameter.scopeOfDisclosureOther, update, abort, 'scopeOfDisclosure') }"
                @input-value="(val) => { setModel(val, 'scopeOfDisclosureOther') }"
                :error="isCommaError(attr.catalogParameter.scopeOfDisclosureOther)"
                error-message="使用禁止文字が含まれています。"
                hide-dropdown-icon
                hint=" , (カンマ)は使用できません。"
              />
              <br><br>
            </div>
          </q-slide-transition>
        </div>
        <div v-show="hideFlgs.termsOfUsePermissibleRegion">
          <font size="3" color="#1d468f">データ活用地域</font>
          <q-btn
            color="grey"
            round
            flat
            dense
            :icon="expanded.termsOfUsePermissibleRegion ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
            @click="expanded.termsOfUsePermissibleRegion = !expanded.termsOfUsePermissibleRegion"
          />
          <q-slide-transition>
            <div v-show="expanded.termsOfUsePermissibleRegion">
              <p>データの活用地域に制限がある場合、利用可能な国や地域を記入してください。<br>
                  CKAN変数名：extras:terms_of_use_permissible_region
              </p>
              <q-select
                class="select-item"
                use-chips
                multiple
                v-model="attr.catalogParameter.permissionResion"
                :options="store.itemList.termsOfUsePermissibleRegion"
                :error-message="errorFieldMessage(attr.catalogParameter.permissionResion, 'list')"
                :error="isError(attr.templateFlg.termsOfUsePermissibleRegion, attr.catalogParameter.permissionResion, 'list')"
              />
              <q-select
                v-show="attr.freeFieldColumn.permissionResion"
                label="自由欄"
                style="padding-left:20px;"
                class="input-item"
                v-model="attr.catalogParameter.permissionResionOther"
                use-input
                hide-selected
                fill-input
                input-debounce="0"
                :options="attr.autoCorrect.permissionResion"
                @filter="(val, update, abort) => { filterFn(attr.catalogParameter.permissionResionOther, update, abort, 'permissionResion') }"
                @input-value="(val) => { setModel(val, 'permissionResionOther') }"
                :error="isCommaError(attr.catalogParameter.permissionResionOther)"
                error-message="使用禁止文字が含まれています。"
                hide-dropdown-icon
                hint=" , (カンマ)は使用できません。"
              />
              <br><br>
            </div>
          </q-slide-transition>
        </div>
        <div v-show="hideFlgs.termsOfUseNotices">
          <font size="3" color="#1d468f">利用に関する注意事項</font>
          <q-btn
            color="grey"
            round
            flat
            dense
            :icon="expanded.termsOfUseNotices ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
            @click="expanded.termsOfUseNotices = !expanded.termsOfUseNotices"
          />
          <q-slide-transition>
            <div v-show="expanded.termsOfUseNotices">
              <p>データを利用する際に注意すべき事項（例えば、利用状況の把握，派生データの取り扱い、データ利用者に求める資格、データの管理方法など）を記入してください。<br>
                  CKAN変数名：extras:terms_of_use_notices
              </p>
              <q-input
                v-model="attr.catalogParameter.notices"
                type="textarea"
                class="input-item"
                autogrow
                :error-message="errorFieldMessage(attr.catalogParameter.notices, 'string')"
                :error="isError(attr.templateFlg.termsOfUseNotices, attr.catalogParameter.notices, 'string')"
              />
            </div>
          </q-slide-transition>
        </div>        
      </q-card-section>
    </q-card>
    <q-card class="q-ma-sm" v-show="hideFlgs.privacyPolicyContainsPersonalData">
      <q-card-section>
        <font size="5" color="#1d468f">データ保護要件</font>
        <br>
        データの管理方法やデータの利用者に求める資格等、データの保護条件を記載してください。
        <br><br>
        <font size="3" color="#1d468f">パーソナルデータの類別</font>
        <q-btn
          color="grey"
          round
          flat
          dense
          :icon="expanded.privacyPolicyContainsPersonalData ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
          @click="expanded.privacyPolicyContainsPersonalData = !expanded.privacyPolicyContainsPersonalData"
        />
        <q-slide-transition>
          <div v-show="expanded.privacyPolicyContainsPersonalData">
            <p>提供するデータセットのパーソナルデータの類別を記入してください。<br>
                CKAN変数名：extras:privacy_policy_contains_personal_data
            </p>
            <q-select
              class="select-item"
              v-model="attr.catalogParameter.personalData"
              :options="store.itemList.privacyPolicyContainsPersonalData"
              :error-message="errorFieldMessage(attr.catalogParameter.personalData, 'object')"
              :error="isError(attr.templateFlg.privacyPolicyContainsPersonalData, attr.catalogParameter.personalData, 'object')"
            >
              <template v-if="attr.catalogParameter.personalData" v-slot:append>
                <q-icon name="cancel" @click.stop="attr.catalogParameter.personalData = ''" class="cursor-pointer" />
              </template>
            </q-select>
            <q-select
              v-show="attr.freeFieldColumn.personalData"
              label="自由欄"
              style="padding-left:20px;"
              class="input-item"
              v-model="attr.catalogParameter.personalDataOther"
              use-input
              hide-selected
              fill-input
              input-debounce="0"
              :options="attr.autoCorrect.personalData"
              @filter="(val, update, abort) => { filterFn(attr.catalogParameter.personalDataOther, update, abort, 'personalData') }"
              @input-value="(val) => { setModel(val, 'personalDataOther') }"
              :error="isCommaError(attr.catalogParameter.personalDataOther)"
              error-message="使用禁止文字が含まれています。"
              hide-dropdown-icon
              hint=" , (カンマ)は使用できません。"
            />
          </div>
        </q-slide-transition>
      </q-card-section>
    </q-card>
    <q-card class="q-ma-sm" v-show="hideFlgs.dataEffectivePeriod || hideFlgs.usageLicensePeriod">
      <q-card-section>
        <font size="5" color="#1d468f">利用期間</font>
        <br>
        データ利用可能な利用期間を記載してください。
        <br><br>
        <div v-show="hideFlgs.dataEffectivePeriod">
          <font size="3" color="#1d468f">データの有効期間</font>
          <q-btn
            color="grey"
            round
            flat
            dense
            :icon="expanded.dataEffectivePeriod ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
            @click="expanded.dataEffectivePeriod = !expanded.dataEffectivePeriod"
          />
          <q-slide-transition>
            <div v-show="expanded.dataEffectivePeriod">
              <p>年月の経過や制度改定によって、データが無効になることはあるかどうかを記入してください。 明確な有効期限がある場合は、開始日と終了日を記入してください。<br>
                  CKAN変数名：extras:data_effective_period
              </p>
              <q-select
                class="select-item"
                v-model="attr.catalogParameter.dataEffectivePeriod.selectTerms"
                :options="store.itemList.dataEffectivePeriod"
                :error-message="errorFieldMessage(attr.catalogParameter.dataEffectivePeriod.selectTerms, 'object')"
                :error="isError(attr.templateFlg.dataEffectivePeriod, attr.catalogParameter.dataEffectivePeriod.selectTerms, 'object')"
              >
                <template v-if="attr.catalogParameter.dataEffectivePeriod.selectTerms" v-slot:append>
                  <q-icon name="cancel" @click.stop="clearDataEffectivePeriod()" class="cursor-pointer" />
                </template>
              </q-select>
              <br>
              <div v-show="attr.dataEffectivePeriodField.date">
                <q-list no-border class="select-item" style="padding-left:10px;">
                  <q-item>
                    <q-item-section>
                      <font size='2' color='#1d468f'>開始日</font>
                      <q-input
                        class="date-input"
                        v-model="attr.catalogParameter.dataEffectivePeriod.startDate"
                        :error="isError(attr.templateFlg.dataEffectivePeriod, attr.catalogParameter.dataEffectivePeriod.startDate, 'startDate')"
                        :error-message="errorFieldMessage(attr.catalogParameter.dataEffectivePeriod.startDate, 'startDate')"
                        mask="####-##-##"
                        :rules="[v => v === '' || isValidDateFormat(v) || '【無効な値】']"
                        :placeholder="placeholderDate"
                      />
                    </q-item-section>
                    <q-item-section>
                      <q-btn
                        icon="date_range"
                        class="calendar-icon"
                        dense
                        color="light-blue-10"
                        @click="startCalender"
                      >
                        <q-tooltip anchor="bottom middle" self="top middle" :offset="[10, 10]">
                          カレンダー入力
                        </q-tooltip>
                      </q-btn>
                    </q-item-section>
                  </q-item>
                </q-list>
                <br>
                <q-list no-border class="select-item" style="padding-left:10px;">
                  <q-item>
                    <q-item-section>
                      <font size='2' color='#1d468f'>終了日</font>
                      <q-input
                        class="date-input"
                        v-model="attr.catalogParameter.dataEffectivePeriod.endDate"
                        :error="isError(attr.templateFlg.dataEffectivePeriod, attr.catalogParameter.dataEffectivePeriod.endDate, 'endDate')"
                        :error-message="errorFieldMessage(attr.catalogParameter.dataEffectivePeriod.endDate, 'endDate')"
                        mask="####-##-##"
                        :rules="[v => v === '' || isValidDateFormat(v) || '【無効な値】']"
                        :placeholder="placeholderDate"
                      />
                    </q-item-section>
                    <q-item-section>
                      <q-btn
                        icon="date_range"
                        class="calendar-icon"
                        dense
                        color="light-blue-10"
                        @click="endCalender"
                      >
                        <q-tooltip anchor="bottom middle" self="top middle" :offset="[10, 10]">
                          カレンダー入力
                        </q-tooltip>
                      </q-btn>
                    </q-item-section>
                  </q-item>
                </q-list>
                <br>
              </div>
              <q-select
                v-show="attr.dataEffectivePeriodField.freeField"
                label="自由欄"
                style="padding-left:20px;"
                class="input-item"
                v-model="attr.catalogParameter.dataEffectivePeriod.freefield"
                use-input
                hide-selected
                fill-input
                input-debounce="0"
                :options="attr.autoCorrect.dataEffectivePeriod"
                @filter="(val, update, abort) => { filterFn(attr.catalogParameter.dataEffectivePeriod.freefield, update, abort, 'dataEffectivePeriod') }"
                @input-value="(val) => { setModel(val, 'dataEffectivePeriod') }"
                :error="isCommaError(attr.catalogParameter.dataEffectivePeriod.freefield)"
                error-message="使用禁止文字が含まれています。"
                hide-dropdown-icon
                hint=" , (カンマ)は使用できません。"
              />
              <br>
            </div>
          </q-slide-transition>
        </div>       
        <div v-show="hideFlgs.usageLicensePeriod">
          <font size="3" color="#1d468f">利用ライセンスの期限</font>
          <q-btn
            color="grey"
            round
            flat
            dense
            :icon="expanded.usageLicensePeriod ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
            @click="expanded.usageLicensePeriod = !expanded.usageLicensePeriod"
          />
          <q-slide-transition>
            <div v-show="expanded.usageLicensePeriod">
              <p>データの購入者が、データを利用できる期間を記入してください。<br>
                  CKAN変数名：extras:usage_license_period
              </p>
              <q-select
                class="select-item"
                v-model="attr.catalogParameter.usageLicensePeriod.selectTerms"
                :options="store.itemList.usageLicensePeriod"
                :error-message="errorFieldMessage(attr.catalogParameter.usageLicensePeriod.selectTerms, 'object')"
                :error="isError(attr.templateFlg.usageLicensePeriod, attr.catalogParameter.usageLicensePeriod.selectTerms, 'object')"
              >
                <template v-if="attr.catalogParameter.usageLicensePeriod.selectTerms" v-slot:append>
                  <q-icon name="cancel" @click.stop="clearUsageLicensePeriod()" class="cursor-pointer" />
                </template>
              </q-select>
              <br>
              <div v-show="attr.usageLicensePeriodField.deadline">
                <q-list no-border class="select-item" style="padding-left:10px;">
                  <q-item>
                    <q-item-section>
                      <font size='2' color='#1d468f'>期限</font>
                      <q-input
                        class="date-input"
                        v-model="attr.catalogParameter.usageLicensePeriod.deadline"
                        :error="isError(attr.templateFlg.usageLicensePeriod, attr.catalogParameter.usageLicensePeriod.deadline, 'string')"
                        :error-message="errorFieldMessage(attr.catalogParameter.usageLicensePeriod.deadline, 'string')"
                        mask="####-##-##"
                        :rules="[v => v === '' || isValidDateFormat(v) || '【無効な値】']"
                        :placeholder="placeholderDate"
                      />
                    </q-item-section>
                    <q-item-section>
                      <q-btn
                        icon="date_range"
                        class="calendar-icon"
                        dense
                        color="light-blue-10"
                        @click="periodCalender"
                      >
                        <q-tooltip anchor="bottom middle" self="top middle" :offset="[10, 10]">
                          カレンダー入力
                        </q-tooltip>
                      </q-btn>
                    </q-item-section>
                  </q-item>
                </q-list>
                <br>
              </div>
              <div v-show="attr.usageLicensePeriodField.periodDulation">
                <q-list no-border style="width: 400px; padding-left:10px;">
                  <q-item>
                    <q-item-section>
                      <font size='2' color='#1d468f'>期間(整数)</font>
                      <q-input
                        style="width: 150px;"
                        v-model="attr.catalogParameter.usageLicensePeriod.period"
                        :error="isError(attr.templateFlg.usageLicensePeriod, attr.catalogParameter.usageLicensePeriod.period, 'string')"
                        :error-message="errorFieldMessage(attr.catalogParameter.usageLicensePeriod.period, 'string')"
                        type="number"
                      />
                    </q-item-section>
                    <q-item-section>
                      <font size='2' color='#1d468f'>期間(単位)</font>
                      <q-select
                        style="width: 100px;"
                        v-model="attr.catalogParameter.usageLicensePeriod.unit"
                        :options="attr.periodUnit"
                        :error="isError(attr.templateFlg.usageLicensePeriod, attr.catalogParameter.usageLicensePeriod.unit, 'object')"
                        :error-message="errorFieldMessage(attr.catalogParameter.usageLicensePeriod.unit, 'object')"
                      />
                    </q-item-section>
                  </q-item>
                </q-list>
                <br>
              </div>
              <q-select
                v-show="attr.usageLicensePeriodField.freeField"
                label="自由欄"
                style="padding-left:20px;"
                class="input-item"
                v-model="attr.catalogParameter.usageLicensePeriod.freefield"
                use-input
                hide-selected
                fill-input
                input-debounce="0"
                :options="attr.autoCorrect.usageLicensePeriod"
                @filter="(val, update, abort) => { filterFn(attr.catalogParameter.usageLicensePeriod.freefield, update, abort, 'usageLicensePeriod') }"
                @input-value="(val) => { setModel(val, 'usageLicensePeriod') }"
                :error="isCommaError(attr.catalogParameter.usageLicensePeriod.freefield)"
                error-message="使用禁止文字が含まれています。"
                hide-dropdown-icon
                hint=" , (カンマ)は使用できません。"
              />
            </div>
          </q-slide-transition>
        </div>
      </q-card-section>
    </q-card>
    <q-card class="q-ma-sm" v-show="hideFlgs.fee || hideFlgs.salesInfoUrl || hideFlgs.pricingPriceRange || hideFlgs.pricingNoticesOfPrice">
      <q-card-section>
        <font size="5" color="#1d468f">支払い</font>
        <br>
        データの購入者への支払方法を記載してください。
        <br><br>
        <div v-show="hideFlgs.fee">
          <font size="3" color="#1d468f">有償無償</font>
          <q-btn
            color="grey"
            round
            flat
            dense
            :icon="expanded.fee ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
            @click="expanded.fee = !expanded.fee"
          />
          <q-slide-transition>
            <div v-show="expanded.fee">
              <p>データセットを無償で提供するか、有償で提供するかを選択してください。<br>
                 条件付きで有償となる場合（例えば、教育用途では無償だが営利用途では有償、一定の期間は無償だが、それを超えると有償等）も有償を選択してください。<br>
                  CKAN変数名：extras:fee
              </p>
              <q-select
                class="select-item"
                v-model="attr.catalogParameter.fee"
                :options="store.itemList.fee"
                :error="isError(attr.templateFlg.fee, attr.catalogParameter.fee, 'object')"
                :error-message="errorFieldMessage(attr.catalogParameter.fee, 'object')"
              >
                <template v-if="attr.catalogParameter.fee" v-slot:append>
                  <q-icon name="cancel" @click.stop="attr.catalogParameter.fee = ''" class="cursor-pointer" />
                </template>
              </q-select>
              <br>
            </div>
          </q-slide-transition>
        </div>
        <div v-show="attr.feeField.salesInfoUrl && hideFlgs.salesInfoUrl">
          <font size="3" color="#1d468f">販売情報</font>
          <q-btn
            color="grey"
            round
            flat
            dense
            :icon="expanded.salesInfoUrl ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
            @click="expanded.salesInfoUrl = !expanded.salesInfoUrl"
          />
          <q-slide-transition>
            <div v-show="expanded.salesInfoUrl">
              <p>このデータセットの販売に関する情報のWebページがあれば、そのURLを記載してください。<br>
                CKAN変数名：extras:sales_info_url
              </p>
              <q-select
                v-model="attr.catalogParameter.salesInfoUrl"
                use-input
                hide-selected
                fill-input
                input-debounce="0"
                :options="attr.autoCorrect.salesInfoUrl"
                @filter="(val, update, abort) => { filterFn(attr.catalogParameter.salesInfoUrl, update, abort, 'salesInfoUrl') }"
                @input-value="(val) => { setModel(val, 'salesInfoUrl') }"
                hide-dropdown-icon
                class="input-item"
              />
              <br><br>
            </div>
          </q-slide-transition>
        </div>
        <div v-show="attr.feeField.priceRange && hideFlgs.pricingPriceRange">
          <font size="3" color="#1d468f">価格帯</font>
          <q-btn
            color="grey"
            round
            flat
            dense
            :icon="expanded.pricingPriceRange ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
            @click="expanded.pricingPriceRange = !expanded.pricingPriceRange"
          />
          <q-slide-transition>
            <div v-show="expanded.pricingPriceRange">
              <p>このデータセットを販売できる価格帯を記入してください。通貨(円, 米ドル等)と、下限価格、上限価格を記入してください。価格が決まっている場合には下限価格と上限価格は同じとしてください。<br>
                CKAN変数名：extras:pricing_price_range
              </p>
              <q-input
                v-model="attr.catalogParameter.priceRange"
                class="input-item"
                type="textarea"
                autogrow
              />
              <br><br>
            </div>
          </q-slide-transition>
        </div>
        <div v-show="attr.feeField.noticesOfPrice && hideFlgs.pricingNoticesOfPrice">
          <font size="3" color="#1d468f">データ販売に関わる特記事項</font>
          <q-btn
            color="grey"
            round
            flat
            dense
            :icon="expanded.pricingNoticesOfPrice ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
            @click="expanded.pricingNoticesOfPrice = !expanded.pricingNoticesOfPrice"
          />
          <q-slide-transition>
            <div v-show="expanded.pricingNoticesOfPrice">
              <p>このデータセットの販売に関わる特記事項（例えば、利用期間に応じて課金する、初回30日間無料にする、長期契約にて優待価格で提供する等）がもしあれば記入してください。<br>
                CKAN変数名：extras:pricing_notices_of_price
              </p>
              <q-select
                v-model="attr.catalogParameter.noticesOfPrice"
                use-input
                hide-selected
                fill-input
                input-debounce="0"
                :options="attr.autoCorrect.noticesOfPrice"
                @filter="(val, update, abort) => { filterFn(attr.catalogParameter.noticesOfPrice, update, abort, 'noticesOfPrice') }"
                @input-value="(val) => { setModel(val, 'noticesOfPrice') }"
                hide-dropdown-icon
                class="input-item"
              />
            </div>
          </q-slide-transition>
        </div>
      </q-card-section>
    </q-card>
    <q-card class="q-ma-sm" v-show="hideFlgs.warrantyExpressWarranty || hideFlgs.warrantyLegalCompliance">
      <q-card-section>
        <font size="5" color="#1d468f">保証</font>
        <br>
        データの利用者への保証内容を記載してください。
        <br><br>
        <div v-show="hideFlgs.warrantyExpressWarranty">
          <font size="3" color="#1d468f">明示された保証</font>
          <q-btn
            color="grey"
            round
            flat
            dense
            :icon="expanded.warrantyExpressWarranty ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
            @click="expanded.warrantyExpressWarranty = !expanded.warrantyExpressWarranty"
          />
          <q-slide-transition>
            <div v-show="expanded.warrantyExpressWarranty">
              <p>データ利用者に対して、保証できることを記入してください。<br>
                  CKAN変数名：extras:warranty_express_warranty
              </p>
              <q-select
                class="select-item"
                v-model="attr.catalogParameter.expressWarranty"
                :options="store.itemList.warrantyExpressWarranty"
                :error="isError(attr.templateFlg.warrantyExpressWarranty, attr.catalogParameter.expressWarranty, 'object')"
                :error-message="errorFieldMessage(attr.catalogParameter.expressWarranty, 'object')"
              >
                <template v-if="attr.catalogParameter.expressWarranty" v-slot:append>
                  <q-icon name="cancel" @click.stop="attr.catalogParameter.expressWarranty = ''" class="cursor-pointer" />
                </template>
              </q-select>
              <q-select
                v-show="attr.freeFieldColumn.expressWarranty"
                label="自由欄"
                style="padding-left:20px;"
                class="input-item"
                v-model="attr.catalogParameter.expressWarrantyOther"
                use-input
                hide-selected
                fill-input
                input-debounce="0"
                :options="attr.autoCorrect.expressWarranty"
                @filter="(val, update, abort) => { filterFn(attr.catalogParameter.expressWarrantyOther, update, abort, 'expressWarranty') }"
                @input-value="(val) => { setModel(val, 'expressWarrantyOther') }"
                :error="isCommaError(attr.catalogParameter.expressWarrantyOther)"
                error-message="使用禁止文字が含まれています。"
                hide-dropdown-icon
                hint=" , (カンマ)は使用できません。"
              />
              <br><br>
            </div>
          </q-slide-transition>
        </div>
        <div v-show="hideFlgs.warrantyLegalCompliance">
          <font size="3" color="#1d468f">準拠法の対象国</font>
          <q-btn
            color="grey"
            round
            flat
            dense
            :icon="expanded.warrantyLegalCompliance ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
            @click="expanded.warrantyLegalCompliance = !expanded.warrantyLegalCompliance"
          />
          <q-slide-transition>
            <div v-show="expanded.warrantyLegalCompliance">
              <p>データ購入者に、どの国・地域の法律に準拠することを求めるかを記入してください。<br>
                  CKAN変数名：extras:warranty_legal_compliance
              </p>
              <q-select
                class="select-item"
                v-model="attr.catalogParameter.leagalCompliance"
                :options="store.itemList.warrantyLegalCompliance"
                use-chips
                multiple
                :error="isError(attr.templateFlg.warrantyLegalCompliance, attr.catalogParameter.leagalCompliance, 'list')"
                :error-message="errorFieldMessage(attr.catalogParameter.leagalCompliance, 'list')"
              />
              <q-select
                v-show="attr.freeFieldColumn.leagalCompliance"
                label="自由欄"
                style="padding-left:20px;"
                class="input-item"
                v-model="attr.catalogParameter.leagalComplianceOther"
                use-input
                hide-selected
                fill-input
                input-debounce="0"
                :options="attr.autoCorrect.leagalCompliance"
                @filter="(val, update, abort) => { filterFn(attr.catalogParameter.leagalComplianceOther, update, abort, 'leagalCompliance') }"
                @input-value="(val) => { setModel(val, 'leagalComplianceOther') }"
                :error="isCommaError(attr.catalogParameter.leagalComplianceOther)"
                error-message="使用禁止文字が含まれています。"
                hide-dropdown-icon
                hint=" , (カンマ)は使用できません。"
              />
            </div>
          </q-slide-transition>
        </div>
      </q-card-section>
    </q-card>
    <!-- 以下、ダイアログ -->
    <q-dialog transition-show="scale" transition-hide="scale" v-model="attr.startCalenderFlg">
      <q-card :content-css="{minWidth: '80vw', minHeight: '80vh'}" color="light-blue-10">
        <div style="padding: 50px">
          <div class="q-display-1 q-mb-md"><font color="#1d468f">開始年月日&nbsp;カレンダー</font></div>
          <q-date
            v-model="attr.catalogParameter.dataEffectivePeriod.startDate"
            minimal
            color="light-blue-10"
            @update:modelValue="startCalenderClose()"
          />
        </div>
      </q-card>
    </q-dialog>
    <q-dialog transition-show="scale" transition-hide="scale" v-model="attr.endCalenderFlg">
      <q-card :content-css="{minWidth: '80vw', minHeight: '80vh'}" color="light-blue-10">
        <div style="padding: 50px">
          <div class="q-display-1 q-mb-md"><font color="#1d468f">終了年月日&nbsp;カレンダー</font></div>
          <q-date
            v-model="attr.catalogParameter.dataEffectivePeriod.endDate"
            minimal
            color="light-blue-10"
            @update:modelValue="endCalenderClose()"
          />
        </div>
      </q-card>
    </q-dialog>
    <q-dialog transition-show="scale" transition-hide="scale" v-model="attr.periodCalenderFlg">
      <q-card :content-css="{minWidth: '80vw', minHeight: '80vh'}" color="light-blue-10">
        <div style="padding: 50px">
          <div class="q-display-1 q-mb-md"><font color="#1d468f">期限年月日&nbsp;カレンダー</font></div>
          <q-date
            v-model="attr.catalogParameter.usageLicensePeriod.deadline"
            minimal
            color="light-blue-10"
            @update:modelValue="periodCalenderClose()"
          />
        </div>
      </q-card>
    </q-dialog>
    <div v-for="message in attr.errorCheckMessage" :key="message">
      <font size="3" color="#FF0000">{{message}}</font>
    </div>
    <!-- 全て非表示項目だった場合、表示するメッセージ -->
    <q-card class="col-grow" v-show="isAllHide">
      <q-card-section>
        <div class="text-h6" style="color: #1d468f;">利用条件の入力項目はありません</div>
      </q-card-section>
    </q-card>
  </div>
</template>

<style lang="scss">
.dataset-useterms .input-item{
  width: 800px;
}

.select-item{
  width: 500px;
}

.calendar-icon{
  width: 30px;
}

.date-input{
  width: 220px;
}
</style>
