(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([[4],{"37c0":function(t,e,a){"use strict";var s=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[t.$store.state.loginInfo.releaseCkanAddr?[a("q-list",{attrs:{"no-border":"",link:"","inset-delimiter":""}},[t.$store.state.loginInfo.sysadmin?a("div",[a("q-item",[a("q-item-section",[a("q-expansion-item",{attrs:{label:"管理","default-opened":""}},[a("div",{staticClass:"text-center"},[a("div",{staticClass:"q-py-xs"},[a("q-btn",{staticClass:"btn-fixed-width",staticStyle:{},attrs:{flat:"",label:"ユーザ管理",align:"left"},on:{click:function(e){return t.btnMoveUserList()}}})],1)])])],1)],1)],1):t._e(),a("q-item",[a("q-item-section",[a("q-expansion-item",{attrs:{label:"カタログ作成","default-opened":""}},[a("div",{staticClass:"text-center"},[a("div",{staticClass:"q-py-xs"},[a("q-btn",{staticClass:"btn-fixed-width",staticStyle:{},attrs:{flat:"",label:"新規登録",align:"left"},on:{click:function(e){return t.btnMoveRegistration()}}})],1),a("div",{staticClass:"q-py-xs"},[a("q-btn",{staticClass:"btn-fixed-width",staticStyle:{},attrs:{flat:"",label:"登録再開",align:"left"},on:{click:function(e){return t.btnMoveRestart()}}})],1),a("div",{staticClass:"q-py-xs"},[a("q-btn",{staticClass:"btn-fixed-width",staticStyle:{},attrs:{flat:"",label:"複製・編集・削除",align:"left"},on:{click:function(e){return t.btnMoveSearch()}}})],1)])])],1)],1),a("q-item",[a("q-item-section",[a("q-expansion-item",{attrs:{label:"ユーティリティ","default-opened":""}},[a("div",{staticClass:"text-center"},[a("div",{staticClass:"q-py-xs"},[a("q-btn",{staticClass:"btn-fixed-width",staticStyle:{},attrs:{flat:"",label:"インポート",align:"left"},on:{click:function(e){return t.btnMoveImport()}}})],1),a("div",{staticClass:"q-py-xs"},[a("q-btn",{staticClass:"btn-fixed-width",staticStyle:{},attrs:{flat:"",label:"エクスポート",align:"left"},on:{click:function(e){return t.btnMoveExport()}}})],1)])])],1)],1),a("q-item",[a("q-item-section",[a("q-expansion-item",{attrs:{label:"設定","default-opened":""}},[a("div",{staticClass:"text-center"},[a("div",{staticClass:"q-py-xs"},[a("q-btn",{staticClass:"btn-fixed-width",staticStyle:{},attrs:{flat:"",label:"テンプレート編集",align:"left"},on:{click:function(e){return t.btnMoveTemplate()}}}),a("div")],1)])])],1)],1)],1)]:t._e()],2)},o=[],i=["hold","another"],n={methods:{btnMoveRegistration:function(){if(this.$store.commit("initStateParams"),this.$store.commit("initField",i),this.$store.commit("updateMode",{mode:"register",ckanType:"",isBothCatalog:!1}),"/register"!==this.$router.currentRoute.fullPath)this.$router.push("/register");else{var t=!0!==this.$store.state.createNewCatalog;this.$store.commit("pushCreate",{createNewCatalog:t})}},btnMoveSearch:function(){this.$store.commit("initStateParams"),this.$store.commit("initField",i),"/search"!==this.$router.currentRoute.fullPath&&this.$router.push("/search")},btnMoveRestart:function(){this.$store.commit("initStateParams"),this.$store.commit("initField",i),"/selectDraft"!==this.$router.currentRoute.fullPath&&this.$router.push("/selectDraft")},btnMoveUserList:function(){this.$store.commit("updateMode",{mode:"userManagement",ckanType:"",isBothCatalog:!1}),"/userManager"!==this.$router.currentRoute.fullPath&&this.$router.push("/userManager")},btnMoveImport:function(){this.$store.commit("updateMode",{mode:"import",ckanType:"",isBothCatalog:!1}),"/import"!==this.$router.currentRoute.fullPath&&this.$router.push("/import")},btnMoveExport:function(){this.$store.commit("updateMode",{mode:"export",ckanType:"",isBothCatalog:!1}),"/export"!==this.$router.currentRoute.fullPath&&this.$router.push("/export")},btnMoveTemplate:function(){if(this.$store.commit("initStateParams"),this.$store.commit("initField",i),this.$store.commit("updateMode",{mode:"template",ckanType:"",isBothCatalog:!1}),"/register"!==this.$router.currentRoute.fullPath)this.$router.push("/register");else{var t=!0!==this.$store.state.createNewCatalog;this.$store.commit("pushCreate",{createNewCatalog:t})}}}},l=n,r=(a("e11d"),a("2877")),c=a("1c1c"),m=a("66e5"),u=a("4074"),d=a("3b73"),f=a("9c40"),h=a("eebe"),p=a.n(h),b=Object(r["a"])(l,s,o,!1,null,null,null);e["a"]=b.exports;p()(b,"components",{QList:c["a"],QItem:m["a"],QItemSection:u["a"],QExpansionItem:d["a"],QBtn:f["a"]})},"49de":function(t,e,a){"use strict";(function(t){a("c975");var s=a("37c0"),o=a("f508"),i=a("bc3a"),n=a.n(i),l=30;e["a"]={name:"MainLayout",components:{EssentialLink:s["a"]},data:function(){return{prefix_uri:"/api/v1/catalog/tool",leftDrawerOpen:!1,releaseUserName:"ゲスト",detailUserName:"ゲスト",user_apikey:"",main_title:"",sub_title:"",releaseCkanCatalogTitle:"(未設定)",releaseCkanCatalogDescription:"(未設定)",releaseCkanCatalogUrl:"(未設定)",releaseCkanPublisher:"(未設定)",releaseCkanPublisherExplanation:"(未設定)",detailCkanCatalogTitle:"(未設定)",detailCkanCatalogDescription:"(未設定)",detailCkanCatalogUrl:"(未設定)",detailCkanPublisher:"(未設定)",detailCkanPublisherExplanation:"(未設定)",visible:!1,selectedMode:""}},mounted:function(){var t=this;this.$store.watch((function(t,e){return e.releaseCkanUserName}),(function(e,a){e?e.length>l?t.releaseUserName=e.substr(0,l)+"...":t.releaseUserName=e:t.releaseUserName="ゲスト"})),this.$store.watch((function(t,e){return e.detailCkanUserName}),(function(e,a){e?e.length>l?t.detailUserName=e.substr(0,l)+"...":t.detailUserName=e:t.detailUserName="ゲスト"})),this.$store.watch((function(t,e){return e.releaseCkanCatalogTitle}),(function(e,a){t.releaseCkanCatalogTitle=e})),this.$store.watch((function(t,e){return e.releaseCkanCatalogDescription}),(function(e,a){t.releaseCkanCatalogDescription=e})),this.$store.watch((function(t,e){return e.releaseCkanCatalogUrl}),(function(e,a){t.releaseCkanCatalogUrl=e})),this.$store.watch((function(t,e){return e.releaseCkanCatalogPublisher}),(function(e,a){t.releaseCkanCatalogPublisher=e||"(未設定)"})),this.$store.watch((function(t,e){return e.releaseCkanCatalogPublisherExplanation}),(function(e,a){t.releaseCkanCatalogPublisherExplanation=e||"(未設定)"})),this.$store.watch((function(t,e){return e.detailCkanCatalogTitle}),(function(e,a){t.detailCkanCatalogTitle=e||"(未設定)"})),this.$store.watch((function(t,e){return e.detailCkanCatalogDescription}),(function(e,a){t.detailCkanCatalogDescription=e||"(未設定)"})),this.$store.watch((function(t,e){return e.detailCkanCatalogUrl}),(function(e,a){t.detailCkanCatalogUrl=e||"(未設定)"})),this.$store.watch((function(t,e){return e.detailCkanCatalogPublisher}),(function(e,a){t.detailCkanCatalogPublisher=e||"(未設定)"})),this.$store.watch((function(t,e){return e.detailCkanCatalogPublisherExplanation}),(function(e,a){t.detailCkanCatalogPublisherExplanation=e||"(未設定)"})),this.$store.watch((function(t,e){return e.mode}),(function(e,a){switch(e){case"register":t.selectedMode="―  新規作成  ―";break;case"userManagement":t.selectedMode="―  ユーザ管理  ―";break;case"duplicate":t.selectedMode="―  複製  ―";break;case"edit":"release"===t.$store.state.selectedMode.ckanType?t.selectedMode="―  横断編集  ―":t.selectedMode="―  詳細編集  ―";break;case"template":t.selectedMode="―  テンプレート編集  ―";break;case"import":t.selectedMode="―  インポート  ―";break;case"export":t.selectedMode="―  エクスポート  ―";break;default:t.selectedMode=""}}))},created:function(){var e=this;window.addEventListener("scroll",this.onScroll);var a=this.$data;this.$root.$on("updateHeaderTitle",(function(t){a.main_title=t})),t.browser,this.$router.beforeEach((function(t,a,s){if("/"===t.fullPath&&"/regist"===a.fullPath||"/login"===t.fullPath&&"/regist"===a.fullPath){var o=confirm("ページを移動すると入力データがリセットされます");o?(e.$store.state.user_name="ゲスト",e.$store.state.user_pass="",s(),e.leftDrawerOpen=!1):(window.alert("キャンセルしました"),e.leftDrawerOpen=!1)}else s(),e.leftDrawerOpen=!1}))},methods:{btnPageDown:function(){scrollTo({top:9999,behavior:"smooth"});var t=window.navigator.userAgent;console.log(t),-1!==t.indexOf("MSIE")||-1!==t.indexOf("trident")?(console.log("Internet Explorer"),scrollTo(0,9999)):-1!==t.indexOf("Edge")?(console.log("Edge"),scrollTo(0,9999)):-1!==t.indexOf("Chrome")?(console.log("Google Chrome"),window.scroll({top:9999,behavior:"smooth"})):-1!==t.indexOf("Safari")?(console.log("Safari"),scrollTo(0,9999)):-1!==t.indexOf("Firefox")?(console.log("Firefox"),window.scroll({top:9999,behavior:"smooth"})):-1!==t.indexOf("Opera")?(console.log("Opera"),scrollTo(0,9999)):(console.log("未知ブラウザ"),scrollTo(0,9999))},btnPageUp:function(){scrollTo({top:0,behavior:"smooth"});var t=window.navigator.userAgent;console.log(t),-1!==t.indexOf("MSIE")||-1!==t.indexOf("trident")?(console.log("Internet Explorer"),scrollTo(0,0)):-1!==t.indexOf("Edge")?(console.log("Edge"),scrollTo(0,0)):-1!==t.indexOf("Chrome")?(console.log("Google Chrome"),window.scroll({top:0,behavior:"smooth"})):-1!==t.indexOf("Safari")?(console.log("Safari"),scrollTo(0,0)):-1!==t.indexOf("Firefox")?(console.log("Firefox"),window.scroll({top:0,behavior:"smooth"})):-1!==t.indexOf("Opera")?(console.log("Opera"),scrollTo(0,0)):(console.log("未知ブラウザ"),scrollTo(0,0))},logout:function(){var t=this;"/"!==this.$route.path&&"/login"!==this.$route.path&&(o["a"].show(),n.a.get(this.prefix_uri+"/logout").then((function(e){o["a"].hide(),console.log(e),t.$store.commit("initLoginCkanInfo"),t.$router.push("/login"),t.$store.commit("updateMode",{mode:"",ckanType:"",isBothCatalog:!1})})).catch((function(t){o["a"].hide(),console.error(t.response)})))},btnLogout:function(){this.$store.commit("initItemListParams"),this.$store.commit("initCkanItemListParams"),this.$store.commit("initLoginCkanInfo"),this.$router.push("/login"),location.reload(!0)},onScroll:function(){this.scrollY=window.scrollY,this.visible?window.scrollY<=0&&(this.visible=!this.visible):this.visible=window.scrollY>0}}}}).call(this,a("4362"))},"546f":function(t,e,a){"use strict";var s=a("6426"),o=a.n(s);o.a},6426:function(t,e,a){},"713b":function(t,e,a){"use strict";a.r(e);var s=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("q-layout",{attrs:{view:"hHh Lpr fFf"}},[a("q-header",{attrs:{elevated:""}},[a("q-toolbar",[a("q-btn",{staticClass:"q-mr-sm",attrs:{dense:"",flat:"",round:"",icon:"menu"},on:{click:function(e){t.leftDrawerOpen=!t.leftDrawerOpen}}}),a("q-separator",{attrs:{dark:"",vertical:"",inset:""}}),a("q-toolbar-title",[t._v("\n        データカタログ作成ツール    "+t._s(t.selectedMode)+"\n      ")]),a("div",{staticClass:"q-pr-md"},[a("font",{attrs:{size:"3px"}},[t._v("Version 1.1")])],1),a("div",{staticClass:"q-pr-md"},[a("q-btn-dropdown",{attrs:{label:"ユーザ情報",icon:"account_circle",outline:""}},[a("q-list",{staticStyle:{width:"600px"},attrs:{dense:""}},[a("q-item",{staticClass:"q-mt-sm"},[a("q-item-section",{staticClass:"col-5 gt-sm",attrs:{top:""}},[a("q-item-label",[a("font",{attrs:{color:"#1d468f"}},[t._v("ユーザ名")])],1)],1),a("q-item-section",{attrs:{top:""}},[a("q-item-label",{attrs:{lines:"1"}},[t._v("\n                  "+t._s(t.releaseUserName)+"\n                ")])],1)],1),a("q-separator"),a("q-item",{staticClass:"q-mt-sm"},[a("q-item-section",{staticClass:"col-5 gt-sm",attrs:{top:""}},[a("q-item-label",[a("font",{attrs:{color:"#1d468f"}},[t._v("横断検索用CKAN")])],1)],1)],1),a("q-item",{staticClass:"q-mt-sm"},[a("q-item-section",{staticClass:"col-5 gt-sm",attrs:{top:""}},[a("q-item-label",[a("font",{attrs:{color:"#1d468f"}},[t._v("  カタログのタイトル")])],1)],1),a("q-item-section",{attrs:{top:""}},[a("q-item-label",{attrs:{lines:"1"}},[t._v("\n                  "+t._s(t.releaseCkanCatalogTitle)+"\n                ")])],1)],1),a("q-item",{staticClass:"q-mt-sm"},[a("q-item-section",{staticClass:"col-5 gt-sm",attrs:{top:""}},[a("q-item-label",[a("font",{attrs:{color:"#1d468f"}},[t._v("  カタログの説明")])],1)],1),a("q-item-section",{attrs:{top:""}},[a("q-item-label",{attrs:{lines:"1"}},[t._v("\n                  "+t._s(t.releaseCkanCatalogDescription)+"\n                ")])],1)],1),a("q-item",{staticClass:"q-mt-sm"},[a("q-item-section",{staticClass:"col-5 gt-sm",attrs:{top:""}},[a("q-item-label",[a("font",{attrs:{color:"#1d468f"}},[t._v("  カタログの記載のホームページ")])],1)],1),a("q-item-section",{attrs:{top:""}},[a("q-item-label",{attrs:{lines:"1"}},[t._v("\n                  "+t._s(t.releaseCkanCatalogUrl)+"\n                ")])],1)],1),a("q-item",{staticClass:"q-mt-sm"},[a("q-item-section",{staticClass:"col-5 gt-sm",attrs:{top:""}},[a("q-item-label",[a("font",{attrs:{color:"#1d468f"}},[t._v("  カタログの公開者")])],1)],1),a("q-item-section",{attrs:{top:""}},[a("q-item-label",{attrs:{lines:"1"}},[t._v("\n                  "+t._s(t.releaseCkanPublisher)+"\n                ")])],1)],1),a("q-item",{staticClass:"q-mt-sm"},[a("q-item-section",{staticClass:"col-5 gt-sm",attrs:{top:""}},[a("q-item-label",[a("font",{attrs:{color:"#1d468f"}},[t._v("  カタログの公開者（説明）")])],1)],1),a("q-item-section",{attrs:{top:""}},[a("q-item-label",{attrs:{lines:"1"}},[t._v("\n                  "+t._s(t.releaseCkanPublisherExplanation)+"\n                ")])],1)],1),a("q-separator"),a("q-item",{staticClass:"q-mt-sm"},[a("q-item-section",{staticClass:"col-5 gt-sm",attrs:{top:""}},[a("q-item-label",[a("font",{attrs:{color:"#1d468f"}},[t._v("詳細検索用CKAN")])],1)],1)],1),a("q-item",{staticClass:"q-mt-sm"},[a("q-item-section",{staticClass:"col-5 gt-sm",attrs:{top:""}},[a("q-item-label",[a("font",{attrs:{color:"#1d468f"}},[t._v("  カタログのタイトル")])],1)],1),a("q-item-section",{attrs:{top:""}},[a("q-item-label",{attrs:{lines:"1"}},[t._v("\n                  "+t._s(t.detailCkanCatalogTitle)+"\n                ")])],1)],1),a("q-item",{staticClass:"q-mt-sm"},[a("q-item-section",{staticClass:"col-5 gt-sm",attrs:{top:""}},[a("q-item-label",[a("font",{attrs:{color:"#1d468f"}},[t._v("  カタログの説明")])],1)],1),a("q-item-section",{attrs:{top:""}},[a("q-item-label",{attrs:{lines:"1"}},[t._v("\n                  "+t._s(t.detailCkanCatalogDescription)+"\n                ")])],1)],1),a("q-item",{staticClass:"q-mt-sm"},[a("q-item-section",{staticClass:"col-5 gt-sm",attrs:{top:""}},[a("q-item-label",[a("font",{attrs:{color:"#1d468f"}},[t._v("  カタログの記載のホームページ")])],1)],1),a("q-item-section",{attrs:{top:""}},[a("q-item-label",{attrs:{lines:"1"}},[t._v("\n                  "+t._s(t.detailCkanCatalogUrl)+"\n                ")])],1)],1),a("q-item",{staticClass:"q-mt-sm"},[a("q-item-section",{staticClass:"col-5 gt-sm",attrs:{top:""}},[a("q-item-label",[a("font",{attrs:{color:"#1d468f"}},[t._v("  カタログの公開者")])],1)],1),a("q-item-section",{attrs:{top:""}},[a("q-item-label",{attrs:{lines:"1"}},[t._v("\n                  "+t._s(t.detailCkanPublisher)+"\n                ")])],1)],1),a("q-item",{staticClass:"q-mt-sm"},[a("q-item-section",{staticClass:"col-5 gt-sm",attrs:{top:""}},[a("q-item-label",[a("font",{attrs:{color:"#1d468f"}},[t._v("  カタログの公開者（説明）")])],1)],1),a("q-item-section",{attrs:{top:""}},[a("q-item-label",{attrs:{lines:"1"}},[t._v("\n                  "+t._s(t.detailCkanPublisherExplanation)+"\n                ")])],1)],1)],1)],1)],1),a("q-btn",{attrs:{outline:"",size:"gl","text-color":"white",label:"ログアウト"},on:{click:function(e){return t.logout()}}})],1)],1),a("q-drawer",{attrs:{bordered:"",width:230,"content-class":"bg-grey-1"},model:{value:t.leftDrawerOpen,callback:function(e){t.leftDrawerOpen=e},expression:"leftDrawerOpen"}},[a("q-list",[a("q-item-label",{staticClass:"text-grey-8",attrs:{header:""}},[t._v("\n        Menu\n      ")]),a("EssentialLink")],1)],1),a("q-page-container",[a("q-page",{staticClass:"background-whitesmoke row justify-center content-center"},[a("router-view"),a("q-page-sticky",{directives:[{name:"show",rawName:"v-show",value:t.visible,expression:"visible"}],attrs:{position:"bottom-right",offset:[18,98]}},[a("q-btn",{staticClass:"animation-pop",attrs:{icon:"keyboard_arrow_down",round:"",color:"light-blue-10"},on:{click:function(e){return t.btnPageDown()}}})],1),a("q-page-sticky",{directives:[{name:"show",rawName:"v-show",value:t.visible,expression:"visible"}],attrs:{position:"bottom-right",offset:[18,158]}},[a("q-btn",{staticClass:"animation-pop play-backtotop non-selectable shadow-2",attrs:{icon:"keyboard_arrow_up",round:"",color:"light-blue-10"},on:{click:function(e){return t.btnPageUp()}}})],1)],1)],1)],1)},o=[],i=a("49de"),n=i["a"],l=(a("546f"),a("2877")),r=a("4d5a"),c=a("e359"),m=a("65c6"),u=a("9c40"),d=a("eb85"),f=a("6ac5"),h=a("f20b"),p=a("1c1c"),b=a("66e5"),C=a("4074"),g=a("0170"),q=a("9404"),v=a("09e3"),k=a("9989"),w=a("de5e"),x=a("eebe"),$=a.n(x),_=Object(l["a"])(n,s,o,!1,null,null,null);e["default"]=_.exports;$()(_,"components",{QLayout:r["a"],QHeader:c["a"],QToolbar:m["a"],QBtn:u["a"],QSeparator:d["a"],QToolbarTitle:f["a"],QBtnDropdown:h["a"],QList:p["a"],QItem:b["a"],QItemSection:C["a"],QItemLabel:g["a"],QDrawer:q["a"],QPageContainer:v["a"],QPage:k["a"],QPageSticky:w["a"]})},e11d:function(t,e,a){"use strict";var s=a("f966"),o=a.n(s);o.a},f966:function(t,e,a){}}]);