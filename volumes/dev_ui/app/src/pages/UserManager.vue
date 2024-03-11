<script setup>
import { reactive, ref } from 'vue'
import UserList from '../components/UserList.vue'
import UserForm from '../components/UserForm.vue'
import { useStore } from '../stores/store'

const nowDisplay = ref('userlist')
const formType = ref('new') 
const username = ref('')
const store = useStore()
const attr = reactive({
  userForm: {
    formType: '',
    username: '',
    nowDisplay: ''
  }
})

function changeDisplay(usernameValue, formTypeValue, nowDisplayValue){
  var execMode = ''
  switch (formTypeValue) {
    case 'new'://ユーザ作成
      execMode = 'createUser'
      break
    case 'edit'://ユーザ編集
      execMode = 'editUser'
      break
    default://ユーザ一覧
      execMode = 'userManagement'
   }
  // 実行モード情報を更新
  store.updateMode({ mode: execMode, ckanType: '', isBothCatalog: false })
  username.value = usernameValue
  formType.value = formTypeValue
  nowDisplay.value = nowDisplayValue
  attr.userForm.username = usernameValue
  attr.userForm.formType = formTypeValue
  attr.userForm.nowDisplay = nowDisplayValue
}

defineExpose({
  formType,
  username,
  nowDisplay,
  changeDisplay
})

</script>

<template>
  <div class="col-12" v-if="nowDisplay === 'userlist'">
    <UserList
      @changeDisplayEvent="changeDisplay"
     />
  </div>
  <div class="col-12" v-else>
    <UserForm 
      v-bind:userManagerInfo="attr.userForm"
      @changeDisplayEvent="changeDisplay"
    />
  </div>
</template>

