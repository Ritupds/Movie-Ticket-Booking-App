import Vue from "vue";
import App from "./App.vue";
import router from "./router";
// import { BForm, BFormGroup, BFormInput, BButton, BModal, BAlert } from 'bootstrap-vue'
import "bootstrap/dist/css/bootstrap.css";
import BootstrapVue from "bootstrap-vue";
import "bootstrap-vue/dist/bootstrap-vue.css";

Vue.config.productionTip = false;
Vue.use(BootstrapVue);

new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");
