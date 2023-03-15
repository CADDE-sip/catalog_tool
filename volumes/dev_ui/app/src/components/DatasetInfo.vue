<script setup>
import { reactive, onMounted, watch } from 'vue'
import { useStore } from '../stores/store'
import CompleteDialog from './dialog/CompleteDialog.vue'
import { config } from'boot/config'
import axios from 'axios'

const store = useStore();
// データセットの説明の最大文字列長
const DESCRIPTION_MAX_LENGTH = 1000
// 必須入力項目エラー文言（未入力）
const ERROR_MESSAGE = {
  title: 'データセットのタイトルは入力必須項目です。入力をお願いします。',
  description: 'データセットの説明は入力必須項目です。入力をお願いします。',
  url: 'データセットの説明ページURLは入力必須項目です。入力をお願いします。',
  registOrg: 'ユーザの属する組織は入力必須項目です。入力をお願いします。',
  caddeProviderId: '提供者IDは入力必須項目です。入力をお願いします。',
  publisherUri: 'データセットの公開者は入力必須項目です。入力をお願いします。',
  publisherName: 'データセットの公開者（説明）は入力必須項目です。入力をお願いします。',
  creatorUrl: 'データセットの作成者は入力必須項目です。入力をお願いします。',
  creatorName: 'データセットの作成者（説明）は入力必須項目です。入力をお願いします。',
  contactUrl: 'データセットの窓口は入力必須項目です。入力をお願いします。',
  contactName: 'データセットの窓口（説明）は入力必須項目です。入力をお願いします。'
}
// 必須入力項目エラー文言（文字列長）
const ERROR_MESSAGE_LENGTH = {
  description: 'データセットの説明が1000文字を超えています。1000文字以内になるように記入をお願いします。'
}
// カタログパラメータ名とCKAN変数名の紐づけデータ
const KEYMAP = {
  title: 'title',
  url: 'url',
  publisherUri: 'publisher_uri',
  creatorUrl: 'creator_url',
  contactUrl: 'contact_url'
}

const catalogParameter = reactive({
  title: store.catalogTitle,
  description: store.catalogDescription,
  url: store.datasetDescriptionUrl,
  caddeDatasetIdForDetail: store.datasetIdForDetail,
  registOrg: store.registOrg,
  caddeProviderId: store.publisherId,
  publisherUri: store.publisherUri,
  publisherName: store.publisher,
  creatorUrl: store.creatorUrl,
  creatorName: store.creator,
  contactUrl: store.contactPointUrl,
  contactName: store.contactPoint
})

// 組織情報リスト(CKAN取得)
const selectOrgOptions = reactive([])
// 提供者IDリスト(Webサーバ取得)
const providerList = reactive([])
// 折りたたみ表示フラグ
const expanded = reactive({
  url: '',
  caddecDatasetIdForDetail: '',
  publisherUri: '',
  publisherName: '',
  creatorUrl: '',
  creatorName: '',
  contactUrl: '',
  contactName: ''
})

// 非表示フラグ
const hideFlgs = reactive({
  url: '',
  caddecDatasetIdForDetail: '',
  publisherUri: '',
  publisherName: '',
  creatorUrl: '',
  creatorName: '',
  contactUrl: '',
  contactName: ''
})

// 前選択時の組織情報
var preRegistOrg = store.registOrg
// エラーメッセージ
const errorCheckMessage = reactive([])
// 自動補完候補
const autoCorrect = reactive({
  title: [],
  description: [],
  url: [],
  publisherUri: [],
  creatorUrl: [],
  contactUrl: []
})

// 完了ダイアログ
const completeDialog = reactive({
  isDisplay: false,
  message: '',
  errorFlg: false,
})

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

// 自動補完候補デフォルト設定
// データセットのタイトル
axios
  .post(config.apiPrefix + '/datacatalog/autocorrect', { label: 'title', value: catalogParameter.title })
  .then((response) => {
    autoCorrect.title = response.data.candidates
  })
  .catch(err => {
    autoCorrect.title = []
    console.log('error message:', err.response.data.message)
  })

// データセットの説明ページURL
axios
  .post(config.apiPrefix + '/datacatalog/autocorrect', { label: 'url', value: catalogParameter.url })
  .then((response) => {
    autoCorrect.url = response.data.candidates
  })
  .catch(err => {
    autoCorrect.url = []
    console.log('error message:', err.response.data.message)
  })

// データセットの公開者
axios
  .post(config.apiPrefix + '/datacatalog/autocorrect', { label: 'publisher_uri', value: catalogParameter.publisherUri })
  .then((response) => {
    autoCorrect.publisherUri = response.data.candidates
  })
  .catch(err => {
    autoCorrect.publisherUri = []
    console.log('error message:', err.response.data.message)
  })

// データセットの作成者
axios
  .post(config.apiPrefix + '/datacatalog/autocorrect', { label: 'creator_url', value: catalogParameter.creatorUrl })
  .then((response) => {
    autoCorrect.creatorUrl = response.data.candidates
  })
  .catch(err => {
    autoCorrect.creatorUrl = []
    console.log('error message:', err.response.data.message)
  })

// データセットの窓口
axios
  .post(config.apiPrefix + '/datacatalog/autocorrect', { label: 'contact_url', value: catalogParameter.contactUrl })
  .then((response) => {
    autoCorrect.contactUrl = response.data.candidates
  })
  .catch(err => {
    autoCorrect.contactUrl = []
    console.log('error message:', err.response.data.message)
  })

// ********************
// Mounted
// ********************
onMounted(function(){
  console.log('-- DatasetInfo.vue onMounted --')

  // 提供者ID取得
  // *****************
  // CKANログイン
  // *****************
  /*
  axios.get('datalist/providerList.json')
    .then((response) => {
      console.log('提供者ID取得：', response)
      for (var num=0; num<response.data.length; num++){
        providerList.push(response.data[num])
      }
      if (!catalogParameter.caddeProviderId.label && providerList.length) {
        if (('label' in providerList[0]) && ('value' in providerList[0])) {
          catalogParameter.caddeProviderId = {
            label: providerList[0].label,
            value: providerList[0].value
          }
        }
      }
    })
    .catch(err => {
      console.log('error message:提供者ID取得に失敗しました。\n管理者に問い合わせてください。')
      completeDialog.isDisplay = true
      completeDialog.message = '提供者ID取得に失敗しました。\n管理者に問い合わせてください。'
      completeDialog.errorFlg = true
    })
  */

  // *****************
  // 認証ログイン
  // *****************
  // 提供者IDの選択肢を生成
  for (var id of store.loginInfo.caddeUserIdList) {
    providerList.push({label: id, value: id})
  }
  // 提供者IDの初期値を設定
  if (store.publisherId.label && store.publisherId.value) {
    // 提供者IDが設定済の場合（テンプレート・複製・編集）
    for (var id of store.loginInfo.caddeUserIdList) {
      if (id === store.publisherId.label) {
        // 設定済のIDがCKANユーザに紐づく場合は設定済の値を設定
        catalogParameter.caddeProviderId = {
          label: store.publisherId.label,
          value: store.publisherId.value
        }
        break
      } else {
        // 設定済のIDがCKANユーザに紐づかない場合は空値を設定
        catalogParameter.caddeProviderId = {
          label: '',
          value: ''
        }
      }
    }
  } else {
    // 提供者IDが未設定の場合
    catalogParameter.caddeProviderId = {
      label: store.loginInfo.caddeUserId,
      value: store.loginInfo.caddeUserId
    }
  }

  // 組織情報取得
  axios
    .get(config.apiPrefix + '/organization')
    .then(response => {
      for (var k = 0; k < response.data.length; k++) {
        selectOrgOptions.push(
          {
            label: response.data[k].org_label,
            value: response.data[k].org_value
          }
        )
      }
      if (selectOrgOptions.length) {
        if (('label' in selectOrgOptions[0]) && ('value' in selectOrgOptions[0])) {
          if (!catalogParameter.registOrg.label || !catalogParameter.registOrg.value) {
            catalogParameter.registOrg = {
              label: selectOrgOptions[0].label,
              value: selectOrgOptions[0].value
            }
            preRegistOrg = catalogParameter.registOrg
            if (!catalogParameter.publisherName) catalogParameter.publisherName = catalogParameter.registOrg.label
            if (!catalogParameter.creatorName) catalogParameter.creatorName = catalogParameter.registOrg.label
            if (!catalogParameter.contactName) catalogParameter.contactName = catalogParameter.registOrg.label
          }
        }
      }
    })
    .catch(err => {
      // 取得エラー
      console.log('error message:', err.response.data.message)
      completeDialog.isDisplay = true
      completeDialog.message = err.response.data.message || '組織情報の取得に失敗しました。\n管理者に問い合わせてください。'
      completeDialog.errorFlg = true
    })

  topScroll()

  // 複製時は詳細検索用データセットIDフィールドを空にする
  if (store.selectedMode.mode === 'release_duplicate' || store.selectedMode.mode === 'detail_duplicate') catalogParameter.caddeDatasetIdForDetail = ''
})

// ********************
// Watch
// ********************
watch(() => catalogParameter.publisherUri,
  (newUrl) => {
  // データセットの公開者フィールド監視
  copyUrlField(newUrl, 'publisherUri')
})

watch(() => catalogParameter.creatorUrl,
  (newUrl) => {
  // データセットの作成者フィールド監視
  copyUrlField(newUrl, 'creatorUrl')
})

watch(() => catalogParameter.contactUrl,
  (newUrl) => {
  // データセットの窓口フィールド監視
  copyUrlField(newUrl, 'contactUrl')
})

// store.modeの監視
watch(() => store.mode,
  (newVal, oldVal) => {
    // データセット情報画面でテンプレート編集ボタンが押下された際に折り畳み表示を無効化
    if (newVal === 'template') {
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

    topScroll()
})

// ********************
// Methods
// ********************
function filterFn (val, update, abort, field) {
  // 自動補完候補取得
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
function setModel (val, field) {
  catalogParameter[field] = val
}

// 必須フィールドエラー判定
function errorFieldMandatory (displayFlg, value, maxLen) {
  if (displayFlg !== 'mandatory') {
    // 必須入力フィールドではないためエラーにしない
    return false
  }
  if (!value && store.selectedMode.mode !== 'template') {
    // 必須入力フィールドかつ値がない場合はエラー(テンプレート編集時は除く)
    return true
  }
  if (maxLen !== 0 && (maxLen < value.length)) {
    // 入力値が最大長を超えている場合はエラー
    return true
  }
  // 入力値問題なし
  return false
}

// 構造体必須フィールドエラー判定
function errorFieldMandatoryForHash (displayFlg, hash, maxLen) {
  var errorLabel = errorFieldMandatory(displayFlg, hash.label, maxLen)
  var errorValue = errorFieldMandatory(displayFlg, hash.value, maxLen)
  return (errorLabel || errorValue)
}

// フィールドエラーメッセージ
function errorFieldMessage (value, maxLen) {
  if (maxLen !== 0 && (maxLen < value.length)) {
    return '【文字数オーバー】'
  } else {
    return '【入力必須項目】'
  }
}

// 所属組織選択機能
function selectCreator () {
  // データセットの公開者（説明）、データセットの作成者（説明）、データセットの窓口（説明）が前回の組織情報と同一ならば更新
  if (preRegistOrg.label === catalogParameter.publisherName) catalogParameter.publisherName = catalogParameter.registOrg.label
  if (preRegistOrg.label === catalogParameter.creatorName) catalogParameter.creatorName = catalogParameter.registOrg.label
  if (preRegistOrg.label === catalogParameter.contactName) catalogParameter.contactName = catalogParameter.registOrg.label
  preRegistOrg = catalogParameter.registOrg
}

// URL情報コピー機能
function copyUrlField (url, field) {
  for (var label in autoCorrect[field]) {
    if (url !== autoCorrect[field][label]) {
      continue
    }
    if (!catalogParameter.publisherUri) catalogParameter.publisherUri = url
    if (!catalogParameter.creatorUrl) catalogParameter.creatorUrl = url
    if (!catalogParameter.contactUrl) catalogParameter.contactUrl = url
  }
}

// 表示メッセージ管理機能(Registration.vueから画面遷移時に呼び出し)
function checkErrorAllFields () {
  // 必須チェックフィールド
  var checkMandatory = {
    title: true,
    description: true,
    url: store.itemDisplayFlg.url === 'mandatory',
    registOrg: true,
    caddeProviderId: true,
    publisherUri: store.itemDisplayFlg.publisherUri === 'mandatory',
    publisherName: store.itemDisplayFlg.publisherName === 'mandatory',
    creatorUrl: store.itemDisplayFlg.creatorUrl === 'mandatory',
    creatorName: store.itemDisplayFlg.creatorName === 'mandatory',
    contactUrl: store.itemDisplayFlg.contactUrl === 'mandatory',
    contactName: store.itemDisplayFlg.contactName === 'mandatory'
  }
  errorCheckMessage.splice(0)
  var noError = true
  for (var checkKey in checkMandatory) {
    if (!checkMandatory[checkKey]) {
      // 必須フィールドではない
      continue
    }
    switch (checkKey) {
      case 'title':
        // データセットのタイトルの入力値チェック
        if (!catalogParameter[checkKey] && store.selectedMode.mode !== 'template') {
          errorCheckMessage.push(ERROR_MESSAGE[checkKey])
          noError = false
        }
        break
      case 'description':
        // データセットの説明文の入力値チェック(テンプレート編集時は除く)
        if (!catalogParameter[checkKey] && store.selectedMode.mode !== 'template') {
          errorCheckMessage.push(ERROR_MESSAGE[checkKey])
          noError = false
        } else if (catalogParameter[checkKey].length > DESCRIPTION_MAX_LENGTH) {
          errorCheckMessage.push(ERROR_MESSAGE_LENGTH[checkKey])
          noError = false
        }
        break
      case 'registOrg':
      case 'caddeProviderId':
        // ユーザの属する組織の入力値チェック
        if (errorFieldMandatoryForHash('mandatory', catalogParameter[checkKey], 0)) {
          errorCheckMessage.push(ERROR_MESSAGE[checkKey])
          noError = false
        }
        break
      default:
        // その他のフィールドの入力値チェック
        if (errorFieldMandatory(store.itemDisplayFlg[checkKey], catalogParameter[checkKey], 0)) {
          errorCheckMessage.push(ERROR_MESSAGE[checkKey])
          noError = false
        }
        break
    }
  }
  return noError
}

// 画面最上部への移動機能
function topScroll () {
  window.scrollTo(0, 0)
}

// データセット情報画面初期化
function initDatasetinfo () {
  var defaultOrg = {
    label: selectOrgOptions[0].label,
    value: selectOrgOptions[0].value
  }
  var templateOrg = {
    label: store.template.registOrg.label,
    value: store.template.registOrg.value
  }
  var defaultProviderId = {
    label: providerList[0].label,
    value: providerList[0].value
  }
  var templateProviderIdValue = {
    label: store.template.publisherId.label,
    value: store.template.publisherId.value
  }
  catalogParameter.title = store.template.catalogTitle
  catalogParameter.description = store.template.catalogDescription
  catalogParameter.url = store.template.datasetDescriptionUrl
  catalogParameter.registOrg = store.template.registOrg.label ? templateOrg : defaultOrg
  catalogParameter.caddeProviderId = store.template.publisherId.label ? templateProviderIdValue : defaultProviderId
  catalogParameter.publisherUri = store.template.publisherUri
  catalogParameter.publisherName = store.template.publisher || defaultOrg.label
  catalogParameter.creatorUrl = store.template.creatorUrl
  catalogParameter.creatorName = store.template.creator || defaultOrg.label
  catalogParameter.contactUrl = store.template.contactPointUrl
  catalogParameter.contactName = store.template.contactPoint || defaultOrg.label
}

// パラメータ更新機能
function commitStore () {
  store.updateDatasetinfo({
      catalogTitle: catalogParameter.title,
      catalogDescription: catalogParameter.description,
      datasetDescriptionUrl: catalogParameter.url,
      datasetIdForDetail: catalogParameter.caddeDatasetIdForDetail,
      registOrg: catalogParameter.registOrg,
      publisherId: catalogParameter.caddeProviderId,
      publisher: catalogParameter.publisherName,
      publisherUri: catalogParameter.publisherUri,
      creatorUrl: catalogParameter.creatorUrl,
      creator: catalogParameter.creatorName,
      contactPointUrl: catalogParameter.contactUrl,
      contactPoint: catalogParameter.contactName,
      storeType: 'state'
    })
}

// ユーザの属する組織の監視
watch(() => catalogParameter.registOrg,
  (newVal, oldVal) => {
    selectCreator()
})

defineExpose({
  checkErrorAllFields,
  initDatasetinfo,
  commitStore
})
</script>

<template>
  <div class="dataset-info">
    <q-card class="q-ma-sm q-card-background-white">
      <q-card-section>
        <div>
          <font size='5' color='#1d468f'>データセットのタイトル</font>
        </div>
        <br>
        <div class="cp_tooltip">データセット
          <span class="cp_tooltiptext">
            <b>【データセット】</b><br>
              &emsp; ある目的で集められたデータを集約した論理的な単位。
          </span>
        </div>
        のタイトルを記入してください。<br>
        CKAN変数名：title
        <br>
        <div class="q-gutter-md input-item">
          <q-select
            v-model="catalogParameter.title"
            placeholder="例：東京オリンピックの会場データ"
            use-input
            hide-selected
            fill-input
            input-debounce="0"
            :options="autoCorrect.title"
            @filter="(val, update, abort) => { filterFn(catalogParameter.title, update, abort, 'title') }"
            @input-value="(val) => { setModel(val, 'title') }"
            bottom-slots
            counter
            :error="errorFieldMandatory('mandatory', catalogParameter.title, 0)"
            :error-message="errorFieldMessage(catalogParameter.title, 0)"
            hide-dropdown-icon
          />
        </div>
      </q-card-section>
    </q-card>
    <q-card class="q-ma-sm q-card-background-white">
      <q-card-section>
        <div>
          <font size='5' color='#1d468f'>データセットの説明</font>
        </div>
        <br>
        <div>
          <p>データセットの特徴を説明する文章を記入してください（最大1000文字）。<br>
            CKAN変数名：notes
          </p>
          <div class="q-gutter-md input-item">
            <q-input
              type="textarea"
              v-model="catalogParameter.description"
              placeholder="例：東京オリンピック・パラリンピックの会場データは、各会場の名称、住所、電話番号、会場の緯度・経度から構成されています。"
              bottom-slots
              counter
              autogrow
              :error="errorFieldMandatory('mandatory', catalogParameter.description, 1000)"
              :error-message="errorFieldMessage(catalogParameter.description, 1000)"
            />
          </div>
        </div>
      </q-card-section>
    </q-card>
    <q-card class="q-ma-sm q-card-background-white" v-show="hideFlgs.url">
      <q-card-section>
        <font size="5" color="#1d468f">データセットの説明ページURL</font>
        <q-btn
          color="grey"
          round
          flat
          dense
          :icon="expanded.url ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
          @click="expanded.url = !expanded.url"
        />
        <q-slide-transition>
          <div v-show="expanded.url">
            <br>
            <p>データセットに関して追加・補足できる情報が公開されているURLを記載してください。<br>
               CKAN変数名：url
            </p>
            <div class="q-gutter-md input-item">
              <q-select
                v-model="catalogParameter.url"
                placeholder="例：http://example.com/landingPage/1"
                use-input
                hide-selected
                fill-input
                input-debounce="0"
                :options="autoCorrect.url"
                @filter="(val, update, abort) => { filterFn(catalogParameter.url, update, abort, 'url') }"
                @input-value="(val) => { setModel(val, 'url') }"
                :error="errorFieldMandatory(store.itemDisplayFlg.url, catalogParameter.url, 0)"
                :error-message="errorFieldMessage(catalogParameter.url, 0)"
                hide-dropdown-icon
              />
            </div>
          </div>
        </q-slide-transition>
      </q-card-section>
    </q-card>
    <q-card class="q-ma-sm q-card-background-white" v-show="hideFlgs.caddecDatasetIdForDetail">
      <q-card-section>
        <font size='5' color='#1d468f'>詳細検索用データセットID</font>
        <q-btn
          color="grey"
          round
          flat
          dense
          :icon="expanded.caddecDatasetIdForDetail ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
          @click="expanded.caddecDatasetIdForDetail = !expanded.caddecDatasetIdForDetail"
        />
        <q-slide-transition>
          <div v-show="expanded.caddecDatasetIdForDetail">
            <br>
            <p>CADDEコネクタが詳細検索時に必要な詳細検索用CKANのデータセットIDが自動で入力されます。<br>
               CKAN変数名：extras:caddec_dataset_id_for_detail
            </p>
            <div class="q-gutter-md input-item">
              <q-input
                v-model="catalogParameter.caddeDatasetIdForDetail"
                placeholder="例：68c8dfec-15ca-4877-89e0-dd09b8030c2f"
                disable
              />
            </div>
          </div>
        </q-slide-transition>
      </q-card-section>
    </q-card>
    <q-card class="q-ma-sm q-card-background-white">
      <q-card-section>
        <div>
          <font size="5" color="#1d468f">ユーザの属する組織</font>
        </div>
        <br>
        <p>あなたが属する組織を選択してください。CKANカタログサイトであなたが属する組織が複数ある場合は、一つ選択してください。</p>
        <div class="q-gutter-md input-item">
          <q-select
            v-model="catalogParameter.registOrg"
            :options="selectOrgOptions"
            :error="errorFieldMandatoryForHash('mandatory', catalogParameter.registOrg, 0)"
            :error-message="errorFieldMessage(catalogParameter.registOrg.label, 0)"
          />
        </div>
      </q-card-section>
    </q-card>
    <q-card class="q-ma-sm q-card-background-white">
      <q-card-section>
        <div>
          <font size="5" color="#1d468f">提供者ID</font>
        </div>
        <br>
        <!-- TODO:認証サーバIF対応完了時に切替 -->
        <!-- <p>CADDEコネクタがデータ提供者を特定するために用いる識別子が自動入力されます。（ログイン時に入力したCADDEユーザID）<br>
           CKAN変数名：extras:caddec_provider_id
        </p> -->
        <p>CADDEコネクタがデータ提供者を特定するために用いる識別子を選択してください。<br>
           CKAN変数名：extras:caddec_provider_id
        </p>
        <div class="q-gutter-md input-item">
          <q-select
            v-model="catalogParameter.caddeProviderId"
            :options="providerList"
            :error="errorFieldMandatoryForHash('mandatory', catalogParameter.caddeProviderId, 0)"
            :error-message="errorFieldMessage(catalogParameter.caddeProviderId.label, 0)"
          />
        </div>
      </q-card-section>
    </q-card>
    <q-card class="q-ma-sm q-card-background-white" v-show="hideFlgs.publisherUri">
      <q-card-section>
        <font size='5' color='#1d468f'>データセットの公開者</font>
        <q-btn
          color="grey"
          round
          flat
          dense
          :icon="expanded.publisherUri ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
          @click="expanded.publisherUri = !expanded.publisherUri"
        />
        <q-slide-transition>
          <div v-show="expanded.publisherUri">
            <br>
            <p>このデータセットを提供する提供者の組織・機関を表すURLを入力してください。<br>
               CKAN変数名：extras:publisher_uri
            </p>
            <div class="q-gutter-md input-item">
              <q-select
                v-model="catalogParameter.publisherUri"
                placeholder="例：http://example.org/7010001008844"
                use-input
                hide-selected
                fill-input
                input-debounce="0"
                :options="autoCorrect.publisherUri"
                @filter="(val, update, abort) => { filterFn(catalogParameter.publisherUri, update, abort, 'publisherUri') }"
                @input-value="(val) => { setModel(val, 'publisherUri') }"
                :error="errorFieldMandatory(store.itemDisplayFlg.publisherUri, catalogParameter.publisherUri, 0)"
                :error-message="errorFieldMessage(catalogParameter.publisherUri, 0)"
                hide-dropdown-icon
              />
            </div>
          </div>
        </q-slide-transition>
      </q-card-section>
    </q-card>
    <q-card class="q-ma-sm q-card-background-white" v-show="hideFlgs.publisherName">
      <q-card-section>
        <font size='5' color='#1d468f'>データセットの公開者（説明）</font>
        <q-btn
          color="grey"
          round
          flat
          dense
          :icon="expanded.publisherName ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
          @click="expanded.publisherName = !expanded.publisherName"
        />
        <q-slide-transition>
          <div v-show="expanded.publisherName">
            <br>
            <p>このデータセットを提供した正式な組織・機関名を入力してください。<br>
               デフォルトでは選択した組織の名称が入力されます。<br>
               CKAN変数名：extras:publisher_name
            </p>
            <div class="q-gutter-md input-item">
              <q-input
                v-model="catalogParameter.publisherName"
                placeholder="例：〇〇株式会社  データサービス事業部"
                :error="errorFieldMandatory(store.itemDisplayFlg.publisherName, catalogParameter.publisherName, 0)"
                :error-message="errorFieldMessage(catalogParameter.publisherName, 0)"
              />
            </div>
          </div>
        </q-slide-transition>
      </q-card-section>
    </q-card>
    <q-card class="q-ma-sm q-card-background-white" v-show="hideFlgs.creatorUrl">
      <q-card-section>
        <font size='5' color='#1d468f'>データセットの作成者</font>
        <q-btn
          color="grey"
          round
          flat
          dense
          :icon="expanded.creatorUrl ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
          @click="expanded.creatorUrl = !expanded.creatorUrl"
        />
        <q-slide-transition>
          <div v-show="expanded.creatorUrl">
            <br>
            <p>データセットを作成する作成者の組織・機関を表すURLを入力してください。<br>
               CKAN変数名：extras:creator_url
            </p>
            <div class="q-gutter-md input-item">
              <q-select
                v-model="catalogParameter.creatorUrl"
                placeholder="例：http://example.org/7010001008844"
                use-input
                hide-selected
                fill-input
                input-debounce="0"
                :options="autoCorrect.creatorUrl"
                @filter="(val, update, abort) => { filterFn(catalogParameter.creatorUrl, update, abort, 'creatorUrl') }"
                @input-value="(val) => { setModel(val, 'creatorUrl') }"
                :error="errorFieldMandatory(store.itemDisplayFlg.creatorUrl, catalogParameter.creatorUrl, 0)"
                :error-message="errorFieldMessage(catalogParameter.creatorUrl, 0)"
                hide-dropdown-icon
              />
            </div>
          </div>
        </q-slide-transition>
      </q-card-section>
    </q-card>
    <q-card class="q-ma-sm q-card-background-white" v-show="hideFlgs.creatorName">
      <q-card-section>
        <font size='5' color='#1d468f'>データセットの作成者（説明）</font>
        <q-btn
          color="grey"
          round
          flat
          dense
          :icon="expanded.creatorName ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
          @click="expanded.creatorName = !expanded.creatorName"
        />
        <q-slide-transition>
          <div v-show="expanded.creatorName">
            <br>
            <p>このデータセットの作成にかかわった正式な組織・機関名を入力してください。<br>
               デフォルトでは選択した組織の名称が入力されます。<br>
               CKAN変数名：extras:creator_name
            </p>
            <div class="q-gutter-md input-item">
              <q-input
                v-model="catalogParameter.creatorName"
                placeholder="例：〇〇株式会社&nbsp;&nbsp;データサービス事業部"
                :error="errorFieldMandatory(store.itemDisplayFlg.creatorName, catalogParameter.creatorName, 0)"
                :error-message="errorFieldMessage(catalogParameter.creatorName, 0)"
              />
            </div>
          </div>
        </q-slide-transition>
      </q-card-section>
    </q-card>
    <q-card class="q-ma-sm q-card-background-white" v-show="hideFlgs.contactUrl">
      <q-card-section>
        <font size='5' color='#1d468f'>データセットの窓口</font>
        <q-btn
          color="grey"
          round
          flat
          dense
          :icon="expanded.contactUrl ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
          @click="expanded.contactUrl = !expanded.contactUrl"
        />
        <q-slide-transition>
          <div v-show="expanded.contactUrl">
            <br>
            <p>データセットについての問い合わせ先が記述されたページのURLを入力してください。<br>
               CKAN変数名：extras:contact_url
            </p>
            <div class="q-gutter-md input-item">
              <q-select
                v-model="catalogParameter.contactUrl"
                placeholder="例：http://example.com/contact_url"
                use-input
                hide-selected
                fill-input
                input-debounce="0"
                :options="autoCorrect.contactUrl"
                @filter="(val, update, abort) => { filterFn(catalogParameter.contactUrl, update, abort, 'contactUrl') }"
                @input-value="(val) => { setModel(val, 'contactUrl') }"
                :error="errorFieldMandatory(store.itemDisplayFlg.contactUrl, catalogParameter.contactUrl, 0)"
                :error-message="errorFieldMessage(catalogParameter.contactUrl, 0)"
                hide-dropdown-icon
              />
            </div>
          </div>
        </q-slide-transition>
      </q-card-section>
    </q-card>
    <q-card class="q-ma-sm q-card-background-white" v-show="hideFlgs.contactName">
      <q-card-section>
        <font size='5' color='#1d468f'>データセットの窓口（説明）</font>
        <q-btn
          color="grey"
          round
          flat
          dense
          :icon="expanded.contactName ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
          @click="expanded.contactName = !expanded.contactName"
        />
        <q-slide-transition>
          <div v-show="expanded.contactName">
            <br>
            <p>データセットについて、問い合わせを行う際の連絡先情報（組織名、部署名、電話番号、emailアドレス）を入力してください。<br>
               デフォルトでは選択した組織の名称が入力されます。<br>
               CKAN変数名：extras:contact_name
            </p>
            <div class="q-gutter-md input-item">
              <q-input
                v-model="catalogParameter.contactName"
                placeholder="例：〇〇株式会社  データサービス事業部  カスタマサポート部
                03-XXXX-XXXX
                aaaa@bbbb.co.jp"
                autogrow
                type="textarea"
                :error="errorFieldMandatory(store.itemDisplayFlg.contactName, catalogParameter.contactName, 0)"
                :error-message="errorFieldMessage(catalogParameter.contactName, 0)"
              />
            </div>
          </div>
        </q-slide-transition>
      </q-card-section>
    </q-card>
    <div v-for="message in errorCheckMessage" :key="message">
      <font size="3" color="#FF0000">{{message}}</font>
    </div>

    <!-- 完了ダイアログ -->
    <CompleteDialog
      v-bind:dialogInfo="completeDialog"
      @close-dialog="completeDialog.isDisplay = false"
    />

  </div>
</template>

<style>
.dataset-info .input-item{
  max-width: 700px;
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

.cp_tooltip .cp_tooltiptext::after {
  position: absolute;
  top: 100%;
  left: 5%;
  margin-left: -5px;
  content: ' ';
  border: 5px solid transparent;
  border-top-color: #6495ed;
}

.cp_tooltip:hover .cp_tooltiptext {
  visibility: visible;
  opacity: 1;
}
</style>
