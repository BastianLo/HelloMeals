import {defineStore} from 'pinia'
import type {ingredient} from "@/stores/IngredientStore";
import authorizedFetch from "@/stores/CommonStore";

const baseUrl = import.meta.env.DEV ? 'http://localhost:8000/api' : window.location.origin + "/api"


interface pantry {
    id: string,
    name: string
}

interface extendedIngredient extends ingredient {
    isHovered: boolean
}

export const usePantryStore = defineStore({
    id: 'PantryStore',
    state: () => ({
        PantryIngredients: [] as extendedIngredient[],
        ShoppingListIngredients: [] as extendedIngredient[],
        availablePantries: [] as pantry[],
        joinedPantryId: null as number | null,
        joinedPantryMembers: null as string[] | null,
    }),
    getters: {
        getJoinedPantryName(): string | null {
            if (this.joinedPantryId === null) return null
            const pantries = this.availablePantries.filter(value => value.id === this.joinedPantryId as any)
            if (pantries.length > 0)
                return pantries[0].name
            else
                return null
        }
    },
    actions: {
        async fetchPantryIngredients() {
            const path = baseUrl + '/Ingredient/Stock?page_size=1000'
            const response = await authorizedFetch(path, {
                method: "GET",
            });
            const jsonResponse = await response!.json();
            if (response!.ok) {
                this.PantryIngredients = jsonResponse.results
            }
        },
        async fetchShoppingListIngredients() {
            const path = baseUrl + '/Ingredient/ShoppingList?page_size=1000'
            const response = await authorizedFetch(path, {
                method: "GET",
            });
            const jsonResponse = await response!.json();
            if (response!.ok) {
                this.ShoppingListIngredients = jsonResponse.results
            }
        },
        async fetchAvailablePantries() {
            const path = baseUrl + '/Stock'
            const response = await authorizedFetch(path, {
                method: "GET",
            });
            const jsonResponse = await response!.json();
            if (response!.ok) {
                this.availablePantries = jsonResponse.results
            }
        },
        async fetchJoinedPantry() {
            const path = baseUrl + '/Stock/Membership'
            const response = await authorizedFetch(path, {
                method: "GET",
            });
            const jsonResponse = await response!.json();
            if (response!.ok) {
                this.joinedPantryId = jsonResponse.stockId
                this.joinedPantryMembers = jsonResponse.members
            }
        },
        async createPantry(name: string) {
            const response = await authorizedFetch(baseUrl + `/Stock`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    name: name
                })
            });
            const jsonResponse = await response!.json();
            const newId = jsonResponse.id
            await this.fetchAvailablePantries();
            await this.joinPantry(newId)
        },
        async joinPantry(id: string) {
            await authorizedFetch(baseUrl + `/Stock/${id}/Membership`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
            });
            await this.fetchJoinedPantry();
        },
        async leavePantry() {
            await authorizedFetch(baseUrl + `/Stock/Membership`, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                },
            });
            await this.fetchJoinedPantry();
            await this.fetchAvailablePantries();
        },
        async addIngredientToPantry(id: string) {
            await authorizedFetch(baseUrl + `/Ingredient/Stock/${id}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
            });
            await this.fetchPantryIngredients();
        },
        async removeIngredientFromPantry(id: string) {
            await authorizedFetch(baseUrl + `/Ingredient/Stock/${id}`, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                },
            });
            await this.fetchPantryIngredients();
        },

    }
})