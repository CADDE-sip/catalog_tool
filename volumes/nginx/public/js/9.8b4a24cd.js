(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([[9],{"013f":function(e,t,a){"use strict";a.r(t);var i=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"col-12"},[[a("div",{staticClass:"q-layout-padding flex justify-center content-center"},[a("q-card",{staticClass:"q-card-background-white",staticStyle:{"max-width":"45%",width:"100%"}},[a("q-card-section",[a("div",{staticClass:"row"},[a("div",{staticClass:"col-sm-10 offset-sm-1"},[a("p",[a("font",{attrs:{size:"5",color:"#1d468f"}},[e._v("ユーザ認証")])],1),a("p",[e._v("分野間データ連携基盤データ検索用カタログサイトの"),a("br"),e._v("\n              ユーザ名とパスワードを入力してください。")]),a("font",{staticStyle:{"white-space":"pre-line"},attrs:{color:"red"}},[e._v(e._s(e.loginErrorMessage))])],1)]),a("div",{staticClass:"row"},[a("div",{staticClass:"col-sm-10 offset-sm-1 text-left"},[a("h5",[e._v(" ユーザ名 ")])])]),a("div",{staticClass:"row"},[a("div",{staticClass:"col-sm-10 offset-sm-1"},[a("q-input",{attrs:{label:"user name"},model:{value:e.username,callback:function(t){e.username=t},expression:"username"}})],1)]),a("div",{staticClass:"row"},[a("div",{staticClass:"col-sm-10 offset-sm-1 text-left"},[a("h5",[e._v(" パスワード ")])])]),a("div",{staticClass:"row"},[a("div",{staticClass:"col-sm-10 offset-sm-1"},[a("q-input",{attrs:{label:"password",type:e.isPwd?"password":"text"},model:{value:e.password,callback:function(t){e.password=t},expression:"password"}},[a("q-icon",{staticClass:"cursor-pointer",attrs:{size:"32px",name:e.isPwd?"visibility_off":"visibility"},on:{click:function(t){e.isPwd=!e.isPwd}}})],1)],1)]),a("div",{staticClass:"row q-mt-lg q-mb-lg"},[a("div",{staticClass:"col-sm-10 offset-sm-1 text-right"},[a("q-btn",{attrs:{color:"light-blue-10",label:"ログイン"},on:{click:function(t){return e.login()}}})],1)])])],1)],1)]],2)},r=[],s=(a("a4d3"),a("e01a"),a("b0c0"),a("96cf"),a("c973")),o=a.n(s),n=a("2a19"),c=a("f508"),l=a("bc3a"),d=a.n(l),u="/api/v1/catalog/tool";n["a"].setDefaults({});var p={name:"user",title:"分析画面",data:function(){return{username:"",password:"",isPwd:!0,loginMessage:"",ckanTitle:"",prefix_uri:"/api/v1/catalog/tool",languageList:[],loginErrorMessage:""}},methods:{login:function(){var e=this;c["a"].show(),this.loginErrorMessage="",d.a.post(this.prefix_uri+"/login",{username:this.username,password:this.password}).then((function(t){c["a"].hide(),e.afterLoginProcess(),e.$store.commit("updateUser",{ckan:t.data.ckan,username:e.username,releaseCkanAddr:t.data.release_ckan_addr,detailCkanAddr:t.data.detail_ckan_addr,sysadmin:t.data.sysadmin}),!0===t.data.sysadmin?(e.$router.push("/userManager"),e.getCataloginfo(),e.$store.commit("updateMode",{mode:"userManagement",ckanType:"",isBothCatalog:!1})):(e.$router.push("/register"),e.getCataloginfo(),e.$store.commit("updateMode",{mode:"register",ckanType:"",isBothCatalog:!1}))})).catch((function(t){c["a"].hide(),console.log("err.response.data.message",t.response.data.message),e.loginErrorMessage=t.response.data.message}))},getCataloginfo:function(){var e=this;d.a.get(u+"/ckaninfo").then(function(){var t=o()(regeneratorRuntime.mark((function t(a){var i,r,s,o,n,c,l;return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:if(console.log("CKANサイト情報",a),200===a.status){for(i=0;i<a.data.length;i++)"release"===a.data[i].ckan_type?(r=a.data[i].title,s=a.data[i].description,o=a.data[i].url):"detail"===a.data[i].ckan_type&&(n=a.data[i].title,c=a.data[i].description,l=a.data[i].url);e.$store.commit("updateCkanCataloginfo",{releaseCkanCatalogTitle:r,releaseCkanCatalogDescription:s,releaseCkanCatalogUrl:o,detailCkanCatalogTitle:n,detaikCkanCatalogDescription:c,detailCkanCatalogUrl:l})}else console.log("ログインしたCKANのカタログ情報の取得に失敗しました");case 2:case"end":return t.stop()}}),t)})));return function(e){return t.apply(this,arguments)}}()).catch((function(e){console.log("ログインしたCKANのカタログ情報の取得時にエラーが発生しました",e)}))},getItemListValueLanguageList:function(){var e=this;d.a.get("datalist/languageList.json").then((function(t){e.languageList=t.data}))},getItemListValue:function(e,t){var a=[],i=[];for(var r in e){var s=e[r].ckanKeyName;if(s===t){a=e[r].valueMap;break}}for(var o in a)i.push({label:a[o],value:o});var n=JSON.stringify(i);return JSON.parse(n)},setItemList:function(){var e=this;d.a.get("datalist/itemValue.json").then((function(t){var a=t.data[0].select_item;e.$store.commit("updateItemList",{frequency:e.getItemListValue(a,"frequency"),caddecResourceType:e.getItemListValue(a,"caddec_resource_type"),caddecContractRequired:e.getItemListValue(a,"caddec_contract_required"),caddecRequired:e.getItemListValue(a,"caddec_required"),tradingPolicyContractType:e.getItemListValue(a,"trading_policy_contract_type"),tradingPolicyNda:e.getItemListValue(a,"trading_policy_nda"),tradingPolicyUseApplication:e.getItemListValue(a,"trading_policy_use_application"),termsOfUseRedistributionRange:e.getItemListValue(a,"terms_of_use_redistribution_range"),termsOfUsePermissibleRegion:e.getItemListValue(a,"terms_of_use_permissible_region"),privacyPolicyContainsPersonalData:e.getItemListValue(a,"privacy_policy_contains_personal_data"),usagePeriodEffectivePeriodOfData:e.getItemListValue(a,"usage_period_effective_period_of_data"),usagePeriodExpirationPeriod:e.getItemListValue(a,"usage_period_expiration_period"),fee:e.getItemListValue(a,"fee"),warrantyExpressWarranty:e.getItemListValue(a,"warranty_express_warranty"),warrantyLegalCompliance:e.getItemListValue(a,"warranty_legal_compliance"),language:e.languageList})}))},checkWithDefault:function(e){console.log(e),d.a.get(u+"/template/default").then((function(e){console.log("デフォルトテンプレ-ト取得値",e),"failed"===e.data.status&&console.log("デフォルトテンプレート取得失敗")}))},itemDisplayFlgStoreCommit:function(e){this.$store.commit("updateItemDisplayFlg",{url:e.datasetinfo.url,caddecDatasetIdForDetail:e.datasetinfo.caddec_dataset_id_for_detail,publisherName:e.datasetinfo.publisher_name,publisherUri:e.datasetinfo.publisher_uri,creatorName:e.datasetinfo.creator_name,creatorUrl:e.datasetinfo.creator_url,contactName:e.datasetinfo.contact_name,contactUrl:e.datasetinfo.contact_url,inputSupportType:e.datajacket.input_support_type,caddecResourceType:e.datajacket.caddec_resource_type,name:e.datajacket.name,description:e.datajacket.description,accessUrl:e.datajacket.access_url,downloadUrl:e.datajacket.download_url,size:e.datajacket.size,valueName:e.datajacket.value_name,mimeType:e.datajacket.mime_type,format:e.datajacket.format,schema:e.datajacket.schema,schemaType:e.datajacket.schema_type,ngsiEntityType:e.datajacket.ngsi_entity_type,ngsiTenant:e.datajacket.ngsi_tenant,ngsiServicePath:e.datajacket.ngsi_service_path,getResourceIdForProvenance:e.datajacket.get_resource_id_for_provenance,caddecResourceIdForProvenance:e.datajacket.caddec_resource_id_for_provenance,theme:e.datasetoptionalinfo.theme,tags:e.datasetoptionalinfo.tags,language:e.datasetoptionalinfo.language,vocabulary:e.datasetoptionalinfo.vocabulary,term:e.datasetoptionalinfo.term,frequency:e.datasetoptionalinfo.frequency,spatial:e.datasetoptionalinfo.spatial,temporal:e.datasetoptionalinfo.temporal,licenseTitle:e.userterms.license_title,licenseUrl:e.userterms.license_url,rights:e.userterms.rights,tradingPolicyContractType:e.userterms.trading_policy_contract_type,tradingPolicyNda:e.userterms.trading_policy_nda,tradingPolicyUseApplication:e.userterms.trading_policy_use_application,termsOfUseRedistributionRange:e.userterms.terms_of_use_redistribution_range,termsOfUsePermissibleRegion:e.userterms.terms_of_use_permissible_region,termsOfUseNotices:e.userterms.terms_of_use_notices,privacyPolicyContainsPersonalData:e.userterms.privacy_policy_contains_personal_data,usagePeriodEffectivePeriodOfData:e.userterms.usage_period_effective_period_of_data,usagePeriodExpirationPeriod:e.userterms.usage_period_expiration_period,fee:e.userterms.fee,salesInfoUrl:e.userterms.sales_info_url,pricingPriceRange:e.userterms.pricing_price_range,pricingNoticesOfPrice:e.userterms.pricing_notices_of_price,warrantyExpressWarranty:e.userterms.warranty_express_warranty,warrantyLegalCompliance:e.userterms.warranty_legal_compliance})},commitDatasetinfo:function(e,t){for(var a=0;a<t.length;a++)this.$store.commit("updateDatasetinfo",{catalogTitle:e.title,catalogDescription:e.notes,datasetDescriptionUrl:e.url,datasetIdForDetail:e.caddec_dataset_id_for_detail,registOrg:e.regist_org,publisherId:e.caddec_provider_id,publisher:e.publisher_name,publisherUri:e.publisher_uri,creator:e.creator_name,creatorUrl:e.creator_url,contactPoint:e.contact_name,contactPointUrl:e.contact_url,storeType:t[a]})},commitDatajacket:function(e,t){var a=[];if(e.length)for(var i=0;i<e.length;i++){if(e[i].contractRequired&&e[i].contractRequired.label&&e[i].contractRequired.value)var r=e[i].contractRequired.label,s=e[i].contractRequired.value;if(e[i].connectRequired&&e[i].connectRequired.label&&e[i].connectRequired.value)var o=e[i].connectRequired.label,n=e[i].connectRequired.value;var c=e[i].filename||"",l=e[i].dataname||"",d=e[i].description||"",u=e[i].dataurl||"",p=e[i].accessurl||"",_=e[i].downloadurl||"",m=e[i].size||"",g=e[i].variables||[],f=e[i].columnName||"",v=e[i].mimetype||"",y=e[i].format||"",h=e[i].schema||"",b=e[i].schemaType||"",P=e[i].ngsiEntityType||"",C=e[i].ngsiTenant||"",k=e[i].ngsiServicePath||"",w=e[i].ngsiDataModel||"";if(e[i].getResourceIDForProvenance)if(e[i].getResourceIDForProvenance.label&&e[i].getResourceIDForProvenance.value)var I=e[i].getResourceIDForProvenance.label,D=e[i].getResourceIDForProvenance.value;else I="",D="";var T=e[i].resourceIDForProvenance||"",R=e[i].previousEventId||"";if(e[i].resourceType.value)if("file/http"===e[i].resourceType.value)var L="ファイル提供(HTTP)",x="file/http";else"file/ftp"===e[i].resourceType.value?(L="ファイル提供(FTP)",x="file/ftp"):"api/ngsi"===e[i].resourceType.value?(L="API提供(NGSI API)",x="api/ngsi"):(L="",x="");var q=e[i].license_title||"",U=e[i].licenseurl||"",j=e[i].issued||"",O=e[i].label||"";a.push({label:O,dataname:l,filename:c,description:d,dataurl:u,accessurl:p,downloadurl:_,size:m,variables:g,columnName:f,mimetype:v,format:y,schema:h,schemaType:b,ngsiEntityType:P,ngsiTenant:C,ngsiServicePath:k,ngsiDataModel:w,contractRequired:{label:r,value:s},connectRequired:{label:o,value:n},getResourceIDForProvenance:{label:I,value:D},resourceIDForProvenance:T,previousEventId:R,resourceType:{label:L,value:x},licensetitle:q,licenseurl:U,issued:j})}for(var F=0;F<t.length;F++)this.$store.commit("updateFiledataDetails",{filedataDetails:a,storeType:t[F]})},commitDatasetoptionalinfo:function(e,t){for(var a=0;a<t.length;a++)this.$store.commit("updateDatasetOptionalInfoParameters",{selectThemes:e.theme,selectTags:e.tags,vocabulary:e.vocabulary,term:e.term,selectLanguage:e.language,frequency:e.frequency,spatialUrl:e.spatial_url,spatialName:e.spatial_text,spatial:e.spatial,start:e.temporal_start,end:e.temporal_end,storeType:t[a]})},commitUserterms:function(e,t){for(var a=0;a<t.length;a++)this.$store.commit("updateUserTerms",{selectedTab:e.selected_tab,termName:e.license_title,termNameUrl:e.license_url,usrRight:e.rights,contractType:e.trading_policy_contract_type,secrecy:e.trading_policy_nda,useApplication:e.trading_policy_use_application,useApplicationOther:e.trading_policy_use_application_free,redistributionRange:e.terms_of_use_redistribution_range,redistributionRangeOther:e.terms_of_use_redistribution_range_free,permissionResion:e.terms_of_use_permissible_region,permissionResionOther:e.terms_of_use_permissible_region_free,notices:e.terms_of_use_notices,personalData:e.privacy_policy_contains_personal_data,personalDataOther:e.privacy_policy_contains_personal_data_free,effectivePeriodOfDataSelectTerms:e.usage_period_effective_period_of_data_term,startDate:e.usage_period_effective_period_of_data_start,endDate:e.usage_period_effective_period_of_data_end,effectivePeriodOfDataFreefield:e.usage_period_effective_period_of_data_free,expirationPeriodSelectTerms:e.usage_period_expiration_period_term,deadline:e.usage_period_expiration_period_deadline,period:e.usage_period_expiration_period_period,unit:e.usage_period_expiration_period_unit,expirationPeriodFreefield:e.usage_period_expiration_period_free,fee:e.fee,salesInfoUrl:e.sales_info_url,priceRange:e.pricing_price_range,noticesOfPrice:e.pricing_notices_of_price,expressWarranty:e.warranty_express_warranty,expressWarrantyOther:e.warranty_express_warranty_free,leagalCompliance:e.warranty_legal_compliance,leagalComplianceOther:e.warranty_legal_compliance_free,storeType:t[a]})},setTemplate:function(){var e=this;d.a.get(u+"/template").then((function(t){if(console.log("テンプレ-ト取得値",t),"failed"!==t.data.status){e.checkWithDefault(t.data.template);var a=t.data.template.catalog_display;e.itemDisplayFlgStoreCommit(a);var i=t.data.template.catalog_value;e.commitDatasetinfo(i.datasetinfo,["state","template"]),e.commitDatajacket(i.datajacket,["template"]),e.commitDatasetoptionalinfo(i.datasetoptionalinfo,["state","template"]),e.commitUserterms(i.userterms,["state","template"])}}))},afterLoginProcess:function(){var e=["hold","another","template"];this.$store.commit("initField",e),this.$store.commit("initStateParams"),this.$store.commit("initItemListParams"),this.$store.commit("initCkanItemListParams"),this.getItemListValueLanguageList(),this.setItemList(),this.setTemplate()}},beforeDestroy:function(){var e=[];d.a.post(u+"/licenselist").then((function(t){if(200===t.status)for(var a=t.data,i=0;i<a.length;i++)e.push({label:a[i].title,value:a[i].id,url:a[i].url});else console.log("ライセンスリストの取得に失敗しました")})),this.$store.commit("updateCkanItemList",{licenseId:e})}},_=p,m=(a("1139"),a("2877")),g=a("4d5a"),f=a("f09f"),v=a("a370"),y=a("27f9"),h=a("0016"),b=a("9c40"),P=a("eebe"),C=a.n(P),k=Object(m["a"])(_,i,r,!1,null,null,null);t["default"]=k.exports;C()(k,"components",{QLayout:g["a"],QCard:f["a"],QCardSection:v["a"],QInput:y["a"],QIcon:h["a"],QBtn:b["a"]})},1139:function(e,t,a){"use strict";var i=a("82e1"),r=a.n(i);r.a},"82e1":function(e,t,a){}}]);