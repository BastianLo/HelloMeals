// https://nuxt.com/docs/api/configuration/nuxt-config
export default ({
    devtools: {enabled: true},
    modules: ['@nuxtjs/tailwindcss', '@nuxtjs/i18n', '@pinia/nuxt', '@pinia/nuxt', '@sidebase/nuxt-auth'],
    app: {
        baseURL: '/frontend/'
    },
    auth: {
        globalAppMiddleware: true,
        baseURL: process.env.NODE_ENV === 'development' ? "http://127.0.0.1:8000/api" : "/api",
        provider: {
            type: 'local',
            endpoints: {
                signIn: {path: '/auth/token/', method: 'post'},
                signOut: {path: '/auth/logout', method: 'get'},
                signUp: {path: '/auth/register', method: 'post'},
                getSession: {path: '/auth/me', method: 'get'}
            },
            pages: {
                login: '/auth/login'
            },
            token: {
                signInResponseTokenPointer: '/access'
            },
            sessionDataType: {}
        },
        enableSessionRefreshPeriodically: 5000,
        enableSessionRefreshOnWindowFocus: true,
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