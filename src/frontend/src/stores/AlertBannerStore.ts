import {defineStore} from 'pinia'


enum AlertBannerType {
    INFO = 'blue',
    WARNING = 'orange',
    ERROR = 'red',
    SUCCESS = 'green',
}

interface AlertBannerInformation {
    alertBannerType: AlertBannerType
    title: string
    message: string
    show: boolean
}

export default AlertBannerType

export const useAlertBannerStore = defineStore({
    id: 'alertBannerStore',
    state: () => ({
        banners: [] as AlertBannerInformation[],
    }),
    getters: {},
    actions: {
        async showBanner(alertBannerType: AlertBannerType, title: string, message: string) {
            this.banners.push({title: title, message: message, alertBannerType: alertBannerType, show: true})
            await this.delay(3000)
            this.banners.shift()
        },
        delay(ms: number) {
            return new Promise(resolve => setTimeout(resolve, ms));
        }
    }
})