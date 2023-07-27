import {defineStore} from 'pinia'
import {useAuth} from "#imports";

const baseUrl = process.env.NODE_ENV === 'development' ? 'http://localhost:8000/api' : window.location.host + "/api"

export const useRecipeStore = defineStore({
    id: 'auth',
    state: () => ({
        recipes: [],
        navigation: {
            count: null,
            start: null,
            end: null,
            next: null,
            previous: null
        },
        baseInformation: {
            totalRecipeCount: null,
            favoriteRecipeCount: null,
        },
    }),
    actions: {
        async fetchRecipes(force = false) {
            if (!force && this.recipes.length) {
                return
            }
            const response = await $fetch(baseUrl + '/Recipe', {
                headers: {
                    "authorization": useAuth().token.value
                }
            })
            this.navigation.count = response.count
            this.navigation.start = response.start
            this.navigation.end = response.end
            this.navigation.next = response.next
            this.navigation.previous = response.previous
            this.recipes = response.results
        },
        async fetchBaseInformation(force = false) {
            if (!force && this.baseInformation.totalRecipeCount) {
                return
            }
            this.baseInformation = await $fetch(baseUrl + '/Recipe/BaseInformation', {
                headers: {
                    "authorization": useAuth().token.value
                }
            })
        }
    }
})