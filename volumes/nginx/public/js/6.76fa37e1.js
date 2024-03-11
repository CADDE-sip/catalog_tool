(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([[6],{"0e74":function(a,t,e){"use strict";var i=e("9b5d"),o=e.n(i);o.a},"37ca":function(a,t,e){"use strict";var i=function(){var a=this,t=a.$createElement,e=a._self._c||t;return e("div",[e("q-dialog",{attrs:{persistent:""},model:{value:a.dialogInfo.isDisplay,callback:function(t){a.$set(a.dialogInfo,"isDisplay",t)},expression:"dialogInfo.isDisplay"}},[e("q-card",{staticStyle:{"max-width":"25%",width:"100%"}},[e("q-card-section",{staticClass:"column items-center"},[e("div",{staticStyle:{width:"100%","text-align":"center"}},[a.dialogInfo.errorFlg?e("q-avatar",{attrs:{icon:"error","font-size":"30px","text-color":"red"}}):e("q-avatar",{attrs:{icon:"check_circle","font-size":"30px","text-color":"secondary"}}),e("span",{staticClass:"q-ml-sm"},[a._v(a._s(a.dialogInfo.message))])],1),a.dialogInfo.moveOtherPage?e("div",{staticClass:"q-mt-md"},[e("q-btn",{directives:[{name:"close-popup",rawName:"v-close-popup"}],attrs:{label:"閉じる",color:"primary"},on:{click:function(t){return a.$emit("close-dialog",a.dialogInfo.moveOtherPage)}}})],1):e("div",{staticClass:"q-mt-md"},[e("q-btn",{directives:[{name:"close-popup",rawName:"v-close-popup"}],attrs:{label:"閉じる",color:"primary"}})],1)])],1)],1)],1)},o=[],l={props:["dialogInfo"]},s=l,r=e("2877"),n=e("24e8"),c=e("f09f"),d=e("a370"),p=e("cb32"),u=e("9c40"),g=e("7f67"),m=e("eebe"),f=e.n(m),v=Object(r["a"])(s,i,o,!1,null,null,null);t["a"]=v.exports;f()(v,"components",{QDialog:n["a"],QCard:c["a"],QCardSection:d["a"],QAvatar:p["a"],QBtn:u["a"]}),f()(v,"directives",{ClosePopup:g["a"]})},"9b5d":function(a,t,e){},a76b:function(a,t,e){"use strict";e.r(t);var i=function(){var a=this,t=a.$createElement,e=a._self._c||t;return e("div",{staticClass:"col-5"},[[e("div",[e("q-card",{staticClass:"q-card-background-white"},[e("q-card-section",[e("div",{staticClass:"col"},[e("div",{staticClass:"q-mb-md row items-center"},[e("div",{staticClass:"col-4"},[e("font",{attrs:{size:"3",color:"#1d468f"}},[a._v("インポート先")])],1),e("div",{staticClass:"col-8 flex justify-start"},[e("q-radio",{attrs:{val:"releaseCkan",label:"横断カタログ",color:"light-blue-10"},model:{value:a.importCkanType,callback:function(t){a.importCkanType=t},expression:"importCkanType"}}),a.$store.state.loginInfo.detailCkanAddr?e("div",[e("q-radio",{staticStyle:{"margin-left":"16px"},attrs:{val:"detailCkan",label:"詳細カタログ",color:"light-blue-10"},model:{value:a.importCkanType,callback:function(t){a.importCkanType=t},expression:"importCkanType"}})],1):a._e()],1)]),e("div",{staticClass:"q-mb-md row"},[e("div",{staticClass:"col-4"},[e("font",{attrs:{size:"3",color:"#1d468f"}},[a._v("読み込みファイル")])],1),e("div",{staticClass:"col-8"},[e("q-uploader",{staticStyle:{width:"100%"},attrs:{multiple:"","field-name":"file",url:a.importURL,filter:a.checkFileType,"max-files":"1"},on:{rejected:a.onRejected,failed:function(t){return a.errorMsg()},uploaded:function(t){return a.uploadedMsg()}},scopedSlots:a._u([{key:"header",fn:function(t){return[e("div",{staticClass:"row no-wrap items-center q-pa-sm q-gutter-xs"},[t.isUploading?e("q-spinner",{staticClass:"q-uploader__spinner"}):a._e(),e("div",{staticClass:"col"},[e("div",{staticClass:"q-uploader__title"},[a._v("Import files")]),e("div",{staticClass:"q-uploader__subtitle"},[a._v(a._s(t.uploadSizeLabel)+" / "+a._s(t.uploadProgressLabel))])]),t.canAddFiles?e("q-btn",{attrs:{type:"a",icon:"add_box",round:"",dense:"",flat:""}},[e("q-uploader-add-trigger"),e("q-tooltip",[a._v("Add File")])],1):a._e(),t.canUpload?e("q-btn",{attrs:{icon:"cloud_upload",round:"",dense:"",flat:""},on:{click:t.upload}},[e("q-tooltip",[a._v("Import Files")])],1):a._e()],1)]}}])})],1)])])])],1)],1)],e("CompleteDialog",{attrs:{dialogInfo:a.dialog}})],2)},o=[],l=(e("4de4"),e("37ca")),s="/api/v1/catalog/tool",r={components:{CompleteDialog:l["a"]},data:function(){return{localFileUrl:"/api/v1/catalog/tool/uploads",dialog:{isDisplay:!1,message:"",errorFlg:!1,moveOtherPage:""},importCkanType:"releaseCkan",localFileData:[]}},computed:{importURL:function(){var a=s+"/import/release";return"detailCkan"===this.importCkanType&&(a=s+"/import/detail"),a}},methods:{checkFileType:function(a){return a.filter((function(a){return"application/x-gzip"===a.type||"application/gzip"===a.type}))},onRejected:function(a){console.log(a),this.dialog.errorFlg=!0,this.dialog.message="gz形式のファイルを選択してください。",this.dialog.isDisplay=!0},uploadedMsg:function(){this.dialog.errorFlg=!1,this.dialog.message="インポートが完了しました。",this.dialog.isDisplay=!0},errorMsg:function(){this.dialog.errorFlg=!0,this.dialog.message="インポートに失敗しました。",this.dialog.isDisplay=!0}}},n=r,c=(e("0e74"),e("2877")),d=e("f09f"),p=e("a370"),u=e("3786"),g=e("ee89"),m=e("0d59"),f=e("9c40"),v=e("cc04"),C=e("05c0"),b=e("eebe"),q=e.n(b),y=Object(c["a"])(n,i,o,!1,null,null,null);t["default"]=y.exports;q()(y,"components",{QCard:d["a"],QCardSection:p["a"],QRadio:u["a"],QUploader:g["a"],QSpinner:m["a"],QBtn:f["a"],QUploaderAddTrigger:v["a"],QTooltip:C["a"]})}}]);