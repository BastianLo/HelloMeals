<template>
  <RefreshSwiper @refresh="load()"/>
  <div class="flex flex-col items-center justify-center mb-24">
    <!-- Status block -->
    <div class="w-fit mb-6" v-for="(status, name) in store.status">
      <div class="flex justify-between mb-1">
        <span class="text-base font-medium text-white">{{ name }}</span>
        <template v-if="status.running">
          <div role="status">
            <svg aria-hidden="true"
                 class="inline w-4 h-4 mr-2 animate-spin text-gray-600 fill-lime-300"
                 viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path
                  d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                  fill="currentColor"></path>
              <path
                  d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                  fill="currentFill"></path>
            </svg>
            <span class="sr-only">Loading...</span>
          </div>
        </template>
        <span class="text-sm font-medium text-white"
              v-text="status.index + ` von ` + status.max"></span>
      </div>

      <div class="w-full rounded-full bg-gray-700">
        <div class="bg-blue-600 text-xs font-medium text-blue-100 text-center p-0.5 leading-none rounded-full"
             :style="'width: '+ Math.round(status.index/status.max*100) +'%'"
             v-text="Math.round(status.index/status.max*100) + '%'"></div>
      </div>
      <div class="mt-2">
        <button @click="store.start(name)"
                class="focus:outline-none text-white focus:ring-4 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 bg-green-600 hover:bg-green-700 focus:ring-green-800">
          Starten
        </button>
        <button @click="store.restart(name)"
                class="text-white focus:ring-4 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-blue-800">
          Neustarten
        </button>
        <button @click="store.stop(name)"
                class="focus:outline-none text-white focus:ring-4 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 bg-red-600 hover:bg-red-700 focus:ring-red-900">
          Stoppen
        </button>
      </div>
      <template v-if="status.exception != null">
        <div
            class="w-64 flex p-4 mb-4 text-sm border rounded-lg bg-gray-800 text-red-400 border-red-800"
            role="alert">
          <svg aria-hidden="true" class="flex-shrink-0 inline w-5 h-5 mr-3" fill="currentColor"
               viewBox="0 0 20 20"
               xmlns="http://www.w3.org/2000/svg">
            <path fill-rule="evenodd"
                  d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                  clip-rule="evenodd"></path>
          </svg>
          <span class="sr-only">Info</span>
          <div>
            <span class="font-medium">Error:</span>
            <span v-text="status.exception"></span>
          </div>
        </div>
      </template>
    </div>

  </div>
</template>
<script setup lang="ts">
import {useDownloaderStore} from "@/stores/DownloaderStore";
import {onBeforeUnmount} from "@vue/runtime-core";
import RefreshSwiper from "@/components/common/RefreshSwiper.vue";

const store = useDownloaderStore()

const load = () => {
  store.fetchStatus()
}

load()


const interval = setInterval(() => {
  store.fetchStatus()
}, 5 * 1000);
onBeforeUnmount(() => {
  clearInterval(interval)
});

</script>

<style scoped>

</style>