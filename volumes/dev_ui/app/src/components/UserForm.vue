<script setup>
import { config } from'boot/config'
import axios from 'axios'
import { Loading } from 'quasar'
import CompleteDialog from './dialog/CompleteDialog.vue'
import { ref, reactive, watch } from 'vue'

const props = defineProps(['userManagerInfo'])
const emit = defineEmits(['changeDisplayEvent'])

const attr = reactive({
  completeDialog: {
    isDisplay: false,
    message: '',
    errorFlg: false,
  }
})
const username = ref('') 
const password = ref('')
const organization = ref('')
const email = ref('')
const caddeUserId = ref('')
const releaseCkanUrl = ref('')
const releaseCkanApikey = ref('')
const releaseCkanUsername = ref('')
const detailCkanUrl = ref('')
const detailCkanApikey = ref('')
const detailCkanUsername = ref('')
const isPwd =  ref(true)
const errorFlg = ref(false)
const errorMessage = ref(null)
const authMethodOptions = []
const form = reactive({
  username: '',
  password: '',
  email: '',
  caddeUserId: '',
  organization: '',
  ckan: 'internal',
  releaseCkanUrl: '',
  releaseCkanApikey: '',
  releaseCkanUsername: '',
  releaseAuthentication: 'noAuth',
  releaseAuthenticationMethod: '',
  detailCkanUrl: '',
  detailCkanApikey: '',
  detailCkanUsername: '',
  detailAuthentication: 'noAuth',
  detailAuthenticationMethod: ''
})
const defaultForm = reactive({
  username: '',
  password: '',
  organization: '',
  email: '',
  caddeUserId: '',
  ckan: 'internal',
  releaseCkanUrl: '',
  releaseCkanApikey: '',
  releaseCkanUsername: '',
  detailCkanUrl: '',
  detailCkanApikey: '',
  detailCkanUsername: ''
})

const checkHyphen = reactive(
  v => (v && v.indexOf('-') === -1) || ' - (ハイフン)は使用できません。'
)
const checkLength = reactive(
  v => (v && (v.length >= 2 && v.length <= 100)) || 'ユーザ名は2文字以上100文字以下で入力してください。'
)
const passRules = reactive({
  minlength: v => (v && v.length >= 12) || 'パスワードは12文字以上にしてください。',
  regex: v => /^(?=.*[!-/:-@[-`{-~])(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])[!-~]{12,}$/.test(v) || 'パスワードは半角英大文字、半角英小文字、半角数字、半角記号の4種類すべてを含む必要があります。'
})
const emailRules = reactive({
  regex: v => /^(([^<>()[\]\\.,;:\s@]+(\.[^<>()[\]\\.,;:\s@]+)*)|(.+))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(v) || 'メールアドレスを正しく入力してください。'
})
const noJapaneseRule = reactive({
  regex: v => /^[a-z0-9!-/:-@¥[-`{-~]*$/.test(v) || '半角英小文字半角数字半角記号で入力してください。'
})
const noLastCommaRule = reactive({
  regex: v => /^(?!.*,$).*$/.test(v) || '語尾に ,（カンマ）は使用できません。'
})

function validateForm(){
  errorFlg.value = false
  // 入力有無の確認
  for (var field in form) {
    if (props.userManagerInfo.formType === 'edit' && field === 'password') {
      continue
    }
    var isError = checkMandatory(form[field], field)
    if (isError) {
      errorFlg.value = true
      errorMessage.value = '入力内容に誤りがあります。'
      return
    }
  }

  // 外部カタログサイトの場合
  if (form.ckan === 'external') {
    if (!form.releaseCkanUrl && !form.releaseCkanApikey && !form.releaseCkanUsername && !form.detailCkanUrl && !form.detailCkanApikey && !form.detailCkanUsername) {
      errorFlg.value = true
      errorMessage.value = '登録先カタログサイトに外部カタログサイトを選択している場合は、外部横断カタログサイト情報または外部詳細カタログサイト情報を入力してください。' 
      return
    }
    username.value.validate()
    email.value.validate()

    // 新規作成の場合にパスワードをチェックする
    if (props.userManagerInfo.formType === 'new') {
      password.value.validate()
      if (password.value.hasError) {
        errorFlg.value = true
        errorMessage.value = '入力内容に誤りがあります。'
      }
    }

    if (!username.value.hasError &&
        !email.value.hasError &&
        !errorFlg.value.value) {
      if (props.userManagerInfo.formType === 'new') {
        createUser()
      } else {
        updateUser()
      }
    } else {
      errorFlg.value = true
      errorMessage.value = '入力内容に誤りがあります。'
    }
  } else {
    username.value.validate()
    organization.value.validate()
    email.value.validate()
    // 新規作成の場合にパスワードをチェックする
    if (props.userManagerInfo.formType === 'new') {
      password.value.validate()
      if (password.value.hasError) {
        errorFlg.value = true
        errorMessage.value = '入力内容に誤りがあります。'
      }
    }

    if (!username.value.hasError &&
        !organization.value.hasError &&
        !email.value.hasError &&
        !errorFlg.value) {
    if (props.userManagerInfo.formType === 'new') {
        createUser()
      } else {
        updateUser()
      }
    } else {
      errorFlg.value = true
      errorMessage.value = '入力内容に誤りがあります。'
    }
  }
}

function initForm(){
  if (props.userManagerInfo.formType === 'edit') {
    axios.get(config.apiPrefix + '/users/' + props.userManagerInfo.username)
      .then(res => {
        form.username = res.data.username
        form.email = res.data.email
        form.caddeUserId = res.data.cadde_user_id
        form.organization = res.data.organization
        form.ckan = res.data.ckan
        if (res.data.ckan === 'external') {
          form.releaseCkanUrl = res.data.about.release_ckan_url
          form.releaseCkanApikey = res.data.about.release_ckan_apikey
          form.releaseCkanUsername = res.data.about.release_ckan_username
          if (res.data.about.release_ckan_auth_method) {
            form.releaseAuthentication = 'isAuth'
            form.releaseAuthenticationMethod = res.data.about.release_ckan_auth_method
          }
          form.detailCkanUrl = res.data.about.detail_ckan_url
          form.detailCkanApikey = res.data.about.detail_ckan_apikey
          form.detailCkanUsername = res.data.about.detail_ckan_username
          if (res.data.about.detail_ckan_auth_method) {
            form.detailAuthentication = 'isAuth'
            form.detailAuthenticationMethod = res.data.about.detail_ckan_auth_method
          } 
        }
      })
      .catch(err => {
        errorFlg.value = true
        errorMessage.value = err.response.data.message.detail
        Loading.hide()
        console.log('error message:', err.response.data.message)
        attr.completeDialog.isDisplay = true
        attr.completeDialog.message = err.response.data.message || 'ユーザデータの取得に失敗しました。管理者に問い合わせてください。'
        attr.completeDialog.errorFlg = true
      })
  } else {
    Object.assign(form, defaultForm)
  }
}

function createUser(){
  Loading.show()
  form.organization = form.organization ? form.organization.split(',') : []
  form.caddeUserId = form.caddeUserId ? form.caddeUserId.split(',') : []
  axios.post(config.apiPrefix + '/users', form)
    .then(res => {
      attr.completeDialog.message = '登録が完了しました。'
      attr.completeDialog.isDisplay = true
      Loading.hide()
    })
    .catch(err => {
      // 組織の値を文字列に変換
      var tmpOrganization = ''
      for (var i in form.organization) {
        tmpOrganization += form.organization[i] + ','
      }
      form.organization = tmpOrganization.slice(0, -1)
      // CADDEユーザIDの値を文字列に変換
      var tmpCaddeUserId = ''
      for (var i in form.caddeUserId) {
        tmpCaddeUserId += form.caddeUserId[i] + ','
      }
      form.caddeUserId = tmpCaddeUserId.slice(0, -1)
      errorFlg.value = true
      console.log('error message:', err.response.data.message)
      errorMessage.value = err.response.data.message || '登録に失敗しました。管理者に問い合わせてください。'
      Loading.hide()
    })
}

function updateUser(){
  Loading.show()
  form.organization = form.organization ? form.organization.split(',') : []
  form.caddeUserId = form.caddeUserId ? form.caddeUserId.split(',') : []
  axios.put(config.apiPrefix + '/users' , form)
    .then(res => {
      attr.completeDialog.message = '登録が完了しました。'
      // console.log('横断CKAN: ' + res.data.message.release + '詳細CKAN: ' + res.data.message.detail)
      attr.completeDialog.isDisplay = true
      Loading.hide()
    })
    .catch(err => {
      // 組織の値を文字列に変換
      var tmpOrganization = ''
      for (var i in form.organization) {
        tmpOrganization += form.organization[i] + ','
      }
      form.organization = tmpOrganization.slice(0, -1)
      // CADDEユーザIDの値を文字列に変換
      var tmpCaddeUserId = ''
      for (var i in form.caddeUserId) {
        tmpCaddeUserId += form.caddeUserId[i] + ','
      }
      form.caddeUserId = tmpCaddeUserId.slice(0, -1)
      errorFlg.value = true
      errorMessage.value = err.response.data.message || '登録に失敗しました。管理者に問い合わせてください。'
      console.log('error message:', err.response.data.message)
      Loading.hide()
    })
}

// 入力必須項目の入力有無判定
function checkMandatory(value, field){
  if (!value) {
    if (field === 'organization' && form.ckan === 'external') {
      // 登録先カタログが「外部カタログサイト」の場合は、組織名は入力項目でない
      return false
    } else if (field === 'detailCkanUrl' && !form.detailCkanApikey && !form.detailCkanUsername && form.detailAuthentication === 'noAuth') {
     return false
    } else if (field === 'detailCkanApikey' && !form.detailCkanUrl && !form.detailCkanUsername && form.detailAuthentication === 'noAuth') {
      return false
    } else if (field === 'detailCkanUsername' && !form.detailCkanUrl && !form.detailCkanApikey && form.detailAuthentication === 'noAuth') {
      return false
    } else if (field === 'detailAuthenticationMethod' && form.detailAuthentication === 'noAuth') {
      return false
    } else if (field === 'releaseCkanUrl' && !form.releaseCkanApikey && !form.releaseCkanUsername && form.releaseAuthentication === 'noAuth') {
      return false
    } else if (field === 'releaseCkanApikey' && !form.releaseCkanUrl && !form.releaseCkanUsername && form.releaseAuthentication === 'noAuth') {
      return false
    } else if (field === 'releaseCkanUsername' && !form.releaseCkanUrl && !form.releaseCkanApikey && form.releaseAuthentication === 'noAuth') {
      return false
    } else if (field === 'releaseAuthenticationMethod' && form.releaseAuthentication === 'noAuth') {
      return false
    } else {
      return true
    }
  }
}

// 入力必須項目の未入力メッセージ表示
function mandatoryMessage(value, field){
  if (!value) {
    if (field === 'organization' && form.ckan === 'external') {
      // 登録先カタログが「外部カタログサイト」の場合は、組織名は入力項目でない
      return ''
    } else if (field === 'detailCkanUrl' && !form.detailCkanApikey && !form.detailCkanUsername && form.detailAuthentication === 'noAuth') {
      return ''
    } else if (field === 'detailCkanApikey' && !form.detailCkanUrl && !form.detailCkanUsername && form.detailAuthentication === 'noAuth') {
      return ''
    } else if (field === 'detailCkanUsername' && !form.detailCkanUrl && !form.detailCkanApikey && form.detailAuthentication === 'noAuth') {
      return ''
    } else if (field === 'detailAuthenticationMethod' && form.detailAuthentication === 'noAuth') {
      return ''
    } else if (field === 'releaseCkanUrl' && !form.releaseCkanApikey && !form.releaseCkanUsername && form.releaseAuthentication === 'noAuth') {
      return ''
    } else if (field === 'releaseCkanApikey' && !form.releaseCkanUrl && !form.releaseCkanUsername && form.releaseAuthentication === 'noAuth') {
      return ''
    } else if (field === 'releaseCkanUsername' && !form.releaseCkanUrl && !form.releaseCkanApikey && form.releaseAuthentication === 'noAuth') {
      return ''
    } else if (field === 'releaseAuthenticationMethod' && form.releaseAuthentication === 'noAuth') {
      return ''
    } else {
      return '【入力必須項目】'
    }
  }
}

// created
initForm()
// CKAN認証方式取得
axios.get(config.apiPrefix + '/config/ckanauth')
.then(res => {
  authMethodOptions.value = res.data
})
.catch(err => {
  console.log('error message:', err.response.data.message)
  attr.completeDialog.isDisplay = true
  attr.completeDialog.message = err.response.data.message
  attr.completeDialog.errorFlg = true
})

// 登録先カタログサイト監視
watch(() => form.ckan,
  (newVal, oldVal) => {
  if (newVal === 'external') {
    form.organization = ''
  }
})
// ユーザ認証の有無監視
watch(() => form.releaseAuthentication,
  (selectedVal) => {
  if (selectedVal === 'noAuth') {
    form.releaseAuthenticationMethod = ''
  }
})
watch(() => form.detailAuthentication,
  (selectedVal) => {
  if (selectedVal === 'noAuth') {
    form.detailAuthenticationMethod = ''
  }
})


</script>

<template>
  <div>
    <div class="q-layout-padding user-form">
      <q-card class="q-mt-sm q-card-background-white">
        <q-card-section>
          <div class="col">
            <div v-if="props.userManagerInfo.formType === 'new'">
              <font size='5' color='#1d468f'>CKANユーザ名</font><br>
              登録するCKANユーザ名を入力してください。
              <q-input
                v-model="form.username"
                ref="username"
                :rules="[checkHyphen, checkLength, noJapaneseRule.regex]"
                class="input-item"
                counter
                :error="checkMandatory(form.username, 'username')"
                :error-message="mandatoryMessage(form.username, 'username')"
              />
            </div>
            <div v-else>
              <font size='5' color='#1d468f'>CKANユーザ名</font><br>
              登録するCKANユーザ名を入力してください。
              <q-input v-model="form.username" ref="username" class="input-item" disable/>
            </div>
            <div class="q-mt-md">
              <font size='5' color='#1d468f'>CKANユーザパスワード</font>
              <br>
              <div v-if="props.userManagerInfo.formType === 'new'">
                登録するCKANユーザのパスワードを入力してください。
              </div>
              <div v-else>
                登録済みのCKANユーザのパスワードを入力してください。<br>
                ここではCKANユーザパスワードを編集することはできません。
              </div>
              <q-input
                v-model="form.password"
                ref="password"
                :type="isPwd ? 'password' : 'text'"
                :rules="[passRules.minlength, passRules.regex]"
                class="input-item"
                :error="checkMandatory(form.password, 'password')"
                :error-message="mandatoryMessage(form.password, 'password')"
              >
                <q-icon
                  size="32px"
                  :name="isPwd ? 'visibility_off' : 'visibility'"
                  class="cursor-pointer"
                  @click="isPwd = !isPwd"
                />
              </q-input>
            </div>
            <div v-if="form.ckan == 'internal' " class="q-mt-md">
              <font size='5' color='#1d468f'>組織名</font>
              <br>
              登録するCKANユーザの組織名を入力してください。<br>
              複数ある場合は、カンマ区切りで入力してください。<br>
              登録先カタログサイトが外部カタログサイトの場合は、入力不要です。
              <q-input
                v-model="form.organization"
                ref="organization"
                :rules="[noJapaneseRule.regex, noLastCommaRule.regex]"
                class="input-item"
                :error="checkMandatory(form.organization, 'organization')"
                :error-message="mandatoryMessage(form.organization, 'organization')"
                placeholder="例: org-a,org-b"
              />
            </div>
            <div class="q-mt-md">
              <font size='5' color='#1d468f'>メール</font>
              <br>
              登録するCKANユーザのメールアドレスを入力してください。
              <q-input
                v-model="form.email"
                ref="email"
                :rules="[emailRules.regex, checkHyphen]"
                class="input-item"
                :error="checkMandatory(form.email, 'email')"
                :error-message="mandatoryMessage(form.email, 'email')"
              />
            </div>
            <div class="q-mt-md">
              <font size='5' color='#1d468f'>CADDEユーザID</font>
              <br>
              CKANユーザと紐づくCADDEユーザIDを入力してください。<br>
              複数ある場合は、カンマ区切りで入力してください。
              <q-input
                v-model="form.caddeUserId"
                :rules="[noJapaneseRule.regex, noLastCommaRule.regex]"
                ref="caddeUserId"
                class="input-item"
                :error="checkMandatory(form.caddeUserId, 'caddeUserId')"
                :error-message="mandatoryMessage(form.caddeUserId, 'caddeUserId')"
                placeholder="例: user-a,user-b"
              />
            </div>
            <div class="q-mb-md">
              <div class="q-mt-md">
                <font size='5' color='#1d468f'>登録先カタログサイト</font>
                <br>
                入力したカタログ情報の登録先カタログサイトを選択してください。
                <br>
                <q-radio v-model="form.ckan" val="internal" label="ローカルカタログサイト" />
                <q-radio v-model="form.ckan" val="external" label="外部カタログサイト" />
              </div>
              <div v-if="form.ckan === 'external'" class="q-mt-md">
                <div>
                  <font size='5' color='#1d468f'>外部横断カタログサイトURL</font>
                  <br>
                  外部のカタログサイトへ登録する場合、対象カタログサイトのURLを入力してください。
                  <q-input
                    v-model="form.releaseCkanUrl"
                    ref="releaseCkanUrl"
                    class="input-item"
                    :error="checkMandatory(form.releaseCkanUrl, 'releaseCkanUrl')"
                    :error-message="mandatoryMessage(form.releaseCkanUrl, 'releaseCkanUrl')"
                  />
                </div>
                <div class="q-mt-md">
                  <font size='5' color='#1d468f'>外部横断カタログサイトAPIキー</font>
                  <br>
                  外部のカタログサイトへ登録する場合、対象カタログサイトのAPIキーを入力してください。
                  <q-input
                    v-model="form.releaseCkanApikey"
                    ref="releaseCkanApikey"
                    class="input-item"
                    :error="checkMandatory(form.releaseCkanApikey, 'releaseCkanApikey')"
                    :error-message="mandatoryMessage(form.releaseCkanApikey, 'releaseCkanApikey')"
                  />
                </div>
                <div class="q-mt-md">
                  <font size='5' color='#1d468f'>外部横断カタログサイトユーザ名</font>
                  <br>
                  外部のカタログサイトへ登録する場合、対象カタログサイトのユーザ名を入力してください。
                  <q-input
                    v-model="form.releaseCkanUsername"
                    ref="releaseCkanUsername"
                    class="input-item"
                    :error="checkMandatory(form.releaseCkanUsername, 'releaseCkanUsername')"
                    :error-message="mandatoryMessage(form.releaseCkanUsername, 'releaseCkanUsername')"
                  />
                </div>
                <div class="q-mt-md">
                  <font size='5' color='#1d468f'>外部横断カタログサイトユーザの外部認証の有無</font>
                  <br>
                  外部横断カタログサイトのユーザの外部認証を行うか否かを選択してください。
                  <br>
                  <q-radio v-model="form.releaseAuthentication" val="isAuth" label="外部認証を行う" />
                  <q-radio v-model="form.releaseAuthentication" val="noAuth" label="外部認証を行わない" />
                  <br>
                  <div v-if="form.releaseAuthentication === 'isAuth'">
                    <br>
                    外部認証方式を選択してください。
                    <q-select
                      v-model="form.releaseAuthenticationMethod"
                      class="select-item"
                      :options="authMethodOptions.value"
                      :error="checkMandatory(form.releaseAuthenticationMethod, 'releaseAuthenticationMethod')"
                      :error-message="mandatoryMessage(form.releaseAuthenticationMethod, 'releaseAuthenticationMethod')"
                    />
                  </div>
                </div>
                <div class="q-mt-md">
                  <font size='5' color='#1d468f'>外部詳細カタログサイトURL</font>
                  <br>
                  外部のカタログサイトへ登録する場合、対象カタログサイトのURLを入力してください。
                  <q-input
                    v-model="form.detailCkanUrl"
                    ref="detailCkanUrl"
                    class="input-item"
                    :error="checkMandatory(form.detailCkanUrl, 'detailCkanUrl')"
                    :error-message="mandatoryMessage(form.detailCkanUrl, 'detailCkanUrl')"
                  />
                </div>
                <div class="q-mt-md">
                  <font size='5' color='#1d468f'>外部詳細カタログサイトAPIキー</font>
                  <br>
                  外部のカタログサイトへ登録する場合、対象カタログサイトのAPIキーを入力してください。
                  <q-input
                    v-model="form.detailCkanApikey"
                    ref="detailCkanApikey"
                    class="input-item"
                    :error="checkMandatory(form.detailCkanApikey, 'detailCkanApikey')"
                    :error-message="mandatoryMessage(form.detailCkanApikey, 'detailCkanApikey')"
                  />
                </div>
                <div class="q-mt-md">
                  <font size='5' color='#1d468f'>外部詳細カタログサイトユーザ名</font>
                  <br>
                  外部のカタログサイトへ登録する場合、対象カタログサイトのユーザ名を入力してください。
                  <q-input
                    v-model="form.detailCkanUsername"
                    ref="detailCkanUsername"
                    class="input-item"
                    :error="checkMandatory(form.detailCkanUsername, 'detailCkanUsername')"
                    :error-message="mandatoryMessage(form.detailCkanUsername, 'detailCkanUsername')"
                  />
                </div>
                <div class="q-mt-md">
                  <font size='5' color='#1d468f'>外部詳細カタログサイトユーザの外部認証の有無</font>
                  <br>
                  外部横断カタログサイトのユーザの外部認証を行うか否かを選択してください。
                  <br>
                  <q-radio v-model="form.detailAuthentication" val="isAuth" label="外部認証を行う" />
                  <q-radio v-model="form.detailAuthentication" val="noAuth" label="外部認証を行わない" />
                  <br>
                  <div v-if="form.detailAuthentication === 'isAuth'">
                    <br>
                    外部認証方式を選択してください。
                    <q-select
                      v-model="form.detailAuthenticationMethod"
                      class="select-item"
                      :options="authMethodOptions.value"
                      :error="checkMandatory(form.detailAuthenticationMethod, 'detailAuthenticationMethod')"
                      :error-message="mandatoryMessage(form.detailAuthenticationMethod, 'detailAuthenticationMethod')"
                    />
                  </div>
                </div>
              </div>
            </div>
            <div v-show="errorFlg">
              <font size="3" color="#FF0000">{{ errorMessage }}</font>
            </div>
          </div>
        </q-card-section>
      </q-card>
      <!-- 登録完了ダイアログ -->
      <CompleteDialog
        v-bind:dialogInfo="attr.completeDialog"
        @close-dialog="emit('changeDisplayEvent', '', '', 'userlist'), attr.completeDialog.isDisplay = false"
      />
      <!-- フッター -->
      <q-footer reveal elevated>
        <q-toolbar class="justify-between">
          <q-btn
            flat
            color="white"
            icon="reply_all"
            @click="emit('changeDisplayEvent', '', '', 'userlist')"
            label="ユーザ一覧に戻る"
          />
          <div v-if="props.userManagerInfo.formType === 'new'">
            <q-btn
              flat
              color="white"
              icon="save_alt"
              @click="validateForm()"
              label="登録"
            />
          </div>
          <div v-else>
            <q-btn
              flat
              color="white"
              icon="save_alt"
              @click="validateForm()"
              label="編集"
            />
          </div>
        </q-toolbar>
      </q-footer>
    </div>
  </div>
</template>

<style lang="scss">
.q-card-background-white{
  background:white
}


.background-whitesmoke{
  background:#f5f5f5;
}

.user-form .input-item{
  padding-left: 15px;
  width: 98%;
}
.user-form .select-item{
  padding-left: 15px;
  width: 30%;
}
</style>
