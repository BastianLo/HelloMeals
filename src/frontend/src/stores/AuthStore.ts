import {defineStore} from 'pinia'

const baseUrl = process.env.NODE_ENV === 'development' ? 'http://localhost:8000/api' : window.location.origin + "/api"

export const useAuthStore = defineStore({
    id: 'auth',
    state: () => ({
        access_token: localStorage.getItem("access_token"),
        refresh_token: localStorage.getItem("refresh_token"),
        user: {
            username: null
        },
        returnUrl: "",
    }),
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
            console.log(this.access_token)
            console.log(this.refresh_token)
            return {"status": response.status, "message": jsonResponse.detail}
        },

        set_access_token(token: string) {
            this.access_token = token
            localStorage.setItem("access_token", token)
        },
        set_refresh_token(token: string) {
            this.refresh_token = token
            localStorage.setItem("refresh_token", token)
        }
    }
})