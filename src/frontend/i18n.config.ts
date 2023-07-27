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
            common: {},
            auth: {
                login: "Login",
                username: "Benutzername",
                password: "Passwort",
            },
            recipe: {
                navLabel: 'Rezepte',
                allRecipes: 'Alle Rezepte',
                favoriteRecipes: 'Lieblings-Rezepte',
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
