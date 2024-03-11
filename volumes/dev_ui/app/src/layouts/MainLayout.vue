<script setup>
import { config } from'boot/config'
import EssentialLink from 'components/EssentialLink.vue'
import { reactive, onMounted, onBeforeMount, watch } from 'vue'
import { Loading } from 'quasar'
import { useStore } from '../stores/store'
import { useRoute, useRouter, isNavigationFailure } from 'vue-router'
import CompleteDialog from '../components/dialog/CompleteDialog.vue'
import axios from 'axios'

const DISPLAY_USERNAME_MAX_LENGTH = 30

const store = useStore()
const route = useRoute()
const router = useRouter()

const form = reactive({
  leftDrawerOpen: true,
  releaseUserName: 'ゲスト',
  detailUserName: 'ゲスト',
  main_title: '',
  releaseCkanCatalogTitle: '(未設定)',
  releaseCkanCatalogDescription: '(未設定)',
  releaseCkanCatalogUrl: '(未設定)',
  releaseCkanPublisher: '(未設定)',
  releaseCkanPublisherExplanation: '(未設定)',
  detailCkanCatalogTitle: '(未設定)',
  detailCkanCatalogDescription: '(未設定)',
  detailCkanCatalogUrl: '(未設定)',
  detailCkanPublisher: '(未設定)',
  detailCkanPublisherExplanation: '(未設定)',
  visible: false,
  selectedMode: ''
})

// 完了ダイアログ
const completeDialog = reactive({
  isDisplay: false,
  message: '',
  errorFlg: false,
})

onBeforeMount(() => {
  window.addEventListener('scroll', onScroll)
  router.beforeEach((to, from, next) => {
    if ((to.fullPath === '/' && from.fullPath === '/regist') ||
      (to.fullPath === '/login' && from.fullPath === '/regist')) {
      var answer = confirm('ページを移動すると入力データがリセットされます')
      if (answer) {
        store.user_name = 'ゲスト'
        store.user_pass = ''
        next()
        form.leftDrawerOpen = true
      } else {
        window.alert('キャンセルしました')
        form.leftDrawerOpen = true
      }
    } else {
      next()
      form.leftDrawerOpen = true
    }
  })
})

// watch
watch(() => store.releaseCkanUserName,
  (newVal, oldVal) => {
    if (!newVal) {
      form.releaseUserName = 'ゲスト'
    } else if (newVal.length > DISPLAY_USERNAME_MAX_LENGTH) {
      form.releaseUserName = newVal.substr(0, DISPLAY_USERNAME_MAX_LENGTH) + '...'
    } else {
      form.releaseUserName = newVal
    }
})

watch(() => store.detailCkanUserName,
  (newVal, oldVal) => {
    if (!newVal) {
      form.detailUserName = 'ゲスト'
    } else if (newVal.length > DISPLAY_USERNAME_MAX_LENGTH) {
      form.detailUserName = newVal.substr(0, DISPLAY_USERNAME_MAX_LENGTH) + '...'
    } else {
      form.detailUserName = newVal
    }
})

watch(() => store.releaseCkanCatalogTitle,
  (newVal, oldVal) => {
    form.releaseCkanCatalogTitle = !newVal ? '(未設定)' : newVal
})

watch(() => store.releaseCkanCatalogDescription,
  (newVal, oldVal) => {
    form.releaseCkanCatalogDescription = !newVal ? '(未設定)' : newVal
})

watch(() => store.releaseCkanCatalogUrl,
  (newVal, oldVal) => {
    form.releaseCkanCatalogUrl = !newVal ? '(未設定)' : newVal
})

watch(() => store.releaseCkanCatalogPublisher,
  (newVal, oldVal) => {
    form.releaseCkanCatalogPublisher = !newVal ? '(未設定)' : newVal
})

watch(() => store.releaseCkanCatalogPublisherExplanation,
  (newVal, oldVal) => {
    form.releaseCkanCatalogPublisherExplanation = !newVal ? '(未設定)' : newVal
})

watch(() => store.detailCkanCatalogTitle,
  (newVal, oldVal) => {
    form.detailCkanCatalogTitle = !newVal ? '(未設定)' : newVal
})

watch(() => store.detailCkanCatalogDescription,
  (newVal, oldVal) => {
    form.detailCkanCatalogDescription = !newVal ? '(未設定)' : newVal
})

watch(() => store.detailCkanCatalogUrl,
  (newVal, oldVal) => {
    form.detailCkanCatalogUrl = !newVal ? '(未設定)' : newVal
})

watch(() => store.detailCkanCatalogPublisher,
  (newVal, oldVal) => {
    form.detailCkanCatalogPublisher = !newVal ? '(未設定)' : newVal
})

watch(() => store.detailCkanCatalogPublisherExplanation,
  (newVal, oldVal) => {
    form.detailCkanCatalogPublisherExplanation = !newVal ? '(未設定)' : newVal
})

watch(() => store.mode,
  (newVal, oldVal) => {
    switch (newVal) {
      case 'userManagement':
        form.selectedMode = '―  ユーザ一覧  ―'
        break
      case 'createUser':
        form.selectedMode = '―  ユーザ作成  ―'
        break
      case 'editUser':
        form.selectedMode = '―  ユーザ編集  ―'
        break
      case 'new_release_register':
      case 'release_duplicate':
      case 'release-link-detail_duplicate'://詳細に紐づく横断
        form.selectedMode = '―  横断検索カタログ作成  ―'
        break
      case 'new_detail_register':
      case 'detail_duplicate':
      case 'detail-link-release_duplicate'://横断に紐づく詳細
        form.selectedMode = '―  詳細検索カタログ作成  ―'
        break
      case 'new_both_register':
      case 'both_duplicate':
        form.selectedMode = '―  横断・詳細検索カタログ作成  ―'
        break
      case 'selectDraft':
        form.selectedMode = '―  登録再開  ―'
        break
      case 'search':
        form.selectedMode = '―  複製・編集・削除  ―'
        break
      case 'edit':
        if (store.selectedMode.ckanType === 'release') {
          form.selectedMode = '―  横断検索カタログ編集  ―'
        } else {
          form.selectedMode = '―  詳細検索カタログ編集  ―'
        }
        break
      case 'import':
        form.selectedMode = '―  インポート  ―'
        break
      case 'export':
        form.selectedMode = '―  エクスポート  ―'
        break
      case 'template':
        form.selectedMode = '―  テンプレート編集  ―'
        break
      default:
        form.selectedMode = ''
   }
})

function btnPageDown () {
  scrollTo({ top: 9999, behavior: 'smooth' })
  // ブラウザ判断
  var userAgent = window.navigator.userAgent
  if (userAgent.indexOf('MSIE') !== -1 || userAgent.indexOf('trident') !== -1) {
    console.log('Internet Explorer')
    scrollTo(0, 9999)
  } else if (userAgent.indexOf('Edge') !== -1) {
    console.log('Edge')
    scrollTo(0, 9999)
  } else if (userAgent.indexOf('Chrome') !== -1) {
    console.log('Google Chrome')
    window.scroll({ top: 9999, behavior: 'smooth' })
  } else if (userAgent.indexOf('Safari') !== -1) {
    console.log('Safari')
    scrollTo(0, 9999)
  } else if (userAgent.indexOf('Firefox') !== -1) {
    console.log('Firefox')
    window.scroll({ top: 9999, behavior: 'smooth' })
  } else if (userAgent.indexOf('Opera') !== -1) {
    console.log('Opera')
    scrollTo(0, 9999)
  } else {
    console.log('未知ブラウザ')
    scrollTo(0, 9999)
  }
}

function btnPageUp () {
  scrollTo({ top: 0, behavior: 'smooth' })
  // ブラウザ判断
  var userAgent = window.navigator.userAgent
  if (userAgent.indexOf('MSIE') !== -1 || userAgent.indexOf('trident') !== -1) {
    console.log('Internet Explorer')
    scrollTo(0, 0)
  } else if (userAgent.indexOf('Edge') !== -1) {
    console.log('Edge')
    scrollTo(0, 0)
  } else if (userAgent.indexOf('Chrome') !== -1) {
    console.log('Google Chrome')
    window.scroll({ top: 0, behavior: 'smooth' })
  } else if (userAgent.indexOf('Safari') !== -1) {
    console.log('Safari')
    scrollTo(0, 0)
  } else if (userAgent.indexOf('Firefox') !== -1) {
    console.log('Firefox')
    window.scroll({ top: 0, behavior: 'smooth' })
  } else if (userAgent.indexOf('Opera') !== -1) {
    console.log('Opera')
    scrollTo(0, 0)
  } else {
    console.log('未知ブラウザ')
    scrollTo(0, 0)
  }
}

function logout () {
  // トップ画面またはログイン画面でのログアウトは実行不可
  if (route.path === '/' || route.path === '/login') return
  Loading.show()
  axios.get(config.apiPrefix + '/logout')
    .then(res => {
      console.log('success logout')
    })
    .catch(err => {
      console.log('error message:', err.response.data.message)
    })
    .finally(() => {
      Loading.hide()
      store.initLoginCkanInfo()

      // *****************
      // 認証ログイン
      // *****************
      // トップページ画面へ遷移
      router.push('/').then(failure => {

      // *****************
      // CKANログイン
      // *****************
      // ログイン画面へ遷移
      // router.push('/login').then(failure => {

        if (!isNavigationFailure(failure)) {
          store.updateMode({ mode: '', ckanType: '', isBothCatalog: false })
        }
      })
    })
}

function btnLogout () {
  store.initItemListParams()
  store.initCkanItemListParams()
  store.initLoginCkanInfo()
  store.resetMode()
  router.push('/login')
  location.reload(true)
}

// スクロールされたら上下のアイコンを表示する
function onScroll () {
  form.scrollY = window.scrollY
  if (!form.visible) {
    form.visible = window.scrollY > 0
  } else if (window.scrollY <= 0) {
    form.visible = !form.visible
  }
}
</script>

<template>
  <q-layout view="hHh Lpr fFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          dense
          flat
          round
          icon="menu"
          @click="form.leftDrawerOpen = !form.leftDrawerOpen"
          class="q-mr-sm"
        />
        <q-separator dark vertical inset />
        <q-toolbar-title>
          データカタログ作成ツール&nbsp;&nbsp;&nbsp;&nbsp;{{ form.selectedMode }}
        </q-toolbar-title>
        <div class="q-pr-md">
          <font size="3px">Version&nbsp;1.2</font>
        </div>
        <div class="q-pr-md">
          <q-btn-dropdown
            label="ユーザ情報"
            icon="account_circle"
            outline
          >
            <q-list dense style="width: 600px">
              <q-item class="q-mt-sm">
                <q-item-section top class="col-5 gt-sm">
                  <q-item-label><font color="#1d468f">CKANユーザ名</font></q-item-label>
                </q-item-section>
                <q-item-section top>
                  <q-item-label lines="1">
                    {{ form.releaseUserName }}
                  </q-item-label>
                </q-item-section>
              </q-item>
              <q-separator></q-separator>
              <q-item class="q-mt-sm">
                <q-item-section top class="col-5 gt-sm">
                  <q-item-label><font color="#1d468f">横断検索用CKAN</font></q-item-label>
                </q-item-section>
              </q-item>
              <q-item class="q-mt-sm">
                <q-item-section top class="col-5 gt-sm">
                  <q-item-label><font color="#1d468f">&nbsp;&nbsp;カタログのタイトル</font></q-item-label>
                </q-item-section>
                <q-item-section top>
                  <q-item-label lines="1">
                    {{ form.releaseCkanCatalogTitle }}
                  </q-item-label>
                </q-item-section>
              </q-item>
              <q-item class="q-mt-sm">
                <q-item-section top class="col-5 gt-sm">
                  <q-item-label><font color="#1d468f">&nbsp;&nbsp;カタログの説明</font></q-item-label>
                </q-item-section>
                <q-item-section top>
                  <q-item-label lines="1">
                    {{ form.releaseCkanCatalogDescription }}
                  </q-item-label>
                </q-item-section>
              </q-item>
              <q-item class="q-mt-sm">
                <q-item-section top class="col-5 gt-sm">
                  <q-item-label><font color="#1d468f">&nbsp;&nbsp;カタログの記載のホームページ</font></q-item-label>
                </q-item-section>
                <q-item-section top>
                  <q-item-label>
                    {{ form.releaseCkanCatalogUrl }}
                  </q-item-label>
                </q-item-section>
              </q-item>
              <q-item class="q-mt-sm">
                <q-item-section top class="col-5 gt-sm">
                  <q-item-label><font color="#1d468f">&nbsp;&nbsp;カタログの公開者</font></q-item-label>
                </q-item-section>
                <q-item-section top>
                  <q-item-label lines="1">
                    {{ form.releaseCkanPublisher }}
                  </q-item-label>
                </q-item-section>
              </q-item>
              <q-item class="q-mt-sm">
                <q-item-section top class="col-5 gt-sm">
                  <q-item-label><font color="#1d468f">&nbsp;&nbsp;カタログの公開者（説明）</font></q-item-label>
                </q-item-section>
                <q-item-section top>
                  <q-item-label lines="1">
                    {{ form.releaseCkanPublisherExplanation }}
                  </q-item-label>
                </q-item-section>
              </q-item>
              <q-separator></q-separator>
              <q-item class="q-mt-sm">
                <q-item-section top class="col-5 gt-sm">
                  <q-item-label><font color="#1d468f">詳細検索用CKAN</font></q-item-label>
                </q-item-section>
              </q-item>
              <q-item class="q-mt-sm">
                <q-item-section top class="col-5 gt-sm">
                  <q-item-label><font color="#1d468f">&nbsp;&nbsp;カタログのタイトル</font></q-item-label>
                </q-item-section>
                <q-item-section top>
                  <q-item-label lines="1">
                    {{ form.detailCkanCatalogTitle }}
                  </q-item-label>
                </q-item-section>
              </q-item>
              <q-item class="q-mt-sm">
                <q-item-section top class="col-5 gt-sm">
                  <q-item-label><font color="#1d468f">&nbsp;&nbsp;カタログの説明</font></q-item-label>
                </q-item-section>
                <q-item-section top>
                  <q-item-label lines="1">
                    {{ form.detailCkanCatalogDescription }}
                  </q-item-label>
                </q-item-section>
              </q-item>
              <q-item class="q-mt-sm">
                <q-item-section top class="col-5 gt-sm">
                  <q-item-label><font color="#1d468f">&nbsp;&nbsp;カタログの記載のホームページ</font></q-item-label>
                </q-item-section>
                <q-item-section top>
                  <q-item-label>
                    {{ form.detailCkanCatalogUrl }}
                  </q-item-label>
                </q-item-section>
              </q-item>
              <q-item class="q-mt-sm">
                <q-item-section top class="col-5 gt-sm">
                  <q-item-label><font color="#1d468f">&nbsp;&nbsp;カタログの公開者</font></q-item-label>
                </q-item-section>
                <q-item-section top>
                  <q-item-label lines="1">
                    {{ form.detailCkanPublisher }}
                  </q-item-label>
                </q-item-section>
              </q-item>
              <q-item class="q-mt-sm">
                <q-item-section top class="col-5 gt-sm">
                  <q-item-label><font color="#1d468f">&nbsp;&nbsp;カタログの公開者（説明）</font></q-item-label>
                </q-item-section>
                <q-item-section top>
                  <q-item-label lines="1">
                    {{ form.detailCkanPublisherExplanation }}
                  </q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown>
        </div>
        <q-btn
          outline
          size="gl"
          text-color="white"
          label="ログアウト"
          @click="logout()"
        />
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="form.leftDrawerOpen"
      bordered
      :width="235"
      content-class="bg-grey-1"
    >
      <q-list>
        <q-item-label
          header
          class="text-grey-8"
        >
          Menu
        </q-item-label>
        <EssentialLink/>
      </q-list>
    </q-drawer>
    <q-page-container>
      <q-page class="background-whitesmoke row justify-center content-center">
        <router-view />
        <q-page-sticky v-show="form.visible" position="bottom-right" :offset="[18, 98]">
          <q-btn
            icon="keyboard_arrow_down"
            round
            color="light-blue-10"
            class="animation-pop"
            @click="btnPageDown()"
          />
        </q-page-sticky>
        <q-page-sticky v-show="form.visible" position="bottom-right" :offset="[18, 158]">
          <q-btn
            icon="keyboard_arrow_up"
            round
            color="light-blue-10"
            class="animation-pop play-backtotop non-selectable shadow-2"
            @click="btnPageUp()"
          />
        </q-page-sticky>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<style lang="scss">
.background-whitesmoke{
  background-color: #f5f5f5;
}

.overflow-hidden{
  overflow: hidden;
}

.body-scroll-lock{
  position: fixed;
  left: 0px;
  right: 0px;
  top: 0px;
  bottom:0px;
}
</style>
