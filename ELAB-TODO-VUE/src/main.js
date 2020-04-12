import "@babel/polyfill";
import "mutationobserver-shim";
import Vue from "vue";
import axios from 'axios';
import VueAxios from 'vue-axios';
import "./plugins/bootstrap-vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";

Vue.config.productionTip = false;

Vue.use(VueAxios, axios);


// Mountujemo Vue instancu na element sa idem app u public/index.html
// Render funkcijom kazujemo koju to komponentu renderujemo u nasem slucaju App
// Mozemo imati vise Vue instanci, ali praksa za SPA (Single Page Applications) je da 
// Postoji samo jedna render funkcija
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");