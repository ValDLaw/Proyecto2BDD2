import { createApp } from 'vue'
import App from './App.vue'
import store from './store'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.css'


createApp(App).use(store).use(Vuetify).mount('#app')
