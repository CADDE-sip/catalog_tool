<script setup>
import { ref, reactive} from 'vue'
import { useStore } from 'stores/store'

const store = useStore();

const props = defineProps({
  registerResult: Object
})

// 登録メッセージ
const registerResultMessage = ref('')
// エラーメッセージ
const errorMessage = ref('')

// 横断カタログ登録情報
const releaseCatalog = reactive({
  success: false,
  ckanUrl: '',
  issued: '',
  modified: '',
  id: '',
  url: '',
  resourcesList: [],
  // isNoIdResources: false,
  // noIdResources: '',
  noIdResourcesForProvenance: '',
  noIdResourcesForNonProvenance: ''

})

// 詳細カタログ登録情報
const detailCatalog = reactive({
  success: false,
  ckanUrl: '',
  issued: '',
  modified: '',
  id: '',
  url: '',
  resourcesList: [],
  // isNoIdResources: false,
  // noIdResources: '',
  noIdResourcesForProvenance: '',
  noIdResourcesForNonProvenance: ''
})

// 登録結果データ整形
function formatDisplayData(){
  if (props.registerResult.res) {
    if (String(props.registerResult.res.message) === 'success') {
      // 登録成功
      var registerData = props.registerResult.res
      registerResultMessage.value = '登録に成功しました'
      if (registerData.release && registerData.release.pkg !== null) {
        // 横断カタログ登録・更新結果整形
        var releaseData = registerData.release
        console.log('横断検索カタログ登録内容確認', releaseData)
        console.log('storeの概要情報確認', store.filedataDetails)
        releaseCatalog.success = true
        releaseCatalog.ckanUrl = releaseData.ckan_url
        releaseCatalog.issued = getExtrasValue(releaseData.pkg.extras, 'issued')
        releaseCatalog.modified = getExtrasValue(releaseData.pkg.extras, 'modified')
        releaseCatalog.id = getExtrasValue(releaseData.pkg.extras, 'identifier')
        releaseCatalog.url = getExtrasValue(releaseData.pkg.extras, 'dataset_url')
        if (releaseData.pkg && releaseData.pkg.resources.length) {
          var noResourceIDListReleaseForProvenance = []
          var noResourceIDListReleaseForNonProvenance = []
          releaseCatalog.resourcesList = releaseData.pkg.resources
          for (var reNum = 0; reNum < releaseCatalog.resourcesList.length; reNum++) {
            if (!releaseCatalog.resourcesList[reNum].name) {
              releaseCatalog.resourcesList[reNum].dispName = '(名称未設定のデータ)'
            } else {
              releaseCatalog.resourcesList[reNum].dispName = releaseCatalog.resourcesList[reNum].name
            }
            // リソース提供手段の識別子が設定されていて、交換実績記録用リソースIDが設定されていない場合は、その旨を画面に表示する
            if (releaseCatalog.resourcesList[reNum].caddec_resource_type) {
              if (!releaseCatalog.resourcesList[reNum].caddec_resource_id_for_provenance && store.filedataDetails[reNum].getResourceIDForProvenance.value === 'yes') {
                noResourceIDListReleaseForProvenance.push(releaseCatalog.resourcesList[reNum].dispName)
              } else if (!releaseCatalog.resourcesList[reNum].caddec_resource_id_for_provenance && store.filedataDetails[reNum].getResourceIDForProvenance.value === 'no') {
                noResourceIDListReleaseForNonProvenance.push(releaseCatalog.resourcesList[reNum].dispName)
              }
            }
          }
        }
        if (noResourceIDListReleaseForProvenance && noResourceIDListReleaseForProvenance.length) {
          releaseCatalog.noIdResourcesForProvenance = noResourceIDListReleaseForProvenance.join(', ')
        }
        if (noResourceIDListReleaseForNonProvenance && noResourceIDListReleaseForNonProvenance.length) {
          releaseCatalog.noIdResourcesForNonProvenance = noResourceIDListReleaseForNonProvenance.join(', ')
        }
      }
      if (registerData.detail && registerData.detail.pkg !== null) {
        // 詳細カタログ登録・更新結果整形
        var detailData = registerData.detail
        detailCatalog.success = true
        detailCatalog.ckanUrl = detailData.ckan_url
        detailCatalog.issued = getExtrasValue(detailData.pkg.extras, 'issued')
        detailCatalog.modified = getExtrasValue(detailData.pkg.extras, 'modified')
        detailCatalog.id = getExtrasValue(detailData.pkg.extras, 'identifier')
        detailCatalog.url = getExtrasValue(detailData.pkg.extras, 'dataset_url')
        if (detailData.pkg && detailData.pkg.resources.length) {
          var noResourceIDListDetailForProvenance = []
          var noResourceIDListDetailForNonProvenance = []   
          detailCatalog.resourcesList = detailData.pkg.resources
          for (var dReNum = 0; dReNum < detailCatalog.resourcesList.length; dReNum++) {
            if (!detailCatalog.resourcesList[dReNum].name) {
              detailCatalog.resourcesList[dReNum].dispName = '(名称未設定のデータ)'
            } else {
              detailCatalog.resourcesList[dReNum].dispName = detailCatalog.resourcesList[dReNum].name
            }
            // リソース提供手段の識別子が設定されていて、交換実績記録用リソースIDが設定されていない場合は、その旨を画面に表示する
            if (detailCatalog.resourcesList[dReNum].caddec_resource_type) {
              if (!detailCatalog.resourcesList[dReNum].caddec_resource_id_for_provenance && store.filedataDetails[dReNum].getResourceIDForProvenance.value === 'yes') {
                noResourceIDListDetailForProvenance.push(detailCatalog.resourcesList[dReNum].dispName)
              } else if (!detailCatalog.resourcesList[dReNum].caddec_resource_id_for_provenance && store.filedataDetails[dReNum].getResourceIDForProvenance.value === 'no') {
                noResourceIDListDetailForNonProvenance.push(detailCatalog.resourcesList[dReNum].dispName)
              }
            }
          }
        }
        if (noResourceIDListDetailForProvenance && noResourceIDListDetailForProvenance.length) {
          detailCatalog.noIdResourcesForProvenance = noResourceIDListDetailForProvenance.join(', ')
        }
        if (noResourceIDListDetailForNonProvenance && noResourceIDListDetailForNonProvenance.length) {
          detailCatalog.noIdResourcesForNonProvenance = noResourceIDListDetailForNonProvenance.join(', ')
        }
      }
    } else {
      // 登録失敗
      registerResultMessage.value = '登録に失敗しました: '
      errorMessage.value = 'エラーメッセージ:' + props.registerResult.res.message
    }
  }
}

// extrasのvalue取得
function getExtrasValue(registeredData, label){
  for (var i = 0; i < registeredData.length; i++) {
    if (registeredData[i].key === label) {
      return registeredData[i].value
    }
  }
}

// CKAN登録先遷移
function btnActionCkanLink(type){
  if (type === 'release') {
    // 横断CKANサイトへ遷移
    window.open(releaseCatalog.ckanUrl)
    } else {
    // 詳細CKANサイトへ遷移
    window.open(detailCatalog.ckanUrl)
  }
}

// created
formatDisplayData()
</script>

<template>
  <div class="dataset-regist-comp">
    <q-card class="q-ma-md q-card-background-white">
      <q-card-section>
        <div>
          <font size="5" color="#1d468f">{{registerResultMessage}}</font>
        </div>
        <div class="row">
          <div v-show="releaseCatalog.success" class="col-12">
            <div class="col q-px-lg">
              <div class="q-py-md">
                <p>以下の情報が横断カタログに追加されました。</p>
                <p><font color="#1d468f">カタログの発行日＞</font><font color="black">{{ releaseCatalog.issued }}</font></p>
                <p><font color="#1d468f">カタログの更新日または修正日＞</font><font color="black">{{ releaseCatalog.modified }}</font></p>
                <p><font color="#1d468f">カタログのID＞</font><font color="black">{{ releaseCatalog.id }}</font></p>
                <p><font color="#1d468f">カタログのURL＞</font><font color="black">{{ releaseCatalog.url }}</font></p>
              </div>
              <div v-if="releaseCatalog.resourcesList.length" class="q-py-md indent-item">
                <p>以下の情報が横断カタログのリソースデータとして追加されました。</p>
                <div v-for="resourceData in releaseCatalog.resourcesList" :key="resourceData.dispName" class="q-py-xs">
                  <p><font color="#1d468f">{{ resourceData.dispName }}</font></p>
                  <p><font color="#1d468f">配信の発行日＞</font><font color="black">{{ resourceData.issued }}</font></p>
                  <p><font color="#1d468f">配信の変更日＞</font><font color="black">{{ resourceData.modified }}</font></p>
                  <p><font color="#1d468f">交換実績記録用リソースID＞</font><font color="black">{{ resourceData.caddec_resource_id_for_provenance }}</font></p>
                </div>
              </div>
              <div v-if="releaseCatalog.noIdResourcesForProvenance" class="indent-item">
                <p><font color="red">
                以下のデータ交換実績記録用リソースIDが未発行です。<br>
                来歴登録時にエラーが発生しました。<br>
                管理者に問い合わせてください。
                </font></p>
                <p><font color="red">{{ releaseCatalog.noIdResourcesForProvenance }}</font></p>
              </div>
              <br>
              <div v-if="releaseCatalog.noIdResourcesForNonProvenance" class="indent-item">
                <p><font color="red">
                来歴登録を行わなかったかったため、以下のデータ交換実績記録用リソースIDは未発行です。<br>
                データ交換実績記録用リソースIDを払い出す場合は、概要情報を更新してください。
                </font></p>
                <p><font color="red">{{ releaseCatalog.noIdResourcesForNonProvenance }}</font></p>
              </div>
              <div v-if="releaseCatalog.success" class="q-pt-md">
                <q-btn
                  size="lg"
                  outline
                  label="横断カタログ登録先へ移動"
                  dense
                  @click="btnActionCkanLink('release')"
                  color="light-blue-10"
                />
                <br>
                <br>
              </div>
              <div v-if!="releaseCatalog.success">
                <p>{{errorMessage}}</p>
              </div>
            </div>
          </div>
          <div v-show="detailCatalog.success" class="col-12">
            <div class="col q-px-lg">
              <div class="q-py-md">
                <p>以下の情報が詳細カタログに追加されました。</p>
                <p><font color="#1d468f">カタログの発行日＞</font><font color="black">{{ detailCatalog.issued }}</font></p>
                <p><font color="#1d468f">カタログの更新日または修正日＞</font><font color="black">{{ detailCatalog.modified }}</font></p>
                <p><font color="#1d468f">カタログのID＞</font><font color="black">{{ detailCatalog.id }}</font></p>
                <p><font color="#1d468f">カタログのURL＞</font><font color="black">{{ detailCatalog.url }}</font></p>
              </div>
              <div v-if="detailCatalog.resourcesList.length" class="q-py-md indent-item">
                <p>以下の情報が詳細カタログのリソースデータとして追加されました。</p>
                <div v-for="resourceData in detailCatalog.resourcesList" :key="resourceData.dispName" class="q-py-xs">
                  <p><font color="#1d468f">{{ resourceData.dispName }}</font></p>
                  <p><font color="#1d468f">配信の発行日＞</font><font color="black">{{ resourceData.issued }}</font></p>
                  <p><font color="#1d468f">配信の変更日＞</font><font color="black">{{ resourceData.modified }}</font></p>
                  <p><font color="#1d468f">交換実績記録用リソースID＞</font><font color="black">{{ resourceData.caddec_resource_id_for_provenance }}</font></p>
                </div>
              </div>
              <div v-if="detailCatalog.noIdResourcesForProvenance" class="indent-item">
                <p><font color="red">
                以下のデータ交換実績記録用リソースIDが未発行です。<br>
                来歴登録時にエラーが発生しました。<br>
                管理者に問い合わせてください。
                </font></p>
                <p><font color="red">{{ detailCatalog.noIdResourcesForProvenance }}</font></p>
              </div>
              <br>
              <div v-if="detailCatalog.noIdResourcesForNonProvenance" class="indent-item">
                <p><font color="red">
                来歴登録を行わなかったかったため、以下のデータ交換実績記録用リソースIDは未発行です。<br>
                データ交換実績記録用リソースIDを払い出す場合は、概要情報を更新してください。
                </font></p>
                <p><font color="red">{{ detailCatalog.noIdResourcesForNonProvenance }}</font></p>
              </div>
              <div v-show="detailCatalog.success" class="q-pt-md">
                <q-btn
                  size="lg"
                  outline
                  label="詳細カタログ登録先へ移動"
                  dense
                  @click="btnActionCkanLink('detail')"
                  color="light-blue-10"
                />
                <br>
                <br>
              </div>
              <div v-if!="detailCatalog.success">
                <p>{{errorMessage}}</p>
              </div>
            </div>
          </div>
        </div>
      </q-card-section>
    </q-card>
  </div>
</template>

<style lang="scss">
.q-card-background-white{
  background:white
}

.dataset-regist-comp .indent-item{
 overflow-wrap: break-word;
}
</style>
