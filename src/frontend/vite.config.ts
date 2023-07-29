import {fileURLToPath, URL} from 'node:url'

import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import {VitePWA} from "vite-plugin-pwa";

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [
        vue(),
        VitePWA({
            mode: "development",
            base: "/",
            srcDir: "src",
            filename: "sw.ts",
            includeAssets: ["/favicon.png"],
            strategies: "injectManifest",
            manifest: {
                name: "HelloMeals",
                short_name: "HelloMeals",
                theme_color: "#0F172A",
                start_url: "/",
                display: "standalone",
                background_color: "#0F172A",
                icons: [{src: "icon-192.png", sizes: "192x192", type: "image/png",}, {
                    src: "/icon-512.png",
                    sizes: "512x512",
                    type: "image/png",
                }, {src: "icon-512.png", sizes: "512x512", type: "image/png", purpose: "any maskable",},],
            },
        }),
    ],
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url))
        }
    }
})
