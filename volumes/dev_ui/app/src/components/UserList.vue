<script setup>
import axios from 'axios'
import { Loading } from 'quasar'
import CompleteDialog from './dialog/CompleteDialog.vue'
import DeleteDialog from './dialog/DeleteDialog.vue'
import PasswordUpdateDialog from './dialog/PasswordUpdateDialog.vue'
import { ref, reactive } from 'vue'
import { config } from '../boot/config.js'

const emit = defineEmits(['changeDisplayEvent'])
const passwordUpdateDialog = ref(null)
const pagination = reactive({
  rowsPerPage: 10
})
const completeDialog = reactive({
  isDisplay: false,
  message: '',
  errorFlg: false,
})
const passUpdateDialog = reactive({
  isDisplay: false,
  userName: '',
  email: '',
  password: '',
  message: ''
})
const deleteDialog = reactive({
  pageName: 'userList',
  isDisplay: false,
  userName: ''
})
const userList = reactive({
  userList: []
})
const columns = reactive([
  { name: 'name', label: 'CKANユーザ名', field: 'name', align: 'left', sortable: true },
  { name: 'id', label: 'CADDEユーザID', field: 'id', align: 'left', sortable: true },
  { name: 'organization', label: '組織名', field: 'organization', align: 'left', sortable: true },
  { name: 'email', label: 'メール', field: 'email', align: 'left', sortable: true },
  { name: 'created', label: '登録日', field: 'created', align: 'center', sortable: true },
  { name: 'update', field: 'update', align: 'center' },
  { name: 'editPass', field: 'editPass', align: 'center' },
  { name: 'delete', field: 'delete', align: 'center' }
])

function fetchUserlist(){
  Loading.show()
  axios.get(config.apiPrefix + '/userlist')
    .then(res => {
      Loading.hide()
      userList.userList = res.data.userlist
    })
    .catch(err => {
      Loading.hide()
      console.log('error message:', err.response.data.message)
      completeDialog.isDisplay = true
      completeDialog.message = err.response.data.message || 'ユーザ一覧の取得に失敗しました。管理者に問い合わせてください。'
      completeDialog.errorFlg = true
    })
}

function deleteUser(username){
  Loading.show()
  axios.delete(config.apiPrefix + '/users/' + username)
    .then(res => {
      Loading.hide()
      fetchUserlist()
      if (res.data.status === 'success') {
          completeDialog.message = 'ユーザを削除しました。'
      }
      completeDialog.isDisplay = true
      deleteDialog.isDisplay = false
      console.log('横断CKAN: ' + res.data.message.release + ', 詳細CKAN: ' + res.data.message.detail)
    })
    .catch(err => {
      Loading.hide()
      fetchUserlist()
      console.log('error message:', err.response.data.message)
      completeDialog.isDisplay = true
      completeDialog.message = err.response.data.message || 'ユーザの削除に失敗しました。管理者に問い合わせてください。'
      completeDialog.errorFlg = true
    })
}

function updatePass(data, newPassword, oldPasswprd){
  Loading.show()
  axios.put(config.apiPrefix + '/users/password', { email: data.email, username: data.userName, new_password: newPassword, old_password: oldPasswprd })
    .then(res => {
      Loading.hide()
      fetchUserlist()
      completeDialog.message = 'パスワードを更新しました。'
      completeDialog.isDisplay = true
      passUpdateDialog.isDisplay = false
      passUpdateDialog.message = ''
      passwordUpdateDialog.value.initField()
    })
    .catch(err => {
      Loading.hide()
      console.log('error message:', err.response.data.message)
      passUpdateDialog.message = err.response.data.message || 'パスワードの更新に失敗しました。管理者に問い合わせてください。'
    })
}

fetchUserlist()

</script>

<template>
  <div class="q-layout-padding flex justify-center content-center">
    <q-card q-card class="q-card-background-white" style="max-width: 95%; width: 100%;">
      <q-card-section>
        <div class="row justify-center items-center full-width">
          <q-table
            title="ユーザ一覧"
            :rows="userList.userList"
            :columns="columns"
            separator="cell"
            v-bind:pagination="pagination"
            row-key="name"
            class="full-width"
          >
            <template v-slot:top>
              <div class="q-table__title text-weight-bolder full-width row justify-between">
                <font size="5" color="#1d468f">ユーザ一覧</font>
                <q-btn size='md' color='light-blue-10' label="新規登録" @click="emit('changeDisplayEvent', '', 'new', 'userform')" ></q-btn>
              </div>
            </template>
            <template v-slot:body="props">
              <q-tr :props="props">
                <q-td key="name" :props="props"><div class="indent-cell">{{ props.row.name }}</div></q-td>
                <q-td key="name" :props="props"><div class="indent-cell">{{ props.row.cadde_user_id }}</div></q-td>
                <q-td key="name" :props="props"><div class="indent-cell">{{ props.row.organization }}</div></q-td>
                <q-td key="name" :props="props"><div class="indent-cell">{{ props.row.email }}</div></q-td>
                <q-td key="name" :props="props"><div class="indent-cell" style="min-width: 66px;">{{ props.row.created }}</div></q-td>
                <q-td key="update" :props="props">
                  <q-btn
                    outline
                    color="secondary"
                    icon="edit"
                    class="full-width"
                    style="font-size: 1em; min-width: 100px;"
                    label="編集"
                    @click="emit('changeDisplayEvent', props.row.name, 'edit', 'userform')"
                  />
                </q-td>
                <q-td key="editPass" :props="props">
                  <q-btn
                    outline
                    color="secondary"
                    icon="lock"
                    class="full-width"
                    style="font-size: 1em; min-width: 170px;"
                    label="CKANユーザパスワード変更"
                    @click="passUpdateDialog.isDisplay=true, passUpdateDialog.userName=props.row.name, passUpdateDialog.email=props.row.email"
                  />
                </q-td>
                <q-td key="delete" :props="props">
                  <q-btn
                    outline
                    color="red"
                    icon="delete"
                    class="full-width"
                    style="font-size: 1em; min-width: 100px;"
                    label="削除"
                    @click="deleteDialog.isDisplay=true, deleteDialog.userName=props.row.name"
                  />
                </q-td>
              </q-tr>
            </template>
          </q-table>
        </div>
      </q-card-section>
    </q-card>

    <!-- 完了ダイアログ -->
    <CompleteDialog
      v-bind:dialogInfo="completeDialog"
      @close-dialog="completeDialog.isDisplay = false"
    />

    <!-- 削除ダイアログ -->
    <DeleteDialog
      v-bind:dialogInfo="deleteDialog"
      @delete-user-data="deleteUser"
      @close-dialog="deleteDialog.isDisplay = false"
    />

    <!-- パスワード設定ダイアログ -->
    <PasswordUpdateDialog
      v-bind:dialogInfo="passUpdateDialog"
      @update-pass="updatePass"
      ref="passwordUpdateDialog"
      @close-dialog="passUpdateDialog.isDisplay = false, passUpdateDialog.message = ''"
    />

  </div>
</template>

<style lang="scss">
.q-card-background-white{
  background:white
}
.background-whitesmoke{
  background:#f5f5f5;
}

.indent-cell{
  max-width:360px;
  white-space:normal;
  overflow-wrap:break-word;
}

</style>
