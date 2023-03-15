<script setup>
import { config } from'boot/config'
import { reactive, onBeforeUnmount, onMounted, watch } from 'vue'
import axios from 'axios'
import { exportFile } from 'quasar'
import CompleteDialog from '../components/dialog/CompleteDialog.vue'
import { useStore } from '../stores/store'

const store = useStore()
const intervalId = undefined
const attr = reactive({
  exportCkanType: 'release',
  dialog: {
    isDisplay: false,
    message: '',
    errorFlg: false
  },
  downloadBtnDisable: true
})

// method
async function startExportFile() {
  var postData = {
    rows: 0,
    start: 1000
  }
  axios
    .post(config.apiPrefix + '/export/' + attr.exportCkanType, postData)
    .then(async res => {
      console.log(res)
      if (res.status === 200) {
        attr.dialog.isDisplay = true
        attr.dialog.message = 'エクスポート処理を開始しました。'
        attr.dialog.errorFlg = false
      } else {
        attr.dialog.isDisplay = true
        attr.dialog.message = 'エクスポート処理を開始できませんでした。'
        attr.dialog.errorFlg = true
      }
    })
    .catch(err => {
      console.log('error message:', err.response.data.message)
      attr.dialog.isDisplay = true
      attr.dialog.message = err.response.data.message || 'エクスポートに失敗しました。\n管理者に問い合わせてください。'
      attr.dialog.errorFlg = true
    })
}

async function downloadFile() {
  // エクスポートボタンを無効
  attr.downloadBtnDisable = true
  // ダウンロード処理
  try {
    const res = await axios.get(config.apiPrefix + '/export' + '/' + 'file' + '/' + attr.exportCkanType, { responseType: 'blob' })
    var fileName = getFileName(res.headers['content-disposition'])
    const status = exportFile(fileName, res.data, 'application/gzip')
    if (status === true) {
      attr.downloadBtnDisable = false
      attr.dialog.isDisplay = true
      attr.dialog.message = 'ダウンロードが完了しました。'
      attr.dialog.errorFlg = false
    } else {
      attr.downloadBtnDisable = false
      attr.dialog.isDisplay = true
      attr.dialog.message = 'ダウンロードができませんでした。'
      attr.dialog.errorFlg = true
    }
  } catch (err) {
    attr.downloadBtnDisable = false
    attr.dialog.isDisplay = true
    attr.dialog.message = 'ダウンロードができませんでした。'
    attr.dialog.errorFlg = true
  }
}

function getFileName(disposition) {
  const utf8FilenameRegex = /filename\*=UTF-8''([\w%\-.]+)(?:; |$)/
  const asciiFilenameRegex = /filename=(["']?)(.*?[^\\])\1(?:; |$)/
  let fileName = null
  if (utf8FilenameRegex.test(disposition)) {
    fileName = decodeURIComponent(utf8FilenameRegex.exec(disposition)[1])
  } else {
    const matches = asciiFilenameRegex.exec(disposition)
    if (matches != null && matches[2]) {
      fileName = matches[2]
    }
  }
  return fileName
}

function checkExportStatus() {
  attr.intervalId = setInterval(async function () {
    // エクスポート状況取得
    const res = await axios.post(config.apiPrefix + '/export/status', {ckan_type: attr.exportCkanType})
    if (res.data.status === 'available') {
      // ダウンロードボタンを有効
      attr.downloadBtnDisable = false
    } else {
      attr.downloadBtnDisable = true
    }
  }, 10000)
}

// mounted
onMounted(function(){
  console.log('-- Export.vue onMounted --')
  attr.intervalId = setInterval(async function () {
    // エクスポート状況取得
    const res = await axios.post(config.apiPrefix + '/export/status', {ckan_type: attr.exportCkanType})
    if (res.data.status === 'available') {
      // ダウンロードボタンを有効
      attr.downloadBtnDisable = false
    } else {
      attr.downloadBtnDisable = true
    }
  }, 10000)
})

// watch
watch(() => attr.exportCkanType,
  (newVal) => {
    axios.post(config.apiPrefix + '/export/status', {ckan_type: attr.exportCkanType})
    .then(res => {
      if (res.data.status === 'available') {
        // ダウンロードボタンを有効
        attr.downloadBtnDisable = false
      } else {
        attr.downloadBtnDisable = true
      }
    })
})

// beforeDestroy
onBeforeUnmount(function(){
  console.log('-- Export.vue onBeforeUnmount --')
  
  clearInterval(attr.intervalId)
})

</script>

<template>
  <div class="col-6">
    <q-card class="q-card-background-white">
      <q-card-section>
        <div class="col">
          <div class="q-mb-md row items-center">
            <div class="col-4">
              <font size='3' color='#1d468f'>エクスポート対象CKAN</font>
            </div>
            <div class="col-8 flex justify-start">
              <q-radio
                v-model="attr.exportCkanType"
                val="release"
                label="横断検索用CKAN"
                color="light-blue-10"
              />
              <div v-if="store.loginInfo.detailCkanAddr">
                <q-radio
                  v-model="attr.exportCkanType"
                  val="detail"
                  label="詳細検索用CKAN"
                  style="margin-left: 16px"
                  color="light-blue-10"
                />
              </div>
            </div>
          </div>
          <div class="flex justify-center content-center">
            <q-btn label="エクスポート" color="primary" @click="startExportFile()" />
            <q-btn label="ダウンロード" color="primary" @click="downloadFile()" :disable="attr.downloadBtnDisable" style="margin-left: 15px;" />
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
.q-card-background-white{
  background: white;
}

.background-whitesmoke{
  background: #f5f5f5;
}
</style>
