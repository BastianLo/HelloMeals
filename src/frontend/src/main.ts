import './assets/main.css'

import {createApp} from 'vue'
import {createPinia} from 'pinia'

import App from './App.vue'
import router from './router'
import de from "./locales/de.json";
import en from "./locales/en.json";
import {createI18n} from 'vue-i18n'

// configure i18n
const i18n = createI18n({
    locale: "de",
    fallbackLocale: "de",
    messages: {de, en},
});
const app = createApp(App)

app.use(createPinia())
app.use(i18n);
app.use(router)

app.mount('#app')
