import AlertBannerType, {useAlertBannerStore} from "@/stores/AlertBannerStore";

export const share = (title: string, url: string) => {
    try {
        navigator.share({title: title, url: url})
    } catch (e) {
        useAlertBannerStore().showBanner(AlertBannerType.SUCCESS, "Link kopiert!", "Der Link zum Rezept wurde in die Zwischenablage kopiert.")
        navigator.clipboard.writeText(url);
    }
}