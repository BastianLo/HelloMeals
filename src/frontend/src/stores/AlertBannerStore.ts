import {defineStore} from 'pinia'


enum AlertBannerType {
    INFO = 'blue',
    WARNING = 'orange',
    ERROR = 'red',
    SUCCESS = 'green',
}

export default AlertBannerType

export const useAlertBannerStore = defineStore({
    id: 'alertBannerStore',
    state: () => ({
        banner_information: {
            alertBannerType: AlertBannerType.INFO,
            title: '',
            message: '',
            show: false
        },
    }),
    getters: {},
    actions: {
        async showBanner(alertBannerType: AlertBannerType, title: string, message: string) {
            this.banner_information.show = true
            this.banner_information.alertBannerType = alertBannerType
            this.banner_information.title = title
            this.banner_information.message = message
            await this.delay(3000)
            this.banner_information.show = false

        },
        delay(ms: number) {
            return new Promise(resolve => setTimeout(resolve, ms));
        }
    }
})