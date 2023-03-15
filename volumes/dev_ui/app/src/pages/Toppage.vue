<script setup>
import { useRouter } from 'vue-router'
import { reactive } from 'vue'
import axios from 'axios'
import { config } from'boot/config'
import { useStore } from '../stores/store'
import CompleteDialog from '../components/dialog/CompleteDialog.vue'

const router = useRouter()
const store = useStore()

// 完了ダイアログ
const completeDialog = reactive({
  isDisplay: false,
  message: '',
  errorFlg: false,
})

function btnActionLoginPage () {
  // *****************
  // 認証ログイン
  // *****************
  axios.post(config.apiPrefix + '/keycloak/redirect', { catalog_tool_url: location.href })
    .then(response => {
      var keycloakRedirectUrl = response.data.redirect_uri
      console.log('keycloakログイン画面URL：%s', keycloakRedirectUrl)
      router.push({ path: '/keycloak', query: { keycloakUrl: keycloakRedirectUrl } })
    })
    .catch(err => {
      console.log('error message:', err.response.data.message)
      completeDialog.isDisplay = true
      completeDialog.message = err.response.data.message || 'keycloakリダイレクトに失敗しました。\n管理者に問い合わせてください。'
      completeDialog.errorFlg = true
    })

  // *****************
  // CKANログイン
  // *****************
  // ログインページへ
  // router.push('/login')
}
</script>

<template>
  <div class="col-12 q-layout-padding flex justify-center content-center">
    <q-card class="q-card-background-white" style="max-width: 80%; width: 100%;">
      <q-card-section>
        <br>
        <div class="row">
          <div class="col-sm-10 offset-sm-1 text-left">
            <q-scroll-area style="height: 650px">
              <span><font size="6" color="#a0a0a0">■&ensp;</font><font size="4" color="#1d468f">データカタログ作成ツール</font></span>
              <br>
              <span>
              &emsp;データカタログ作成ツール（以下、本ツール）は、
              データ提供者がデータカタログサイトにデータセットを登録する際に必要となる、
              データカタログの作成、データカタログサイトへの登録の作業を支援するためのツールです。
              本ツールのガイドに従って項目を入力していくだけで、
              迅速にデータカタログの作成・登録を行うことができます。
              <br>
              &emsp;また、データカタログの一部の項目については、
              値の候補を推測・表示することにより、一定の基準で値を記入・選択でき、
              値の記入・選択にかかる時間も短縮することができます。
              </span>
              <br>
              <span><font size="6" color="#a0a0a0">■&ensp;</font><font size="4" color="#1d468f">ツールを利用するメリット</font></span>
              <br>
              <font color="#1d468f">
                &emsp;・簡単に入力可能
              </font>
              <br>
              &emsp;データカタログに詳しくなくても本ツールのガイドに従って項目を入力していくだけで、
              データカタログの作成・登録ができます。
              <br>
              <br>
              <font color="#1d468f">
                &emsp;・ 迅速に作成可能
              </font>
              <br>
              &emsp;AIを活用して値の候補を表示したり、
              よく使うパターンを選択するだけで入力可能とすることで、
              迅速にデータカタログを作成できます。
              <br>
              <br>
              <font color="#1d468f">
                &emsp;・利用者から評価の高いデータカタログを作成可能
              </font>
              <br>
              &emsp;将来的に業界標準になると推測されるDTAが
              策定したデータカタログ項目の必須項目を作成できます。
              <br>
              &emsp;多数の項目を備えることで、
              利用者が見つけやすく・理解しやすくなるため、データ取引を促進できます。
              <br>
              <br>
              <span><font size="6" color="#a0a0a0">■&ensp;</font><font size="4" color="#1d468f">ツールでの操作の流れ</font></span>
              <br>
              &emsp;以下の手順で記入し、内容を確認したのちにデータカタログサイトに登録します。
              <br>
              &emsp;・データセット情報（データセットのタイトル、説明、組織、提供者・作成者・連絡先情報）の記入
              <br>
              &emsp;・データ概要情報（データの配信方法の説明、URLなど）の記入
              <br>
              &emsp;・データセット情報(任意)（データセットのテーマ、キーワードなどの任意登録情報）の記入
              <br>
              &emsp;・利用条件（データの利用条件）の記入
              <br>
            </q-scroll-area>
          </div>
        </div>
        <div class="row q-mt-lg">
          <div class="col-sm-10 offset-sm-1 text-center">
            <q-btn
              color="light-blue-10"
              @click="btnActionLoginPage()"
              label="ログインページへ"
            />
          </div>
        </div>
        <br>
      </q-card-section>
    </q-card>

    <!-- 完了ダイアログ -->
    <CompleteDialog
      v-bind:dialogInfo="completeDialog"
      @close-dialog="completeDialog.isDisplay = false"
    />

  </div>
</template>

<style lang="scss">
.q-card-background-white{
  background: white
}
</style>
