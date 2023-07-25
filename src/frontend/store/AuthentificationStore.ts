import {defineStore} from 'pinia'

const baseUrl = 'http://localhost:8000/api'

export const useAuthStore = defineStore({
    id: 'auth',
    state: () => ({
        user: process.client ? localStorage.getItem('user') : "",
        access_token: process.client ? localStorage.getItem('access_token') : "",
        refresh_token: process.client ? localStorage.getItem('refresh_token') : "",
    }),
    actions: {
        async login(username, password) {
            await useFetch(`${baseUrl}/auth/token/`, {
                method: 'POST',
                body: {"username": username, "password": password}
            })
                .then(response => {
                    this.user = username
                    this.access_token = response.data.value.access
                    this.refresh_token = response.data.value.refresh
                    /* Store user in local storage to keep them logged in between page refreshes */
                    if (process.client) {
                        localStorage.setItem('user', this.user)
                        localStorage.setItem('access_token', this.access_token)
                        localStorage.setItem('refresh_token', this.refresh_token)
                    }
                })
                .catch(error => {
                    throw error
                })
        },
        logout() {
            this.user = null
            this.access_token = null
            this.refresh_token = null
            if (process.client) {
                localStorage.removeItem('user')
                localStorage.removeItem('access_token')
                localStorage.removeItem('refresh_token')
            }
        }
    }
})