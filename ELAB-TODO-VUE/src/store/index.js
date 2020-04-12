import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);
// Vuex je centralizovano skladiste state-a nase aplikacije, kao npr. Redux
// U ovom primeru imamo samo baseUrl, koji setujemo kako bismo iz cele aplikacije
// znali na kojoj adresi nam je backend server
export default new Vuex.Store({
  state: {
    baseUrl: process.env.BACK_APP_URL
  },
  mutations: {},
  actions: {},
  modules: {}
});
