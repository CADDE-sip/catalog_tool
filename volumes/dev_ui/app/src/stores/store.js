import { defineStore } from 'pinia';

// カタログ項目のフィールド名と初期値
const CATALOG_ITEM_LIST = [
  { key: 'dispGroupList', value: [], type: 'list' },
  { key: 'catalogTitle', value: '', type: 'string' },
  { key: 'catalogDescription', value: '', type: 'string' },
  { key: 'datasetDescriptionUrl', value: '', type: 'string' },
  { key: 'datasetIdForDetail', value: '', type: 'string' },
  { key: 'registOrg', value: '', type: 'string' },
  { key: 'publisherId', value: '', type: 'string' },
  { key: 'publisher', value: '', type: 'string' },
  { key: 'publisherUri', value: '', type: 'string' },
  { key: 'creator', value: '', type: 'string' },
  { key: 'creatorUrl', value: '', type: 'string' },
  { key: 'contactPoint', value: '', type: 'string' },
  { key: 'contactPointUrl', value: '', type: 'string' },
  { key: 'filedataDetails', value: [], type: 'list' },
  { key: 'selectThemes', value: '', type: 'list' },
  { key: 'selectTags', value: '', type: 'list' },
  { key: 'vocabulary', value: '', type: 'string' },
  { key: 'term', value: '', type: 'string' },
  { key: 'selectLanguage', value: [], type: 'list' },
  { key: 'frequency', value: '', type: 'string' },
  { key: 'dataCalender', value: { start: '', end: '' }, type: 'object' },
  { key: 'geonames', value: { spatialUrl: '', spatialName: '', spatial: '' }, type: 'object' },
  { key: 'termName', value: '', type: 'string' },
  { key: 'termNameUrl', value: '', type: 'string' },
  { key: 'usrRight', value: '', type: 'string' },
  { key: 'accessRights', value: '', type: 'string' },
  { key: 'accessRightsUrl', value: '', type: 'string' },
  { key: 'haspolicyUrl', value: '', type: 'string' },
  { key: 'provWasGeneratedByUrl', value: '', type: 'string' },
  { key: 'conformsTo', value: '', type: 'string' },
  { key: 'contractType', value: '', type: 'string' },
  { key: 'secrecy', value: '', type: 'string' },
  { key: 'useApplication', value: [], type: 'list' },
  { key: 'useApplicationOther', value: '', type: 'string' },
  { key: 'scopeOfDisclosure', value: '', type: 'string' },
  { key: 'scopeOfDisclosureOther', value: '', type: 'string' },
  { key: 'permissionResion', value: [], type: 'list' },
  { key: 'permissionResionOther', value: '', type: 'string' },
  { key: 'notices', value: '', type: 'string' },
  { key: 'personalData', value: '', type: 'string' },
  { key: 'personalDataOther', value: '', type: 'string' },
  { key: 'dataEffectivePeriod', value: { selectTerms: '', startDate: '', endDate: '', freefield: '' }, type: 'object' },
  { key: 'usageLicensePeriod', value: { selectTerms: '', deadline: '', period: '', unit: '', freefield: '' }, type: 'object' },
  { key: 'fee', value: '', type: 'string' },
  { key: 'priceRange', value: '', type: 'string' },
  { key: 'salesInfoUrl', value: '', type: 'string' },
  { key: 'noticesOfPrice', value: '', type: 'string' },
  { key: 'expressWarranty', value: '', type: 'string' },
  { key: 'expressWarrantyOther', value: '', type: 'string' },
  { key: 'leagalCompliance', value: [], type: 'list' },
  { key: 'leagalComplianceOther', value: '', type: 'string' },
  { key: 'groups', value: [], type: 'list' }
]

export const useStore = defineStore('store', {
  state: () => ({
    releaseCkanDataName: '',
    detailCkanDataName: '',
    // サーバの自動設定値
    issued: '',
    identifier: '',
    datasetUrl: '',
    // ログインパラメータ
    loginInfo: {
      sysadmin: false,
      username: '',
      caddeUserId: '',
      caddeUserIdList: [],
      releaseCkanAddr: '',
      detailCkanAddr: '',
      ckan: ''
    },
    authInfo: {
      // 認証情報パラメータ
      keycloakState: '',
      keycloakCode: ''
    },
    // ログインCKANカタログパラメータ
    catalogInfo: {
      releaseCkan: {
        catalogTitle: '',
        catalogDescription: '',
        catalogUrl: '',
        catalogPublisher: '',
        catalogPublisherExplanation: ''
      },
      detailCkan: {
        catalogTitle: '',
        catalogDescription: '',
        catalogUrl: '',
        catalogPublisher: '',
        catalogPublisherExplanation: ''
      }
    },
    // 外部サービス・機械学習使用有無フラグ
    configValue: {
      geonames: false,
      theme: true,
      keyword: true,
      spatial: true,
      temporal: true
    },
    // 「新規作成」ボタン押下フラグパラメータ
    _createNewCatalog: false,
    // カタログ（グループ）パラメータ
    dispGroupList: null,
    // データセット情報パラメータ
    catalogTitle: '',
    catalogDescription: '',
    datasetDescriptionUrl: '',
    datasetIdForDetail: '',
    registOrg: '',
    publisherId: '',
    publisher: '',
    publisherUri: '',
    creator: '',
    creatorUrl: '',
    contactPoint: '',
    contactPointUrl: '',
    // データ概要パラメータ
    filedataDetails: [],
    // データセット情報(任意)パラメータ
    selectThemes: [],
    selectTags: [],
    vocabulary: '',
    term: '',
    selectLanguage: [{ label: '日本語', value: 'ja' }],
    frequency: '',
    dataCalender: {
      start: '',
      end: ''
    },
    geonames: {
      spatialUrl: '',
      spatialName: '',
      spatial: ''
    },
    // データ利用条件パラメータ
    termName: '',
    termNameUrl: '',
    usrRight: '',
    accessRights: '',
    accessRightsUrl: '',
    haspolicyUrl: '',
    provWasGeneratedByUrl: '',
    conformsTo: '',
    contractType: '',
    secrecy: '',
    useApplication: [],
    useApplicationOther: '',
    scopeOfDisclosure: '',
    scopeOfDisclosureOther: '',
    redistributionRequirement: '',
    redistributionRequirementOther: '',
    permissionResion: [
      {
        label: '制限なし',
        value: '制限なし'
      }
    ],
    permissionResionOther: '',
    notices: '',
    personalData: '',
    personalDataOther: '',
    dataEffectivePeriod: {
      selectTerms: '',
      startDate: '',
      endDate: '',
      freefield: ''
    },
    usageLicensePeriod: {
      selectTerms: '',
      deadline: '',
      period: '',
      unit: '',
      freefield: ''
    },
    fee: '',
    priceRange: '',
    salesInfoUrl: '',
    noticesOfPrice: '',
    billingPeriod: '',
    expressWarranty: '',
    expressWarrantyOther: '',
    leagalCompliance: [],
    leagalComplianceOther: '',
    groups: [],
    // 選択モードのパラメータ
    selectedMode: {
      mode: '',
      ckanType: '',
      isBothCatalog: false
    },
    // 選択肢リストのパラメータ
    itemList: {
      frequency: [],
      caddecResourceType: [],
      caddecContractRequired: [],
      caddecRequired: [],
      accessRights: [],
      tradingPolicyContractType: [],
      tradingPolicyNda: [],
      tradingPolicyUseApplication: [],
      scopeOfDisclosure: [],
      termsOfUsePermissibleRegion: [],
      privacyPolicyContainsPersonalData: [],
      dataEffectivePeriod: [],
      usageLicensePeriod: [],
      fee: [],
      warrantyExpressWarranty: [],
      warrantyLegalCompliance: [],
      mimetype: [],
      compressFormat: [],
      packageFormat: [],
      schemaType: [],
      language: []
    },
    // CKANから取得する選択肢リストのパラメータ
    ckanItemList: {
      licenseId: []
    },
    // 表示・非表示フラグリストのパラメータ
    itemDisplayFlg: {
      url: '',
      caddecDatasetIdForDetail: '',
      publisherUri: '',
      publisherName: '',
      creatorName: '',
      creatorUrl: '',
      contactName: '',
      contactUrl: '',
      inputSupportType: '',
      caddecResourceType: '',
      filename: '',
      description: '',
      downloadUrl: '',
      explainUrl: '',
      size: '',
      valueName: '',
      mimeType: '',
      format: '',
      compressFormat: '',
      packageFormat: '',
      schema: '',
      schemaType: '',
      ngsiEntityType: '',
      ngsiTenant: '',
      ngsiServicePath: '',
      ngsiDataModel: '',
      getResourceIDForProvenance: '',
      caddecResourceIdForProvenance: '',
      previousEventId: '',
      dataServiceTitle: '',
      dataServiceEndpointUrl: '',
      dataServiceEndpointDescription: '',
      theme: '',
      tags: '',
      language: '',
      vocabulary: '',
      term: '',
      frequency: '',
      spatial: '',
      temporal: '',
      licenseTitle: '',
      licenseUrl: '',
      rights: '',
      accessRights: '',
      accessRightsUrl: '',
      haspolicyUrl: '',
      provWasGeneratedByUrl: '',
      conformsTo: '',
      tradingPolicyContractType: '',
      tradingPolicyNda: '',
      tradingPolicyUseApplication: '',
      scopeOfDisclosure: '',
      termsOfUsePermissibleRegion: '',
      termsOfUseNotices: '',
      privacyPolicyContainsPersonalData: '',
      dataEffectivePeriod: '',
      usageLicensePeriod: '',
      fee: '',
      salesInfoUrl: '',
      pricingPriceRange: '',
      pricingNoticesOfPrice: '',
      warrantyExpressWarranty: '',
      warrantyLegalCompliance: ''
    },
    hold: {},// 登録済みカタログ情報
    another: {},// 紐づけ先カタログ情報
    template: {},// テンプレート情報
    isCatalogEditing: false,// 編集中フラグ
    useTermsAllHide: false,
    datasetOptionAllHide: false,
  }),
  getters: {
    releaseCkanUserName(state) { return state.loginInfo.username },
    detailCkanUserName(state) { return state.loginInfo.username },
    releaseCkanCatalogTitle(state) { return state.catalogInfo.releaseCkan.catalogTitle },
    releaseCkanCatalogDescription(state) { return state.catalogInfo.releaseCkan.catalogDescription },
    releaseCkanCatalogUrl(state) { return state.catalogInfo.releaseCkan.catalogUrl },
    releaseCkanCatalogPublisher(state) { return state.catalogInfo.releaseCkan.catalogPublisher },
    releaseCkanCatalogPublisherExplanation(state) { return state.catalogInfo.releaseCkan.catalogPublisherExplanation },
    detailCkanCatalogTitle(state) { return state.catalogInfo.detailCkan.catalogTitle },
    detailCkanCatalogDescription(state) { return state.catalogInfo.detailCkan.catalogDescription },
    detailCkanCatalogUrl(state) { return state.catalogInfo.detailCkan.catalogUrl },
    detailCkanCatalogPublisher(state) { return state.catalogInfo.detailCkan.catalogPublisher },
    detailCkanCatalogPublisherExplanation(state) { return state.catalogInfo.detailCkan.catalogPublisherExplanation },
    createNewCatalog(state) { return state._createNewCatalog },
    mode(state) { return state.selectedMode.mode }
  },
  actions: {
    // CKANデータ名更新
    updateCkanName(getMes) {
      console.log('updateCkanName:CKANデータ名更新')
      this.releaseCkanDataName = getMes.releaseCkanDataName
      this.detailCkanDataName = getMes.detailCkanDataName
    },
    // サーバの自動設定値更新
    updateAutoSetValue(getMes) {
      console.log('updateAutoSetValue:サーバの自動設定値更新')
      this.issued = getMes.issued
      this.identifier = getMes.identifier
      this.datasetUrl = getMes.datasetUrl
    },
    // サーバの自動設定値更新
    updateAutoSetValueAnother(getMes) {
      console.log('updateAutoSetValueAnother:サーバの自動設定値更新')
      this.another.issued = getMes.issued
      this.another.identifier = getMes.identifier
      this.another.datasetUrl = getMes.datasetUrl
    },
    // ユーザ情報のパラメータ更新
    updateUser(getMes) {
      console.log('updateUser:ユーザ情報のパラメータ更新')
      this.loginInfo.sysadmin = getMes.sysadmin
      this.loginInfo.username = getMes.username
      this.loginInfo.caddeUserId = getMes.caddeUserId
      this.loginInfo.caddeUserIdList = getMes.caddeUserIdList
      this.loginInfo.releaseCkanAddr = getMes.releaseCkanAddr
      this.loginInfo.detailCkanAddr = getMes.detailCkanAddr
      this.loginInfo.ckan = getMes.ckan
    },
    // 認証情報のパラメータ更新
    updateAuthInfo(getMes) {
      this.authInfo.keycloakState = getMes.keycloakState
      this.authInfo.keycloakCode =  getMes.keycloakCode
    },
    // ログインCKANカタログパラメータ更新
    updateCkanCataloginfo(getMes) {
      console.log('updateCkanCataloginfo:ログインCKANカタログパラメータ更新')
      this.catalogInfo.releaseCkan.catalogTitle = getMes.releaseCkanCatalogTitle
      this.catalogInfo.releaseCkan.catalogDescription = getMes.releaseCkanCatalogDescription
      this.catalogInfo.releaseCkan.catalogUrl = getMes.releaseCkanCatalogUrl
      this.catalogInfo.releaseCkan.catalogPublisher = getMes.releaseCkanCatalogPublisher
      this.catalogInfo.releaseCkan.catalogPublisherExplanation = getMes.releaseCkanCatalogPublisherExplanation
      this.catalogInfo.detailCkan.catalogTitle = getMes.detailCkanCatalogTitle
      this.catalogInfo.detailCkan.catalogDescription = getMes.detaikCkanCatalogDescription
      this.catalogInfo.detailCkan.catalogUrl = getMes.detailCkanCatalogUrl
      this.catalogInfo.detailCkan.catalogPublisher = getMes.detailCkanCatalogPublisher
      this.catalogInfo.detailCkan.catalogPublisherExplanation = getMes.detailCkanCatalogPublisherExplanation
    },
    updateConfigValue(getMes) {
      console.log('外部サービス・機械学習使用有無フラグ更新')
      this.configValue.geonames = getMes.geonames
      this.configValue.theme = getMes.theme
      this.configValue.keyword = getMes.keyword
      this.configValue.spatial = getMes.spatial
      this.configValue.temporal = getMes.temporal
    },
    pushCreate(getMes) {
      this._createNewCatalog = getMes.createNewCatalog
    },
    // カタログ（グループ）のパラメータ更新
    updateGroupList(getMes) {
      console.log('updateGroupList:カタログ（グループ）のパラメータ更新')
      this.dispGroupList = getMes.dispGroupList
    },
    // データセット情報のパラメータ更新
    updateDatasetinfo(getMes) {
      console.log('updateDatasetinfo:データセット情報のパラメータ更新')
      if (getMes.storeType === 'state') {
        this.catalogTitle = getMes.catalogTitle
        this.catalogDescription = getMes.catalogDescription
        this.registOrg = getMes.registOrg
        this.datasetDescriptionUrl = getMes.datasetDescriptionUrl
        this.datasetIdForDetail = getMes.datasetIdForDetail
        this.publisherId = getMes.publisherId
        this.publisher = getMes.publisher
        this.publisherUri = getMes.publisherUri
        this.creator = getMes.creator
        this.creatorUrl = getMes.creatorUrl
        this.contactPoint = getMes.contactPoint
        this.contactPointUrl = getMes.contactPointUrl
      } else {
        this[getMes.storeType].catalogTitle = getMes.catalogTitle
        this[getMes.storeType].catalogDescription = getMes.catalogDescription
        this[getMes.storeType].registOrg = getMes.registOrg
        this[getMes.storeType].datasetDescriptionUrl = getMes.datasetDescriptionUrl
        this[getMes.storeType].datasetIdForDetail = getMes.datasetIdForDetail
        this[getMes.storeType].publisherId = getMes.publisherId
        this[getMes.storeType].publisher = getMes.publisher
        this[getMes.storeType].publisherUri = getMes.publisherUri
        this[getMes.storeType].creator = getMes.creator
        this[getMes.storeType].creatorUrl = getMes.creatorUrl
        this[getMes.storeType].contactPoint = getMes.contactPoint
        this[getMes.storeType].contactPointUrl = getMes.contactPointUrl
      }
    },
    // データ概要情報のパラメータ更新
    updateFiledataDetails(getMes) {
      console.log('updateFiledataDetails:データ概要情報のパラメータ更新')
      var i = 0
      if (getMes.storeType === 'state') {
        this.filedataDetails = []
        for (i = 0; i < getMes.filedataDetails.length; i++) {
          this.filedataDetails.push({
            label: getMes.filedataDetails[i].label,
            dataname: getMes.filedataDetails[i].dataname,
            filename: getMes.filedataDetails[i].filename,
            description: getMes.filedataDetails[i].description,
            inputSupportUrl: getMes.filedataDetails[i].inputSupportUrl,
            inputSupportResourceType: getMes.filedataDetails[i].inputSupportResourceType,
            inputSupportNgsiTenant: getMes.filedataDetails[i].inputSupportNgsiTenant,
            inputSupportNgsiServicePath: getMes.filedataDetails[i].inputSupportNgsiServicePath,
            inputSupportIsRequestSuccess: getMes.filedataDetails[i].inputSupportIsRequestSuccess,
            downloadUrl: getMes.filedataDetails[i].downloadUrl,
            explainurl: getMes.filedataDetails[i].explainurl,
            size: getMes.filedataDetails[i].size,
            columnName: getMes.filedataDetails[i].columnName,
            mimetype: getMes.filedataDetails[i].mimetype,
            format: getMes.filedataDetails[i].format,
            compressFormat: getMes.filedataDetails[i].compressFormat,
            compressFormatOther: getMes.filedataDetails[i].compressFormatOther,
            packageFormat: getMes.filedataDetails[i].packageFormat,
            packageFormatOther: getMes.filedataDetails[i].packageFormatOther,
            schema: getMes.filedataDetails[i].schema,
            schemaType: getMes.filedataDetails[i].schemaType,
            ngsiEntityType: getMes.filedataDetails[i].ngsiEntityType,
            ngsiTenant: getMes.filedataDetails[i].ngsiTenant,
            ngsiServicePath: getMes.filedataDetails[i].ngsiServicePath,
            ngsiDataModel: getMes.filedataDetails[i].ngsiDataModel,
            contractRequired: getMes.filedataDetails[i].contractRequired,
            connectRequired: getMes.filedataDetails[i].connectRequired,
            getResourceIDForProvenance: getMes.filedataDetails[i].getResourceIDForProvenance,
            resourceIDForProvenance: getMes.filedataDetails[i].resourceIDForProvenance,
            previousEventId: getMes.filedataDetails[i].previousEventId,
            dataServiceTitle: getMes.filedataDetails[i].dataServiceTitle,
            dataServiceEndpointUrl: getMes.filedataDetails[i].dataServiceEndpointUrl,
            dataServiceEndpointDescription: getMes.filedataDetails[i].dataServiceEndpointDescription,
            urlForProvenance: getMes.filedataDetails[i].urlForProvenance,
            caddeUserId: getMes.filedataDetails[i].caddeUserId,
            resourceType: getMes.filedataDetails[i].resourceType,
            licensetitle: getMes.filedataDetails[i].licensetitle,
            licenseurl: getMes.filedataDetails[i].licenseurl,
            issued: getMes.filedataDetails[i].issued,
            id: getMes.filedataDetails[i].id
          })
        }
      } else {
        this[getMes.storeType].filedataDetails = []
        for (i = 0; i < getMes.filedataDetails.length; i++) {
          this[getMes.storeType].filedataDetails.push({
            label: getMes.filedataDetails[i].label,
            dataname: getMes.filedataDetails[i].dataname,
            filename: getMes.filedataDetails[i].filename,
            description: getMes.filedataDetails[i].description,
            dataurl: getMes.filedataDetails[i].dataurl,
            downloadUrl: getMes.filedataDetails[i].downloadUrl,
            explainurl: getMes.filedataDetails[i].explainurl,
            size: getMes.filedataDetails[i].size,
            columnName: getMes.filedataDetails[i].columnName,
            mimetype: getMes.filedataDetails[i].mimetype,
            format: getMes.filedataDetails[i].format,
            compressFormat: getMes.filedataDetails[i].compressFormat,
            compressFormatOther: getMes.filedataDetails[i].compressFormatOther,
            packageFormat: getMes.filedataDetails[i].packageFormat,
            packageFormatOther: getMes.filedataDetails[i].packageFormatOther,
            schema: getMes.filedataDetails[i].schema,
            schemaType: getMes.filedataDetails[i].schemaType,
            ngsiEntityType: getMes.filedataDetails[i].ngsiEntityType,
            ngsiTenant: getMes.filedataDetails[i].ngsiTenant,
            ngsiServicePath: getMes.filedataDetails[i].ngsiServicePath,
            ngsiDataModel: getMes.filedataDetails[i].ngsiDataModel,
            contractRequired: getMes.filedataDetails[i].contractRequired,
            connectRequired: getMes.filedataDetails[i].connectRequired,
            getResourceIDForProvenance: getMes.filedataDetails[i].getResourceIDForProvenance,
            resourceIDForProvenance: getMes.filedataDetails[i].resourceIDForProvenance,
            previousEventId: getMes.filedataDetails[i].previousEventId,
            dataServiceTitle: getMes.filedataDetails[i].dataServiceTitle,
            dataServiceEndpointUrl: getMes.filedataDetails[i].dataServiceEndpointUrl,
            dataServiceEndpointDescription: getMes.filedataDetails[i].dataServiceEndpointDescription,
            urlForProvenance: getMes.filedataDetails[i].urlForProvenance,
            caddeUserId: getMes.filedataDetails[i].caddeUserId,
            resourceType: getMes.filedataDetails[i].resourceType,
            licensetitle: getMes.filedataDetails[i].licensetitle,
            licenseurl: getMes.filedataDetails[i].licenseurl,
            issued: getMes.filedataDetails[i].issued,
            id: getMes.filedataDetails[i].id
          })
        }
      }
    },
    // 1件分のファイル概要情報更新
    updateOneFiledataDetails(getMes) {
      console.log('updateOneFiledataDetails:1件分のファイル概要情報更新')
      for (var i = 0; i < this.filedataDetails.length; i++) {
        if (this.filedataDetails[i].label === getMes.label) {
          this.filedataDetails[i].dataname = getMes.dataname
        }
      }
    },
    // データセット情報（任意）ページのパラメータ更新
    updateDatasetOptionalInfoParameters(getMes) {
      console.log('updateDatasetOptionalInfoParameters:データセット情報（任意）ページのパラメータ更新')
      if (getMes.storeType === 'state') {
        this.selectThemes = getMes.selectThemes
        this.selectTags = getMes.selectTags
        this.vocabulary = getMes.vocabulary
        this.term = getMes.term
        this.selectLanguage = getMes.selectLanguage
        this.frequency = getMes.frequency
        this.geonames.spatialUrl = getMes.spatialUrl
        this.geonames.spatialName = getMes.spatialName
        this.geonames.spatial = getMes.spatial
        this.dataCalender.start = getMes.start
        this.dataCalender.end = getMes.end
      } else {
        this[getMes.storeType].selectThemes = getMes.selectThemes
        this[getMes.storeType].selectTags = getMes.selectTags
        this[getMes.storeType].vocabulary = getMes.vocabulary
        this[getMes.storeType].term = getMes.term
        this[getMes.storeType].selectLanguage = getMes.selectLanguage
        this[getMes.storeType].frequency = getMes.frequency
        this[getMes.storeType].geonames.spatialUrl = getMes.spatialUrl
        this[getMes.storeType].geonames.spatialName = getMes.spatialName
        this[getMes.storeType].geonames.spatial = getMes.spatial
        this[getMes.storeType].dataCalender.start = getMes.start
        this[getMes.storeType].dataCalender.end = getMes.end
      }
    },
    // データ利用条件ページのパラメータ更新
    updateUserTerms(getMes) {
      console.log('updateUserTerms:データ利用条件ページのパラメータ更新')
      if (getMes.storeType === 'state') {
        this.termName = getMes.termName
        this.usrRight = getMes.usrRight
        this.accessRights = getMes.accessRights
        this.accessRightsUrl = getMes.accessRightsUrl
        this.haspolicyUrl = getMes.haspolicyUrl
        this.provWasGeneratedByUrl = getMes.provWasGeneratedByUrl
        this.conformsTo = getMes.conformsTo
        this.contractType = getMes.contractType
        this.secrecy = getMes.secrecy
        this.useApplication = getMes.useApplication
        this.useApplicationOther = getMes.useApplicationOther
        this.scopeOfDisclosure = getMes.scopeOfDisclosure
        this.scopeOfDisclosureOther = getMes.scopeOfDisclosureOther
        this.termNameUrl = getMes.termNameUrl
        this.permissionResion = getMes.permissionResion
        this.permissionResionOther = getMes.permissionResionOther
        this.notices = getMes.notices
        this.personalData = getMes.personalData
        this.personalDataOther = getMes.personalDataOther
        this.dataEffectivePeriod.selectTerms = getMes.dataEffectivePeriodSelectTerms
        this.dataEffectivePeriod.startDate = getMes.startDate
        this.dataEffectivePeriod.endDate = getMes.endDate
        this.dataEffectivePeriod.freefield = getMes.dataEffectivePeriodFreefield
        this.usageLicensePeriod.selectTerms = getMes.usageLicensePeriodSelectTerms
        this.usageLicensePeriod.deadline = getMes.deadline
        this.usageLicensePeriod.period = getMes.period
        this.usageLicensePeriod.unit = getMes.unit
        this.usageLicensePeriod.freefield = getMes.usageLicensePeriodFreefield
        this.fee = getMes.fee
        this.priceRange = getMes.priceRange
        this.salesInfoUrl = getMes.salesInfoUrl
        this.noticesOfPrice = getMes.noticesOfPrice
        this.expressWarranty = getMes.expressWarranty
        this.expressWarrantyOther = getMes.expressWarrantyOther
        this.leagalCompliance = getMes.leagalCompliance
        this.leagalComplianceOther = getMes.leagalComplianceOther
      } else {
        this[getMes.storeType].termName = getMes.termName
        this[getMes.storeType].usrRight = getMes.usrRight
        this[getMes.storeType].accessRights = getMes.accessRights
        this[getMes.storeType].accessRightsUrl = getMes.accessRightsUrl
        this[getMes.storeType].haspolicyUrl = getMes.haspolicyUrl
        this[getMes.storeType].provWasGeneratedByUrl = getMes.provWasGeneratedByUrl
        this[getMes.storeType].conformsTo = getMes.conformsTo
        this[getMes.storeType].contractType = getMes.contractType
        this[getMes.storeType].secrecy = getMes.secrecy
        this[getMes.storeType].useApplication = getMes.useApplication
        this[getMes.storeType].useApplicationOther = getMes.useApplicationOther
        this[getMes.storeType].scopeOfDisclosure = getMes.scopeOfDisclosure
        this[getMes.storeType].scopeOfDisclosureOther = getMes.scopeOfDisclosureOther
        this[getMes.storeType].termNameUrl = getMes.termNameUrl
        this[getMes.storeType].permissionResion = getMes.permissionResion
        this[getMes.storeType].permissionResionOther = getMes.permissionResionOther
        this[getMes.storeType].notices = getMes.notices
        this[getMes.storeType].personalData = getMes.personalData
        this[getMes.storeType].personalDataOther = getMes.personalDataOther
        this[getMes.storeType].dataEffectivePeriod.selectTerms = getMes.dataEffectivePeriodSelectTerms
        this[getMes.storeType].dataEffectivePeriod.startDate = getMes.startDate
        this[getMes.storeType].dataEffectivePeriod.endDate = getMes.endDate
        this[getMes.storeType].dataEffectivePeriod.freefield = getMes.dataEffectivePeriodFreefield
        this[getMes.storeType].usageLicensePeriod.selectTerms = getMes.usageLicensePeriodSelectTerms
        this[getMes.storeType].usageLicensePeriod.deadline = getMes.deadline
        this[getMes.storeType].usageLicensePeriod.period = getMes.period
        this[getMes.storeType].usageLicensePeriod.unit = getMes.unit
        this[getMes.storeType].usageLicensePeriod.freefield = getMes.usageLicensePeriodFreefield
        this[getMes.storeType].fee = getMes.fee
        this[getMes.storeType].priceRange = getMes.priceRange
        this[getMes.storeType].salesInfoUrl = getMes.salesInfoUrl
        this[getMes.storeType].noticesOfPrice = getMes.noticesOfPrice
        this[getMes.storeType].expressWarranty = getMes.expressWarranty
        this[getMes.storeType].expressWarrantyOther = getMes.expressWarrantyOther
        this[getMes.storeType].leagalCompliance = getMes.leagalCompliance
        this[getMes.storeType].leagalComplianceOther = getMes.leagalComplianceOther
      }
    },
    // groupsのパラメータ更新
    updateGroups(getMes) {
      console.log('updateGroups:groupsのパラメータ更新')
      for (var i = 0; i < getMes.groups.length; i++) {
        this.groups.push({
          description: getMes.groups[i].description,
          display_name: getMes.groups[i].display_name,
          id: getMes.groups[i].id,
          image_display_url: getMes.groups[i].image_display_url,
          name: getMes.groups[i].name,
          title: getMes.groups[i].title
        })
      }
    },
    // groupsのパラメータ更新
    updateGroupsAnother(getMes) {
      console.log('updateGroupsAnother:groupsのパラメータ更新')
      for (var i = 0; i < getMes.groups.length; i++) {
        this.another.groups.push({
          description: getMes.groups[i].description,
          display_name: getMes.groups[i].display_name,
          id: getMes.groups[i].id,
          image_display_url: getMes.groups[i].image_display_url,
          name: getMes.groups[i].name,
          title: getMes.groups[i].title
        })
      }
    },
    // 選択モードパラメータ更新
    updateMode(getMes) {
      console.log('updateMode:選択モードパラメータ更新')
      this.selectedMode.mode = getMes.mode
      this.selectedMode.ckanType = getMes.ckanType
      this.selectedMode.isBothCatalog = getMes.isBothCatalog
    },
    // 実行モード情報の初期化
    resetMode() {
      this.selectedMode.mode = ''
      this.selectedMode.ckanType = ''
      this.selectedMode.isBothCatalog = false
    },
    // 選択肢リストのパラメータ更新
    updateItemList(getMes) {
      console.log('updateItemList:選択肢リストのパラメータ更新')
      this.itemList.frequency = getMes.frequency
      this.itemList.caddecResourceType = getMes.caddecResourceType
      this.itemList.caddecContractRequired = getMes.caddecContractRequired
      this.itemList.caddecRequired = getMes.caddecRequired
      this.itemList.accessRights = getMes.accessRights
      this.itemList.tradingPolicyContractType = getMes.tradingPolicyContractType
      this.itemList.tradingPolicyContractType = getMes.tradingPolicyContractType
      this.itemList.tradingPolicyNda = getMes.tradingPolicyNda
      this.itemList.tradingPolicyUseApplication = getMes.tradingPolicyUseApplication
      this.itemList.scopeOfDisclosure = getMes.scopeOfDisclosure
      this.itemList.termsOfUsePermissibleRegion = getMes.termsOfUsePermissibleRegion
      this.itemList.privacyPolicyContainsPersonalData = getMes.privacyPolicyContainsPersonalData
      this.itemList.dataEffectivePeriod = getMes.dataEffectivePeriod
      this.itemList.usageLicensePeriod = getMes.usageLicensePeriod
      this.itemList.fee = getMes.fee
      this.itemList.warrantyExpressWarranty = getMes.warrantyExpressWarranty
      this.itemList.warrantyLegalCompliance = getMes.warrantyLegalCompliance
      this.itemList.mimetype = getMes.mimetype
      this.itemList.compressFormat = getMes.compressFormat
      this.itemList.packageFormat = getMes.packageFormat
      this.itemList.schemaType = getMes.schemaType
      this.itemList.language = getMes.language
    },
    // CKANから取得する選択肢リストのパラメータ更新
    updateCkanItemList(getMes) {
      console.log('updateCkanItemList:CKANから取得する選択肢リストのパラメータ更新')
      this.ckanItemList.licenseId = getMes.licenseId
    },
    // 表示・非表示フラグリストのパラメータ更新
    updateItemDisplayFlg(getMes) {
      console.log('updateItemDisplayFlg:表示・非表示フラグリストのパラメータ更新')
      for (var key in this.itemDisplayFlg) {
        this.itemDisplayFlg[key] = getMes[key]
      }
    },
    // カタログ項目のフィールド初期化
    initField(fields) {
      console.log('initField:カタログ項目のフィールド初期化')
      for (var cnt in fields) {
        this[fields[cnt]] = {}
        for (var j = 0; j < CATALOG_ITEM_LIST.length; j++) {
          var catalogItemFieldName = CATALOG_ITEM_LIST[j].key
          var catalogItemFieldValue = CATALOG_ITEM_LIST[j].value
          var catalogItemFieldType = CATALOG_ITEM_LIST[j].type
          switch (catalogItemFieldType) {
            case 'object':
              this[fields[cnt]][catalogItemFieldName] = JSON.parse(JSON.stringify(catalogItemFieldValue))
              break
            case 'list':
              this[fields[cnt]][catalogItemFieldName] = JSON.parse(JSON.stringify(catalogItemFieldValue))
              break
            case 'string':
            case 'int':
              this[fields[cnt]][catalogItemFieldName] = catalogItemFieldValue
              break
          }
        }
      }
    },
    // TODO:使用されていない可能性があるためコメントアウト、動作確認後問題なければ削除する
    // initCreateNewCatalog() {
    //   this._createNewCatalog = false
    // },
    // データセット情報パラメータ初期化
    initStateParams() {
      console.log('initStateParams:データセット情報パラメータ初期化')
      // this.selectedMode.mode = ''
      // this.selectedMode.ckanType = ''
      // this.selectedMode.isBothCatalog = false
      for (var i = 0; i < CATALOG_ITEM_LIST.length; i++) {
        var catalogItemFieldName = CATALOG_ITEM_LIST[i].key
        var catalogItemFieldValue = CATALOG_ITEM_LIST[i].value
        var catalogItemFieldType = CATALOG_ITEM_LIST[i].type
        var templateValue = this.template[catalogItemFieldName]
        switch (catalogItemFieldType) {
          case 'object':
            this[catalogItemFieldName] = templateValue ? JSON.parse(JSON.stringify(templateValue)) : JSON.parse(JSON.stringify(catalogItemFieldValue))
            break
          case 'list':
            if (catalogItemFieldName === 'filedataDetails') {
              // データ概要情報のテンプレート値は初期化ではstateに反映しない
              this[catalogItemFieldName] = []
              break
            } else {
              this[catalogItemFieldName] = templateValue ? JSON.parse(JSON.stringify(templateValue)) : JSON.parse(JSON.stringify(catalogItemFieldValue))
              break
            }
          case 'string':
          case 'int':
            this[catalogItemFieldName] = templateValue || catalogItemFieldValue
            break
        }
      }
      // サーバの自動設定値削除
      this.issued = ''
      this.identifier = ''
      this.datasetUrl = ''
    },
    // 選択肢リスト初期化
    initItemListParams() {
      console.log('initItemListParams:選択肢リスト初期化')
      this.itemList.frequency = []
      this.itemList.caddecResourceType = []
      this.itemList.caddecContractRequired = []
      this.itemList.caddecRequired = []
      this.itemList.accessRights = []
      this.itemList.tradingPolicyContractType = []
      this.itemList.tradingPolicyNda = []
      this.itemList.tradingPolicyUseApplication = []
      this.itemList.scopeOfDisclosure = []
      this.itemList.termsOfUsePermissibleRegion = []
      this.itemList.privacyPolicyContainsPersonalData = []
      this.itemList.dataEffectivePeriod = []
      this.itemList.usageLicensePeriod = []
      this.itemList.fee = []
      this.itemList.warrantyExpressWarranty = []
      this.itemList.warrantyLegalCompliance = []
      this.itemList.mimetype = []
      this.itemList.compressFormat = []
      this.itemList.packageFormat = []
      this.itemList.schemaType = []
      this.itemList.language = []
    },
    // CKANから取得する選択肢リスト初期化
    initCkanItemListParams() {
      console.log('initCkanItemListParams:CKANから取得する選択肢リスト初期化')
      this.ckanItemList.licenseId = []
    },
    // ログイン中のCKAN情報初期化
    initLoginCkanInfo() {
      console.log('initLoginCkanInfo:ログイン中のCKAN情報初期化')
      this.catalogInfo.releaseCkan.catalogTitle = ''
      this.catalogInfo.releaseCkan.catalogDescription = ''
      this.catalogInfo.releaseCkan.catalogUrl = ''
      this.catalogInfo.releaseCkan.catalogPublisher = ''
      this.catalogInfo.releaseCkan.catalogPublisherExplanation = ''
      this.catalogInfo.detailCkan.catalogTitle = ''
      this.catalogInfo.detailCkan.catalogDescription = ''
      this.catalogInfo.detailCkan.catalogUrl = ''
      this.catalogInfo.detailCkan.catalogPublisher = ''
      this.catalogInfo.detailCkan.catalogPublisherExplanation = ''
      this.loginInfo.sysadmin = 'false'
      this.loginInfo.username = ''
      this.loginInfo.caddeUserId = ''
      this.loginInfo.caddeUserIdList = ''
      this.loginInfo.releaseCkanAddr = ''
      this.loginInfo.detailCkanAddr = ''
      this.loginInfo.ckan = ''
      this.authInfo.keycloakState = ''
      this.authInfo.keycloakCode = ''
    },
    // 外部サービス・機械学習使用有無フラグ初期化
    initConfigValue() {
      console.log('initConfigValue:外部サービス・機械学習使用有無フラグ初期化')
      this.configValue.geonames = false
      this.configValue.theme = true
      this.configValue.keyword = true
      this.configValue.spatial = true
      this.configValue.temporal = true
    },
    backup() {
      // stateの中身をholdにコピー
      // カタログ（グループ）パラメータ
      this.hold.dispGroupList = this.dispGroupList
      // データセット情報パラメータ
      this.hold.catalogTitle = this.catalogTitle
      this.hold.catalogDescription = this.catalogDescription
      this.hold.datasetDescriptionUrl = this.datasetDescriptionUrl
      this.hold.datasetIdForDetail = this.datasetIdForDetail
      this.hold.registOrg = this.registOrg
      this.hold.publisherId = this.publisherId
      this.hold.publisher = this.publisher
      this.hold.publisherUri = this.publisherUri
      this.hold.creator = this.creator
      this.hold.creatorUrl = this.creatorUrl
      this.hold.contactPoint = this.contactPoint
      this.hold.contactPointUrl = this.contactPointUrl
      // データセット情報(任意)パラメータ
      this.hold.selectThemes = JSON.parse(JSON.stringify(this.selectThemes))
      this.hold.selectTags = JSON.parse(JSON.stringify(this.selectTags))
      this.hold.vocabulary = this.vocabulary
      this.hold.term = this.term
      // this.hold.dispLang = Vue.util.extend([], this.dispLang)//使用されている箇所がない
      this.hold.dispRegularity = this.dispRegularity
      this.hold.selectLanguage = JSON.parse(JSON.stringify(this.selectLanguage))
      this.hold.frequency = this.frequency
      this.hold.dataCalender.start = this.dataCalender.start
      this.hold.dataCalender.end = this.dataCalender.end
      this.hold.geonames.spatialUrl = this.geonames.spatialUrl
      this.hold.geonames.spatialName = this.geonames.spatialName
      this.hold.geonames.spatial = this.geonames.spatial
      // データ概要パラメータ
      for (var i = 0; i < this.filedataDetails.length; i++) {
        this.hold.filedataDetails.push(JSON.parse(JSON.stringify(this.filedataDetails[i])))
      }
      // データ利用条件パラメータ
      this.hold.termName = this.termName
      this.hold.usrRight = this.usrRight
      this.hold.accessRights = this.accessRights
      this.hold.accessRightsUrl = this.accessRightsUrl
      this.hold.haspolicyUrl = this.haspolicyUrl
      this.hold.provWasGeneratedByUrl = this.provWasGeneratedByUrl
      this.hold.conformsTo = this.conformsTo
      this.hold.contractType = this.contractType
      this.hold.secrecy = this.secrecy
      this.hold.useApplication = JSON.parse(JSON.stringify(this.useApplication))
      this.hold.useApplicationOther = this.useApplicationOther
      this.hold.monitoring = this.monitoring
      this.hold.scopeOfDisclosure = this.scopeOfDisclosure
      this.hold.scopeOfDisclosureOther = this.scopeOfDisclosureOther
      this.hold.permissibleReceipient = this.permissibleReceipient
      this.hold.termNameUrl = this.termNameUrl
      this.hold.permissionResion = JSON.parse(JSON.stringify(this.permissionResion))
      this.hold.permissionResionOther = this.permissionResionOther
      this.hold.notices = this.notices
      this.hold.rightsOfDelivativeWork = this.rightsOfDelivativeWork
      this.hold.personalData = this.personalData
      this.hold.personalDataOther = this.personalDataOther
      this.hold.privacyProtectionRule = this.privacyProtectionRule
      this.hold.dataEffectivePeriod.selectTerms = this.dataEffectivePeriod.selectTerms
      this.hold.dataEffectivePeriod.startDate = this.dataEffectivePeriod.startDate
      this.hold.dataEffectivePeriod.endDate = this.dataEffectivePeriod.endDate
      this.hold.dataEffectivePeriod.freefield = this.dataEffectivePeriod.freefield
      this.hold.usageLicensePeriod.selectTerms = this.usageLicensePeriod.selectTerms
      this.hold.usageLicensePeriod.deadline = this.usageLicensePeriod.deadline
      this.hold.usageLicensePeriod.period = this.usageLicensePeriod.period
      this.hold.usageLicensePeriod.unit = this.usageLicensePeriod.unit
      this.hold.usageLicensePeriod.freefield = this.usageLicensePeriod.freefield
      this.hold.fee = this.fee
      this.hold.billingType = this.billingType
      this.hold.meteringType = this.meteringType
      this.hold.priceRange = this.priceRange
      this.hold.salesInfoUrl = this.salesInfoUrl
      this.hold.noticesOfPrice = this.noticesOfPrice
      this.hold.billingPeriod = this.billingPeriod
      this.hold.expressWarranty = this.expressWarranty
      this.hold.expressWarrantyOther = this.expressWarrantyOther
      this.hold.leagalCompliance = JSON.parse(JSON.stringify(this.leagalCompliance))
      this.hold.leagalComplianceOther = this.leagalComplianceOther
      for (var j = 0; j < this.groups.length; j++) {
        this.hold.groups.push(JSON.parse(JSON.stringify(this.groups[j])))
      }
    },
    copyLicenseToFiledataDetails() { 
      console.log('copyLicenseToFiledataDetails:データセットのライセンスの入力値を配信のライセンスに反映')
      for (var i = 0; i < this.filedataDetails.length; i++) {
        if (this.termName && this.termName.label) {
          this.filedataDetails[i].licensetitle = this.termName.label
        } else {
          this.filedataDetails[i].licensetitle = ''
        }
        if (this.termNameUrl) {
          this.filedataDetails[i].licenseurl = this.termNameUrl
        } else {
          this.filedataDetails[i].licenseurl = ''
        }
      }
    },
    // 確認画面（利用条件）の全非表示項目フラグの更新
    updateUseTermsAllHide(status) { 
      this.useTermsAllHide = status
    },
    // 確認画面（データセット情報（任意））の全非表示項目フラグの更新
    updateDatasetOptionAllHide(status) {
      this.datasetOptionAllHide = status
    }
  },
});
