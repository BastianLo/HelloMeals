export default defineI18nConfig(() => ({
    legacy: false,
    locale: 'en',
    messages: {
        en: {
            welcome: 'Welcome',
            recipe: {
                navLabel: 'Recipes'
            },
            storage: {
                navLabel: 'Storage'
            },
            planner: {
                navLabel: 'Planner'
            },
            settings: {
                navLabel: 'Settings'
            },
        },
        de: {
            welcome: 'Willkommen',
            recipe: {
                navLabel: 'Rezepte'
            },
            storage: {
                navLabel: 'Vorrat'
            },
            planner: {
                navLabel: 'Planer'
            },
            settings: {
                navLabel: 'Einstellungen'
            },
        }
    }
}))
