!function(e,t){"object"==typeof exports&&"object"==typeof module?module.exports=t():"function"==typeof define&&define.amd?define([],t):"object"==typeof exports?exports["collective.nitf"]=t():e["collective.nitf"]=t()}(this,function(){return function(e){function t(o){if(n[o])return n[o].exports;var r=n[o]={i:o,l:!1,exports:{}};return e[o].call(r.exports,r,r.exports,t),r.l=!0,r.exports}var n={};return t.m=e,t.c=n,t.i=function(e){return e},t.d=function(e,n,o){t.o(e,n)||Object.defineProperty(e,n,{configurable:!1,enumerable:!0,get:o})},t.n=function(e){var n=e&&e.__esModule?function(){return e.default}:function(){return e};return t.d(n,"a",n),n},t.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},t.p="++resource++collective.nitf/",t(t.s=3)}([function(e,t){},function(e,t,n){e.exports=n.p+"nitf_icon.png"},function(e,t,n){e.exports=n.p+"tile-nitf.png"},function(e,t,n){"use strict";function o(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}var r=function(){function e(e,t){for(var n=0;n<t.length;n++){var o=t[n];o.enumerable=o.enumerable||!1,o.configurable=!0,"value"in o&&(o.writable=!0),Object.defineProperty(e,o.key,o)}}return function(t,n,o){return n&&e(t.prototype,n),o&&e(t,o),t}}();n(0),n(1),n(2);var i=function(){function e(t){o(this,e),this.$el=$(t),this.proportion=1.5,this.bind_events()}return r(e,[{key:"$",value:function(e){function t(t){return e.apply(this,arguments)}return t.toString=function(){return e.toString()},t}(function(e){return $(e,this.$el)})},{key:"bind_events",value:function(){this.$(".cycle-player").on("cycle-next cycle-prev",$.proxy(this.sync_slideshows,this)),this.$(".cycle-carrossel .thumb-itens").on("click",$.proxy(this.thumbs_click,this))}},{key:"sync_slideshows",value:function(e,t){var n;n=this.$(".cycle-slideshow"),n.cycle("goto",t.currSlide)}},{key:"thumbs_click",value:function(e){var t,n,o,r;e.preventDefault(),n=this.$(".cycle-carrossel"),o=n.data("cycle.API"),t=o.getSlideIndex(e.target.parentElement),r=this.$(".cycle-slideshow"),r.cycle("goto",t)}}]),e}();$(window).load(function(){$(".portaltype-collective-nitf-content.template-slideshow_view").length>0&&new i($(".slideshow-container"))}),e.exports=i}])});
//# sourceMappingURL=nitf.js.map