<script setup>
// props.dialogInfo.isDisplay : 表示(true)/非表示(false)
// props.dialogInfo.type : ダイアログのタイプ。以下のいずれか
// * create-catalog-release-link-detail : 詳細カタログと紐づく横断カタログ作成
//   options : catalogTitle        // 紐づく詳細カタログ名
//             detailId            // 紐づく詳細カタログid
//             releaseCkanDataName // 横断Ckanデータ名
//             detailCkanDataName  // 詳細Ckanデータ名
// * create-catalog-detail-link-release : 横断カタログと紐づく詳細カタログ作成
//   options : catalogTitle        // 紐づく横断カタログ名
//             releaseId           // 紐づく横断カタログid
//             releaseCkanDataName // 横断Ckanデータ名
//             detailCkanDataName  // 詳細Ckanデータ名
// * create-catalog-release-from-release : 横断カタログの情報を元に、新規で横断カタログ作成
//   options : catalogTitle        // 元にする横断カタログ名
//             releaseId           // 元にする横断カタログid
//             releaseCkanDataName // 横断Ckanデータ名
// * create-catalog-detail-from-release : 横断カタログの情報を元に、新規で詳細カタログ作成
//   options : catalogTitle        // 元にする横断カタログ名
//             releaseId           // 元にする横断カタログid
//             releaseCkanDataName // 横断Ckanデータ名
//             detailCkanDataName  // 詳細Ckanデータ名
// * create-catalog-both-from-release : 横断カタログの情報を元に、新規で横断カタログと詳細カタログを作成
//   options : catalogTitle // 元にする横断カタログ名
//             releaseId    // 元にする横断カタログid
//             releaseCkanDataName // 横断Ckanデータ名
//             detailCkanDataName  // 詳細Ckanデータ名
// * edit-catalog-release : 横断カタログ編集
//   options : catalogTitle // 編集する横断カタログ名
//             releaseId    // 編集する横断カタログid
//             releaseCkanDataName // 横断Ckanデータ名
// * edit-catalog-detail : 詳細カタログ編集
//   options : catalogTitle // 編集する詳細カタログ名
//             detailId     // 編集する詳細カタログid
//             detailCkanDataName  // 詳細Ckanデータ名
// * confirm-discard : 編集中にページを離れる際の確認ダイアログ
//   options : なし
// props.dialogInfo.options : ダイアログのオプション情報
// props.dialogInfo.confirmCallback // 決定が押されたときのコールバック関数(props.dialogInfoを引数とする)
// props.dialogInfo.cancelCallback  // キャンセルが押されたときのコールバック関数(props.dialogInfoを引数とする)

import { computed } from 'vue'
const props = defineProps(['dialogInfo'])
const emit = defineEmits(['confirm, close-dialog'])

// 決定ボタンが押されたときの動作
function onConfirm(){
  if(typeof props.dialogInfo.confirmCallback === "function"){
    props.dialogInfo.confirmCallback(props.dialogInfo)
  }
  emit('confirm', props.dialogInfo)
}

// キャンセルボタンが押されたときの動作
function onCancel(){
  if(typeof props.dialogInfo.cancelCallback === "function"){
    props.dialogInfo.cancelCallback(props.dialogInfo)
  }
  emit('close-dialog')
}
</script>

<template>
  <div>
    <q-dialog persistent :modelValue="props.dialogInfo.isDisplay" transition-show="scale" transition-hide="scale">
      <q-card class="card-size">
        <div class="q-pa-md">
          <q-card-section>

            <!-- １．横断カタログと紐づく詳細カタログ作成 -->
            <div v-if="props.dialogInfo.type === 'create-catalog-detail-link-release'" class="text-center message-area">
              <font size=3>
                横断カタログ：&ensp;
                <span class="bold-font">{{ props.dialogInfo.options.catalogTitle }}</span>
                &ensp;に紐づく詳細カタログを作成します。よろしいですか？
              </font>
            </div>

            <!-- ２．横断カタログの情報を元に、新規で横断カタログ作成 -->
            <div v-if="props.dialogInfo.type === 'create-catalog-release-from-release'" class="text-center message-area">
              <font size=3>
                横断カタログ：&ensp;
                <span class="bold-font">{{ props.dialogInfo.options.catalogTitle }}</span>
                &ensp;の入力情報を元に、新規に別の横断カタログを作成します。よろしいですか？
              </font>
            </div>

            <!-- ３．横断カタログの情報を元に、新規で詳細カタログ作成 -->
            <div v-if="props.dialogInfo.type === 'create-catalog-detail-from-release'" class="text-center message-area">
              <font size=3>
                横断カタログ：&ensp;
                <span class="bold-font">{{ props.dialogInfo.options.catalogTitle }}</span>
                &ensp;の入力情報を元に、新規に別の詳細カタログを作成します。よろしいですか？
              </font>
            </div>

            <!-- ４．横断カタログの情報を元に、新規で横断カタログと詳細カタログを作成 -->
            <div v-if="props.dialogInfo.type === 'create-catalog-both-from-release'" class="text-center message-area">
              <font size=3>
                横断カタログ：&ensp;
                <span class="bold-font">{{ props.dialogInfo.options.catalogTitle }}</span>
                &ensp;の入力情報を元に、新規に別の横断カタログと詳細カタログを作成します。よろしいですか？
              </font>
            </div>

            <!-- ５．詳細カタログと紐づく横断カタログ作成 -->
            <div v-if="props.dialogInfo.type === 'create-catalog-release-link-detail'" class="text-center message-area">
              <font size=3>
                詳細カタログ：&ensp;
                <span class="bold-font">{{ props.dialogInfo.options.catalogTitle }}</span>
                &ensp;に紐づく横断カタログを作成します。よろしいですか？
              </font>
            </div>

            <!-- ６．詳細カタログの情報を元に、新規で横断カタログ作成 -->
            <div v-if="props.dialogInfo.type === 'create-catalog-release-from-detail'" class="text-center message-area">
              <font size=3>
                詳細カタログ：&ensp;
                <span class="bold-font">{{ props.dialogInfo.options.catalogTitle }}</span>
                &ensp;の入力情報を元に、新規に別の横断カタログを作成します。よろしいですか？
              </font>
            </div>

            <!-- ７．詳細カタログの情報を元に、新規で詳細カタログ作成 -->
            <div v-if="props.dialogInfo.type === 'create-catalog-detail-from-detail'" class="text-center message-area">
              <font size=3>
                詳細カタログ：&ensp;
                <span class="bold-font">{{ props.dialogInfo.options.catalogTitle }}</span>
                &ensp;の入力情報を元に、新規に別の詳細カタログを作成します。よろしいですか？
              </font>
            </div>

            <!-- ８．詳細カタログの情報を元に、新規で横断カタログと詳細カタログを作成 -->
            <div v-if="props.dialogInfo.type === 'create-catalog-both-from-detail'" class="text-center message-area">
              <font size=3>
                詳細カタログ：&ensp;
                <span class="bold-font">{{ props.dialogInfo.options.catalogTitle }}</span>
                &ensp;の入力情報を元に、新規に別の横断カタログと詳細カタログを作成します。よろしいですか？
              </font>
            </div>

            <!-- 横断カタログ編集 -->
            <div v-if="props.dialogInfo.type === 'edit-catalog-release'" class="text-center message-area">
              <font size=3>
                横断カタログ：&ensp;
                <span class="bold-font">{{ props.dialogInfo.options.catalogTitle }}</span>
                &ensp;を編集します。よろしいですか？
              </font>
            </div>

            <!-- 詳細カタログ編集 -->
            <div v-if="props.dialogInfo.type === 'edit-catalog-detail'" class="text-center message-area">
              <font size=3>
                詳細カタログ：&ensp;
                <span class="bold-font">{{ props.dialogInfo.options.catalogTitle }}</span>
                &ensp;を編集します。よろしいですか？
              </font>
            </div>

            <!-- 編集中にページを離れる際の確認ダイアログ -->
            <div v-if="props.dialogInfo.type === 'confirm-discard'" class="text-center message-area">
              <font size=3>現在入力している情報はクリアされますがよろしいですか。</font>
            </div>

            <div class="q-gutter-md row justify-center q-mt-sm">
              <q-btn v-close-popup outline color="black" class="col" label="キャンセル" @click="onCancel()"></q-btn>
              <q-btn v-close-popup unelevated color="primary" class="col" label="決定" @click="onConfirm()"></q-btn>
            </div>
          </q-card-section>
        </div>
      </q-card>
    </q-dialog>
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

