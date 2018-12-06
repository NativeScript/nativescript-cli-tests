import Vue from "nativescript-vue"

export default class BaseVueComponent extends Vue {
}

export class Home extends BaseVueComponent {
}

new Vue({
   render: h => {
       return h("frame", [h(Home )]);
   }
}).$start()