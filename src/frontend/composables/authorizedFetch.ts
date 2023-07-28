// authorizedFetch.ts
import {useAuthStore} from "@/stores/AuthStore";

export default async function authorizedFetch(url: string, options: RequestInit = {}): Promise<Response> {
    options.headers = {
        ...options.headers,
        Authorization: `Bearer ${await useAuthStore().get_valid_token()}`,
    };
    return fetch(url, options);
}
