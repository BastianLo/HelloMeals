import {defineStore} from 'pinia'
import authorizedFetch from "../../composables/authorizedFetch";

const baseUrl = import.meta.env.DEV ? 'http://localhost:8000/api' : window.location.origin + "/api"

export const useAuthStore = defineStore({
    id: 'auth',
    state: () => ({
        access_token: localStorage.getItem("access_token") || "",
        refresh_token: localStorage.getItem("refresh_token") || "",
        user: JSON.parse(localStorage.getItem("user") || "{}"),
        returnUrl: "/",
    }),
    getters: {
        get_access_token: (state) => state.access_token,
        get_refresh_token: (state) => state.refresh_token,
        is_logged_in: (state) => !!state.access_token
    },
    actions: {
        isTokenValid(token: string) {
            if (token === "") return false
            const expiry = (JSON.parse(atob(token.split('.')[1]))).exp;
            return (Math.floor((new Date).getTime() / 1000)) <= expiry;
        },
        async get_valid_token() {
            //Check if the token is valid
            if (this.isTokenValid(this.get_access_token)) return this.get_access_token
            else if (this.isTokenValid(this.get_refresh_token)) {
                await this.refresh_access_token()
                return this.get_access_token
            } else {
                return null
            }
        },
        async refresh_access_token() {
            const response = await fetch(baseUrl + '/auth/refresh/', {
                method: "POST",
                body: JSON.stringify({
                    refresh: this.get_refresh_token
                }),
                headers: {
                    "Content-Type": "application/json",
                }
            })
            const jsonResponse = await response.json()
            if (response.ok) {
                this.set_access_token(jsonResponse.access)
            }
        },
        async login(username: string, password: string) {
            const response = await fetch(baseUrl + '/auth/token/', {
                method: "POST",
                body: JSON.stringify({
                    username: username,
                    password: password
                }),
                headers: {
                    "Content-Type": "application/json",
                }
            })
            const jsonResponse = await response.json()
            if (response.ok) {
                this.set_access_token(jsonResponse.access)
                this.set_refresh_token(jsonResponse["refresh"])
                await this.get_user_information()
            }
            return {"response": response, "message": jsonResponse.detail}
        },
        async get_user_information() {
            const response = await authorizedFetch(baseUrl + '/auth/me/', {
                method: "GET",
            })
            const jsonResponse = await response.json()
            this.set_user(jsonResponse)
        },

        set_access_token(token: string) {
            this.access_token = token
            localStorage.setItem("access_token", token)
        },
        set_refresh_token(token: string) {
            this.refresh_token = token
            localStorage.setItem("refresh_token", token)
        },
        set_user(user: any) {
            this.user = user
            localStorage.setItem("user", JSON.stringify(user))
        }
    }
})