
<script setup>
const props = defineProps(['dialogInfo'])
const emit = defineEmits(['close-dialog'])

// method
function convertMessage(message) {
  // 画面から取得したメッセージの改行部を<br>タグに変換する
  if (message) {
    return message.replace(/\r?\n/g, '<br>')
  } else {
    return 'エラーメッセージの取得に失敗しました。<br>管理者に問い合わせてください。'
  }
}
</script>

<template>
  <div>
    <q-dialog :modelValue="props.dialogInfo.isDisplay" persistent>
      <q-card style="max-width: 35% width: 100%;">
        <q-card-section class="column items-center">
          <div style="width: 100%; text-align: center;">
            <q-avatar  v-if="props.dialogInfo.errorFlg" icon="error" font-size="30px" text-color="red" />
            <q-avatar  v-else icon="check_circle" font-size="30px" text-color="secondary" />
            <!-- <span class="q-ml-sm">{{ props.dialogInfo.message }}</span> -->
            <p v-html=convertMessage(props.dialogInfo.message)></p>
          </div>
          <div class="q-mt-md">
            <q-btn v-close-popup unelevated label="閉じる" color="primary" @click="emit('close-dialog')"/>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
  </div>
</template>
