<template>
  <div v-for="(banner, index) in banners">
    <transition name="fade" mode="out-in">
      <div v-if="banner.show" key="banner" :style="{'top': (1 + index*4)+'rem'}"
           class="fixed inset-x-0 flex items-center justify-center">
        <div class="flex p-4 mb-4 text-sm border rounded-lg bg-gray-800"
             :class="['text-' + banner.alertBannerType + '-400', 'border-' + banner.alertBannerType + '-800']"
             role="alert">
          <svg aria-hidden="true" class="flex-shrink-0 inline w-5 h-5 mr-3" fill="currentColor"
               viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
            <path fill-rule="evenodd"
                  d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                  clip-rule="evenodd"></path>
          </svg>
          <span class="sr-only">Info</span>
          <div>
            <span class="font-medium">{{ banner.title }}</span> {{ banner.message }}
          </div>
          <button type="button" @click="banners.splice(index, 1)"
                  class="ml-2 flex-shrink-0 p-1 transition duration-300 ease-in-out rounded-full hover:bg-red-100 focus:outline-none focus:ring-2 focus:ring-red-500 dark:hover:bg-red-800 dark:focus:ring-red-500">
            <span class="sr-only">Dismiss</span>
            <svg aria-hidden="true" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"
                 xmlns="http://www.w3.org/2000/svg">
              <path fill-rule="evenodd"
                    d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                    clip-rule="evenodd"></path>
            </svg>
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import {useAlertBannerStore} from "@/stores/AlertBannerStore";
import {ref, watch} from "vue";

const alertBannerStore = useAlertBannerStore();
const banners = ref(alertBannerStore.banners);

watch(() => alertBannerStore.banners, (newBanners) => {
  if (newBanners) {
    banners.value = newBanners;
  }
});
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease-in-out;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>


