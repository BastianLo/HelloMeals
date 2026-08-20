import {defineStore} from 'pinia'
import authorizedFetch from "@/stores/CommonStore";

const baseUrl = import.meta.env.DEV ? 'http://localhost:8000/api' : window.location.origin + "/api"

export interface globalPreference {
    id: number,
    section: string,
    name: string,
    identifier: string,
    value: boolean | number,
    help_text: string,
    field: {
        class: string,
    },
}

export const useSettingsStore = defineStore({
    id: 'SettingsStore',
    state: () => ({
        preferences: [] as globalPreference[],
    }),
    getters: {},
    actions: {
        async fetchPreferences() {
            const response = await authorizedFetch(baseUrl + '/settings/global/', {
                method: "GET",
            });
            const jsonResponse = await response!.json();
            if (response!.ok) {
                this.preferences = jsonResponse
            }
        },
        async updatePreference(preference: globalPreference, value: boolean | number) {
            const response = await authorizedFetch(baseUrl + '/settings/global/' + preference.id + '/', {
                method: "PATCH",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({value: value}),
            });
            if (response!.ok) {
                preference.value = value
            }
        },
    }
})
