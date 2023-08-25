import {defineStore} from 'pinia'
import authorizedFetch from "@/stores/CommonStore";

const baseUrl = import.meta.env.DEV ? 'http://localhost:8000/api' : window.location.origin + "/api"

export const useDownloaderStore = defineStore({
    id: 'downloaderStore',
    state: () => ({
        status: {
            Chefkoch: {
                max: 0,
                index: 0,
                running: false,
                exception: null
            },
            KitchenStories: {
                max: 0,
                index: 0,
                running: false,
                exception: null
            },
            HelloFresh: {
                max: 0,
                index: 0,
                running: false,
                exception: null
            },
            Lecker: {
                index: 0,
                max: 0,
                running: false,
                exception: null
            },
            EatSmarter: {
                max: 0,
                index: 0,
                running: false,
                exception: null
            }
        }
    }),
    getters: {},
    actions: {
        async fetchStatus() {
            const response = await authorizedFetch(baseUrl + '/Scraper/status', {
                method: "GET",
            });
            const jsonResponse = await response!.json();
            if (response!.ok) {
                this.status = jsonResponse
            }
        },
        async start(name: string) {
            const response = await authorizedFetch(baseUrl + '/Scraper/' + name.toLowerCase() + '/start', {
                method: "POST",
            });
            const jsonResponse = await response!.json();
            if (response!.ok) {
                this.status[name] = jsonResponse
            }
        },
        async stop(name: string) {
            const response = await authorizedFetch(baseUrl + '/Scraper/' + name.toLowerCase() + '/stop', {
                method: "POST",
            });
            const jsonResponse = await response!.json();
            if (response!.ok) {
                this.status[name] = jsonResponse
            }
        },
        async restart(name: string) {
            const response = await authorizedFetch(baseUrl + '/Scraper/' + name.toLowerCase() + '/restart', {
                method: "POST",
            });
            const jsonResponse = await response!.json();
            if (response!.ok) {
                this.status[name] = jsonResponse
            }
        }
    }
})