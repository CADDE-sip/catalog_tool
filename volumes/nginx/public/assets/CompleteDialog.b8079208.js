var He=Object.defineProperty,De=Object.defineProperties;var Me=Object.getOwnPropertyDescriptors;var Z=Object.getOwnPropertySymbols;var Ve=Object.prototype.hasOwnProperty,ze=Object.prototype.propertyIsEnumerable;var ee=(e,t,o)=>t in e?He(e,t,{enumerable:!0,configurable:!0,writable:!0,value:o}):e[t]=o,w=(e,t)=>{for(var o in t||(t={}))Ve.call(t,o)&&ee(e,o,t[o]);if(Z)for(var o of Z(t))ze.call(t,o)&&ee(e,o,t[o]);return e},M=(e,t)=>De(e,Me(t));import{v as Fe,h as F,c as Ie,i as Qe,j as $e,Q as Le,a as Re}from"./QBtn.5c02f783.js";import{c as ce,h as Oe,e as Ae,f as je}from"./render.ce2d7a1b.js";import{w as k,o as Ke,g as de,n as C,r as x,b as Ne,h as g,$ as Ue,c as f,f as Q,J as fe,W as me,a0 as te,P as oe,t as N,x as Ge,d as V,y as U,H as G,z as ne,j as We}from"./index.f310304c.js";import{Q as Je,b as Xe}from"./QCard.b3936020.js";import{e as ie,d as Ye,f as Ze,r as et,p as tt,a as ot}from"./config.7e38babc.js";const nt={modelValue:{type:Boolean,default:null},"onUpdate:modelValue":[Function,Array]},it=["before-show","show","before-hide","hide"];function at({showing:e,canShow:t,hideOnRouteChange:o,handleShow:a,handleHide:l,processOnMount:s}){const r=de(),{props:u,emit:d,proxy:p}=r;let c;function m(i){e.value===!0?q(i):v(i)}function v(i){if(u.disable===!0||i!==void 0&&i.qAnchorHandled===!0||t!==void 0&&t(i)!==!0)return;const h=u["onUpdate:modelValue"]!==void 0;h===!0&&(d("update:modelValue",!0),c=i,C(()=>{c===i&&(c=void 0)})),(u.modelValue===null||h===!1)&&T(i)}function T(i){e.value!==!0&&(e.value=!0,d("before-show",i),a!==void 0?a(i):d("show",i))}function q(i){if(u.disable===!0)return;const h=u["onUpdate:modelValue"]!==void 0;h===!0&&(d("update:modelValue",!1),c=i,C(()=>{c===i&&(c=void 0)})),(u.modelValue===null||h===!1)&&B(i)}function B(i){e.value!==!1&&(e.value=!1,d("before-hide",i),l!==void 0?l(i):d("hide",i))}function E(i){u.disable===!0&&i===!0?u["onUpdate:modelValue"]!==void 0&&d("update:modelValue",!1):i===!0!==e.value&&(i===!0?T:B)(c)}k(()=>u.modelValue,E),o!==void 0&&Fe(r)===!0&&k(()=>p.$route.fullPath,()=>{o.value===!0&&e.value===!0&&q()}),s===!0&&Ke(()=>{E(u.modelValue)});const H={show:v,hide:q,toggle:m};return Object.assign(p,H),H}const I=[];function lt(e){return I.find(t=>t.__qPortalInnerRef.value!==null&&t.__qPortalInnerRef.value.contains(e))}function st(e,t){do{if(e.$options.name==="QMenu"){if(e.hide(t),e.$props.separateClosePopup===!0)return F(e)}else if(e.__qPortalInnerRef!==void 0){const o=F(e);return o!==void 0&&o.$options.name==="QPopupProxy"?(e.hide(t),o):e}e=F(e)}while(e!=null)}function rt(e,t,o){for(;o!==0&&e!==void 0&&e!==null;){if(e.__qPortalInnerRef!==void 0){if(o--,e.$options.name==="QMenu"){e=st(e,t);continue}e.hide(t)}e=F(e)}}function ut(e){for(e=e.parent;e!=null;){if(e.type.name==="QGlobalDialog")return!0;if(e.type.name==="QDialog"||e.type.name==="QMenu")return!1;e=e.parent}return!1}function ct(e,t,o,a){const l=x(!1),s=x(!1);let r=null;const u={},d=a===!0&&ut(e);function p(m){if(m===!0){ie(u),s.value=!0;return}s.value=!1,l.value===!1&&(d===!1&&r===null&&(r=Ye()),l.value=!0,I.push(e.proxy),Ze(u))}function c(m){if(s.value=!1,m!==!0)return;ie(u),l.value=!1;const v=I.indexOf(e.proxy);v>-1&&I.splice(v,1),r!==null&&(et(r),r=null)}return Ne(()=>{c(!0)}),Object.assign(e.proxy,{__qPortalInnerRef:t}),{showPortal:p,hidePortal:c,portalIsActive:l,portalIsAccessible:s,renderPortal:()=>d===!0?o():l.value===!0?[g(Ue,{to:r},o())]:void 0}}const dt={transitionShow:{type:String,default:"fade"},transitionHide:{type:String,default:"fade"},transitionDuration:{type:[String,Number],default:300}};function Mt(e,t){const o=x(t.value);return k(t,a=>{C(()=>{o.value=a})}),{transition:f(()=>"q-transition--"+(o.value===!0?e.transitionHide:e.transitionShow)),transitionStyle:f(()=>`--q-transition-duration: ${e.transitionDuration}ms`)}}function ft(){let e;return Q(()=>{e=void 0}),{registerTick(t){e=t,C(()=>{e===t&&(e(),e=void 0)})},removeTick(){e=void 0}}}function mt(){let e;return Q(()=>{clearTimeout(e)}),{registerTimeout(t,o){clearTimeout(e),e=setTimeout(t,o)},removeTimeout(){clearTimeout(e)}}}const _=[];let S;function vt(e){S=e.keyCode===27}function ht(){S===!0&&(S=!1)}function gt(e){S===!0&&(S=!1,fe(e,27)===!0&&_[_.length-1](e))}function ve(e){window[e]("keydown",vt),window[e]("blur",ht),window[e]("keyup",gt),S=!1}function pt(e){me.is.desktop===!0&&(_.push(e),_.length===1&&ve("addEventListener"))}function ae(e){const t=_.indexOf(e);t>-1&&(_.splice(t,1),_.length===0&&ve("removeEventListener"))}const b=[];function he(e){b[b.length-1](e)}function yt(e){me.is.desktop===!0&&(b.push(e),b.length===1&&document.body.addEventListener("focusin",he))}function le(e){const t=b.indexOf(e);t>-1&&(b.splice(t,1),b.length===0&&document.body.removeEventListener("focusin",he))}function xt(e,t,o){let a;function l(){a!==void 0&&(te.remove(a),a=void 0)}return Q(()=>{e.value===!0&&l()}),{removeFromHistory:l,addToHistory(){a={condition:()=>o.value===!0,handler:t},te.add(a)}}}function _t(){let e;return{preventBodyScroll(t){t!==e&&(e!==void 0||t===!0)&&(e=t,tt(t))}}}let z=0;const bt={standard:"fixed-full flex-center",top:"fixed-top justify-center",bottom:"fixed-bottom justify-center",right:"fixed-right items-center",left:"fixed-left items-center"},se={standard:["scale","scale"],top:["slide-down","slide-up"],bottom:["slide-up","slide-down"],right:["slide-left","slide-right"],left:["slide-right","slide-left"]};var qt=ce({name:"QDialog",inheritAttrs:!1,props:M(w(w({},nt),dt),{transitionShow:String,transitionHide:String,persistent:Boolean,autoClose:Boolean,allowFocusOutside:Boolean,noEscDismiss:Boolean,noBackdropDismiss:Boolean,noRouteDismiss:Boolean,noRefocus:Boolean,noFocus:Boolean,noShake:Boolean,seamless:Boolean,maximized:Boolean,fullWidth:Boolean,fullHeight:Boolean,square:Boolean,position:{type:String,default:"standard",validator:e=>e==="standard"||["top","bottom","left","right"].includes(e)}}),emits:[...it,"shake","click","escape-key"],setup(e,{slots:t,emit:o,attrs:a}){const l=de(),s=x(null),r=x(!1),u=x(!1),d=x(!1);let p,c=null,m,v;const T=f(()=>e.persistent!==!0&&e.noRouteDismiss!==!0&&e.seamless!==!0),{preventBodyScroll:q}=_t(),{registerTimeout:B,removeTimeout:E}=mt(),{registerTick:H,removeTick:i}=ft(),{showPortal:h,hidePortal:W,portalIsAccessible:ge,renderPortal:pe}=ct(l,s,Ce,!0),{hide:D}=at({showing:r,hideOnRouteChange:T,handleShow:Te,handleHide:Be,processOnMount:!0}),{addToHistory:ye,removeFromHistory:xe}=xt(r,D,T),_e=f(()=>`q-dialog__inner flex no-pointer-events q-dialog__inner--${e.maximized===!0?"maximized":"minimized"} q-dialog__inner--${e.position} ${bt[e.position]}`+(d.value===!0?" q-dialog__inner--animating":"")+(e.fullWidth===!0?" q-dialog__inner--fullwidth":"")+(e.fullHeight===!0?" q-dialog__inner--fullheight":"")+(e.square===!0?" q-dialog__inner--square":"")),be=f(()=>"q-transition--"+(e.transitionShow===void 0?se[e.position][0]:e.transitionShow)),qe=f(()=>"q-transition--"+(e.transitionHide===void 0?se[e.position][1]:e.transitionHide)),we=f(()=>u.value===!0?qe.value:be.value),J=f(()=>`--q-transition-duration: ${e.transitionDuration}ms`),$=f(()=>r.value===!0&&e.seamless!==!0),ke=f(()=>e.autoClose===!0?{onClick:Ee}:{}),Se=f(()=>[`q-dialog fullscreen no-pointer-events q-dialog--${$.value===!0?"modal":"seamless"}`,a.class]);k(r,n=>{C(()=>{u.value=n})}),k(()=>e.maximized,n=>{r.value===!0&&O(n)}),k($,n=>{q(n),n===!0?(yt(A),pt(R)):(le(A),ae(R))});function Te(n){E(),i(),ye(),c=e.noRefocus===!1&&document.activeElement!==null?document.activeElement:null,O(e.maximized),h(),d.value=!0,e.noFocus!==!0&&(document.activeElement!==null&&document.activeElement.blur(),H(P)),B(()=>{if(l.proxy.$q.platform.is.ios===!0){if(e.seamless!==!0&&document.activeElement){const{top:y,bottom:j}=document.activeElement.getBoundingClientRect(),{innerHeight:Y}=window,K=window.visualViewport!==void 0?window.visualViewport.height:Y;y>0&&j>K/2&&(document.scrollingElement.scrollTop=Math.min(document.scrollingElement.scrollHeight-K,j>=Y?1/0:Math.ceil(document.scrollingElement.scrollTop+j-K/2))),document.activeElement.scrollIntoView()}v=!0,s.value.click(),v=!1}h(!0),d.value=!1,o("show",n)},e.transitionDuration)}function Be(n){E(),i(),xe(),X(!0),d.value=!0,W(),c!==null&&(c.focus(),c=null),B(()=>{W(!0),d.value=!1,o("hide",n)},e.transitionDuration)}function P(n){ot(()=>{let y=s.value;y===null||y.contains(document.activeElement)===!0||(y=y.querySelector(n||"[autofocus], [data-autofocus]")||y,y.focus({preventScroll:!0}))})}function L(){P(),o("shake");const n=s.value;n!==null&&(n.classList.remove("q-animate--scale"),n.classList.add("q-animate--scale"),clearTimeout(p),p=setTimeout(()=>{s.value!==null&&(n.classList.remove("q-animate--scale"),P())},170))}function R(){e.seamless!==!0&&(e.persistent===!0||e.noEscDismiss===!0?e.maximized!==!0&&e.noShake!==!0&&L():(o("escape-key"),D()))}function X(n){clearTimeout(p),(n===!0||r.value===!0)&&(O(!1),e.seamless!==!0&&(q(!1),le(A),ae(R))),n!==!0&&(c=null)}function O(n){n===!0?m!==!0&&(z<1&&document.body.classList.add("q-body--dialog"),z++,m=!0):m===!0&&(z<2&&document.body.classList.remove("q-body--dialog"),z--,m=!1)}function Ee(n){v!==!0&&(D(n),o("click",n))}function Pe(n){e.persistent!==!0&&e.noBackdropDismiss!==!0?D(n):e.noShake!==!0&&L()}function A(n){e.allowFocusOutside!==!0&&ge.value===!0&&Ie(s.value,n.target)!==!0&&P('[tabindex]:not([tabindex="-1"])')}Object.assign(l.proxy,{focus:P,shake:L,__updateRefocusTarget(n){c=n||null}}),Q(X);function Ce(){return g("div",M(w({},a),{class:Se.value}),[g(oe,{name:"q-transition--fade",appear:!0},()=>$.value===!0?g("div",{class:"q-dialog__backdrop fixed-full",style:J.value,"aria-hidden":"true",onMousedown:Pe}):null),g(oe,{name:we.value,appear:!0},()=>r.value===!0?g("div",w({ref:s,class:_e.value,style:J.value,tabindex:-1},ke.value),Oe(t.default)):null)])}return pe}});function re(e){if(e===!1)return 0;if(e===!0||e===void 0)return 1;const t=parseInt(e,10);return isNaN(t)?0:t}var wt=Ae({name:"close-popup",beforeMount(e,{value:t}){const o={depth:re(t),handler(a){o.depth!==0&&setTimeout(()=>{const l=lt(e);l!==void 0&&rt(l,a,o.depth)})},handlerKey(a){fe(a,13)===!0&&o.handler(a)}};e.__qclosepopup=o,e.addEventListener("click",o.handler),e.addEventListener("keyup",o.handlerKey)},updated(e,{value:t,oldValue:o}){t!==o&&(e.__qclosepopup.depth=re(t))},beforeUnmount(e){const t=e.__qclosepopup;e.removeEventListener("click",t.handler),e.removeEventListener("keyup",t.handlerKey),delete e.__qclosepopup}}),ue=ce({name:"QAvatar",props:M(w({},Qe),{fontSize:String,color:String,textColor:String,icon:String,square:Boolean,rounded:Boolean}),setup(e,{slots:t}){const o=$e(e),a=f(()=>"q-avatar"+(e.color?` bg-${e.color}`:"")+(e.textColor?` text-${e.textColor} q-chip--colored`:"")+(e.square===!0?" q-avatar--square":e.rounded===!0?" rounded-borders":"")),l=f(()=>e.fontSize?{fontSize:e.fontSize}:null);return()=>{const s=e.icon!==void 0?[g(Le,{name:e.icon})]:void 0;return g("div",{class:a.value,style:o.value},[g("div",{class:"q-avatar__content row flex-center overflow-hidden",style:l.value},je(t.default,s))])}}});const kt={style:{width:"100%","text-align":"center"}},St=["innerHTML"],Tt={class:"q-mt-md"},Vt={props:["dialogInfo"],emits:["close-dialog"],setup(e,{emit:t}){const o=e;function a(l){return l?l.replace(/\r?\n/g,"<br>"):"\u30A8\u30E9\u30FC\u30E1\u30C3\u30BB\u30FC\u30B8\u306E\u53D6\u5F97\u306B\u5931\u6557\u3057\u307E\u3057\u305F\u3002<br>\u7BA1\u7406\u8005\u306B\u554F\u3044\u5408\u308F\u305B\u3066\u304F\u3060\u3055\u3044\u3002"}return(l,s)=>(N(),Ge("div",null,[V(qt,{modelValue:o.dialogInfo.isDisplay,persistent:""},{default:U(()=>[V(Je,{style:{"max-width":"35% width: 100%"}},{default:U(()=>[V(Xe,{class:"column items-center"},{default:U(()=>[G("div",kt,[o.dialogInfo.errorFlg?(N(),ne(ue,{key:0,icon:"error","font-size":"30px","text-color":"red"})):(N(),ne(ue,{key:1,icon:"check_circle","font-size":"30px","text-color":"secondary"})),G("p",{innerHTML:a(o.dialogInfo.message)},null,8,St)]),G("div",Tt,[We(V(Re,{unelevated:"",label:"\u9589\u3058\u308B",color:"primary",onClick:s[0]||(s[0]=r=>t("close-dialog"))},null,512),[[wt]])])]),_:1})]),_:1})]),_:1},8,["modelValue"])]))}};export{wt as C,qt as Q,Vt as _,it as a,mt as b,at as c,xt as d,_t as e,dt as f,ft as g,Mt as h,ct as i,yt as j,ae as k,st as l,pt as m,I as p,le as r,nt as u};