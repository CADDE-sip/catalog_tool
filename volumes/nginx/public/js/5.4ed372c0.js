(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([[5],{"37c0":function(e,t,n){"use strict";var a=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("q-item",{attrs:{clickable:"",tag:"a",target:"_blank",href:e.link}},[e.icon?n("q-item-section",{attrs:{avatar:""}},[n("q-icon",{attrs:{name:e.icon}})],1):e._e(),n("q-item-section",[n("q-item-label",[e._v(e._s(e.title))]),n("q-item-label",{attrs:{caption:""}},[e._v("\n      "+e._s(e.caption)+"\n    ")])],1)],1)},o=[],r={name:"EssentialLink",props:{title:{type:String,required:!0},caption:{type:String,default:""},link:{type:String,default:"#"},icon:{type:String,default:""}}},i=r,l=n("2877"),s=n("66e5"),c=n("4074"),u=n("0016"),f=n("0170"),d=n("eebe"),p=n.n(d),h=Object(l["a"])(i,a,o,!1,null,null,null);t["a"]=h.exports;p()(h,"components",{QItem:s["a"],QItemSection:c["a"],QIcon:u["a"],QItemLabel:f["a"]})},"49de":function(e,t,n){"use strict";(function(e){n("c975");var a=n("37c0");t["a"]={name:"MainLayout",components:{EssentialLink:a["a"]},data:function(){return{leftDrawerOpen:!1,user_name:"ゲスト",user_apikey:"",main_title:"",sub_title:"",ckanURL:"https://www.data-linkage.jp/",essentialLinks:[{title:"Docs",caption:"quasar.dev",icon:"school",link:"https://quasar.dev"},{title:"Forum",caption:"forum.quasar.dev",icon:"record_voice_over",link:"https://forum.quasar.dev"}]}},mounted:function(){var e=this;this.$store.watch((function(e,t){return t.user_name}),(function(t,n){e.user_name=t}))},created:function(){var t=this,n=this.$data;this.$root.$on("updateHeaderTitle",(function(e){n.main_title=e})),e.browser,this.$router.beforeEach((function(e,n,a){if("/"===e.fullPath&&"/regist"===n.fullPath||"/login"===e.fullPath&&"/regist"===n.fullPath){var o=confirm("ページを移動すると入力データがリセットされます");o?(t.$store.state.user_name="ゲスト",t.$store.state.user_pass="",a(),t.leftDrawerOpen=!1):(window.alert("キャンセルしました"),t.leftDrawerOpen=!1)}else a(),t.leftDrawerOpen=!1}))},watch:{"this.$store.state.user_name":function(e,t){this.user_name=e}},methods:{btnPageDown:function(){scrollTo({top:9999,behavior:"smooth"});var e=window.navigator.userAgent;console.log(e),-1!==e.indexOf("MSIE")||-1!==e.indexOf("trident")?(console.log("Internet Explorer"),scrollTo(0,9999)):-1!==e.indexOf("Edge")?(console.log("Edge"),scrollTo(0,9999)):-1!==e.indexOf("Chrome")?(console.log("Google Chrome"),window.scroll({top:9999,behavior:"smooth"})):-1!==e.indexOf("Safari")?(console.log("Safari"),scrollTo(0,9999)):-1!==e.indexOf("Firefox")?(console.log("Firefox"),window.scroll({top:9999,behavior:"smooth"})):-1!==e.indexOf("Opera")?(console.log("Opera"),scrollTo(0,9999)):(console.log("未知ブラウザ"),scrollTo(0,9999))},btnCkanPage:function(){window.open(this.ckanURL)},btnLogout:function(){this.$router.push("/login")}}}}).call(this,n("4362"))},"713b":function(e,t,n){"use strict";n.r(t);var a=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("q-layout",{attrs:{view:"lHh Lpr lFf"}},[n("q-header",{attrs:{elevated:""}},[n("q-toolbar",[n("q-btn",{attrs:{flat:"",dense:"",round:"",icon:"menu","aria-label":"Menu"},on:{click:function(t){e.leftDrawerOpen=!e.leftDrawerOpen}}}),n("q-toolbar-title",[e._v("\n        データカタログ作成支援ツール\n      ")]),n("q-icon",{staticStyle:{"padding-right":"20px"},attrs:{size:"32px",name:"person"}}),n("q-input",{attrs:{dark:"",color:"#1d468f",flat:"",readonly:"","hide-underline":""},model:{value:e.user_name,callback:function(t){e.user_name=t},expression:"user_name"}}),n("q-btn",{attrs:{size:"gl",color:"light-blue-9","text-color":"white",label:"ログアウト"},on:{click:function(t){return e.btnLogout()}}})],1)],1),n("q-drawer",{attrs:{"show-if-above":"",bordered:"","content-class":"bg-grey-1"},model:{value:e.leftDrawerOpen,callback:function(t){e.leftDrawerOpen=t},expression:"leftDrawerOpen"}},[n("q-list",[n("q-item-label",{staticClass:"text-grey-8",attrs:{header:""}},[e._v("\n        Essential Links\n      ")]),e._l(e.essentialLinks,(function(t){return n("EssentialLink",e._b({key:t.title},"EssentialLink",t,!1))}))],2)],1),n("q-page-container",[n("router-view")],1)],1)},o=[],r=n("49de"),i=r["a"],l=n("2877"),s=n("4d5a"),c=n("e359"),u=n("65c6"),f=n("9c40"),d=n("6ac5"),p=n("0016"),h=n("27f9"),m=n("9404"),b=n("1c1c"),w=n("0170"),g=n("09e3"),v=n("eebe"),_=n.n(v),k=Object(l["a"])(i,a,o,!1,null,null,null);t["default"]=k.exports;_()(k,"components",{QLayout:s["a"],QHeader:c["a"],QToolbar:u["a"],QBtn:f["a"],QToolbarTitle:d["a"],QIcon:p["a"],QInput:h["a"],QDrawer:m["a"],QList:b["a"],QItemLabel:w["a"],QPageContainer:g["a"]})}}]);