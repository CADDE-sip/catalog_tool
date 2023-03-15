<script setup>
import { config } from'boot/config'
import { reactive , ref, watch, onMounted, computed } from 'vue'
import {useStore} from 'stores/store'
import axios from 'axios'
import CompleteDialog from './dialog/CompleteDialog.vue'

const store = useStore();
const EXPECT_URL = '/analysis'

const EMPTY_ERROR_MESSAGE = '【入力必須項目】'
const INVALID_ERROR_MESSAGE = '【無効な値】'

const KEYWORD_ERROR_LOWER_LIMIT = 'キーワードは2文字以上で入力してください。'
const KEYWORD_ERROR_ONLY_SPACE = '空文字は追加できません。'
const KEYWORD_ERROR_INVALID_SYMBOL = '記号「・」は使用できません。'
const KEYWORD_ERROR_DUPLICAE = '既に入力されているキーワードは追加できません。'

// データセット情報(任意)入力フィールド
const catalogParameter = reactive({
  theme: store.selectThemes,
  tags: store.selectTags,
  language: store.selectLanguage,
  vocabulary: store.vocabulary,
  term: store.term,
  frequency: store.frequency,
  spatialUrl: store.geonames.spatialUrl,
  spatialName: store.geonames.spatialName,
  spatial: store.geonames.spatial,
  startDate: store.dataCalender.start,
  endDate: store.dataCalender.end
})

const startCalenderFlg = ref(false)
const endCalenderFlg = ref(false)
const pointNameList = []
const resultAllPoints = []
const selectGeonamesWindow = ref(false)
const countryKeyword = ref('')
const extractSpatialActive = ref(true)
const columns = reactive([
  { name: 'id', label: 'Geoname ID', field: 'id', align: 'center' },
  { name: 'name', label: 'name', field: 'name', align: 'center' },
  { name: 'country', label: 'country', field: 'country', align: 'center' },
  { name: 'adminname', label: 'adminname', field: 'adminname', align: 'center' },
  { name: 'lat', label: 'Lat', field: 'lat', align: 'center' },
  { name: 'lng', label: 'Lng', field: 'lng', align: 'center' },
  { name: 'fcl', label: 'fcl', field: 'fcl', align: 'center' }
])

const resultData = ref([])
const tableLoading = ref(false)
const optLanguages = ref(store.itemList.language)
const filedataDetails = store.filedataDetails
const themeList = reactive([])
const tagList = reactive([])
const eventsMlThema = ref(false)
const eventsMlTag = ref(false)
const selectPredMain = ref([])
const predMain = reactive([])
const selectPredSub = ref([])
const predSub = reactive([])
const selectPredMainTags = ref([])
const predMainTags = reactive([])
const selectPredSubTags = ref([])
const predSubTags = reactive([])
const predProbThemas = ref('')
const predProbTags = ref('')
const predPrefectureTags = reactive([])
const addTag = ref('')
const errorCheckMessage = reactive([])
const placeholderDate = ref('')
const tableErrorMessage = ref('')
const isFreeKeywordError = ref(false)
const freeKeywordErrorMessage = ref('')

// 項目ごとのitemDisplayFlgの値がfoldならばfalse、それ以外はtrueを設定
const expanded = reactive({
  theme: '',
  tags: '',
  language: '',
  vocabulary: '',
  term: '',
  frequency: '',
  spatial: '',
  temporal: ''
})

// 非表示設定
const hideFlgs = reactive({
  frequency: '',
  language: '',
  spatial: '',
  tags: '',
  temporal: '',
  term: '',
  theme: '',
  vocabulary: ''
})

// 完了ダイアログ
const completeDialog = reactive({
  isDisplay: false,
  message: '',
  errorFlg: false,
})

// 表示項目がすべて非表示の場合にtrue
const isAllHide = computed( () => {
  // テンプレート編集中はfalse
  if(store.selectedMode.mode === 'template'){
    store.updateDatasetOptionAllHide(false)
    return false
  }

  for(var key in hideFlgs){
    // 1つでもhideでない項目があったら、falseを返す
    if (store.itemDisplayFlg[key] !== 'hide'){
      store.updateDatasetOptionAllHide(false)
      return false
    }
  }

  store.updateDatasetOptionAllHide(true)
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

// 自動補完候補
const autoCorrect = reactive({
  vocabulary: [],
  term: []
})

///////////
// watch
///////////
// データセットのキーワード監視
watch(() => catalogParameter.tags,
  (newReg, oldReg) => {
  if (oldReg.length !== newReg.length) {
    isFreeKeywordError.value = false
    freeKeywordErrorMessage.value = ''
  }
})

function isValidDateFormat(value) {
  if (!/^-?[0-9]{4}\-(0[1-9]||1[0-2])\-(0[1-9]|[12][0-9]|3[01])$/.test(value)) {
    return false
  }
  if (value.indexOf('02-30') !== -1 || value.indexOf('02-31') !== -1 || value.indexOf('04-31') !== -1 || value.indexOf('06-31') !== -1 || value.indexOf('09-31') !== -1 || value.indexOf('11-31') !== -1) {
    return false
  }
  if (value.indexOf('02-29') !== -1) {
    let year = value.slice(0, 4)
    console.log('year', year)
    if ((year % 4 == 0) && (year % 100 != 0) || (year % 400 == 0)) {
      return true
    } else {
      return false
    }
  }
  let date = new Date(value)
  return !isNaN(date.getDate())
}

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
// 語彙
axios
  .post(config.apiPrefix + '/datacatalog/autocorrect', { label: 'vocabulary', value: catalogParameter.vocabulary })
  .then((response) => {
    autoCorrect.vocabulary = response.data.candidates
  })
  .catch(err => {
    autoCorrect.vocabulary = []
    console.log('error message:', err.response.data.message)
  })
// 用語
axios
  .post(config.apiPrefix + '/datacatalog/autocorrect', { label: 'term', value: catalogParameter.term })
  .then((response) => {
    autoCorrect.term = response.data.candidates
  })
  .catch(err => {
    autoCorrect.term = []
    console.log('error message:', err.response.data.message)
  })

onMounted(function(){
  console.log('-- DatasetOption.vue onMounted --')

  topScroll()

  // 日時分析機能実行条件
  // カタログ作成モードであること
  // コンフィグで日時分析が有効で設定されていること
  // 「データセットの対象期間フィールドが空であること
  // 「ファイルのカラム名」が入力されていること
  if (store.selectedMode.mode === 'new_release_register' || store.selectedMode.mode === 'new_detail_register' || store.selectedMode.mode === 'new_both_register' || store.selectedMode.mode === 'release_duplicate' || store.selectedMode.mode === 'detail_duplicate' || store.selectedMode.mode === 'both_duplicate') {
    if (store.configValue.temporal) {
      if (filedataDetails.length && filedataDetails[0].columnName && !store.dataCalender.start && !store.dataCalender.end) {
        const analyzeExtractTemporal = {
          text: store.catalogTitle + store.catalogDescription,
          filepath: filedataDetails[0].dataname,
          column_name: filedataDetails[0].columnName,
          input_datetime_format: 'auto'
        }
        axios.post(config.apiPrefix + '/extracttemporal', analyzeExtractTemporal)
          .then(response => {
            if (response.data.start_datetime === 'None') {
              catalogParameter.startDate = ''
            } else {
              catalogParameter.startDate = response.data.start_datetime.slice(0, 10)
            }
            if (response.data.end_datetime === 'None') {
              catalogParameter.endDate = ''
            } else {
              catalogParameter.endDate = response.data.end_datetime.slice(0, 10)
            }
          })
          .catch(err => {
            console.log('error message:', err.response.data.message)
            catalogParameter.startDate = ''
            catalogParameter.endDate = ''
            completeDialog.isDisplay = true
            completeDialog.message = err.response.data.message || '日時分析に失敗しました。\n管理者に問い合わせてください。'
            completeDialog.errorFlg = true
          })
      }
    }
    // 地域分析機能実行条件
    // カタログ作成モードであること
    // コンフィグで地域分析が有効で設定されていること
    // filedataDetails[0]のデータがcsvファイルであること
    // filedataDetails[0]のデータの取得・保存が完了していること（datanameを保持していること）
    if (store.configValue.spatial) {
      if (filedataDetails[0] && filedataDetails[0].dataname && (filedataDetails[0].format === 'csv' || filedataDetails[0].format === 'CSV')) {
        extractSpatialActive.value = false
      }
    }
  }
  // 主分類の読み込み
  axios.get('datalist/themeList.json')
    .then((response) => {
      for (var num = 0; num < response.data.length; num++){
        themeList.push(response.data[num])
      }
    })
    .catch(err => {
      console.log('error message:主分類の読み込みに失敗しました。\n管理者に問い合わせてください。')
      completeDialog.isDisplay = true
      completeDialog.message = '主分類の読み込みに失敗しました。\n管理者に問い合わせてください。'
      completeDialog.errorFlg = true
    })
  // キーワードの読み込み
  axios.get('datalist/tagList.json')
    .then((response) => {
      for (var num = 0; num < response.data.length; num++){
        tagList.push(response.data[num])
      }
    })
    .catch(err => {
      console.log('error message:キーワードの読み込みに失敗しました。\n管理者に問い合わせてください。')
      completeDialog.isDisplay = true
      completeDialog.message = 'キーワードの読み込みに失敗しました。\n管理者に問い合わせてください。'
      completeDialog.errorFlg = true
    })
  // 現在日付取得
  getCurrentDate()
})

// 自動補完候補取得
function filterFn(val, update, abort, field) {
  setTimeout(() => {
    update(() => {
      var req = {
        label: field,
        value: val
      }
      // 自動補完候補検索API実行
      axios
        .post(config.apiPrefix + '/datacatalog/autocorrect', req)
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
function setModel(val, field) {
  catalogParameter[field] = val
}

// 必須フィールドエラー判定
function errorFieldMandatory(displayFlg, value) {
  if (displayFlg !== 'mandatory') {
    // 必須入力フィールドではないためエラーにしない
    return false
  }
  if (store.selectedMode.mode === 'template') {
    // テンプレート編集時はエラー判定をしない
    return false
  }
  if (!value) {
    // 必須入力フィールドかつ値がない場合はエラー(テンプレート編集時は除く)
    return true
  }
  // 入力値問題なし
  return false
}

function isErrorDatasetDate(displayFlg, value, type){
  if(type === 'startDate'){
    // 開始日が終了日より後の場合はエラー
    if (value && catalogParameter.endDate && (value > catalogParameter.endDate)) {
      return true
    }
  }else if(type === 'endDate'){
    // 終了日が開始日より前の場合はエラー
    if (value && catalogParameter.startDate && (value < catalogParameter.startDate)) {
      return true
    }
  }

  if (store.selectedMode.mode === 'template') {
    // テンプレート編集時はエラー判定をしない
    return false
  }

  // 必須入力フィールドかつ値がない場合はエラー
  if (displayFlg === 'mandatory' && value === '') {
    return true
  }

  // 問題なし
  return false
}

function errorDatasetDateMessage(displayFlg, value, type){
  if(type==='startDate'){
    // 開始日が終了日より後の場合はエラー
    if (value && catalogParameter.endDate && (value > catalogParameter.endDate)) {
      return INVALID_ERROR_MESSAGE
    }
  }else if(type==='endDate'){
    // 終了日が開始日より前の場合はエラー
    if (value && catalogParameter.startDate && (value < catalogParameter.startDate)) {
      return INVALID_ERROR_MESSAGE
    }
  }
    
  if (store.selectedMode.mode === 'template') {
    // テンプレート編集時はエラー判定をしない
    return ''
  }

  // 必須入力フィールドかつ値がない場合はエラー
  if (displayFlg === 'mandatory' && value === '') {
    return EMPTY_ERROR_MESSAGE
  }

  // 問題なし
  return ''
}

function btnActionOpenThemas() {
  var i = 0
  var j = 0
  const analyseDataset = {
    analyse_type: 'theme',
    catarog_title: store.catalogTitle,
    catarog_description: store.catalogDescription
  }
  axios
    .post(config.apiPrefix + EXPECT_URL, analyseDataset)
    .then(async res => {
      // 予測候補を作成
      predMain.splice(0)
      for (i = 0; i < res.data.pred_main.length; i++) {
        predMain.push({
          label: String(res.data.pred_main[i].label).replace(/'/g, ''),
          value: String(res.data.pred_main[i].value).replace(/'/g, '')
        })
      }
      // 予測候補から選択済み項目を抽出
      for (i = 0; i < catalogParameter.theme.length; i++) {
        for (j = 0; j < predMain.length; j++) {
          if (catalogParameter.theme[i] === predMain[j].label) {
            selectPredMain.value.push(predMain[j].label)
          }
        }
      }

      // テーマ toplist
      predSub.splice(0)
      for (j = 0; j < res.data.pred_sub.length; j++) {
        predSub.push({
          label: String(res.data.pred_sub[j].label).replace(/'/g, ''),
          value: String(res.data.pred_sub[j].value).replace(/'/g, '')
        })
      }
      // 予測候補から選択済み項目を抽出
      for (i = 0; i < catalogParameter.theme.length; i++) {
        for (j = 0; j < predSub.length; j++) {
          if (catalogParameter.theme[i] === predSub[j].label) {
            selectPredSub.value.push(predSub[j].label)
          }
        }
      }
      predProbThemas.value = ''
      for (var k = 0; k < res.data.pred_prob.length; k++) {
        if (k === 0) {
          predProbThemas.value += String(res.data.pred_prob[k].label).replace(/'/g, '') + ('\n')
        } else {
          predProbThemas.value += String(res.data.pred_prob[k].label).replace(/'/g, '').replace(' ', '') + ('\n')
        }
      }
      eventsMlThema.value = true
    })
    .catch(err => {
      console.log('error message:', err.response.data.message)
      completeDialog.isDisplay = true
      completeDialog.message = err.response.data.message || '主分類分析に失敗しました。\n管理者に問い合わせてください。'
      completeDialog.errorFlg = true
    })
}

function btnActionCloseThemes() {
  var i = 0
  var j = 0
  var selectThemesList = []
  if (catalogParameter.theme.length) {
    for (i = 0; i < catalogParameter.theme.length; i++) {
      selectThemesList.push(catalogParameter.theme[i])
    }
    catalogParameter.theme.splice(0)
  }
  // テーマリストから予測候補、予測候補の上位リストの項目を除去
  var predList = []
  for (i = 0; i < predMain.length; i++) {
    predList.push(predMain[i].label)
  }
  for (i = 0; i < predSub.length; i++) {
    predList.push(predSub[i].label)
  }
  predList = predList.filter(function (x, i, self) {
    return self.indexOf(x) === i
  })
  for (i = 0; i < selectThemesList.length; i++) {
    for (j = 0; j < predList.length; j++) {
      if (selectThemesList[i] === predList[j]) {
        selectThemesList.splice(i, 1)
      }
    }
  }
  selectThemesList = selectThemesList.concat(selectPredMain.value, selectPredSub.value)
  // テーマリストの重複をはじく
  selectThemesList = selectThemesList.filter(function (x, i, self) {
    return self.indexOf(x) === i
  })
  // v-modelのテーマリストに反映
  for (i = 0; i < selectThemesList.length; i++) {
    catalogParameter.theme.push(selectThemesList[i])
  }
  eventsMlThema.value = false
  selectPredMain.value.splice(0)
  selectPredSub.value.splice(0)
}

function btnActionOpenTags() {
  // ここでデータをMLに送り結果を受け取る。
  var i = 0
  var j = 0
  const analyseDataset = {
    analyse_type: 'tag',
    catarog_title: store.catalogTitle,
    catarog_description: store.catalogDescription
  }
  isFreeKeywordError.value = false
  freeKeywordErrorMessage.value = ''
  axios
    .post(config.apiPrefix + EXPECT_URL, analyseDataset)
    .then(async res => {
      predMainTags.splice(0)
      for (i = 0; i < res.data.pred_main.length; i++) {
        predMainTags.push({
          label: String(res.data.pred_main[i].label).replace(/'/g, '').replace(' ', ''),
          value: String(res.data.pred_main[i].value).replace(/'/g, '').replace(' ', '')
        })
      }
      // 予測候補から選択済み項目を抽出
      for (i = 0; i < catalogParameter.tags.length; i++) {
        for (j = 0; j < predMainTags.length; j++) {
          if (catalogParameter.tags[i] === predMainTags[j].label) {
            selectPredMainTags.value.push(predMainTags[j].label)
          }
        }
      }
      // テーマ toplist
      predSubTags.splice(0)
      for (j = 0; j < res.data.pred_sub.length; j++) {
        predSubTags.push({
          label: String(res.data.pred_sub[j].label).replace(/'/g, '').replace(' ', ''),
          value: String(res.data.pred_sub[j].value).replace(/'/g, '').replace(' ', '')
        })
      }
      // 予測候補から選択済み項目を抽出
      for (i = 0; i < catalogParameter.tags.length; i++) {
        for (j = 0; j < predSubTags.length; j++) {
          if (catalogParameter.tags[i] === predSubTags[j].label) {
            selectPredSubTags.value.push(predSubTags[j].label)
          }
        }
      }
      predProbTags.value = ''
      for (var k = 0; k < res.data.pred_prob.length; k++) {
        predProbTags.value += String(res.data.pred_prob[k].label).replace(/'/g, '').replace(' ', '') + ('\n')
      }
    })
    .catch(err => {
      console.log('error message:', err.response.data.message)
      completeDialog.isDisplay = true
      completeDialog.message = err.response.data.message || 'キーワード分析に失敗しました。\n管理者に問い合わせてください。'
      completeDialog.errorFlg = true
    })
  // 都道府県の候補予測
  const analyseDatasetPrefecture = {
    analyse_type: 'prefecture',
    catarog_title: store.catalogTitle,
    catarog_description: store.catalogDescription
  }
  axios
    .post(config.apiPrefix + EXPECT_URL, analyseDatasetPrefecture)
    .then(async res => {
      predPrefectureTags.splice(0)
      for (var _pre = 0; _pre < res.data.pred_main.length; _pre++) {
        predPrefectureTags.push({
          label: String(res.data.pred_main[_pre].label).replace(/'/g, '').replace(' ', ''),
          value: String(res.data.pred_main[_pre].value).replace(/'/g, '').replace(' ', '')
        })
      }
      eventsMlTag.value = true
    })
    .catch(err => {
      console.log('error message:', err.response.data.message)
      completeDialog.isDisplay = true
      completeDialog.message = err.response.data.message || 'キーワード分析に失敗しました。\n管理者に問い合わせてください。'
      completeDialog.errorFlg = true
    })
}

function btnActionCloseTags() {
  var i = 0
  var j = 0
  var selectTagList = []
  if (catalogParameter.tags.length) {
    for (i = 0; i < catalogParameter.tags.length; i++) {
      selectTagList.push(catalogParameter.tags[i])
    }
    catalogParameter.tags.splice(0)
  }
  // テーマリストから予測候補、予測候補の上位リストの項目を除去
  var predList = []
  for (i = 0; i < predMainTags.length; i++) {
    predList.push(predMainTags[i].label)
  }
  for (i = 0; i < predSubTags.length; i++) {
    predList.push(predSubTags[i].label)
  }
  predList = predList.filter(function (x, i, self) {
    return self.indexOf(x) === i
  })
  for (i = 0; i < selectTagList.length; i++) {
    for (j = 0; j < predList.length; j++) {
      if (selectTagList[i] === predList[j]) {
        selectTagList.splice(i, 1)
      }
    }
  }
  selectTagList = selectTagList.concat(selectPredMainTags.value, selectPredSubTags.value)
  // テーマリストの重複をはじく
  selectTagList = selectTagList.filter(function (x, i, self) {
    return self.indexOf(x) === i
  })
  // v-modelのテーマリストに反映
  for (i = 0; i < selectTagList.length; i++) {
    catalogParameter.tags.push(selectTagList[i])
  }
  eventsMlTag.value = false
}

function btnActionAddTag() {
  // 空白のみのキーワードはエラー
  if (addTag.value === '' || !addTag.value.match(/\S/g)) {
    addTag.value = ''
    isFreeKeywordError.value = true
    freeKeywordErrorMessage.value = KEYWORD_ERROR_ONLY_SPACE
    return
  }
  if (addTag.value.match(/・/g)) {
    // 使用禁止文字を含むキーワードはエラー
    addTag.value = ''
    isFreeKeywordError.value = true
    freeKeywordErrorMessage.value = KEYWORD_ERROR_INVALID_SYMBOL
    return
  }
  if (addTag.value.length <= 1) {
    // 2文字未満のキーワードはエラー
    addTag.value = ''
    isFreeKeywordError.value = true
    freeKeywordErrorMessage.value = KEYWORD_ERROR_LOWER_LIMIT
    return
  }
  if (catalogParameter.tags === null) {
    catalogParameter.tags = []
  }
  // 重複がなければcatalogParameter.tagsに追加
  if (catalogParameter.tags.some(el => el === addTag.value)) {
    isFreeKeywordError.value = true
    freeKeywordErrorMessage.value = KEYWORD_ERROR_DUPLICAE
    console.log('キーワードが重複しているため追加できません。')
  } else {
    isFreeKeywordError.value = false
    freeKeywordErrorMessage.value = ''
    catalogParameter.tags.push(addTag.value)
  }
  // 重複なければディスプレイリストに追加
  if (tagList.some(el => el === addTag.value)) {
    console.log('キーワードが重複しているため追加できません。')
  } else {
    tagList.push(addTag.value)
  }
  addTag.value = ''
}

function startCalenderClose() {
  catalogParameter.startDate = catalogParameter.startDate.split('T')[0].replace(/\//g, '-')
  startCalenderFlg.value = false
}

function endCalenderClose() {
  catalogParameter.endDate = catalogParameter.endDate.split('T')[0].replace(/\//g, '-')
  endCalenderFlg.value = false
}

function startCalender() {
  startCalenderFlg.value = true
}

function endCalender() {
  endCalenderFlg.value = true
}

function geonameSearch() {
  if (countryKeyword.value !== '') {
    tableLoading.value = true
    pointNameList.splice(0)
    resultAllPoints.splice(0)
    resultData.value.splice(0)
    selectGeonamesWindow.value = true
    axios.get(config.apiPrefix + '/geonamesearch', {
      params: {
        keyword: String(countryKeyword.value)
      }
    })
      .then((response) => {
        tableLoading.value = false
        for (var num = 0; num < response.data.length; num++){
          resultAllPoints.push(response.data[num])
        }
        for (var i = 0; i < resultAllPoints.length; i++) {
          resultData.value.push({
            id: resultAllPoints[i].geonameId,
            name: resultAllPoints[i].name,
            country: resultAllPoints[i].countryName,
            adminname: resultAllPoints[i].adminName1,
            lat: resultAllPoints[i].lat,
            lng: resultAllPoints[i].lng,
            fcl: resultAllPoints[i].fcl
          })
          const labelname = resultAllPoints[i].geonameId + ' ' +
            resultAllPoints[i].name + ' ' +
            resultAllPoints[i].countryName + ' ' +
            resultAllPoints[i].adminName1 + ' ' +
            resultAllPoints[i].lat + ' ' +
            resultAllPoints[i].lng + ' ' +
            resultAllPoints[i].fcl
          pointNameList.push({
            label: labelname,
            value: labelname
          })
        }
      })
      .catch(err => {
        console.log('error message:', err.response.data.message)
        tableErrorMessage.value = err.response.data.message || '地域検索に失敗しました。管理者に問い合わせてください。'
        tableLoading.value = false
      })
  }
}

function rowClick(evt, row, index) {
  axios.get(config.apiPrefix + '/geonameIdsearch', {
    params: {
      geonameId: row.id
    }
  })
    .then((response) => {
      catalogParameter.spatialUrl = 'https://www.geonames.org/' + String(row.id)
      catalogParameter.spatialName = String(response.data)
      catalogParameter.spatial = '{"type":"Point", "coordinates":[' + String(row.lng) + ', ' + String(row.lat) + ']}'
      selectGeonamesWindow.value = false
    })
    .catch(err => {
      console.log('error message:', err.response.data.message)
      tableErrorMessage.value = err.response.data.message || '地域のフルネーム取得に失敗しました。管理者に問い合わせてください。'
    })
}

function analyzeSpatialData() {
  const analyzeExtractSpatial = {
    title: store.catalogTitle,
    filepath: filedataDetails[0].dataname,
    notes: store.catalogDescription,
    method: 'hybrid'
  }
  tableLoading.value = true
  pointNameList.splice(0)
  resultAllPoints.splice(0)
  resultData.value.splice(0)
  selectGeonamesWindow.value = true
  axios.post(config.apiPrefix + '/extractspatial', analyzeExtractSpatial)
    .then(response => {
      tableLoading.value = false
      for (var num = 0; num < response.data.spatial_list.length; num++){
        resultAllPoints.push(response.data.spatial_list[num])
      }
      for (var i = 0; i < resultAllPoints.length; i++) {
        var resultAdminName = ''
        var resultName = ''
        if (resultAllPoints[i].adminName2) {
          resultAdminName = resultAllPoints[i].adminName2
        } else {
          resultAdminName = resultAllPoints[i].adminName1
        }
        if (resultAllPoints[i].name) {
          resultName = resultAllPoints[i].name
        } else {
          resultName = resultAllPoints[i].adminName1
        }
        resultData.value.push({
          id: resultAllPoints[i].geonameId,
          name: resultName,
          // 取得データが国名データを保持していないため「日本」を固定で設定
          country: '日本',
          adminname: resultAdminName,
          lat: resultAllPoints[i].lat,
          lng: resultAllPoints[i].lng,
          fcl: resultAllPoints[i].fcl
        })
        const labelname = resultAllPoints[i].geonameId + ' ' +
          resultName + ' ' +
          // 取得データが国名データを保持していないため「日本」を固定で設定
          '日本' + ' ' +
          resultAdminName + ' ' +
          resultAllPoints[i].lat + ' ' +
          resultAllPoints[i].lng + ' ' +
          resultAllPoints[i].fcl
        pointNameList.push({
          label: labelname,
          value: labelname
        })
      }
    })
    .catch(err => {
      console.log('error message:', err.response.data.message)
      tableErrorMessage.value = err.response.data.message || '地域分析に失敗しました。管理者に問い合わせてください。'
      tableLoading.value = false
    })
}

function topScroll() {
  window.scrollTo(0, 0)
}

// エラーフラグの管理機能（次へボタン押下時、Dataset.vueから呼ばれる）
function checkErrorAllFields() {
  const mesEmptyTheme = 'データセットの主分類は入力必須項目です。入力をお願いします。'
  const mesEmptyTags = 'データセットのキーワードは入力必須項目です。入力をお願いします。'
  const mesEmptyLanguage = 'データセットの情報を記述する言語は入力必須項目です。入力をお願いします。'
  const mesEmptyVocabulary = '語彙は入力必須項目です。入力をお願いします。'
  const mesEmptyTerm = '用語は入力必須項目です。入力をお願いします。'
  const mesEmptyFrequency = 'データセットの提供頻度は入力必須項目です。入力をお願いします。'
  const mesEmptySpatial = 'データセットの対象地域は入力必須項目です。入力をお願いします。'
  const mesEmptyTemporal = 'データセットの対象期間は入力必須項目です。入力をお願いします。'
  const mesInvalidTemporal = 'データセットの対象期間の終了が開始より前に設定されています。'
  const invalidStartDateFormat = 'データセットの対象期間の開始に無効な値が入力されています。'
  const invalidEndDateFormat = 'データセットの対象期間の終了に無効な値が入力されています。'

  errorCheckMessage.splice(0)
  var noError = true
  // 各フィールドの入力有無の確認
  if (errorFieldMandatory(store.itemDisplayFlg.theme, catalogParameter.theme.length)) {
    errorCheckMessage.push(mesEmptyTheme)
    noError = false
  }
  if (errorFieldMandatory(store.itemDisplayFlg.tags, catalogParameter.tags.length)) {
    errorCheckMessage.push(mesEmptyTags)
    noError = false
  }
  if (errorFieldMandatory(store.itemDisplayFlg.language, catalogParameter.language.length)) {
    errorCheckMessage.push(mesEmptyLanguage)
    noError = false
  }
  if (errorFieldMandatory(store.itemDisplayFlg.vocabulary, catalogParameter.vocabulary)) {
    errorCheckMessage.push(mesEmptyVocabulary)
    noError = false
  }
  if (errorFieldMandatory(store.itemDisplayFlg.term, catalogParameter.term)) {
    errorCheckMessage.push(mesEmptyTerm)
    noError = false
  }
  if (errorFieldMandatory(store.itemDisplayFlg.frequency, catalogParameter.frequency)) {
    errorCheckMessage.push(mesEmptyFrequency)
    noError = false
  }
  if (errorFieldMandatory(store.itemDisplayFlg.spatial, catalogParameter.spatial)) {
    errorCheckMessage.push(mesEmptySpatial)
    noError = false
  }

    // 開始に無効な値が入力されているかの判定
  if (catalogParameter.startDate) {
    if(!isValidDateFormat(catalogParameter.startDate)){
      errorCheckMessage.push(invalidStartDateFormat)
      noError = false
    }
  }

  // 終了に無効な値が入力されているかの判定
  if (catalogParameter.endDate) {
    if(!isValidDateFormat(catalogParameter.endDate)){
      errorCheckMessage.push(invalidEndDateFormat)
      noError = false
    }
  }

  if (errorFieldMandatory(store.itemDisplayFlg.temporal, catalogParameter.startDate) || errorFieldMandatory(store.itemDisplayFlg.temporal, catalogParameter.endDate)) {
    errorCheckMessage.push(mesEmptyTemporal)
    noError = false
  } else {
    if (isErrorDatasetDate(store.itemDisplayFlg.temporal, catalogParameter.startDate,'startDate') || isErrorDatasetDate(store.itemDisplayFlg.temporal, catalogParameter.endDate, 'endDate')) {
      // データセットの対象期間の入力値の有効性確認
      errorCheckMessage.push(mesInvalidTemporal)
      noError = false
    }
  }

  return noError
}

// パラメータ更新
function commitStore() {
  store.updateDatasetOptionalInfoParameters(
    {
      selectThemes: catalogParameter.theme,
      selectTags: catalogParameter.tags,
      vocabulary: catalogParameter.vocabulary,
      term: catalogParameter.term,
      selectLanguage: catalogParameter.language,
      frequency: catalogParameter.frequency,
      spatialUrl: catalogParameter.spatialUrl,
      spatialName: catalogParameter.spatialName,
      spatial: catalogParameter.spatial,
      start: catalogParameter.startDate,
      end: catalogParameter.endDate,
      storeType: 'state'
    }
  )
}

function clearInputData() {
  // データセットの対象地域・データセットの対象地域（説明）・データセットの対象地域(緯度経度)を一括削除
  catalogParameter.spatialUrl = ''
  catalogParameter.spatialName = ''
  catalogParameter.spatial = ''
}

function getCurrentDate() {
  // 現在の日付を取得する
  var currentData = new Date()
  var year = currentData.getFullYear()
  var month = currentData.getMonth()+1
  var day = currentData.getDate()
  placeholderDate.value = year + "-" + month + "-" + day
}


defineExpose({
  checkErrorAllFields,
  commitStore
})

</script>

<template>
  <div :style="fillHeightClass" class="dataset-option">
    <q-card class="q-ma-sm q-card-background-white" v-show="hideFlgs.theme">
      <q-card-section>
        <font size='5' color='#1d468f'>データセットの主分類</font>
        <q-btn
          color="grey"
          round
          flat
          dense
          :icon="expanded.theme ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
          @click="expanded.theme = !expanded.theme"
        />
        <q-slide-transition>
          <div v-show="expanded.theme">
            <br>
            このデータセットに含まれるデータがどのようなジャンルに該当するかを選択してください。<br>
            <div v-if="store.configValue.theme">
              <div class="cp_tooltip">推薦される候補
                <span class="cp_tooltiptext">
                  <b>【主分類の候補について】</b><br>
                    &emsp; 下記に入力した値から候補を推測します。<br>
                    &emsp; ・データセットのタイトル<br>
                    &emsp; ・データセットの説明
                </span>
              </div>
              から選択する場合は、候補表示のボタンを押してください。<br>
            </div>
            CKAN変数名：extras:theme
            <q-item>
              <div class="input-item" style="padding-right:25px">
                <q-select
                  placeholder="例： 観光 > イベント"
                  use-chips
                  color="light-blue-10"
                  multiple
                  v-model="catalogParameter.theme"
                  :options="themeList"
                  :error-message="EMPTY_ERROR_MESSAGE"
                  :error="errorFieldMandatory(store.itemDisplayFlg.theme, catalogParameter.theme.length)"
                />
              </div>
              <div v-if="store.configValue.theme">
                <q-btn
                  outline
                  @click="btnActionOpenThemas()"
                  label="候補表示"
                  color="light-blue-10"
                />
              </div>
            </q-item>
          </div>
        </q-slide-transition>
      </q-card-section>
    </q-card>
    <q-card class="q-ma-sm q-card-background-white" v-show="hideFlgs.tags">
      <q-card-section>
        <font size='5' color='#1d468f'>データセットのキーワード</font>
        <q-btn
          color="grey"
          round
          flat
          dense
          :icon="expanded.tags ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
          @click="expanded.tags = !expanded.tags"
        />
        <q-slide-transition>
          <div v-show="expanded.tags">
            <br>
            データセットに関連するキーワードを選択してください。<br>
            <div v-if="store.configValue.keyword">
               <div class="cp_tooltip">推薦される候補
                 <span class="cp_tooltiptext">
                   <b>【キーワードの候補について】</b><br>
                     &emsp; 下記に入力した値から候補を推測します。<br>
                     &emsp; ・データセットのタイトル<br>
                     &emsp; ・データセットの説明
                 </span>
               </div>
               から選択する場合は、候補表示のボタンを押してください。<br>
             </div>
             もし選択肢にないキーワードを入力する場合は、自由記述の欄に自由なキーワードを入力してください。<br>
             CKAN変数名：tags
            <q-item>
              <div class="input-item" style="padding-right: 25px">
                <q-select
                  placeholder="例：観光, 観光スポット, スポーツ, イベント"
                  use-chips
                  color="light-blue-10"
                  multiple
                  v-model="catalogParameter.tags"
                  :options="tagList"
                  :error-message="EMPTY_ERROR_MESSAGE"
                  :error="errorFieldMandatory(store.itemDisplayFlg.tags, catalogParameter.tags.length)"
                />
              </div>
              <div v-if="store.configValue.keyword">
                <q-btn
                  outline
                  @click="btnActionOpenTags()"
                  label="候補表示"
                  color="light-blue-10"
                />
              </div>
            </q-item>
            <q-item>
              <div class="input-item">
                <q-input
                  v-model="addTag"
                  label="自由なキーワードの追加"
                  :error="isFreeKeywordError"
                  :error-message="freeKeywordErrorMessage"
                />
              </div>
              <div>
                <q-btn
                  outline
                  label="追加"
                  @click="btnActionAddTag()"
                  color="light-blue-10"
                />
              </div>
            </q-item>
          </div>
        </q-slide-transition>
      </q-card-section>
    </q-card>
    <!-- ################# -->
    <div class="dialog-area">
      <q-dialog persistent transition-show="scale" transition-hide="scale" v-model="eventsMlThema">
        <q-card :content-css="{minWidth: '80vw', minHeight: '80vh'}" color="light-blue-10">
          <q-page padding class="docs-input row justify-center">
            <div class="dialog-area">
              <span slot:name="label"><font size="4">予測候補</font></span>
              <div class="q-px-sm">機械で予測した分類テーマです。</div>
              <q-option-group
                type="checkbox"
                color="light-blue-10"
                v-model="selectPredMain"
                :options="predMain"
              />
              <p />
              <span slot:name="label"><font size="4">予測候補の上位リスト</font></span>
              <div class="q-px-sm">機械で予測した分類テーマの上位テーマです。</div>
              <q-option-group
                type="checkbox"
                color="light-blue-10"
                v-model="selectPredSub"
                :options="predSub"
              />
              <p />
              <span slot:name="label"><font size="4">予測候補の確率</font></span>
              <q-input type="textarea" rows="5" v-model="predProbThemas" hint="各候補の確率です。" readonly/>
              <div align="right">
                <q-btn color="light-blue-10" @click="btnActionCloseThemes()" label="閉じる" />
              </div>
            </div>
          </q-page>
        </q-card>
      </q-dialog>
    </div>
    <!-- ################# -->
    <!-- ################# -->
    <div class="dialog-area">
      <q-dialog persistent transition-show="scale" transition-hide="scale" v-model="eventsMlTag">
        <q-card :content-css="{minWidth: '80vw', minHeight: '80vh'}" color="light-blue-10">
          <q-page padding class="docs-input row justify-center">
            <div class="dialog-area">
              <span slot:name="label"><font size="4">予測候補</font></span>
              <div class="q-px-sm">機械で予測したキーワードです</div>
              <q-option-group
                type="checkbox"
                color="light-blue-10"
                v-model="selectPredMainTags"
                :options="predMainTags"
              />
              <p />
              <q-item>
                <!-- タグの予測 -->
                <q-item-side>
                  <div style="padding-right: 70px; padding-top:10px">
                    <span slot:name="label"><font size="4">予測候補の上位リスト</font></span>
                    <div class="q-px-sm">機械で予測したキーワードの上位キーワードです。</div>
                    <q-option-group
                      type="checkbox"
                      text-color="black"
                      color="light-blue-10"
                      v-model="selectPredSubTags"
                      :options="predSubTags"
                    />
                    <!-- 都道府県の予測 -->
                    <q-option-group
                      type="checkbox"
                      color="light-blue-10"
                      v-model="selectPredSubTags"
                      :options="predPrefectureTags"
                    />
                  </div>
                  <p />
                </q-item-side>
              </q-item>
              <span slot:name="label"><font size="4">予測候補の確率</font></span>
              <q-input type="textarea" rows="5" v-model="predProbTags" hint="各候補の確率です。" readonly/>
              <div align="right">
                <q-btn color="light-blue-10" @click="btnActionCloseTags()" label="閉じる" />
              </div>
            </div>
          </q-page>
        </q-card>
      </q-dialog>
    </div>
    <q-card class="q-ma-sm q-card-background-white" v-show="hideFlgs.language">
      <q-card-section>
        <font size='5' color='#1d468f'>データセットの情報を記述する言語</font>
        <q-btn
          color="grey"
          round
          flat
          dense
          :icon="expanded.language ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
          @click="expanded.language = !expanded.language"
        />
        <q-slide-transition>
          <div v-show="expanded.language">
            <br>
            <p>データセットがどの言語で記述されているかを選択してください(複数選択可)。<br>
            CKAN変数名：extras:language
            </p>
            <q-select
              placeholder="例：日本語"
              use-chips
              multiple
              filter
              class="input-item"
              v-model="catalogParameter.language"
              :options="optLanguages"
              color="light-blue-10"
              :error-message="EMPTY_ERROR_MESSAGE"
              :error="errorFieldMandatory(store.itemDisplayFlg.language, catalogParameter.language.length)"
            />
          </div>
        </q-slide-transition>
      </q-card-section>
    </q-card>
    <q-card class="q-ma-sm q-card-background-white" v-show="hideFlgs.vocabulary">
      <q-card-section>
        <font size="5" color="#1d468f">語彙</font>
        <q-btn
          color="grey"
          round
          flat
          dense
          :icon="expanded.vocabulary ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
          @click="expanded.vocabulary = !expanded.vocabulary"
        />
        <q-slide-transition>
          <div v-show="expanded.vocabulary">
            <br>
            <p>データセットの内容の記述（データ項目見出し、データ項目の値）で使われる語彙を定義しているURLを入力してください。<br>
            CKAN変数名：extras:vocabulary
            </p>
            <q-select
              v-model="catalogParameter.vocabulary"
              placeholder="例：http://imi.go.jp/ns/core/RDF#"
              use-input
              hide-selected
              fill-input
              input-debounce="0"
              class="input-item"
              :options="autoCorrect.vocabulary"
              @filter="(val, update, abort) => { filterFn(catalogParameter.vocabulary, update, abort, 'vocabulary') }"
              @input-value="(val) => { setModel(val, 'vocabulary') }"
              :error-message="EMPTY_ERROR_MESSAGE"
              :error="errorFieldMandatory(store.itemDisplayFlg.vocabulary, catalogParameter.vocabulary)"
              hide-dropdown-icon
            />
          </div>
        </q-slide-transition>
      </q-card-section>
    </q-card>
    <q-card class="q-ma-sm q-card-background-white" v-show="hideFlgs.term">
      <q-card-section>
        <font size="5" color="#1d468f">用語</font>
        <q-btn
          color="grey"
          round
          flat
          dense
          :icon="expanded.term ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
          @click="expanded.term = !expanded.term"
        />
        <q-slide-transition>
          <div v-show="expanded.term">
            <br>
            <p>データセットの内容の記述（データ項目見出し、データ項目の値）で使われる代表的な用語を入力してください。複数ある場合は、カンマ区切りで入力してください。<br>
            CKAN変数名：extras:term
            </p>
            <q-select
              v-model="catalogParameter.term"
              placeholder="例：人型,住所"
              use-input
              hide-selected
              fill-input
              input-debounce="0"
              class="input-item"
              :options="autoCorrect.term"
              @filter="(val, update, abort) => { filterFn(catalogParameter.term, update, abort, 'term') }"
              @input-value="(val) => { setModel(val, 'term') }"
              :error-message="EMPTY_ERROR_MESSAGE"
              :error="errorFieldMandatory(store.itemDisplayFlg.vocabulary, catalogParameter.term)"
              hide-dropdown-icon
            />
          </div>
        </q-slide-transition>
      </q-card-section>
    </q-card>
    <q-card class="q-ma-sm q-card-background-white" v-show="hideFlgs.frequency">
      <q-card-section>
        <font size="5" color="#1d468f">データセットの提供頻度</font>
        <q-btn
          color="grey"
          round
          flat
          dense
          :icon="expanded.frequency ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
          @click="expanded.frequency = !expanded.frequency"
        />
        <q-slide-transition>
          <div v-show="expanded.frequency">
            <br>
            <p>データセットが提供・更新される頻度を選択してください。<br>
            CKAN変数名：extras:frequency
            </p>
            <div class="row justify-start">
              <q-list no-border style="width: 500px;" class="row justify-start">
                <q-item>
                  <q-item-section>
                    <q-select
                      style="width: 300px;"
                      v-model="catalogParameter.frequency"
                      :options="store.itemList.frequency"
                      :error-message="EMPTY_ERROR_MESSAGE"
                      :error="errorFieldMandatory(store.itemDisplayFlg.frequency, catalogParameter.frequency)"
                    >
                      <template v-if="catalogParameter.frequency" v-slot:append>
                        <q-icon name="cancel" @click.stop="catalogParameter.frequency = ''" class="cursor-pointer" />
                      </template>
                    </q-select>
                  </q-item-section>
                </q-item>
              </q-list>
            </div>
          </div>
        </q-slide-transition>
      </q-card-section>
    </q-card>
    <q-card class="q-ma-sm q-card-background-white" v-show="hideFlgs.spatial">
      <q-card-section>
        <font size="5" color="#1d468f">データセットの対象地域</font>
        <q-btn
          color="grey"
          round
          flat
          dense
          :icon="expanded.spatial ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
          @click="expanded.spatial = !expanded.spatial"
        />
        <q-slide-transition>
          <div v-show="expanded.spatial">
            <br>
            <div v-if="store.configValue.geonames">
              データセットの対象地域を選択してください。<br>
              国名や都道府県名、地方公共団体名、スポット名などの地名のキーワードを入力して、検索ボタンを押し、該当する地名を選択してください。<br>
              選択すると、地名を一意に表すURL、名前、経度や緯度が自動的に表示されます。<br>
            </div>
            <div v-else>
              データセットの対象地域を入力してください。<br>
            </div>
            <div v-if="store.configValue.spatial">
              下記の条件にすべて当てはまる場合、候補表示ボタンを押下し
              <div class="cp_tooltip">推薦される候補
                <span class="cp_tooltiptext">
                  <b>【対象地域の候補について】</b><br>
                    &emsp; 下記に入力した値から候補を推測します。<br>
                    &emsp; ・データセットのタイトル<br>
                    &emsp; ・データセットの説明<br>
                    &emsp; ・データ概要情報の配信1のデータ内容
                </span>
              </div>
              から選択が可能です。<br>
              ・新規登録時または登録再開時<br>
              ・データ概要情報の配信1がcsvファイルである<br>
              ・データ概要情報の配信1の取り込み(入力支援機能を利用)を完了している<br>
              CKAN変数名：extras:spatial_url、extras:spatial_text、extras:spatial
            </div>
            <q-item style="padding-left: 0;">
              <div v-if="store.configValue.geonames">
                <div class="input-item">
                  <q-input
                    v-model="countryKeyword"
                    placeholder="例：横浜市"
                  />
                </div>
              </div>
              <div v-if="store.configValue.geonames">
                <div class="q-px-sm q-mb-lg">
                  <q-btn
                    label="検索"
                    color="light-blue-10"
                    @click="geonameSearch()"
                  />
                </div>
              </div>
              <div v-if="store.configValue.spatial">
                <div class="q-px-sm q-mb-lg">
                  <q-btn
                    label="候補表示"
                    color="light-blue-10"
                    @click="analyzeSpatialData()"
                    :disable="extractSpatialActive"
                  />
                </div>
              </div>
              <div v-if="store.configValue.geonames">
                <div class="q-px-sm q-mb-lg">
                  <q-btn
                    outline
                    label="クリア"
                    color="primary"
                    @click="clearInputData()"
                  />
                </div>
              </div>
            </q-item>
            <div v-if="store.configValue.geonames">
              <div class="input-item">
                <br>
                <span slot:name="label"><font size="3" color="#1d468f">データセットの対象地域</font></span>
                <q-input
                  readonly
                  v-model="catalogParameter.spatialUrl"
                  :error-message="EMPTY_ERROR_MESSAGE"
                  :error="errorFieldMandatory(store.itemDisplayFlg.spatial, catalogParameter.spatialUrl)"
                />
                <br>
                <span slot:name="label"><font size="3" color="#1d468f">データセットの対象地域（説明）</font></span>
                <q-input
                  readonly
                  v-model="catalogParameter.spatialName"
                  :error-message="EMPTY_ERROR_MESSAGE"
                  :error="errorFieldMandatory(store.itemDisplayFlg.spatial, catalogParameter.spatialName)"
                />
                <br>
                <span slot:name="label"><font size="3" color="#1d468f">データセットの対象地域（緯度経度）</font></span>
                <q-input
                  readonly
                  v-model="catalogParameter.spatial"
                  :error-message="EMPTY_ERROR_MESSAGE"
                  :error="errorFieldMandatory(store.itemDisplayFlg.spatial, catalogParameter.spatial)"
                />
              </div>
            </div>
            <div v-else>
              <div class="input-item">
                <span slot:name="label"><font size="3" color="#1d468f">データセットの対象地域</font></span>
                <q-input
                  v-model="catalogParameter.spatialUrl"
                  :error-message="EMPTY_ERROR_MESSAGE"
                  :error="errorFieldMandatory(store.itemDisplayFlg.spatial, catalogParameter.spatialUrl)"
                  placeholder="例：https://www.geonames.org/1864529"
                />
                <br>
                <span slot:name="label"><font size="3" color="#1d468f">データセットの対象地域（説明）</font></span>
                <q-input
                  v-model="catalogParameter.spatialName"
                  :error-message="EMPTY_ERROR_MESSAGE"
                  :error="errorFieldMandatory(store.itemDisplayFlg.spatial, catalogParameter.spatialName)"
                  placeholder="例：日本>東京都>千代田区"
                />
                <br>
                <span slot:name="label"><font size="3" color="#1d468f">データセットの対象地域（緯度経度）</font></span>
                <q-input
                  v-model="catalogParameter.spatial"
                  :error-message="EMPTY_ERROR_MESSAGE"
                  :error="errorFieldMandatory(store.itemDisplayFlg.spatial, catalogParameter.spatial)"
                  placeholder="例：{'type':'Point', 'coordinates':[139.75363, 35.69402]}"
                />
              </div>
            </div>
          </div>
        </q-slide-transition>
      </q-card-section>
    </q-card>
    <q-card class="q-ma-sm q-card-background-white" v-show="hideFlgs.temporal">
      <q-card-section>
        <font size="5" color="#1d468f">データセットの対象期間</font>
        <q-btn
          color="grey"
          round
          flat
          dense
          :icon="expanded.temporal ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
          @click="expanded.temporal = !expanded.temporal"
        />
        <q-slide-transition>
          <div v-show="expanded.temporal">
            <br>
            データセットに収録されている配信が対象とする期間を選択してください。<br>
            未来に渡って継続して配信を収集する場合、終了年月日は入力不要です。<br>
            下記の条件にすべて当てはまる場合、
            <div class="cp_tooltip">推測機能
              <span class="cp_tooltiptext">
                <b>【対象期間の推測機能について】</b><br>
                  &emsp; 下記に入力した値から推測します。<br>
                  &emsp; ・データセットのタイトル<br>
                  &emsp; ・データセットの説明<br>
                  &emsp; ・データ概要情報の配信1のデータ内容<br>
                  &emsp; ・データ概要情報の配信1のファイルカラム名
              </span>
            </div>
            が実行されます。<br>
            ・開始・終了フィールドが未設定<br>
            ・カタログの新規登録時または登録再開時<br>
            ・データ概要情報の配信1のファイルカラム名が設定されている<br>
            ・データ概要情報の配信1の取り込み(入力支援機能を利用)を完了している<br>
            推測機能によって日付データが取得できた場合、開始・終了フィールドに自動入力されます。<br>
            CKAN変数名：extras:temporal_start、extras:temporal_end
            <p />
            <q-list no-border style="width: 400px; padding-left: 50px">
              <q-item>
                <q-item-section>
                  <font color="#1d468f">開始</font>
                </q-item-section>
                <q-item-label>
                  <q-input
                    v-model="catalogParameter.startDate"
                    :error="isErrorDatasetDate(store.itemDisplayFlg.temporal, catalogParameter.startDate,'startDate')"
                    :error-message="errorDatasetDateMessage(store.itemDisplayFlg.temporal, catalogParameter.startDate,'startDate')"
                    mask="####-##-##"
                    :rules="[v => v === '' || isValidDateFormat(v) || '【無効な値】']"
                    :placeholder="placeholderDate"
                  />
                </q-item-label>
                <q-item-section>
                  <q-btn
                    icon="date_range"
                    style="width: 40px;"
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
              <p />
              <q-item>
                <q-item-section>
                  <font color="#1d468f">終了</font>
                </q-item-section>
                <q-item-label>
                  <q-input
                    v-model="catalogParameter.endDate"
                    :error="isErrorDatasetDate(store.itemDisplayFlg.temporal, catalogParameter.endDate,'endDate')"
                    :error-message="errorDatasetDateMessage(store.itemDisplayFlg.temporal, catalogParameter.endDate,'endDate')"
                    mask="####-##-##"
                    :rules="[v =>  v === '' || isValidDateFormat(v) || '【無効な値】']"
                    :placeholder="placeholderDate"
                  />
                </q-item-label>
                <q-item-section>
                  <q-btn
                    icon="date_range"
                    style="width: 40px;"
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
          </div>
        </q-slide-transition>
      </q-card-section>
    </q-card>
    <!-- ###################### -->
    <!-- 以下、ポップアップ画面 -->
    <!-- ###################### -->

    <!-- 完了ダイアログ -->
    <CompleteDialog
      v-bind:dialogInfo="completeDialog"
      @close-dialog="completeDialog.isDisplay = false"
    />

    <!-- データセットの対象地域の検索・分析結果テーブル -->
    <q-dialog transition-show="scale" transition-hide="scale" full-width v-model="selectGeonamesWindow">
      <q-card :content-css="{minWidth: '80vw', minHeight: '80vh'}" color="light-blue-1">
        <div style="padding: 50px">
          <div class="q-display-1 q-mb-md"><font color="#1d468f">検索結果一覧</font></div>
          <q-table
            :rows="resultData"
            :columns="columns"
            row-key="id"
            :loading=tableLoading
            @row-click="rowClick"
          >
            <q-tr
              slot:name="body"
              v-slot="props"
              :props="props"
              @click="rowClick(props.row)"
              class="cursor-pointer"
            >
              <q-td v-for="col in props.cols" :key="col.name" :props="props">
                {{ col.value }}
              </q-td>
            </q-tr>
          </q-table>
          <div align="left">
            <font size="3" color="#FF0000">{{tableErrorMessage}}</font>
          </div>
          <p />
          <div align="right">
            <q-btn
              color="light-blue-10"
              label="閉じる"
              @click="selectGeonamesWindow = false, tableErrorMessage = ''"
            />
          </div>
        </div>
      </q-card>
    </q-dialog>

    <!-- 開始年月日カレンダー -->
    <q-dialog transition-show="scale" transition-hide="scale" v-model="startCalenderFlg">
      <q-card :content-css="{minWidth: '80vw', minHeight: '80vh'}" color="light-blue-10">
        <div style="padding: 50px">
          <div class="q-display-1 q-mb-md"><font color="#1d468f">開始年月日&nbsp;カレンダー</font></div>
          <q-date
            v-model="catalogParameter.startDate"
            minimal
            color="light-blue-10"
            @update:modelValue="startCalenderClose()"
          />
        </div>
      </q-card>
    </q-dialog>

    <!-- 終了年月日カレンダー -->
    <q-dialog transition-show="scale" transition-hide="scale" v-model="endCalenderFlg">
      <q-card :content-css="{minWidth: '80vw', minHeight: '80vh'}" color="light-blue-10">
        <div style="padding: 50px">
          <div class="q-display-1 q-mb-md"><font color="#1d468f">終了年月日&nbsp;カレンダー</font></div>
          <q-date
            v-model="catalogParameter.endDate"
            minimal
            color="light-blue-10"
            @update:modelValue="endCalenderClose()"
          />
        </div>
      </q-card>
    </q-dialog>

    <!-- エラーメッセージ -->
    <div v-for="message in errorCheckMessage" :key="message">
      <font size="3" color="#FF0000">{{message}}</font>
    </div>

    <!-- 全て非表示項目だった場合、表示するメッセージ -->
    <q-card v-show="isAllHide">
      <q-card-section>
        <div class="text-h6" style="color: #1d468f;">データセット情報（任意）の入力項目はありません</div>
      </q-card-section>
    </q-card>
  </div>
</template>

<style>
.dialog-area{
  width: 700px;
  max-width: 90vw;
}

.dataset-option .input-item{
  width: 700px;
}

.cp_tooltip {
  position: relative;
  display: inline-block;
  cursor: pointer;
  background: linear-gradient(transparent 90%, #add8e6 60%);
}

.cp_tooltip .cp_tooltiptext {
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
</style>
