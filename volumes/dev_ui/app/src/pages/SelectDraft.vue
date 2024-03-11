
<script setup>
import { config } from'boot/config'
import { ref, reactive, onMounted, watch } from 'vue'
import axios from 'axios'
import DeleteDialog from '../components/dialog/DeleteDialog.vue'
import CompleteDialog from '../components/dialog/CompleteDialog.vue'
import { useStore } from '../stores/store'
import { useRouter, isNavigationFailure } from 'vue-router'

const store = useStore()
const router = useRouter()

var tmpDataList = []
const selected = ref([])
const attr = reactive({
  columns: [
    { name: 'fileName', align: 'left', label: 'ファイル名', sortable: true, field: 'fileName' },
    { name: 'ckanInfo', align: 'left', label: '登録先CKAN', sortable: true, field: 'ckanInfo' },
    { name: 'saved', align: 'left', label: '保存日', sortable: true, field: 'saved' },
    { name: 'restart', align: 'left', field: 'restart' },
    { name: 'delete', align: 'left', field: 'delete' }
  ],
  tableData: [],
  noSelectedCatalog: true,
  deleteDialog: {
    pageName: '',
    isDisplay: false,
    catalogName: ''
  },
  completeDialog: {
    isDisplay: false,
    message: '',
    errorFlg: false
  }
})

// mounted
onMounted(function(){
  console.log('-- SelectDraft.vue onMounted --')

  axios
    .get(config.apiPrefix + '/temporal')
    .then(async res => {
      tmpDataList = res.data
      // 保存日を降順にソート
      tmpDataList.sort((a, b) => b.tmpFile.saved - a.tmpFile.saved)
      for (var i = 0; i < tmpDataList.length; i++) {
        var tmpSaved = tmpDataList[i].tmpFile.saved
        var dispSaved = tmpSaved.slice(0, 4) + '/' + tmpSaved.slice(4, 6) + '/' + tmpSaved.slice(6, 8) + ' ' + tmpSaved.slice(8, 10) + ':' + tmpSaved.slice(10, 12) + ':' + tmpSaved.slice(12, 14)
        var dispData = {
          fileName: tmpDataList[i].tmpFile.tmp_file_name,
          ckanInfo: tmpDataList[i].tmpFile.ckan_info,
          saved: dispSaved
        }
        attr.tableData.push(dispData)
      }
    })
    .catch(err => {
      console.log('error message:', err.response.data.message)
      attr.completeDialog.isDisplay = true
      attr.completeDialog.message = err.response.data.message || '一時保存データ取得に失敗しました。\n管理者に問い合わせてください。'
      attr.completeDialog.errorFlg = true
    })
})

function commitDatasetinfo(data) {
  store.updateDatasetinfo({
      catalogTitle: data.title,
      catalogDescription: data.notes,
      datasetDescriptionUrl: data.url,
      datasetIdForDetail: data.caddec_dataset_id_for_detail,
      registOrg: data.regist_org,
      publisherId: data.caddec_provider_id,
      publisher: data.publisher_name,
      publisherUri: data.publisher_uri,
      creator: data.creator_name,
      creatorUrl: data.creator_url,
      contactPoint: data.contact_name,
      contactPointUrl: data.contact_url,
      storeType: 'state'
    })
}

function commitDatajacket(data) {
  var registedFiledataDetails = []
  if (data.length) {
    for (var i = 0; i < data.length; i++) {
      // 配信のラベル（画面タブの表示値）
      var label = data[i].label || ''

      // 入力支援
      // 配信の取得方法
      var inputSupportResourceType = data[i].inputSupportResourceType || ''
      // 配信の取得先URL
      var inputSupportUrl = data[i].inputSupportUrl || ''
      // NGSIテナント
      var inputSupportNgsiTenant = data[i].inputSupportNgsiTenant || ''
      // NGSIサービスパス
      var inputSupportNgsiServicePath = data[i].inputSupportNgsiServicePath || ''
      // 配信の取得成否フラグ
      var inputSupportIsRequestSuccess = data[i].inputSupportIsRequestSuccess || false
      // 配信リソース名（リソース取得・保存時にwebサーバから付与）
      var dataName = data[i].dataname || ''

      // 配信情報
      // リソース提供手段の識別子
      var resourceType = data[i].resourceType
      // 配信のダウンロードURL
      var downloadUrl = data[i].downloadUrl || ''
      // 配信の情報提供ページURL
      var explainurl = data[i].explainurl || ''
      // 配信の名称
      var filename = data[i].filename || ''
      // 配信の説明
      var description = data[i].description || ''
      // 配信のバイトサイズ
      var size = data[i].size || ''
      // ファイルのカラム名
      var columnName = data[i].columnName || ''
      // 配信のメディアタイプ
      var mimetype = data[i].mimetype || ''
      // 配信のファイル形式
      var format = data[i].format || ''
      // 配信の圧縮形式
      var compressFormat = {
        label: data[i].compressFormat.label || '',
        value: data[i].compressFormat.value || ''
      }
      var compressFormatOther = data[i].compressFormatOther || ''
      // 配信のパッケージ形式
      var packageFormat = {
        label: data[i].packageFormat.label || '',
        value: data[i].packageFormat.value || ''
      }
      var packageFormatOther = data[i].packageFormatOther || ''
      // スキーマ
      var schema = data[i].schema || ''
      // スキーマタイプ
      var schemaType = data[i].schemaType || ''
      // NGSIデータ種別
      var ngsiEntityType = data[i].ngsiEntityType || ''
      // NGSIテナント
      var ngsiTenant = data[i].ngsiTenant || ''
      // NGSIサービスパス
      var ngsiServicePath = data[i].ngsiServicePath || ''
      // NGSIデータモデル
      var ngsiDataModel = data[i].ngsiDataModel || ''
      // 契約確認の要否
      var contractRequired = data[i].contractRequired
      // コネクタ利用の要否
      var connectRequired = data[i].connectRequired
      // 来歴登録の有無
      var getResourceIdForProvenance = data[i].getResourceIDForProvenance || ''
      // 交換実績記録用リソースID
      var resourceIdForProvenance = data[i].resourceIDForProvenance || ''
      // 前段イベント識別子
      var previousEventId = data[i].previousEventId || ''
      // 来歴登録済みの配信のダウンロードURL
      var urlForProvenance = data[i].urlForProvenance || ''
      // 来歴登録済みのCADDEユーザID
      var caddeUserId = data[i].caddeUserId || ''
      // データサービスのタイトル
      var dataServiceTitle = data[i].dataServiceTitle || ''
      // データサービスのエンドポイント
      var dataServiceEndpointUrl = data[i].dataServiceEndpointUrl || ''
      // データサービスのエンドポイントの定義
      var dataServiceEndpointDescription = data[i].dataServiceEndpointDescription || ''

      // 配信のライセンス
      var resourceLicenseTitle = data[i].license_title || ''
      // 配信のライセンス（URL)
      var resourceLicenseUrl = data[i].licenseurl || ''
      // 配信の発行日
      var issued = data[i].issued || ''
      // 配信のID
      var id = data[i].id || ''

      registedFiledataDetails.push({
        label: label,
        inputSupportResourceType: inputSupportResourceType,
        inputSupportUrl: inputSupportUrl,
        inputSupportNgsiTenant: inputSupportNgsiTenant,
        inputSupportNgsiServicePath: inputSupportNgsiServicePath,
        inputSupportIsRequestSuccess: inputSupportIsRequestSuccess,
        dataName: dataName,
        resourceType: resourceType,
        downloadUrl: downloadUrl,
        explainurl: explainurl,
        filename: filename,
        description: description,
        size: size,
        columnName: columnName,
        mimetype: mimetype,
        format: format,
        compressFormat: compressFormat,
        compressFormatOther: compressFormatOther,
        packageFormat: packageFormat,
        packageFormatOther: packageFormatOther,
        schema: schema,
        schemaType: schemaType,
        ngsiEntityType: ngsiEntityType,
        ngsiTenant: ngsiTenant,
        ngsiServicePath: ngsiServicePath,
        ngsiDataModel: ngsiDataModel,
        contractRequired: contractRequired,
        connectRequired: connectRequired,
        getResourceIDForProvenance: getResourceIdForProvenance,
        resourceIDForProvenance: resourceIdForProvenance,
        previousEventId: previousEventId,
        urlForProvenance: urlForProvenance,
        caddeUserId: caddeUserId,
        dataServiceTitle: dataServiceTitle,
        dataServiceEndpointUrl: dataServiceEndpointUrl,
        dataServiceEndpointDescription: dataServiceEndpointDescription,
        licensetitle: resourceLicenseTitle,
        licenseurl: resourceLicenseUrl,
        issued: issued,
        id: id
      })
    }
  }
  store.updateFiledataDetails({
      filedataDetails: registedFiledataDetails,
      storeType: 'state'
    }
  )
}

function commitDatasetoptionalinfo(data) {
  store.updateDatasetOptionalInfoParameters({
      selectThemes: data.theme,
      selectTags: data.tags,
      vocabulary: data.vocabulary,
      term: data.term,
      selectLanguage: data.language,
      frequency: data.frequency,
      spatialUrl: data.spatial_url,
      spatialName: data.spatial_text,
      spatial: data.spatial,
      start: data.temporal_start,
      end: data.temporal_end,
      storeType: 'state'
    }
  )
}

function commitUserterms(data) {
  store.updateUserTerms({
      termName: data.license_title,
      termNameUrl: data.license_url,
      usrRight: data.rights,
      accessRights: data.access_rights,
      accessRightsUrl: data.access_rights_url,
      haspolicyUrl: data.haspolicy_url,
      provWasGeneratedByUrl: data.prov_was_generated_by_url,
      conformsTo: data.conforms_to,
      contractType: data.trading_policy_contract_type,
      secrecy: data.trading_policy_nda,
      useApplication: data.trading_policy_use_application,
      useApplicationOther: data.trading_policy_use_application_free,
      scopeOfDisclosure: data.scope_of_disclosure,
      scopeOfDisclosureOther: data.scope_of_disclosure_free,
      permissionResion: data.terms_of_use_permissible_region,
      permissionResionOther: data.terms_of_use_permissible_region_free,
      notices: data.terms_of_use_notices,
      personalData: data.privacy_policy_contains_personal_data,
      personalDataOther: data.privacy_policy_contains_personal_data_free,
      dataEffectivePeriodSelectTerms: data.data_effective_period_term,
      startDate: data.data_effective_period_start,
      endDate: data.data_effective_period_end,
      dataEffectivePeriodFreefield: data.data_effective_period_free,
      usageLicensePeriodSelectTerms: data.usage_license_period_term,
      deadline: data.usage_license_period_deadline,
      period: data.usage_license_period_period,
      unit: data.usage_license_period_unit,
      usageLicensePeriodFreefield: data.usage_license_period_free,
      fee: data.fee,
      salesInfoUrl: data.sales_info_url,
      priceRange: data.pricing_price_range,
      noticesOfPrice: data.pricing_notices_of_price,
      expressWarranty: data.warranty_express_warranty,
      expressWarrantyOther: data.warranty_express_warranty_free,
      leagalCompliance: data.warranty_legal_compliance,
      leagalComplianceOther: data.warranty_legal_compliance_free,
      storeType: 'state'
    })
}

function commitDataForUpdate(tmpData) {
  store.updateCkanName({
      ckanDataName: tmpData.ckan_data_name
    })
  store.updateAutoSetValue({
      issued: tmpData.issued,
      identifier: tmpData.identifier,
      datasetUrl: tmpData.dataset_url
    })
}

function editRow(tmpData) {
  var restartData = ''
  for (var i = 0; i < tmpDataList.length; i++) {
    if (tmpData.row.fileName === tmpDataList[i].tmpFile.tmp_file_name) {
      restartData = tmpDataList[i]
      break
    }
  }
  commitDatasetinfo(restartData.datasetinfo)
  commitDatajacket(restartData.datajacket)
  commitDatasetoptionalinfo(restartData.datasetoptionalinfo)
  commitUserterms(restartData.userterms)
  commitDataForUpdate(restartData.dataForUpdate)
  router.push('/register').then(failure => {
    if (!isNavigationFailure(failure)) {
      console.log('editRow-------------------')
      console.log(tmpData.row.ckanInfo)
      store.updateMode({ mode: tmpData.row.ckanInfo, ckanType: '', isBothCatalog: false })
    }
  })
}

// カタログ一括削除確認ダイアログ表示
function btnConfirmSelectedDelete() {
  attr.deleteDialog.pageName = 'selectDraftSelectedDelete'
  attr.deleteDialog.isDisplay = true
}

// カタログ一件削除確認ダイアログ表示
function btnConfirmOneDelete(props) {
  attr.deleteDialog.pageName = 'selectDraftOneDelete'
  attr.deleteDialog.isDisplay = true
  attr.deleteDialog.catalogName = props.row.fileName
}

function deleteRow(filename) {
  var deleteFileList = []
  deleteFileList.push(filename)
  axios
    .request({ method: 'delete', url: config.apiPrefix + '/temporal', data: deleteFileList })
    .then(async res => {
      var deleteRes = res.data.del_data
      if (deleteRes.length) {
        for (var i = 0; i < attr.tableData.length; i++) {
          for (var j = 0; j < deleteRes.length; j++) {
            if (attr.tableData[i].fileName === deleteRes[j]) {
              attr.tableData.splice(i, 1)
            }
          }
        }
      }
      selected.value = []
      attr.deleteDialog.isDisplay = false
    })
    .catch(err => {
      console.log('error message:', err.response.data.message)
      attr.completeDialog.isDisplay = true
      attr.completeDialog.message = err.response.data.message || '一時保存データ削除に失敗しました。\n管理者に問い合わせてください。'
      attr.completeDialog.errorFlg = true
    })
}

function deleteSelectedRows() {
  var i = 0
  var deleteFileList = []
  for (i = 0; i < selected.value.length; i++) {
    deleteFileList.push(selected.value[i].fileName)
  }
  axios
    .request({ method: 'delete', url: config.apiPrefix + '/temporal', data: deleteFileList })
    .then(async res => {
      var deleteRes = res.data.del_data
      if (deleteRes.length) {
        for (var i = 0; i < attr.tableData.length; i++) {
          for (var j = 0; j < deleteRes.length; j++) {
            if (attr.tableData[i].fileName === deleteRes[j]) {
              attr.tableData.splice(i, 1)
            }
          }
        }
      }
      selected.value = []
      attr.deleteDialog.isDisplay = false
    })
    .catch(err => {
      console.log('error message:', err.response.data.message)
      attr.completeDialog.isDisplay = true
      attr.completeDialog.message = err.response.data.message || '一時保存データ削除に失敗しました。\n管理者に問い合わせてください。'
      attr.completeDialog.errorFlg = true
    })
}

// watch
watch(() => attr.tableData,
  (newReg, oldReg) => {
  attr.tableData = newReg
})

watch(() => selected.value,
  (newVal) => {
  if (newVal.length) {
    attr.noSelectedCatalog = false
  } else {
    attr.noSelectedCatalog = true
  }
})
</script>

<template>
  <div class="col-12 q-layout-padding flex justify-center content-center">
    <q-card class="q-card-background-white" style="width: 100%;">
      <q-card-section>
        <div class="col-sm-10 offset-sm-1 text-center">
          <q-table
            :columns="attr.columns"
            :rows="attr.tableData"
            v-model:selected="selected"
            selection="multiple"
            row-key="fileName"
            separator="cell"
            no-data-label="一時保存されているデータがありません"
            class="temporarySavedDataTable"
          >
            <template v-slot:top>
              <div class="q-table__title text-weight-bolder">
                <font size="5" color="#1d468f">一時保存データ一覧</font>
              </div>
              <q-space />
              <q-btn
                style="width: 12%;"
                outline
                color="red"
                @click="btnConfirmSelectedDelete()"
                :disable="attr.noSelectedCatalog"
                icon="delete"
                label="削除"
              />
            </template>
            <template v-slot:body-cell-saved="props">
              <q-td key="fileName" :props="props" class="btn-cell">{{ props.row.saved }}</q-td>
            </template>
            <template v-slot:body-cell-ckanInfo="props">
              <q-td key="ckanInfo" :props="props" class="btn-cell">
                <span v-if="props.row.ckanInfo === 'new_release_register'">横断検索用CKAN</span>
                <span v-if="props.row.ckanInfo === 'new_detail_register'">詳細検索用CKAN</span>
                <span v-if="props.row.ckanInfo === 'new_both_register'">横断・詳細検索用CKAN</span>
              </q-td>
            </template>
            <template v-slot:body-cell-restart="props">
              <q-td class="btn-cell">
                <q-btn outline color="secondary" class="full-width" @click="editRow(props)" label="再開" icon="edit" field='restart'></q-btn>
              </q-td>
            </template>
            <template v-slot:body-cell-delete="props">
              <q-td class="btn-cell">
                <q-btn outline color="red" class="full-width" @click="btnConfirmOneDelete(props)" label="削除" icon="delete" field='delete'></q-btn>
              </q-td>
            </template>
          </q-table>
        </div>

        <!-- 削除ダイアログ -->
        <DeleteDialog
          v-bind:dialogInfo="attr.deleteDialog"
          @delete-one-catalog-data="deleteRow"
          @delete-selected-catalog-data="deleteSelectedRows"
          @close-dialog="attr.deleteDialog.isDisplay = false"
        />

        <!-- 完了ダイアログ -->
        <CompleteDialog
          v-bind:dialogInfo="attr.completeDialog"
          @close-dialog="attr.completeDialog.isDisplay = false, attr.deleteDialog.isDisplay = false"
        />

      </q-card-section>
    </q-card>
  </div>
</template>

<style lang="scss">
.q-card-background-white{
  background: white;
}

.btn-cell{
  width: 15%;
}

.temporarySavedDataTable .q-table__top, .temporarySavedDataTable .q-table__bottom, .temporarySavedDataTable thead tr:first-child th{
  background-color: rgba(25, 118, 210, 0.1)
}
</style>
