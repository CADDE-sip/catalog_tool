(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([[9],{"013f":function(e,a,t){"use strict";t.r(a);var r=function(){var e=this,a=e.$createElement,t=e._self._c||a;return t("div",{staticClass:"col-12"},[[t("div",{staticClass:"q-layout-padding flex justify-center content-center"},[t("q-card",{staticClass:"q-card-background-white",staticStyle:{"max-width":"45%",width:"100%"}},[t("q-card-section",[t("div",{staticClass:"row"},[t("div",{staticClass:"col-sm-10 offset-sm-1"},[t("p",[t("font",{attrs:{size:"5",color:"#1d468f"}},[e._v("ユーザ認証")])],1),t("p",[e._v("分野間データ連携基盤データ検索用カタログサイトの"),t("br"),e._v("\n              ユーザ名とパスワードを入力してください。")]),t("font",{staticStyle:{"white-space":"pre-line"},attrs:{color:"red"}},[e._v(e._s(e.loginErrorMessage))])],1)]),t("div",{staticClass:"row"},[t("div",{staticClass:"col-sm-10 offset-sm-1 text-left"},[t("h5",[e._v(" ユーザ名 ")])])]),t("div",{staticClass:"row"},[t("div",{staticClass:"col-sm-10 offset-sm-1"},[t("q-input",{attrs:{label:"user name"},model:{value:e.username,callback:function(a){e.username=a},expression:"username"}})],1)]),t("div",{staticClass:"row"},[t("div",{staticClass:"col-sm-10 offset-sm-1 text-left"},[t("h5",[e._v(" パスワード ")])])]),t("div",{staticClass:"row"},[t("div",{staticClass:"col-sm-10 offset-sm-1"},[t("q-input",{attrs:{label:"password",type:e.isPwd?"password":"text"},model:{value:e.password,callback:function(a){e.password=a},expression:"password"}},[t("q-icon",{staticClass:"cursor-pointer",attrs:{size:"32px",name:e.isPwd?"visibility_off":"visibility"},on:{click:function(a){e.isPwd=!e.isPwd}}})],1)],1)]),t("div",{staticClass:"row q-mt-lg q-mb-lg"},[t("div",{staticClass:"col-sm-10 offset-sm-1 text-right"},[t("q-btn",{attrs:{color:"light-blue-10",label:"ログイン"},on:{click:function(a){return e.login()}}})],1)])])],1)],1)]],2)},i=[],s=(t("a4d3"),t("e01a"),t("b0c0"),t("96cf"),t("c973")),o=t.n(s),n=t("2a19"),l=t("f508"),c=t("bc3a"),d=t.n(c),u="/api/v1/catalog/tool";n["a"].setDefaults({});var p={name:"user",title:"分析画面",data:function(){return{username:"",password:"",isPwd:!0,loginMessage:"",ckanTitle:"",prefix_uri:"/api/v1/catalog/tool",languageList:[],loginErrorMessage:""}},methods:{login:function(){var e=this;l["a"].show(),this.loginErrorMessage="",d.a.post(this.prefix_uri+"/login",{username:this.username,password:this.password}).then((function(a){console.log("res",a),l["a"].hide(),e.afterLoginProcess(),e.$store.commit("updateUser",{ckan:a.data.ckan,username:e.username,releaseCkanAddr:a.data.release_ckan_addr,detailCkanAddr:a.data.detail_ckan_addr,sysadmin:a.data.sysadmin}),!0===a.data.sysadmin?(e.$router.push("/userManager"),e.getCataloginfo(),e.$store.commit("updateMode",{mode:"userManagement",ckanType:"",isBothCatalog:!1})):(e.$router.push("/register"),e.getCataloginfo(),e.$store.commit("updateMode",{mode:"register",ckanType:"",isBothCatalog:!1}))})).catch((function(a){l["a"].hide(),console.log("err.response.data.message",a.response.data.message),e.loginErrorMessage=a.response.data.message}))},getCataloginfo:function(){var e=this;d.a.get(u+"/ckaninfo").then(function(){var a=o()(regeneratorRuntime.mark((function a(t){var r,i,s,o,n,l,c;return regeneratorRuntime.wrap((function(a){while(1)switch(a.prev=a.next){case 0:if(console.log("CKANサイト情報",t),200===t.status){for(r=0;r<t.data.length;r++)"release"===t.data[r].ckan_type?(i=t.data[r].title,s=t.data[r].description,o=t.data[r].url):"detail"===t.data[r].ckan_type&&(n=t.data[r].title,l=t.data[r].description,c=t.data[r].url);e.$store.commit("updateCkanCataloginfo",{releaseCkanCatalogTitle:i,releaseCkanCatalogDescription:s,releaseCkanCatalogUrl:o,detailCkanCatalogTitle:n,detaikCkanCatalogDescription:l,detailCkanCatalogUrl:c})}else console.log("ログインしたCKANのカタログ情報の取得に失敗しました");case 2:case"end":return a.stop()}}),a)})));return function(e){return a.apply(this,arguments)}}()).catch((function(e){console.log("ログインしたCKANのカタログ情報の取得時にエラーが発生しました",e)}))},getItemListValueLanguageList:function(){var e=this;d.a.get("datalist/languageList.json").then((function(a){e.languageList=a.data}))},getItemListValue:function(e,a){var t=[],r=[];for(var i in e){var s=e[i].ckanKeyName;if(s===a){t=e[i].valueMap;break}}for(var o in t)r.push({label:t[o],value:o});var n=JSON.stringify(r);return JSON.parse(n)},setItemList:function(){var e=this;d.a.get("datalist/itemValue.json").then((function(a){var t=a.data[0].select_item;e.$store.commit("updateItemList",{frequency:e.getItemListValue(t,"frequency"),caddecResourceType:e.getItemListValue(t,"caddec_resource_type"),caddecContractRequired:e.getItemListValue(t,"caddec_contract_required"),caddecRequired:e.getItemListValue(t,"caddec_required"),tradingPolicyContractType:e.getItemListValue(t,"trading_policy_contract_type"),tradingPolicyNda:e.getItemListValue(t,"trading_policy_nda"),tradingPolicyUseApplication:e.getItemListValue(t,"trading_policy_use_application"),termsOfUseRedistributionRange:e.getItemListValue(t,"terms_of_use_redistribution_range"),termsOfUsePermissibleRegion:e.getItemListValue(t,"terms_of_use_permissible_region"),privacyPolicyContainsPersonalData:e.getItemListValue(t,"privacy_policy_contains_personal_data"),usagePeriodEffectivePeriodOfData:e.getItemListValue(t,"usage_period_effective_period_of_data"),usagePeriodExpirationPeriod:e.getItemListValue(t,"usage_period_expiration_period"),fee:e.getItemListValue(t,"fee"),warrantyExpressWarranty:e.getItemListValue(t,"warranty_express_warranty"),warrantyLegalCompliance:e.getItemListValue(t,"warranty_legal_compliance"),language:e.languageList})}))},itemDisplayFlgStoreCommit:function(e){this.$store.commit("updateItemDisplayFlg",{url:e.datasetinfo.url,caddecDatasetIdForDetail:e.datasetinfo.caddec_dataset_id_for_detail,publisherName:e.datasetinfo.publisher_name,publisherUri:e.datasetinfo.publisher_uri,creatorName:e.datasetinfo.creator_name,creatorUrl:e.datasetinfo.creator_url,contactName:e.datasetinfo.contact_name,contactUrl:e.datasetinfo.contact_url,inputSupportType:e.datajacket.input_support_type,caddecResourceType:e.datajacket.caddec_resource_type,name:e.datajacket.name,description:e.datajacket.description,accessUrl:e.datajacket.access_url,downloadUrl:e.datajacket.download_url,size:e.datajacket.size,valueName:e.datajacket.value_name,mimeType:e.datajacket.mime_type,format:e.datajacket.format,schema:e.datajacket.schema,schemaType:e.datajacket.schema_type,ngsiTenant:e.datajacket.ngsi_tenant,ngsiServicePath:e.datajacket.ngsi_service_path,getResourceIdForProvenance:e.datajacket.get_resource_id_for_provenance,caddecResourceIdForProvenance:e.datajacket.caddec_resource_id_for_provenance,theme:e.datasetoptionalinfo.theme,tags:e.datasetoptionalinfo.tags,language:e.datasetoptionalinfo.language,vocabulary:e.datasetoptionalinfo.vocabulary,term:e.datasetoptionalinfo.term,frequency:e.datasetoptionalinfo.frequency,spatial:e.datasetoptionalinfo.spatial,temporal:e.datasetoptionalinfo.temporal,licenseTitle:e.userterms.license_title,licenseUrl:e.userterms.license_url,rights:e.userterms.rights,tradingPolicyContractType:e.userterms.trading_policy_contract_type,tradingPolicyNda:e.userterms.trading_policy_nda,tradingPolicyUseApplication:e.userterms.trading_policy_use_application,termsOfUseRedistributionRange:e.userterms.terms_of_use_redistribution_range,termsOfUsePermissibleRegion:e.userterms.terms_of_use_permissible_region,termsOfUseNotices:e.userterms.terms_of_use_notices,privacyPolicyContainsPersonalData:e.userterms.privacy_policy_contains_personal_data,usagePeriodEffectivePeriodOfData:e.userterms.usage_period_effective_period_of_data,usagePeriodExpirationPeriod:e.userterms.usage_period_expiration_period,fee:e.userterms.fee,salesInfoUrl:e.userterms.sales_info_url,pricingPriceRange:e.userterms.pricing_price_range,pricingNoticesOfPrice:e.userterms.pricing_notices_of_price,warrantyExpressWarranty:e.userterms.warranty_express_warranty,warrantyLegalCompliance:e.userterms.warranty_legal_compliance})},commitDatasetinfo:function(e,a){for(var t=0;t<a.length;t++)this.$store.commit("updateDatasetinfo",{catalogTitle:e.title,catalogDescription:e.notes,datasetDescriptionUrl:e.url,datasetIdForDetail:e.caddec_dataset_id_for_detail,registOrg:e.regist_org,publisherId:e.caddec_provider_id,publisher:e.publisher_name,publisherUri:e.publisher_uri,creator:e.creator_name,creatorUrl:e.creator_url,contactPoint:e.contact_name,contactPointUrl:e.contact_url,storeType:a[t]})},commitDatajacket:function(e,a){var t=[];if(e.length)for(var r=0;r<e.length;r++){if(e[r].contractRequired&&e[r].contractRequired.label&&e[r].contractRequired.value)var i=e[r].contractRequired.label,s=e[r].contractRequired.value;if(e[r].connectRequired&&e[r].connectRequired.label&&e[r].connectRequired.value)var o=e[r].connectRequired.label,n=e[r].connectRequired.value;if(e[r].filename)var l=e[r].filename;else l="";if(e[r].dataname)var c=e[r].dataname;else c="";if(e[r].description)var d=e[r].description;else d="";if(e[r].dataurl)var u=e[r].dataurl;else u="";if(e[r].accessurl)var p=e[r].accessurl;else p="";if(e[r].downloadurl)var _=e[r].downloadurl;else _="";if(e[r].size)var m=e[r].size;else m="";if(e[r].variables.length>0)var f=e[r].variables;else f=[];if(e[r].mimetype)var g=e[r].mimetype;else g="";if(e[r].format)var v=e[r].format;else v="";if(e[r].schema)var y=e[r].schema;else y="";if(e[r].schemaType)var h=e[r].schemaType;else h="";if(e[r].ngsiTenant)var b=e[r].ngsiTenant;else b="";if(e[r].ngsiServicePath)var P=e[r].ngsiServicePath;else P="";if(e[r].getResourceIDForProvenance)if(e[r].getResourceIDForProvenance.label&&e[r].getResourceIDForProvenance.value)var C=e[r].getResourceIDForProvenance.label,w=e[r].getResourceIDForProvenance.value;else C="",w="";if(e[r].resourceIDForProvenance)var k=e[r].resourceIDForProvenance;else k="";if(e[r].resourceType.value)if("file/http"===e[r].resourceType.value)var I="ファイル提供(HTTP)",T="file/http";else"file/ftp"===e[r].resourceType.value?(I="ファイル提供(FTP)",T="file/ftp"):"api/ngsi"===e[r].resourceType.value?(I="API提供(NGSI API)",T="api/ngsi"):(I="",T="");if(e[r].license_title)var D=e[r].license_title;else D="";if(e[r].licenseurl)var R=e[r].licenseurl;else R="";if(e[r].issued)var L=e[r].issued;else L="";if(e[r].label)var x=e[r].label;else x="";t.push({label:x,dataname:c,filename:l,description:d,dataurl:u,accessurl:p,downloadurl:_,size:m,variables:f,mimetype:g,format:v,schema:y,schemaType:h,ngsiTenant:b,ngsiServicePath:P,contractRequired:{label:i,value:s},connectRequired:{label:o,value:n},getResourceIDForProvenance:{label:C,value:w},resourceIDForProvenance:k,resourceType:{label:I,value:T},licensetitle:D,licenseurl:R,issued:L})}for(var q=0;q<a.length;q++)this.$store.commit("updateFiledataDetails",{filedataDetails:t,storeType:a[q]})},commitDatasetoptionalinfo:function(e,a){for(var t=0;t<a.length;t++)this.$store.commit("updateDatasetOptionalInfoParameters",{selectThemes:e.theme,selectTags:e.tags,vocabulary:e.vocabulary,term:e.term,selectLanguage:e.language,frequency:e.frequency,spatialUrl:e.spatial_url,spatialName:e.spatial_text,spatial:e.spatial,start:e.temporal_start,end:e.temporal_end,storeType:a[t]})},commitUserterms:function(e,a){for(var t=0;t<a.length;t++)this.$store.commit("updateUserTerms",{selectedTab:e.selected_tab,termName:e.license_title,termNameUrl:e.license_url,usrRight:e.rights,contractType:e.trading_policy_contract_type,secrecy:e.trading_policy_nda,useApplication:e.trading_policy_use_application,useApplicationOther:e.trading_policy_use_application_free,redistributionRange:e.terms_of_use_redistribution_range,redistributionRangeOther:e.terms_of_use_redistribution_range_free,permissionResion:e.terms_of_use_permissible_region,permissionResionOther:e.terms_of_use_permissible_region_free,notices:e.terms_of_use_notices,personalData:e.privacy_policy_contains_personal_data,personalDataOther:e.privacy_policy_contains_personal_data_free,effectivePeriodOfDataSelectTerms:e.usage_period_effective_period_of_data_term,startDate:e.usage_period_effective_period_of_data_start,endDate:e.usage_period_effective_period_of_data_end,effectivePeriodOfDataFreefield:e.usage_period_effective_period_of_data_free,expirationPeriodSelectTerms:e.usage_period_expiration_period_term,deadline:e.usage_period_expiration_period_deadline,period:e.usage_period_expiration_period_period,unit:e.usage_period_expiration_period_unit,expirationPeriodFreefield:e.usage_period_expiration_period_free,fee:e.fee,salesInfoUrl:e.sales_info_url,priceRange:e.pricing_price_range,noticesOfPrice:e.pricing_notices_of_price,expressWarranty:e.warranty_express_warranty,expressWarrantyOther:e.warranty_express_warranty_free,leagalCompliance:e.warranty_legal_compliance,leagalComplianceOther:e.warranty_legal_compliance_free,storeType:a[t]})},setTemplate:function(){var e=this;d.a.get(u+"/template").then((function(a){if(console.log("テンプレ-ト取得値",a),"failed"!==a.data.status){var t=a.data.template.catalog_display;e.itemDisplayFlgStoreCommit(t);var r=a.data.template.catalog_value;e.commitDatasetinfo(r.datasetinfo,["state","template"]),e.commitDatajacket(r.datajacket,["template"]),e.commitDatasetoptionalinfo(r.datasetoptionalinfo,["state","template"]),e.commitUserterms(r.userterms,["state","template"])}}))},afterLoginProcess:function(){var e=["hold","another","template"];this.$store.commit("initField",e),this.$store.commit("initStateParams"),this.$store.commit("initItemListParams"),this.$store.commit("initCkanItemListParams"),this.getItemListValueLanguageList(),this.setItemList(),this.setTemplate()}},beforeDestroy:function(){var e=[];d.a.post(u+"/licenselist").then((function(a){if(200===a.status)for(var t=a.data,r=0;r<t.length;r++)e.push({label:t[r].title,value:t[r].id,url:t[r].url});else console.log("ライセンスリストの取得に失敗しました")})),this.$store.commit("updateCkanItemList",{licenseId:e})}},_=p,m=(t("1139"),t("2877")),f=t("4d5a"),g=t("f09f"),v=t("a370"),y=t("27f9"),h=t("0016"),b=t("9c40"),P=t("eebe"),C=t.n(P),w=Object(m["a"])(_,r,i,!1,null,null,null);a["default"]=w.exports;C()(w,"components",{QLayout:f["a"],QCard:g["a"],QCardSection:v["a"],QInput:y["a"],QIcon:h["a"],QBtn:b["a"]})},1139:function(e,a,t){"use strict";var r=t("82e1"),i=t.n(r);i.a},"82e1":function(e,a,t){}}]);