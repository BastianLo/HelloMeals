import {defineStore} from 'pinia'
import authorizedFetch from "@/stores/CommonStore";

const baseUrl = import.meta.env.DEV ? 'http://localhost:8000/api' : window.location.origin + "/api"

interface invite {
    issuer: number,
    issuer_name: string
    id: string
}

export const useInviteStore = defineStore({
    id: 'InviteStore',
    state: () => ({
        invites: [] as invite[],
    }),
    getters: {},
    actions: {
        async fetchInvites() {
            const response = await authorizedFetch(baseUrl + '/auth/invites/', {
                method: "GET",
            });
            const jsonResponse = await response!.json();
            if (response!.ok) {
                this.invites = jsonResponse.results
            }
        },
        async deleteInvite(id: string) {
            const response = await authorizedFetch(baseUrl + '/auth/invites/' + id, {
                method: "DELETE",
            });
            if (response!.ok) {
                await this.fetchInvites()
            }
        },
        async createInvite() {
            const response = await authorizedFetch(baseUrl + '/auth/invites/', {
                method: "POST",
            });
            if (response!.ok) {
                await this.fetchInvites()
            }
        },

    }
})