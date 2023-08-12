import {defineStore} from 'pinia'


enum AlertBannerType {
    INFO = 'info',
    WARNING = 'warning',
    ERROR = 'error',
    SUCCESS = 'success',
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
            console.log(alertBannerType)
            this.banner_information.show = true
            this.banner_information.title = title
            this.banner_information.message = message
            await this.delay(100000)
            console.log("test")
            this.banner_information.show = false

        },
        delay(ms: number) {
            return new Promise(resolve => setTimeout(resolve, ms));
        }
    }
})