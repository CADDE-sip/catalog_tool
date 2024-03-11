<script setup>
const props = defineProps(['dialogInfo'])
const emit = defineEmits(['delete-user-data, delete-one-catalog-data, delete-selected-catalog-data, close-dialog'])
</script>

<template>
  <div>
    <div v-if="props.dialogInfo.pageName==='userList'">
      <q-dialog persistent :modelValue="props.dialogInfo.isDisplay" transition-show="scale" transition-hide="scale">
        <q-card class="card-size">
          <div class="q-pa-md">
            <q-card-section>
              <div class="text-center message-area">
                <font size=3>ユーザ&ensp;<span class="bold-font">{{ props.dialogInfo.userName }}</span>&ensp;を削除しますか？</font>
              </div>
              <div class="q-gutter-md row justify-center q-mt-sm">
                <q-btn v-close-popup outline color="black" class="col" label="キャンセル" @click="emit('close-dialog')" />
                <q-btn v-close-popup unelevated color="primary" class="col" label="削除" @click="emit('delete-user-data', props.dialogInfo.userName)" />
              </div>
            </q-card-section>
          </div>
        </q-card>
      </q-dialog>
    </div>
    <div v-if="props.dialogInfo.pageName==='searchOneDelete'">
      <q-dialog persistent :modelValue="props.dialogInfo.isDisplay" transition-show="scale" transition-hide="scale">
        <q-card class="card-size">
          <div class="q-pa-md">
            <q-card-section>
              <div v-if="props.dialogInfo.type==='release'" class="text-center message-area">
                <font size=3>横断カタログ&ensp;<span class="bold-font">{{ props.dialogInfo.options.catalogName }}</span>&ensp;を削除しますか？</font>
                <div v-if="props.dialogInfo.options.detailId"><font size=3>紐づけられている詳細カタログは削除されません。</font></div>
              </div>
              <div v-if="props.dialogInfo.type==='detail'" class="text-center message-area">
                <font size=3>詳細カタログ&ensp;<span class="bold-font">{{ props.dialogInfo.options.catalogName }}</span>&ensp;を削除しますか？</font>
                <div v-if="props.dialogInfo.options.releaseId"><font size=3>紐づけられている横断カタログは削除されません。</font></div>
              </div>
              <div v-if="props.dialogInfo.type==='release_both'" class="text-center message-area">
                <font size=3>横断カタログ&ensp;<span class="bold-font">{{ props.dialogInfo.options.catalogName }}</span>&ensp;と紐づく詳細カタログを削除しますか？</font>
              </div>
              <div v-if="props.dialogInfo.type==='detail_both'" class="text-center message-area">
                <font size=3>詳細カタログ&ensp;<span class="bold-font">{{ props.dialogInfo.options.catalogName }}</span>&ensp;と紐づく横断カタログを削除しますか？</font>
              </div>
              <div class="q-gutter-md row justify-center q-mt-sm">
                <q-btn v-close-popup outline color="black" class="col" label="キャンセル" @click="emit('close-dialog')" />
                <q-btn v-close-popup unelevated color="primary" class="col" label="削除" @click="emit('delete-one-catalog-data', props.dialogInfo)" />
              </div>
            </q-card-section>
          </div>
        </q-card>
      </q-dialog>
    </div>
    <div v-if="props.dialogInfo.pageName==='searchSelectedDelete'">
      <q-dialog persistent :modelValue="props.dialogInfo.isDisplay" transition-show="scale" transition-hide="scale">
        <q-card class="card-size">
          <div class="q-pa-md">
            <q-card-section>
              <div  v-if="props.dialogInfo.options==='deleteWarningRelease'" class="text-center message-area">
                <font size=3>
                  選択したデータを削除しますか？<br>
                  （紐づく詳細カタログは削除されません。）
                </font>
              </div>
              <div  v-if="props.dialogInfo.options==='deleteWarningDetail'" class="text-center message-area">
                <font size=3>
                  選択したデータを削除しますか？<br>
                  （紐づく横断カタログは削除されません。）
                </font>
              </div>
              <div  v-if="props.dialogInfo.options==='noDeleteWarning'" class="text-center message-area">
                <font size=3>
                  選択したデータを削除しますか？
                </font>
              </div>
              <div class="q-gutter-md row justify-center q-mt-sm">
                <q-btn v-close-popup outline color="black" class="col" label="キャンセル" @click="emit('close-dialog')" />
                <q-btn v-close-popup unelevated color="primary" class="col" label="削除" @click="emit('delete-selected-catalog-data')" />
              </div>
            </q-card-section>
          </div>
        </q-card>
      </q-dialog>
    </div>
    <div v-if="props.dialogInfo.pageName==='selectDraftOneDelete'">
      <q-dialog persistent :modelValue="props.dialogInfo.isDisplay" transition-show="scale" transition-hide="scale">
        <q-card class="card-size">
          <div class="q-pa-md">
            <q-card-section>
              <div class="text-center message-area">
                <font size=3>一時保存データ&ensp;<span class="bold-font">{{ props.dialogInfo.catalogName }}</span>&ensp;を削除しますか？</font>
              </div>
              <div class="q-gutter-md row justify-center q-mt-sm">
                <q-btn v-close-popup outline color="black" class="col" label="キャンセル" @click="emit('close-dialog')" />
                <q-btn v-close-popup unelevated color="primary" class="col" label="削除" @click="emit('delete-one-catalog-data', props.dialogInfo.catalogName)" />
              </div>
            </q-card-section>
          </div>
        </q-card>
      </q-dialog>
    </div>
    <div v-if="props.dialogInfo.pageName==='selectDraftSelectedDelete'">
      <q-dialog persistent :modelValue="props.dialogInfo.isDisplay" transition-show="scale" transition-hide="scale">
        <q-card class="card-size">
          <div class="q-pa-md">
            <q-card-section>
              <div class="text-center message-area">
                <font size=3>選択したデータを削除しますか？</font>
              </div>
              <div class="q-gutter-md row justify-center q-mt-sm">
                <q-btn v-close-popup outline color="black" class="col" label="キャンセル" @click="emit('close-dialog')" />
                <q-btn v-close-popup unelevated color="primary" class="col" label="削除" @click="emit('delete-selected-catalog-data')" />
              </div>
            </q-card-section>
          </div>
        </q-card>
      </q-dialog>
    </div>
  </div>
</template>

<style lang="scss">
.card-size{
  max-width: 35%;
  width: 100%;
}

.message-area{
  overflow-wrap: break-word;
}

.bold-font{
  font-weight: bold;
}
</style>
