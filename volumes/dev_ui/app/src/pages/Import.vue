<script setup>
import { config } from'boot/config'
import { reactive, computed, ref } from 'vue'
import CompleteDialog from '../components/dialog/CompleteDialog.vue'
import { useStore } from '../stores/store'
import axios from 'axios'

const localFileUrl = ref('api/v1/catalog/tool/localuploads')
const localFileData = ref([])

const store = useStore()
const attr = reactive({
  dialog: {
    isDisplay: false,
    message: '',
    errorFlg: false,
  },
  importCkanType: 'releaseCkan',
  deleteCkanCheck: 'true'
})

// method
function checkImportFile() {
  if (localFileData.value.type !== 'application/x-gzip' && localFileData.value.type !== 'application/gzip') {
    attr.dialog.errorFlg = true
    attr.dialog.message = 'gz形式のファイルを選択してください。'
    attr.dialog.isDisplay = true
    return true
  } else if (localFileData.value.name.indexOf('(') !== -1 || localFileData.value.name.indexOf(')') !== -1){
    attr.dialog.errorFlg = true
    attr.dialog.message = 'ファイル名に()（括弧）を含まないファイルを選択してください。'
    attr.dialog.isDisplay = true
    return true
  } else {
    return false
  }
}

async function importFile() {
  if (checkImportFile()) return
  let importUrl = config.apiPrefix + '/import/release'
  if (attr.importCkanType === 'detailCkan') {
    importUrl = config.apiPrefix + '/import/detail'
  }
  let deleteFlg = {
    delete_ckan: attr.deleteCkanCheck
  }
  const formData = new FormData()
  let requestConfig = {
    headers: {
      'content-type': 'multipart/form-data',
    }
  }
  let data = JSON.stringify(deleteFlg)
  formData.append('data', data)
  formData.append('file', localFileData.value)
  try {
    const res = await axios.post(importUrl, formData, requestConfig)
    attr.dialog.errorFlg = false
    attr.dialog.message = 'インポートが完了しました。'
    attr.dialog.isDisplay = true
  } catch (err) {
    console.log('error message:', err.response.data.message)
    attr.dialog.isDisplay = true
    attr.dialog.message = err.response.data.message || 'インポートに失敗しました。\n管理者に問い合わせてください。'
    attr.dialog.errorFlg = true
  }
}

// 選択ファイルアップロード機能
async function uploadFactory(file) {
  localFileData.value = file[0]
  return new Promise((resolve, reject) => {
    resolve(file)
  })
}
</script>

<template>
  <div class="col-6">
    <q-card class="q-card-background-white">
      <q-card-section>
        <div class="col">
          <div class="q-mb-md row items-center">
            <div class="col-4">
              <font size='3' color='#1d468f'>インポート先CKAN</font>
            </div>
            <div class="col-8 flex justify-start">
              <q-radio
                v-model="attr.importCkanType"
                val="releaseCkan"
                label="横断検索用CKAN"
                color="light-blue-10"
              />
              <div v-if="store.loginInfo.detailCkanAddr">
                <q-radio
                  v-model="attr.importCkanType"
                  val="detailCkan"
                  label="詳細検索用CKAN"
                  style="margin-left: 16px"
                  color="light-blue-10"
                />
              </div>
            </div>
            <div class="col-4">
              <font size='3' color='#1d468f'>
                <div class="cp_tooltip">カタログ削除有無
                  <span class="cp_tooltiptext">
                    &emsp; 「削除する」を選択した場合、インポート先の<br>
                    &emsp; CKANに登録されている全カタログを削除後、<br>
                    &emsp; インポートを実行します。
                  </span>
                </div>
              </font>
            </div>
            <div class="col-8 flex justify-start">
              <q-radio
                v-model="attr.deleteCkanCheck"
                val="true"
                label="削除する"
                color="light-blue-10"
              />
              <q-radio
                v-model="attr.deleteCkanCheck"
                val="false"
                label="削除しない"
                style="margin-left: 16px"
                color="light-blue-10"
              />
            </div>
          </div>
          <div class="q-mb-md row">
            <div class="col-4">
              <font size='3' color='#1d468f'>読み込みファイル</font>
            </div>
            <div class="col-8">
              <q-uploader
                name="uploader"
                style="width: 100%;"
                field-name="file"
                :url="localFileUrl"
                @finish="importFile()"
                :factory="uploadFactory"
                max-files="1"
              >
                <template v-slot:header="scope">
                  <div class="row no-wrap items-center q-pa-sm q-gutter-xs">
                    <q-spinner v-if="scope.isUploading" class="q-uploader__spinner" />
                    <div class="col">
                      <div class="q-uploader__title">Import files</div>
                      <div class="q-uploader__subtitle">{{ scope.uploadSizeLabel }} / {{ scope.uploadProgressLabel }}</div>
                    </div>
                    <q-btn v-if="scope.canAddFiles" type="a" icon="add_box" round dense flat>
                      <q-uploader-add-trigger />
                      <q-tooltip>Add File</q-tooltip>
                    </q-btn>
                    <q-btn v-if="scope.canUpload" icon="cloud_upload" @click="scope.upload" round dense flat >
                      <q-tooltip>Import Files</q-tooltip>
                    </q-btn>
                  </div>
                </template>
              </q-uploader>
            </div>
          </div>
        </div>
      </q-card-section>
    </q-card>
    <CompleteDialog
      v-bind:dialogInfo="attr.dialog"
      @close-dialog="attr.dialog.isDisplay = false"
    />
  </div>
</template>

<style lang="scss">
.cp_tooltip {
  position: relative;
  display: inline-block;
  cursor: pointer;
  background: linear-gradient(transparent 90%, #add8e6 60%);
}
.cp_tooltip .cp_tooltiptext {
  position: absolute;
  z-index: 1;
  bottom: 100%;
  left: 0;
  visibility: hidden;
  width: auto;
  white-space: nowrap;
  padding: 0.3em 0.5em;
  transition: opacity 1s;
  text-align: left;
  opacity: 0;
  color: #ffffff;
  border-radius: 6px;
  background-color: #6495ed;
}
.cp_tooltip .cp_tooltiptext::after {
  position: absolute;
  top: 100%;
  left: 5%;
  margin-left: -5px;
  content: ' ';
  border: 5px solid transparent;
  border-top-color: #6495ed;
}
.cp_tooltip:hover .cp_tooltiptext {
  visibility: visible;
  opacity: 1;
}

.q-card-background-white{
  background: white;
}

.background-whitesmoke{
  background: #f5f5f5;
}
</style>
