<script setup>
import { ref, reactive } from 'vue'

const props = defineProps(['dialogInfo'])
const emit = defineEmits(['update-pass, close-dialog'])
const requiredRule = reactive(v => (v && !!v) || '【入力必須項目】')
const passwordRules = reactive({
  minlength: v => (v && v.length >= 12) || 'パスワードは12文字以上にしてください。',
  checkPass: v => (v === newPassword.value) || '新しいパスワードと同じパスワードを入力してください。',
  regex: v => /^(?=.*[!-/:-@[-`{-~])(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])[!-~]{12,}$/.test(v) || 'パスワードは半角英大文字、半角英小文字、半角数字、半角記号の4種類すべてを含む必要があります。'
})

const oldPassword = ref('')
const newPassword = ref('')
const checkNewPassword = ref('')
const oldPass = ref(null)
const newPass = ref(null)
const checkNewPass = ref(null)

// 入力値のエラー判定
function validate(){
  oldPass.value.validate()
  newPass.value.validate()
  checkNewPass.value.validate()
  if (!oldPass.value.hasError && !newPass.value.hasError && !checkNewPass.value.hasError) {
    // 全ての項目にエラーがなければ、パスワード更新
    emit('update-pass', props.dialogInfo, checkNewPassword.value, oldPassword.value)
  } else {
    console.log('error oldPass:' + oldPass.value.hasError)
    console.log('error newPass:' + newPass.value.hasError)
    console.log('error checkNewPass:' + checkNewPass.value.hasError)
  }
}

// 入力フィールドの初期化
function initField(){
  oldPassword.value = ''
  newPassword.value = ''
  checkNewPassword.value = ''
}

defineExpose({
  initField
})
</script>

<template>
  <div>
    <q-dialog :modelValue="props.dialogInfo.isDisplay" persistent transition-show="scale" transition-hide="scale" class="password-update-dialog">
      <q-card style="max-width: 45%; width: 100%;">
        <q-bar class="bg-primary text-white">
          <q-icon name="lock" />
          <div><font size=3>パスワード設定</font></div>
          <q-space />
        </q-bar>
        <q-card-section>
          <div class="column">
            <div class="row items-center justify-center q-py-sm fit">
              <q-input
                class="input-item" 
                dense 
                outlined 
                hide-bottom-space 
                v-model="oldPassword" 
                ref="oldPass"
                :rules="[requiredRule, passwordRules.minlength, passwordRules.regex]"
               >
                <template v-slot:before>
                  <div class="indent-cell label-area"><font size=3>古いパスワード&ensp;：&ensp;</font></div>
                </template>
              </q-input>
            </div>
            <div class="row items-center justify-center q-py-sm fit">
              <q-input 
                class="input-item"
                outlined 
                dense 
                hide-bottom-space 
                v-model="newPassword" 
                :rules="[requiredRule, passwordRules.minlength, passwordRules.regex]" 
                ref="newPass" 
               >
                <template v-slot:before>
                  <div class="indent-cell label-area"><font size=3>新しいパスワード&ensp;：&ensp;</font></div>
                </template>
              </q-input>
            </div>
            <div class="row items-center justify-center q-py-sm fit">
              <q-input 
              class="input-item"
              outlined 
              dense 
              hide-bottom-space 
              v-model="checkNewPassword" 
              ref="checkNewPass" 
              :rules="[requiredRule, passwordRules.minlength, passwordRules.checkPass, passwordRules.regex]" 
              >
                <template v-slot:before>
                  <div class="indent-cell label-area"><font size=3>パスワードの確認&ensp;：&ensp;</font></div>
                </template>
              </q-input>
            </div>
            <div v-if="dialogInfo.message">
              <div class="q-pa-md"><font size=3 color="red">{{dialogInfo.message}}</font></div>
            </div>
          </div>
        </q-card-section>
        <q-card-section style="padding-top: 0;">
          <div class="q-gutter-md row justify-center">
            <q-btn v-close-popup outline color="black" class="col" label="キャンセル" @click="emit('close-dialog'), initField()" />
            <q-btn unelevated color="primary" class="col" label="変更" @click="validate()" />
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
  </div>
</template>



<style lang="scss">
.indent-cell{
  max-width:360px;
  white-space:normal;
  overflow-wrap:break-word;
}

.password-update-dialog .input-item{
  width: 95%;
}

.label-area{
  width:162px;
  text-align: right;
  color: #000;
}
</style>
