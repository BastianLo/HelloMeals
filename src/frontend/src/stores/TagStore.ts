import {defineStore} from 'pinia'
import authorizedFetch from "@/stores/CommonStore";

const baseUrl = import.meta.env.DEV ? 'http://localhost:8000/api' : window.location.origin + "/api"


interface tag {
    helloFreshId: string
    type: string
    name: string
    tagGroup: string
}

interface tagGroup {
    name: string
}

export const useTagStore = defineStore({
    id: 'TagStore',
    state: () => ({
        tags: [] as tag[],
        tagGroups: [] as string[],
    }),
    getters: {},
    actions: {
        async fetchTags() {
            const response = await authorizedFetch(baseUrl + '/Tag?page_size=10000', {
                method: "GET",
            });
            const jsonResponse = await response!.json();
            if (response!.ok) {
                this.tags = jsonResponse.results
            }
        },
        async fetchTagGroups() {
            const response = await authorizedFetch(baseUrl + '/Tag/Group?page_size=10000', {
                method: "GET",
            });
            const jsonResponse = await response!.json();
            if (response!.ok) {
                this.tagGroups = (jsonResponse.results as tagGroup[]).map(tg => tg.name)
            }
        },
        async deleteTags(tags: tag[]) {
            for (const tag of tags) {
                await authorizedFetch(baseUrl + '/Tag/Merge', {
                    method: "POST",
                    body: JSON.stringify({
                        source: tag.helloFreshId,
                        target: null,
                        delete: true
                    }),
                    headers: {
                        "Content-Type": "application/json",
                    }
                });
            }
        },
        async groupTags(tags: tag[], group: string) {
            for (const tag of tags) {
                tag.tagGroup = group
                await authorizedFetch(baseUrl + '/Tag/' + tag.helloFreshId, {
                    method: "PATCH",
                    body: JSON.stringify(tag),
                    headers: {
                        "Content-Type": "application/json",
                    }
                });
            }
        },
        async mergeTags(tags: tag[], targetId: string) {
            for (const tag of tags) {
                await authorizedFetch(baseUrl + '/Tag/Merge', {
                    method: "POST",
                    body: JSON.stringify({
                        source: tag.helloFreshId,
                        target: targetId,
                        delete: true
                    }),
                    headers: {
                        "Content-Type": "application/json",
                    }
                });
            }
        },


    }
})