var m=Object.defineProperty,l=Object.defineProperties;var p=Object.getOwnPropertyDescriptors;var s=Object.getOwnPropertySymbols;var d=Object.prototype.hasOwnProperty,i=Object.prototype.propertyIsEnumerable;var t=(a,r,e)=>r in a?m(a,r,{enumerable:!0,configurable:!0,writable:!0,value:e}):a[r]=e,o=(a,r)=>{for(var e in r||(r={}))d.call(r,e)&&t(a,e,r[e]);if(s)for(var e of s(r))i.call(r,e)&&t(a,e,r[e]);return a},n=(a,r)=>l(a,p(r));import{u as v,a as b}from"./QCard.b3936020.js";import{c as f,h}from"./render.ce2d7a1b.js";import{c as k,h as q,g}from"./index.f310304c.js";var w=f({name:"QBar",props:n(o({},v),{dense:Boolean}),setup(a,{slots:r}){const e=g(),u=b(a,e.proxy.$q),c=k(()=>`q-bar row no-wrap items-center q-bar--${a.dense===!0?"dense":"standard"}  q-bar--${u.value===!0?"dark":"light"}`);return()=>q("div",{class:c.value,role:"toolbar"},h(r.default))}});export{w as Q};
