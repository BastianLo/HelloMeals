import {defineStore} from 'pinia'

const baseUrl = process.env.NODE_ENV === 'development' ? 'http://localhost:8000/api' : window.location.origin + "/api"

export const useAuthStore = defineStore({
    id: 'auth',
    state: () => ({
        access_token: localStorage.getItem("access_token"),
        refresh_token: localStorage.getItem("refresh_token"),
        user: JSON.parse(localStorage.getItem("user") || "{}"),
        returnUrl: "",
    }),
    getters: {
        get_access_token: (state) => state.access_token,
    },
    actions: {
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
            }
            return {"status": response.status, "message": jsonResponse.detail}
        },
        async get_user_information() {
            const response = await fetch(baseUrl + '/auth/me/', {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + this.get_access_token
                }
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