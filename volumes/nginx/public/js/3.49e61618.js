(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([[3],{"37ca":function(e,a,t){"use strict";var s=function(){var e=this,a=e.$createElement,t=e._self._c||a;return t("div",[t("q-dialog",{attrs:{persistent:""},model:{value:e.dialogInfo.isDisplay,callback:function(a){e.$set(e.dialogInfo,"isDisplay",a)},expression:"dialogInfo.isDisplay"}},[t("q-card",{staticStyle:{"max-width":"25%",width:"100%"}},[t("q-card-section",{staticClass:"column items-center"},[t("div",{staticStyle:{width:"100%","text-align":"center"}},[e.dialogInfo.errorFlg?t("q-avatar",{attrs:{icon:"error","font-size":"30px","text-color":"red"}}):t("q-avatar",{attrs:{icon:"check_circle","font-size":"30px","text-color":"secondary"}}),t("span",{staticClass:"q-ml-sm"},[e._v(e._s(e.dialogInfo.message))])],1),e.dialogInfo.moveOtherPage?t("div",{staticClass:"q-mt-md"},[t("q-btn",{directives:[{name:"close-popup",rawName:"v-close-popup"}],attrs:{label:"閉じる",color:"primary"},on:{click:function(a){return e.$emit("close-dialog",e.dialogInfo.moveOtherPage)}}})],1):t("div",{staticClass:"q-mt-md"},[t("q-btn",{directives:[{name:"close-popup",rawName:"v-close-popup"}],attrs:{label:"閉じる",color:"primary"}})],1)])],1)],1)],1)},r=[],i={props:["dialogInfo"]},o=i,n=t("2877"),l=t("24e8"),c=t("f09f"),d=t("a370"),p=t("cb32"),m=t("9c40"),f=t("7f67"),u=t("eebe"),g=t.n(u),h=Object(n["a"])(o,s,r,!1,null,null,null);a["a"]=h.exports;g()(h,"components",{QDialog:l["a"],QCard:c["a"],QCardSection:d["a"],QAvatar:p["a"],QBtn:m["a"]}),g()(h,"directives",{ClosePopup:f["a"]})},"59b4":function(e,a,t){"use strict";t.r(a);var s=function(){var e=this,a=e.$createElement,t=e._self._c||a;return"userlist"===e.nowDisplay?t("div",{staticClass:"col-12"},[t("UserList")],1):t("div",{staticClass:"col-12"},[t("UserForm")],1)},r=[],i=function(){var e=this,a=e.$createElement,t=e._self._c||a;return t("div",{staticClass:"q-layout-padding flex justify-center content-center"},[t("q-card",{staticClass:"q-card-background-white",staticStyle:{"max-width":"95%",width:"100%"},attrs:{"q-card":""}},[t("q-card-section",[t("div",{staticClass:"row justify-center items-center full-width"},[t("q-table",{staticClass:"full-width",attrs:{title:"ユーザ一覧",data:e.userList,columns:e.columns,separator:"cell",pagination:e.pagination,"row-key":"name"},on:{"update:pagination":function(a){e.pagination=a}},scopedSlots:e._u([{key:"top",fn:function(){return[t("div",{staticClass:"q-table__title text-weight-bolder full-width row justify-between"},[t("font",{attrs:{size:"5",color:"#1d468f"}},[e._v("ユーザ一覧")]),t("q-btn",{attrs:{size:"md",color:"light-blue-10",label:"新規登録"},on:{click:function(a){e.$parent.formType="new",e.$parent.nowDisplay="userform"}}})],1)]},proxy:!0},{key:"body",fn:function(a){return[t("q-tr",{attrs:{props:a}},[t("q-td",{key:"name",attrs:{props:a}},[t("div",{staticClass:"indent-cell"},[e._v(e._s(a.row.name))])]),t("q-td",{key:"name",attrs:{props:a}},[t("div",{staticClass:"indent-cell"},[e._v(e._s(a.row.organization))])]),t("q-td",{key:"name",attrs:{props:a}},[t("div",{staticClass:"indent-cell"},[e._v(e._s(a.row.email))])]),t("q-td",{key:"name",attrs:{props:a}},[t("div",{staticClass:"indent-cell",staticStyle:{"min-width":"66px"}},[e._v(e._s(a.row.created))])]),t("q-td",{key:"update",attrs:{props:a}},[t("q-btn",{staticClass:"full-width",staticStyle:{"font-size":"1em","min-width":"100px"},attrs:{outline:"",color:"secondary",icon:"edit",label:"編集"},on:{click:function(t){e.$parent.username=a.row.name,e.$parent.formType="edit",e.$parent.nowDisplay="userform"}}})],1),t("q-td",{key:"editPass",attrs:{props:a}},[t("q-btn",{staticClass:"full-width",staticStyle:{"font-size":"1em","min-width":"170px"},attrs:{outline:"",color:"secondary",icon:"lock",label:"パスワード変更"},on:{click:function(t){e.passUpdateDialog.isDisplay=!0,e.passUpdateDialog.userName=a.row.name,e.passUpdateDialog.email=a.row.email}}})],1),t("q-td",{key:"delete",attrs:{props:a}},[t("q-btn",{staticClass:"full-width",staticStyle:{"font-size":"1em","min-width":"100px"},attrs:{outline:"",color:"red",icon:"delete",label:"削除"},on:{click:function(t){e.deleteDialog.isDisplay=!0,e.deleteDialog.userName=a.row.name}}})],1)],1)]}}])})],1)])],1),t("CompleteDialog",{attrs:{dialogInfo:e.completeDialog}}),t("DeleteDialog",{attrs:{dialogInfo:e.deleteDialog},on:{"delete-user-data":e.deleteUser}}),t("PasswordUpdateDialog",{ref:"passwordUpdateDialog",attrs:{dialogInfo:e.passUpdateDialog},on:{"update-pass":e.updatePass}})],1)},o=[],n=t("bc3a"),l=t.n(n),c=t("f508"),d=t("37ca"),p=t("d6bd"),m=function(){var e=this,a=e.$createElement,t=e._self._c||a;return t("div",[t("q-dialog",{attrs:{persistent:"","transition-show":"scale","transition-hide":"scale"},model:{value:e.dialogInfo.isDisplay,callback:function(a){e.$set(e.dialogInfo,"isDisplay",a)},expression:"dialogInfo.isDisplay"}},[t("q-card",{staticStyle:{"max-width":"45%",width:"100%"}},[t("q-bar",{staticClass:"bg-primary text-white"},[t("q-icon",{attrs:{name:"lock"}}),t("div",[t("font",{attrs:{size:"3"}},[e._v("パスワード設定")])],1),t("q-space")],1),t("q-card-section",[t("div",{staticClass:"column"},[t("div",{staticClass:"row items-center justify-center q-py-sm"},[t("q-input",{ref:"oldPass",staticStyle:{width:"95%"},attrs:{outlined:"",dense:"",rules:[e.requiredRule,e.passwordRules.minlength,e.passwordRules.regex],"hide-bottom-space":""},scopedSlots:e._u([{key:"before",fn:function(){return[t("div",{staticClass:"text-right indent-cell",staticStyle:{width:"162px","text-align":"right",color:"#000"}},[t("font",{attrs:{size:"3"}},[e._v("古いパスワード ： ")])],1)]},proxy:!0}]),model:{value:e.oldPass,callback:function(a){e.oldPass=a},expression:"oldPass"}})],1),t("div",{staticClass:"row items-center justify-center q-py-sm"},[t("q-input",{ref:"newPass",staticStyle:{width:"95%"},attrs:{outlined:"",dense:"",rules:[e.requiredRule,e.passwordRules.minlength,e.passwordRules.regex],"hide-bottom-space":""},scopedSlots:e._u([{key:"before",fn:function(){return[t("div",{staticClass:"text-right indent-cell",staticStyle:{width:"162px","text-align":"right",color:"#000"}},[t("font",{attrs:{size:"3"}},[e._v("新しいパスワード ： ")])],1)]},proxy:!0}]),model:{value:e.newPass,callback:function(a){e.newPass=a},expression:"newPass"}})],1),t("div",{staticClass:"row items-center justify-center q-py-sm"},[t("q-input",{ref:"checkNewPass",staticStyle:{width:"95%"},attrs:{outlined:"",dense:"",rules:[e.requiredRule,e.passwordRules.minlength,e.passwordRules.checkPass,e.passwordRules.regex],"hide-bottom-space":""},scopedSlots:e._u([{key:"before",fn:function(){return[t("div",{staticClass:"text-right indent-cell",staticStyle:{width:"162px","text-align":"right",color:"#000"}},[t("font",{attrs:{size:"3"}},[e._v("パスワードの確認 ： ")])],1)]},proxy:!0}]),model:{value:e.checkNewPass,callback:function(a){e.checkNewPass=a},expression:"checkNewPass"}})],1)])]),t("q-card-section",{staticStyle:{"padding-top":"0"}},[t("div",{staticClass:"q-gutter-md row justify-center"},[t("q-btn",{directives:[{name:"close-popup",rawName:"v-close-popup"}],attrs:{color:"light-blue-10 col",label:"キャンセル"},on:{click:function(a){e.oldPass="",e.newPass="",e.checkNewPass=""}}}),t("q-btn",{directives:[{name:"close-popup",rawName:"v-close-popup"}],attrs:{color:"red col",label:"変更"},on:{click:e.validate}})],1)])],1)],1)],1)},f=[],u={props:["dialogInfo"],data:function(){var e=this;return{requiredRule:function(e){return e&&!!e||"入力必須項目"},passwordRules:{minlength:function(e){return e&&e.length>=12||"パスワードは12文字以上にしてください。"},checkPass:function(a){return a===e.$refs.newPass.value||"新しいパスワードと同じパスワードを入力してください。"},regex:function(e){return/^(?=.*[!-/:-@[-`{-~])(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])[!-~]{12,}$/.test(e)||"パスワードは半角英大文字、半角英小文字、半角数字、半角記号の4種類すべてを含む必要があります。"}},oldPass:"",newPass:"",checkNewPass:""}},methods:{validate:function(){this.$refs.oldPass.validate(),this.$refs.newPass.validate(),this.$refs.checkNewPass.validate(),this.$refs.oldPass.hasError||this.$refs.newPass.hasError||this.$refs.checkNewPass.hasError?(console.log("this.$refs.oldPass.hasError : "+this.$refs.oldPass.hasError),console.log("this.$refs.newPass.hasError : "+this.$refs.newPass.hasError),console.log("this.$refs.checkNewPass.hasError : "+this.$refs.checkNewPass.hasError)):(this.$props.dialogInfo.password=this.checkNewPass,this.$emit("update-pass",this.$props.dialogInfo))},initField:function(){this.oldPass="",this.newPass="",this.checkNewPass=""}}},g=u,h=(t("8071"),t("2877")),k=t("24e8"),v=t("f09f"),w=t("d847"),y=t("0016"),C=t("2c91"),b=t("a370"),q=t("27f9"),_=t("9c40"),x=t("7f67"),U=t("eebe"),$=t.n(U),D=Object(h["a"])(g,m,f,!1,null,null,null),z=D.exports;$()(D,"components",{QDialog:k["a"],QCard:v["a"],QBar:w["a"],QIcon:y["a"],QSpace:C["a"],QCardSection:b["a"],QInput:q["a"],QBtn:_["a"]}),$()(D,"directives",{ClosePopup:x["a"]});var P={components:{CompleteDialog:d["a"],DeleteDialog:p["a"],PasswordUpdateDialog:z},data:function(){return{pagination:{rowsPerPage:10},selectedUser:"",completeDialog:{isDisplay:!1,message:"",errorFlg:!1,moveOtherPage:""},passUpdateDialog:{isDisplay:!1,userName:"",email:"",password:""},deleteDialog:{pageName:"userList",isDisplay:!1,userName:""},userList:[],columns:[{name:"name",label:"ユーザ名",field:"name",align:"left",sortable:!0},{name:"organization",label:"組織名",field:"organization",align:"left",sortable:!0},{name:"email",label:"メール",field:"email",align:"left",sortable:!0},{name:"created",label:"登録日",field:"created",align:"center",sortable:!0},{name:"update",field:"update",align:"center"},{name:"editPass",field:"editPass",align:"center"},{name:"delete",field:"delete",align:"center"}]}},methods:{fetchUserlist:function(){var e=this;c["a"].show(),l.a.get(this.api_prefix+"/userlist").then((function(a){c["a"].hide(),e.userList=a.data.userlist})).catch((function(e){c["a"].hide(),console.error(e),console.log(e.response.message)}))},deleteUser:function(e){var a=this;c["a"].show(),l.a.delete(this.api_prefix+"/users/"+e).then((function(e){c["a"].hide(),a.fetchUserlist(),a.completeDialog.message=e.data.message.release,console.log("横断CKAN: "+e.data.message.release+", 詳細CKAN: "+e.data.message.detail),a.completeDialog.isDisplay=!0})).catch((function(e){console.error(e),c["a"].hide(),a.fetchUserlist(),console.log(e.response.data.message.error+", 横断CKAN: "+e.response.data.message.release+", 詳細CKAN: "+e.response.data.message.detail)}))},updatePass:function(e){var a=this;c["a"].show(),console.log(e),l.a.put(this.api_prefix+"/users/password/"+e.userName,{email:e.email,password:e.password}).then((function(e){c["a"].hide(),a.fetchUserlist(),console.log(e),a.completeDialog.message=e.data.message.release,a.completeDialog.isDisplay=!0,a.$refs.passwordUpdateDialog.initField()})).catch((function(e){c["a"].hide(),console.log(e),a.fetchUserlist()}))}},created:function(){this.fetchUserlist()}},N=P,I=(t("740b"),t("4d5a")),S=t("eaac"),A=t("bd08"),M=t("db86"),Q=Object(h["a"])(N,i,o,!1,null,null,null),F=Q.exports;$()(Q,"components",{QLayout:I["a"],QCard:v["a"],QCardSection:b["a"],QTable:S["a"],QBtn:_["a"],QTr:A["a"],QTd:M["a"]});var R=function(){var e=this,a=e.$createElement,t=e._self._c||a;return t("div",[t("div",{staticClass:"q-layout-padding"},[t("q-card",{staticClass:"q-mt-sm q-card-background-white"},[t("q-card-section",[t("div",{staticClass:"col"},["new"===e.$parent.formType?t("div",[t("font",{attrs:{size:"5",color:"#1d468f"}},[e._v("ユーザ名")]),t("br"),e._v("\n            登録するユーザ名を入力してください。\n            "),t("q-input",{ref:"username",staticStyle:{"padding-left":"15px",width:"98%"},attrs:{rules:[e.checkHyphen,e.checkLength,e.noJapaneseRule.regex],counter:"",error:e.checkMandatory(e.form.username,"username"),"error-message":e.mandatoryMessage(e.form.username,"username")},model:{value:e.form.username,callback:function(a){e.$set(e.form,"username",a)},expression:"form.username"}})],1):t("div",[t("font",{attrs:{size:"5",color:"#1d468f"}},[e._v("ユーザ名")]),t("br"),e._v("\n            登録するユーザ名を入力してください。\n            "),t("q-input",{ref:"username",staticStyle:{"padding-left":"15px",width:"98%"},attrs:{disable:""},model:{value:e.form.username,callback:function(a){e.$set(e.form,"username",a)},expression:"form.username"}})],1),"new"===e.$parent.formType?t("div",{staticClass:"q-mt-md"},[t("font",{attrs:{size:"5",color:"#1d468f"}},[e._v("パスワード")]),t("br"),e._v("\n            登録するユーザのパスワードを入力してください。\n            "),t("q-input",{ref:"password",staticStyle:{"padding-left":"15px",width:"98%"},attrs:{type:e.isPwd?"password":"text",rules:[e.passRules.minlength,e.passRules.regex],error:e.checkMandatory(e.form.password,"password"),"error-message":e.mandatoryMessage(e.form.password,"password")},model:{value:e.form.password,callback:function(a){e.$set(e.form,"password",a)},expression:"form.password"}},[t("q-icon",{staticClass:"cursor-pointer",attrs:{size:"32px",name:e.isPwd?"visibility_off":"visibility"},on:{click:function(a){e.isPwd=!e.isPwd}}})],1)],1):e._e(),"internal"==e.form.ckan?t("div",{staticClass:"q-mt-md"},[t("font",{attrs:{size:"5",color:"#1d468f"}},[e._v("組織名")]),t("br"),e._v("\n            登録するユーザの組織名を入力してください。"),t("br"),e._v("\n            複数ある場合は、カンマ区切りで入力してください。"),t("br"),e._v("\n            例: org-a,org-b\n            "),t("q-input",{ref:"organization",staticStyle:{"padding-left":"15px",width:"98%"},attrs:{rules:[e.noJapaneseRule.regex,e.noLastCommaRule.regex],error:e.checkMandatory(e.form.organization,"organization"),"error-message":e.mandatoryMessage(e.form.organization,"organization")},model:{value:e.form.organization,callback:function(a){e.$set(e.form,"organization",a)},expression:"form.organization"}})],1):e._e(),t("div",{staticClass:"q-mt-md"},[t("font",{attrs:{size:"5",color:"#1d468f"}},[e._v("メール")]),t("br"),e._v("\n            登録するユーザのメールアドレスを入力してください。\n            "),t("q-input",{ref:"email",staticStyle:{"padding-left":"15px",width:"98%"},attrs:{rules:[e.emailRules.regex,e.checkHyphen],error:e.checkMandatory(e.form.email,"email"),"error-message":e.mandatoryMessage(e.form.email,"email")},model:{value:e.form.email,callback:function(a){e.$set(e.form,"email",a)},expression:"form.email"}})],1),t("div",{staticClass:"q-mb-md"},[t("div",{staticClass:"q-mt-md"},[t("font",{attrs:{size:"5",color:"#1d468f"}},[e._v("登録先カタログサイト")]),t("br"),e._v("\n              入力したカタログ情報の登録先カタログサイトを選択してください。\n              "),t("br"),t("q-radio",{attrs:{val:"internal",label:"ローカルカタログサイト"},model:{value:e.form.ckan,callback:function(a){e.$set(e.form,"ckan",a)},expression:"form.ckan"}}),t("q-radio",{attrs:{val:"external",label:"外部カタログサイト"},model:{value:e.form.ckan,callback:function(a){e.$set(e.form,"ckan",a)},expression:"form.ckan"}})],1),"external"===e.form.ckan?t("div",{staticClass:"q-mt-md"},[t("div",[t("font",{attrs:{size:"5",color:"#1d468f"}},[e._v("外部横断カタログサイトURL")]),t("br"),e._v("\n                外部のカタログサイトへ登録する場合、対象カタログサイトのURLを入力してください。\n                "),t("q-input",{ref:"releaseCkanUrl",staticStyle:{"padding-left":"15px",width:"98%"},attrs:{error:e.checkMandatory(e.form.releaseCkanUrl,"releaseCkanUrl"),"error-message":e.mandatoryMessage(e.form.releaseCkanUrl,"releaseCkanUrl")},model:{value:e.form.releaseCkanUrl,callback:function(a){e.$set(e.form,"releaseCkanUrl",a)},expression:"form.releaseCkanUrl"}})],1),t("div",{staticClass:"q-mt-md"},[t("font",{attrs:{size:"5",color:"#1d468f"}},[e._v("外部横断カタログサイトアプリキー")]),t("br"),e._v("\n                外部のカタログサイトへ登録する場合、対象カタログサイトのアプリキーを入力してください。\n                "),t("q-input",{ref:"releaseCkanApikey",staticStyle:{"padding-left":"15px",width:"98%"},attrs:{error:e.checkMandatory(e.form.releaseCkanApikey,"releaseCkanApikey"),"error-message":e.mandatoryMessage(e.form.releaseCkanApikey,"releaseCkanApikey")},model:{value:e.form.releaseCkanApikey,callback:function(a){e.$set(e.form,"releaseCkanApikey",a)},expression:"form.releaseCkanApikey"}})],1),t("div",{staticClass:"q-mt-md"},[t("font",{attrs:{size:"5",color:"#1d468f"}},[e._v("外部横断カタログサイトユーザ名")]),t("br"),e._v("\n                外部のカタログサイトへ登録する場合、対象カタログサイトのユーザ名を入力してください。\n                "),t("q-input",{ref:"releaseCkanUsername",staticStyle:{"padding-left":"15px",width:"98%"},attrs:{error:e.checkMandatory(e.form.releaseCkanUsername,"releaseCkanUsername"),"error-message":e.mandatoryMessage(e.form.releaseCkanUsername,"releaseCkanUsername")},model:{value:e.form.releaseCkanUsername,callback:function(a){e.$set(e.form,"releaseCkanUsername",a)},expression:"form.releaseCkanUsername"}})],1),t("div",{staticClass:"q-mt-md"},[t("font",{attrs:{size:"5",color:"#1d468f"}},[e._v("外部詳細カタログサイトURL")]),t("br"),e._v("\n                外部のカタログサイトへ登録する場合、対象カタログサイトのURLを入力してください。\n                "),t("q-input",{ref:"detailCkanUrl",staticStyle:{"padding-left":"15px",width:"98%"},attrs:{error:e.checkMandatory(e.form.detailCkanUrl,"detailCkanUrl"),"error-message":e.mandatoryMessage(e.form.detailCkanUrl,"detailCkanUrl")},model:{value:e.form.detailCkanUrl,callback:function(a){e.$set(e.form,"detailCkanUrl",a)},expression:"form.detailCkanUrl"}})],1),t("div",{staticClass:"q-mt-md"},[t("font",{attrs:{size:"5",color:"#1d468f"}},[e._v("外部詳細カタログサイトアプリキー")]),t("br"),e._v("\n                外部のカタログサイトへ登録する場合、対象カタログサイトのアプリキーを入力してください。\n                "),t("q-input",{ref:"detailCkanApikey",staticStyle:{"padding-left":"15px",width:"98%"},attrs:{error:e.checkMandatory(e.form.detailCkanApikey,"detailCkanApikey"),"error-message":e.mandatoryMessage(e.form.detailCkanApikey,"detailCkanApikey")},model:{value:e.form.detailCkanApikey,callback:function(a){e.$set(e.form,"detailCkanApikey",a)},expression:"form.detailCkanApikey"}})],1),t("div",{staticClass:"q-mt-md"},[t("font",{attrs:{size:"5",color:"#1d468f"}},[e._v("外部詳細カタログサイトユーザ名")]),t("br"),e._v("\n                外部のカタログサイトへ登録する場合、対象カタログサイトのユーザ名を入力してください。\n                "),t("q-input",{ref:"detailCkanUsername",staticStyle:{"padding-left":"15px",width:"98%"},attrs:{error:e.checkMandatory(e.form.detailCkanUsername,"detailCkanUsername"),"error-message":e.mandatoryMessage(e.form.detailCkanUsername,"detailCkanUsername")},model:{value:e.form.detailCkanUsername,callback:function(a){e.$set(e.form,"detailCkanUsername",a)},expression:"form.detailCkanUsername"}})],1)]):e._e()]),t("div",{directives:[{name:"show",rawName:"v-show",value:e.errorFlg,expression:"errorFlg"}]},[t("font",{attrs:{size:"3",color:"#FF0000"}},[e._v(e._s(e.errorMessage))])],1)])])],1),t("CompleteDialog",{attrs:{dialogInfo:e.completeDialog},on:{"close-dialog":function(a){e.$parent.nowDisplay=a}}}),t("q-footer",{attrs:{reveal:"",elevated:""}},[t("q-toolbar",{staticClass:"justify-between"},[t("q-btn",{attrs:{flat:"",color:"white",icon:"reply_all",label:"ユーザ一覧に戻る"},on:{click:function(a){e.$parent.nowDisplay="userlist"}}}),"new"===e.$parent.formType?t("div",[t("q-btn",{attrs:{flat:"",color:"white",icon:"save_alt",label:"登録"},on:{click:function(a){return e.validateForm()}}})],1):t("div",[t("q-btn",{attrs:{flat:"",color:"white",icon:"save_alt",label:"編集"},on:{click:function(a){return e.validateForm()}}})],1)],1)],1)],1)])},E=[],T=(t("c975"),t("cca6"),t("ac1f"),t("1276"),{components:{CompleteDialog:d["a"]},data:function(){return{isPwd:!0,pagination:{rowsPerPage:0},completeDialog:{isDisplay:!1,message:"",errorFlg:!1,moveOtherPage:"userlist"},errorFlg:!1,errorMessage:null,form:{username:"",password:"",email:"",organization:"",ckan:"internal",releaseCkanUrl:"",releaseCkanApikey:"",releaseCkanUsername:"",detailCkanUrl:"",detailCkanApikey:"",detailCkanUsername:""},defaultForm:{username:"",password:"",organization:"",email:"",ckan:"internal",releaseCkanUrl:"",releaseCkanApikey:"",releaseCkanUsername:"",detailCkanUrl:"",detailCkanApikey:"",detailCkanUsername:""},checkHyphen:function(e){return e&&-1===e.indexOf("-")||" - (ハイフン)は使用できません。"},checkLength:function(e){return e&&e.length>=2&&e.length<=100||"ユーザ名は2文字以上100文字以下で入力してください。"},passRules:{minlength:function(e){return e&&e.length>=12||"パスワードは12文字以上にしてください。"},regex:function(e){return/^(?=.*[!-/:-@[-`{-~])(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])[!-~]{12,}$/.test(e)||"パスワードは半角英大文字、半角英小文字、半角数字、半角記号の4種類すべてを含む必要があります。"}},emailRules:{regex:function(e){return/^(([^<>()[\]\\.,;:\s@]+(\.[^<>()[\]\\.,;:\s@]+)*)|(.+))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(e)||"メールアドレスを正しく入力してください。"}},noJapaneseRule:{regex:function(e){return/^[a-z0-9!-/:-@¥[-`{-~]*$/.test(e)||"半角英小文字半角数字半角記号で入力してください。"}},noLastCommaRule:{regex:function(e){return/^(?!.*,$).*$/.test(e)||"語尾に ,（カンマ）は使用できません。"}}}},watch:{"form.organization":function(e){"external"===e&&(this.form.organization="")}},methods:{validateForm:function(){for(var e in this.errorFlg=!1,this.form)if("edit"!==this.$parent.formType||"password"!==e){var a=this.checkMandatory(this.form[e],e);if(a){this.errorFlg=!0,this.errorMessage="入力内容に誤りがあります。";break}}"external"===this.form.ckan?(this.$refs.username.validate(),this.$refs.email.validate(),"new"===this.$parent.formType&&(this.$refs.password.validate(),this.$refs.password.hasError&&(this.errorFlg=!0,this.errorMessage="入力内容に誤りがあります。")),this.$refs.username.hasError||this.$refs.email.hasError||this.errorFlg?(this.errorFlg=!0,this.errorMessage="入力内容に誤りがあります。"):"new"===this.$parent.formType?this.createUser():this.updateUser()):(this.$refs.username.validate(),this.$refs.organization.validate(),this.$refs.email.validate(),"new"===this.$parent.formType&&(this.$refs.password.validate(),this.$refs.password.hasError&&(this.errorFlg=!0,this.errorMessage="入力内容に誤りがあります。")),this.$refs.username.hasError||this.$refs.organization.hasError||this.$refs.email.hasError||this.errorFlg?(this.errorFlg=!0,this.errorMessage="入力内容に誤りがあります。"):"new"===this.$parent.formType?this.createUser():this.updateUser())},initForm:function(){var e=this;"edit"===this.$parent.formType?l.a.get(this.api_prefix+"/users/"+this.$parent.username).then((function(a){e.form.username=a.data.username,e.form.email=a.data.email,e.form.organization=a.data.organization,e.form.ckan=a.data.ckan,"external"===a.data.ckan&&(e.form.releaseCkanUrl=a.data.about.release_ckan_url,e.form.releaseCkanApikey=a.data.about.release_ckan_apikey,e.form.detailCkanUrl=a.data.about.detail_ckan_url,e.form.detailCkanApikey=a.data.about.detail_ckan_apikey)})).catch((function(a){e.errorFlg=!0,e.errorMessage=a.response.data.message.detail,c["a"].hide()})):Object.assign(this.form,this.defaultForm)},createUser:function(){var e=this;c["a"].show(),this.form.organization=this.form.organization?this.form.organization.split(","):[],l.a.post(this.api_prefix+"/users",this.form).then((function(a){e.completeDialog.message="登録が完了しました。",console.log("横断CKAN: "+a.data.message.release+"詳細CKAN: "+a.data.message.detail),e.completeDialog.isDisplay=!0,c["a"].hide()})).catch((function(a){e.errorFlg=!0,console.log("エラー内容: "+a.response.data.error+", 横断CKAN: "+a.response.data.message.release+", 詳細CKAN: "+a.response.data.message.detail),e.errorMessage=a.response.data.message.release||a.response.data.message.detail,c["a"].hide()}))},updateUser:function(){var e=this;c["a"].show(),this.form.organization=this.form.organization?this.form.organization.split(","):[],l.a.put(this.api_prefix+"/users/"+this.form.username,this.form).then((function(a){e.completeDialog.message="登録が完了しました。",console.log("横断CKAN: "+a.data.message.release+"詳細CKAN: "+a.data.message.detail),e.completeDialog.isDisplay=!0,c["a"].hide()})).catch((function(a){e.errorFlg=!0,e.errorMessage="入力内容に誤りがあります。",console.log("エラー内容: ,"+a.response.data.error+", 横断CKAN: "+a.response.data.message.release+", 詳細CKAN: "+a.response.data.message.detail),c["a"].hide()}))},checkMandatory:function(e,a){if(!e)return("organization"!==a||"external"!==this.form.ckan)&&(!("detailCkanUrl"===a&&!this.form.detailCkanApikey&&!this.form.detailCkanUsername)&&(!("detailCkanApikey"===a&&!this.form.detailCkanUrl&&!this.form.detailCkanUsername)&&(!("detailCkanUsername"===a&&!this.form.detailCkanUrl&&!this.form.detailCkanApikey)&&("releaseCkanUrl"!==a&&"releaseCkanApikey"!==a&&"releaseCkanUsername"!==a||"internal"!==this.form.ckan))))},mandatoryMessage:function(e,a){if(!e)return"organization"===a&&"external"===this.form.ckan?"":("detailCkanUrl"!==a||this.form.detailCkanApikey||this.form.detailCkanUsername)&&("detailCkanApikey"!==a||this.form.detailCkanUrl||this.form.detailCkanUsername)&&("detailCkanUsername"!==a||this.form.detailCkanUrl||this.form.detailCkanApikey)&&("releaseCkanUrl"!==a&&"releaseCkanApikey"!==a&&"releaseCkanUsername"!==a||"internal"!==this.form.ckan)?"【入力必須項目】":""}},created:function(){this.initForm()}}),j=T,L=(t("6988"),t("3786")),O=t("7ff0"),K=t("65c6"),B=Object(h["a"])(j,R,E,!1,null,null,null),J=B.exports;$()(B,"components",{QLayout:I["a"],QCard:v["a"],QCardSection:b["a"],QInput:q["a"],QIcon:y["a"],QRadio:L["a"],QFooter:O["a"],QToolbar:K["a"],QBtn:_["a"]});var Z={components:{UserList:F,UserForm:J},data:function(){return{nowDisplay:"userlist",formType:"new",username:""}}},H=Z,G=Object(h["a"])(H,s,r,!1,null,null,null);a["default"]=G.exports},6119:function(e,a,t){},6988:function(e,a,t){"use strict";var s=t("da1b"),r=t.n(s);r.a},"740b":function(e,a,t){"use strict";var s=t("6119"),r=t.n(s);r.a},8071:function(e,a,t){"use strict";var s=t("9afa"),r=t.n(s);r.a},"9afa":function(e,a,t){},d6bd:function(e,a,t){"use strict";var s=function(){var e=this,a=e.$createElement,t=e._self._c||a;return t("div",["userList"===e.dialogInfo.pageName?[t("q-dialog",{attrs:{persistent:"","transition-show":"scale","transition-hide":"scale"},model:{value:e.dialogInfo.isDisplay,callback:function(a){e.$set(e.dialogInfo,"isDisplay",a)},expression:"dialogInfo.isDisplay"}},[t("q-card",{staticStyle:{"max-width":"35%",width:"100%"}},[t("div",{staticClass:"q-pa-md"},[t("q-card-section",[t("div",{staticClass:"text-center",staticStyle:{"overflow-wrap":"break-word"}},[t("font",{attrs:{size:"3"}},[e._v("ユーザ "),t("span",{staticStyle:{"font-weight":"bold"}},[e._v(e._s(e.dialogInfo.userName))]),e._v(" を削除しますか？")])],1),t("div",{staticClass:"q-gutter-md row justify-center q-mt-sm"},[t("q-btn",{directives:[{name:"close-popup",rawName:"v-close-popup"}],attrs:{color:"light-blue-10 col",label:"キャンセル"}}),t("q-btn",{directives:[{name:"close-popup",rawName:"v-close-popup"}],attrs:{color:"red col",label:"削除"},on:{click:function(a){return e.$emit("delete-user-data",e.dialogInfo.userName)}}})],1)])],1)])],1)]:e._e(),"searchOneDelete"===e.dialogInfo.pageName?[t("q-dialog",{attrs:{persistent:"","transition-show":"scale","transition-hide":"scale"},model:{value:e.dialogInfo.isDisplay,callback:function(a){e.$set(e.dialogInfo,"isDisplay",a)},expression:"dialogInfo.isDisplay"}},[t("q-card",{staticStyle:{"max-width":"35%",width:"100%"}},[t("div",{staticClass:"q-pa-md"},[t("q-card-section",["release"===e.dialogInfo.ckanType?t("div",{staticClass:"text-center",staticStyle:{"overflow-wrap":"break-word"}},[t("font",{attrs:{size:"3"}},[e._v("横断カタログ "),t("span",{staticStyle:{"font-weight":"bold"}},[e._v(e._s(e.dialogInfo.catalogName))]),e._v(" を削除しますか？")])],1):e._e(),"detail"===e.dialogInfo.ckanType?t("div",{staticClass:"text-center",staticStyle:{"overflow-wrap":"break-word"}},[t("font",{attrs:{size:"3"}},[e._v("詳細カタログ "),t("span",{staticStyle:{"font-weight":"bold"}},[e._v(e._s(e.dialogInfo.catalogName))]),e._v(" を削除しますか？")])],1):e._e(),"both"===e.dialogInfo.ckanType?t("div",{staticClass:"text-center",staticStyle:{"overflow-wrap":"break-word"}},[t("font",{attrs:{size:"3"}},[e._v("紐づく詳細カタログをもつ横断カタログは削除できません。")])],1):e._e(),"release"===e.dialogInfo.ckanType||"detail"===e.dialogInfo.ckanType?t("div",{staticClass:"q-gutter-md row justify-center q-mt-sm"},[t("q-btn",{directives:[{name:"close-popup",rawName:"v-close-popup"}],attrs:{color:"light-blue-10 col",label:"キャンセル"}}),t("q-btn",{directives:[{name:"close-popup",rawName:"v-close-popup"}],attrs:{color:"red col",label:"削除"},on:{click:function(a){return e.$emit("delete-one-catalog-data",e.dialogInfo)}}})],1):e._e(),"both"===e.dialogInfo.ckanType?t("div",{staticClass:"q-gutter-md row justify-center q-mt-sm"},[t("q-btn",{directives:[{name:"close-popup",rawName:"v-close-popup"}],attrs:{color:"light-blue-10 col",label:"キャンセル"}})],1):e._e()])],1)])],1)]:e._e(),"searchSelectedDelete"===e.dialogInfo.pageName?[t("q-dialog",{attrs:{persistent:"","transition-show":"scale","transition-hide":"scale"},model:{value:e.dialogInfo.isDisplay,callback:function(a){e.$set(e.dialogInfo,"isDisplay",a)},expression:"dialogInfo.isDisplay"}},[t("q-card",{staticStyle:{"max-width":"35%",width:"100%"}},[t("div",{staticClass:"q-pa-md"},[t("q-card-section",[t("div",{staticClass:"text-center",staticStyle:{"overflow-wrap":"break-word"}},[t("font",{attrs:{size:"3"}},[e._v("選択したデータを削除しますか？")])],1),t("div",{staticClass:"q-gutter-md row justify-center q-mt-sm"},[t("q-btn",{directives:[{name:"close-popup",rawName:"v-close-popup"}],attrs:{color:"light-blue-10 col",label:"キャンセル"}}),t("q-btn",{directives:[{name:"close-popup",rawName:"v-close-popup"}],attrs:{color:"red col",label:"削除"},on:{click:function(a){return e.$emit("delete-selected-catalog-data")}}})],1)])],1)])],1)]:e._e(),"selectDraftOneDelete"===e.dialogInfo.pageName?[t("q-dialog",{attrs:{persistent:"","transition-show":"scale","transition-hide":"scale"},model:{value:e.dialogInfo.isDisplay,callback:function(a){e.$set(e.dialogInfo,"isDisplay",a)},expression:"dialogInfo.isDisplay"}},[t("q-card",{staticStyle:{"max-width":"35%",width:"100%"}},[t("div",{staticClass:"q-pa-md"},[t("q-card-section",[t("div",{staticClass:"text-center",staticStyle:{"overflow-wrap":"break-word"}},[t("font",{attrs:{size:"3"}},[e._v("一時保存データ "),t("span",{staticStyle:{"font-weight":"bold"}},[e._v(e._s(e.dialogInfo.catalogName))]),e._v(" を削除しますか？")])],1),t("div",{staticClass:"q-gutter-md row justify-center q-mt-sm"},[t("q-btn",{directives:[{name:"close-popup",rawName:"v-close-popup"}],attrs:{color:"light-blue-10 col",label:"キャンセル"}}),t("q-btn",{directives:[{name:"close-popup",rawName:"v-close-popup"}],attrs:{color:"red col",label:"削除"},on:{click:function(a){return e.$emit("delete-one-catalog-data",e.dialogInfo.catalogName)}}})],1)])],1)])],1)]:e._e(),"selectDraftSelectedDelete"===e.dialogInfo.pageName?[t("q-dialog",{attrs:{persistent:"","transition-show":"scale","transition-hide":"scale"},model:{value:e.dialogInfo.isDisplay,callback:function(a){e.$set(e.dialogInfo,"isDisplay",a)},expression:"dialogInfo.isDisplay"}},[t("q-card",{staticStyle:{"max-width":"35%",width:"100%"}},[t("div",{staticClass:"q-pa-md"},[t("q-card-section",[t("div",{staticClass:"text-center",staticStyle:{"overflow-wrap":"break-word"}},[t("font",{attrs:{size:"3"}},[e._v("選択したデータを削除しますか？")])],1),t("div",{staticClass:"q-gutter-md row justify-center q-mt-sm"},[t("q-btn",{directives:[{name:"close-popup",rawName:"v-close-popup"}],attrs:{color:"light-blue-10 col",label:"キャンセル"}}),t("q-btn",{directives:[{name:"close-popup",rawName:"v-close-popup"}],attrs:{color:"red col",label:"削除"},on:{click:function(a){return e.$emit("delete-selected-catalog-data")}}})],1)])],1)])],1)]:e._e()],2)},r=[],i={props:["dialogInfo"]},o=i,n=t("2877"),l=t("24e8"),c=t("f09f"),d=t("a370"),p=t("9c40"),m=t("7f67"),f=t("eebe"),u=t.n(f),g=Object(n["a"])(o,s,r,!1,null,null,null);a["a"]=g.exports;u()(g,"components",{QDialog:l["a"],QCard:c["a"],QCardSection:d["a"],QBtn:p["a"]}),u()(g,"directives",{ClosePopup:m["a"]})},da1b:function(e,a,t){}}]);