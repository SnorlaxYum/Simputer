(window.webpackJsonp=window.webpackJsonp||[]).push([[11],{362:function(t,n,e){"use strict";e.r(n);var r={asyncData:function(t){t.params;var n=t.error,data=t.store.state.blog.tags;return data?{tags:data}:n({message:"Section not found",statusCode:404})},head:function(){return{title:"Tags"}}},o=e(2),component=Object(o.a)(r,(function(){var t=this,n=t.$createElement,e=t._self._c||n;return e("article",[e("header",[t._v("Tags")]),e("content",[e("ul",t._l(t.tags,(function(n){return e("li",[e("nuxt-link",{attrs:{to:["","tags",n[0]].join("/")}},[t._v(t._s(n[1].title))]),t._v("          ("+t._s(n[1].posts.size)+")")],1)})),0)])])}),[],!1,null,null,null);n.default=component.exports}}]);