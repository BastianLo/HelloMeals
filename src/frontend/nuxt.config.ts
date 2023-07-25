// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    devtools: {enabled: true},
    modules: ['@nuxtjs/tailwindcss', '@nuxtjs/i18n', '@pinia/nuxt', '@pinia/nuxt'],
    app: {
        baseURL: '/frontend/'
    },
    i18n: {
        vueI18n: './i18n.config.ts',
        defaultLocale: 'de',
        locales: [
            {
                code: 'en',
                name: 'English'
            },
            {
                code: 'de',
                name: 'Deutsch'
            },
        ]
    }
})