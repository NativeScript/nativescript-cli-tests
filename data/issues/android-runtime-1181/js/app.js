import Vue from "nativescript-vue"

var BaseVueComponent = /** @class */ (function (_super) {
   __extends(BaseVueComponent, _super);
   function BaseVueComponent() {
       return _super !== null && _super.apply(this, arguments) || this;
   }
   return BaseVueComponent;
}(Vue.default));


exports.default = BaseVueComponent;
var Home = /** @class */ (function (_super) {
   __extends(Home, _super);
   function Home() {
       return _super !== null && _super.apply(this, arguments) || this;
   }
   return Home;
}(BaseVueComponent));


exports.Home = Home;
new Vue.default({
   render: function (h) {
       return h("frame", [h(Home)]);
   }
}).$start();
