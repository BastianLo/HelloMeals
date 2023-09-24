import AlertBannerType, {useAlertBannerStore} from "@/stores/AlertBannerStore";

export const share = (title: string, url: string, bannerTitle: string, bannerMessage: string) => {
    try {
        navigator.share({title: title, url: url});
    } catch (e) {
        useAlertBannerStore().showBanner(AlertBannerType.SUCCESS, bannerTitle, bannerMessage)
        navigator.clipboard.writeText(url);
    }
}