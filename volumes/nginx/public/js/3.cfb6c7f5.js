(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([[3],{"013f":function(s,t,a){"use strict";a.r(t);var e=function(){var s=this,t=s.$createElement,a=s._self._c||t;return a("login")},n=[],r=function(){var s=this,t=s.$createElement,a=s._self._c||t;return a("div",[a("div",{staticClass:"layout-padding row justify-center background-whitesmoke items-center"},[a("div",{staticClass:"col-xs-12 col-sm-7 col-lg-5"},[a("q-card",{staticClass:"q-card-background-white"},[a("q-card-section",[a("div",[a("div",{staticClass:"row"},[a("div",{staticClass:"col-sm-10 offset-sm-1 text-center"},[a("p",[a("font",{attrs:{size:"5",color:"#1d468f"}},[s._v("ユーザ認証")])],1),a("p",[s._v("分野間データ連携基盤データ検索用カタログサイトの"),a("br"),s._v("\n                ユーザ名とパスワードを入力してください。")]),a("q-input",{attrs:{readonly:"","hide-underline":""},model:{value:s.loginMessage,callback:function(t){s.loginMessage=t},expression:"loginMessage"}})],1)]),a("div",{staticClass:"row"},[a("div",{staticClass:"col-sm-10 offset-sm-1 text-left"},[a("h5",[s._v(" ユーザ名 ")]),a("q-separeter")],1)]),a("div",{staticClass:"row"},[a("div",{staticClass:"col-sm-10 offset-sm-1"},[a("q-input",{attrs:{"float-label":"user name"},model:{value:s.username,callback:function(t){s.username=t},expression:"username"}})],1)]),a("div",{staticClass:"row"},[a("div",{staticClass:"col-sm-10 offset-sm-1 text-left"},[a("h5",[s._v(" パスワード ")])])]),a("div",{staticClass:"row"},[a("div",{staticClass:"col-sm-10 offset-sm-1"},[a("q-input",{attrs:{"float-label":"password",type:"password"},model:{value:s.password,callback:function(t){s.password=t},expression:"password"}})],1)]),a("div",{staticClass:"row",staticStyle:{"padding-top":"20px"}},[a("div",{staticClass:"col-sm-10 offset-sm-1 text-right"},[a("q-btn",{attrs:{color:"light-blue-10",label:"ログイン"},on:{click:function(t){return s.btn_action_login()}}})],1)])])])],1)],1)])])},i=[],o=(a("c975"),a("96cf"),a("c973")),c=a.n(o),l=a("2a19"),u=a("bc3a"),d=a.n(u);l["a"].setDefaults({});var f={name:"user",title:"分析画面",data:function(){return{prefix_uri:"/api/v1/catalog/tool",accessURL:"/users",username:"",password:"",loginMessage:""}},methods:{btn_action_login:function(){var s=this;this.loginMessage="ログイン中...";var t={name:this.username,password:this.password};d.a.post(this.prefix_uri+this.accessURL,t).then(function(){var t=c()(regeneratorRuntime.mark((function t(a){return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:"success"===a.data.status?(s.$store.commit("updateUser",{user_name:a.data.user_name,user_pass:a.data.user_pass}),s.$router.push("/regist")):("error"===a.data.status||"not_same"===a.data.status||"not_username"===a.data.status||a.data.status,s.loginMessage="ログインに失敗しました");case 1:case"end":return t.stop()}}),t)})));return function(s){return t.apply(this,arguments)}}()).catch((function(s){null!=s.response&&s.response.data.indexOf("!DOCTYPE html")}))}}},p=f,m=(a("bf2d"),a("2877")),v=a("f09f"),g=a("a370"),w=a("27f9"),h=a("9c40"),b=a("eebe"),_=a.n(b),C=Object(m["a"])(p,r,i,!1,null,null,null),x=C.exports;_()(C,"components",{QCard:v["a"],QCardSection:g["a"],QInput:w["a"],QBtn:h["a"]});var k={name:"PageIndex",components:{login:x}},q=k,y=Object(m["a"])(q,e,n,!1,null,null,null);t["default"]=y.exports},"6d7c":function(s,t,a){},bf2d:function(s,t,a){"use strict";var e=a("6d7c"),n=a.n(e);n.a}}]);