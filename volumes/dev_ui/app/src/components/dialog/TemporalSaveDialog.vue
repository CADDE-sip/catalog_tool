<script setup>
import { reactive, onBeforeUpdate } from 'vue'
const props = defineProps(['dialogInfo'])
const emit = defineEmits(['tmp-save, close-dialog'])

const TITLE_MAX_LENGTH = 50
const ERROR_MESSAGE = {
  required: 'カタログの名前の入力は必須です。',
  maxLength: 'カタログの名前は50文字以内で設定してください。'
}

const attr = reactive({
  inActiveSaveBtn: false,
  catalogName: ''
})

// カタログ名のエラー判定
function errorField() {
  if (!attr.catalogName) {
    attr.inActiveSaveBtn = true
    return true
  } else if (attr.catalogName.length > TITLE_MAX_LENGTH) {
    attr.inActiveSaveBtn = true
    return true
  } else {
    attr.inActiveSaveBtn = false
    return false
  }
}

// フィールド下に表示するエラーメッセージ生成
function errorFieldMessage() {
  if (!attr.catalogName) {
    return ERROR_MESSAGE.required
  } else if (attr.catalogName.length > TITLE_MAX_LENGTH) {
    return ERROR_MESSAGE.maxLength
  } else {
    return ''
  }
}

onBeforeUpdate(() => {
  // データセットのタイトルを反映させる
  attr.catalogName = props.dialogInfo.catalogName
})

</script>

<template>
  <div>
    <q-dialog :modelValue="props.dialogInfo.isDisplay" persistent transition-show="scale" transition-hide="scale">
      <q-card style="max-width: 45%; width: 100%;">
        <q-bar class="bg-primary text-white">
          <q-icon name="folder" />
          <div><font size=3>一時保存</font></div>
          <q-space />
        </q-bar>
        <q-card-section>
          <div class="column">
            <div class="row items-center justify-center">
              <font size=3>一時保存するカタログの名前を入力してください。（最大50文字）<br>
              同一名で保存する場合、カタログが上書きされます。<br><br>
              </font>
              <q-input
                outlined
                v-model="attr.catalogName"
                dense
                style="width: 95%;"
                counter
                :error="errorField()"
                :error-message="errorFieldMessage()"
              >
                <template v-slot:before>
                  <div class="text-right" style="width:162px; text-align: right; color: #000;"><font size=3>カタログ名&ensp;：&ensp;</font></div>
                </template>
              </q-input>
            </div>
          </div>
        </q-card-section>
        <q-card-section style="padding-top: 0;">
          <div class="q-gutter-md row justify-center">
            <q-btn v-close-popup outline color="black" class="col" label="キャンセル" @click="emit('close-dialog')" />
            <q-btn 
            unelevated 
            color="primary"
            class="col" 
            label="保存"
            @click="emit('tmp-save', attr.catalogName)"
            :disable="attr.inActiveSaveBtn"
            v-close-popup />
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
  </div>
</template>
