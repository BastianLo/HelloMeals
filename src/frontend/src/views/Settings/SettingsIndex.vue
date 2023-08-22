<script setup lang="ts">

import {useAuthStore} from "@/stores/AuthStore";
</script>

<template>
  <div class="flex justify-center mt-4">
    <div
        class="w-48 border rounded-lg bg-gray-700 border-gray-600 text-white">
      <router-link :to="{ name: 'SettingsProfile' }"
                   class="relative inline-flex items-center w-full px-4 py-2 text-sm font-medium border-b
        rounded-t-lg focus:z-10 focus:ring-2
        border-gray-600 hover:bg-gray-600 hover:text-white focus:ring-gray-500
        focus:text-white">
        <svg class="w-4 h-4 mr-2" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5"
             viewBox="0 0 24 24"
             xmlns="http://www.w3.org/2000/svg">
          <path
              d="M17.982 18.725A7.488 7.488 0 0012 15.75a7.488 7.488 0 00-5.982 2.975m11.963 0a9 9 0 10-11.963 0m11.963 0A8.966 8.966 0 0112 21a8.966 8.966 0 01-5.982-2.275M15 9.75a3 3 0 11-6 0 3 3 0 016 0z"
              stroke-linecap="round" stroke-linejoin="round"></path>
        </svg>
        Profil
      </router-link>
      <button v-if="useAuthStore().user.is_superuser"
              class="relative inline-flex items-center w-full px-4 py-2 text-sm font-medium border-b focus:z-10 focus:ring-2 border-gray-600 hover:bg-gray-600 hover:text-white focus:ring-gray-500 focus:text-white">
        <svg aria-hidden="true" class="w-4 h-4 mr-2" fill="none" stroke="currentColor" stroke-width="1.5"
             viewBox="0 0 24 24"
             xmlns="http://www.w3.org/2000/svg">
          <path
              d="M11.42 15.17L17.25 21A2.652 2.652 0 0021 17.25l-5.877-5.877M11.42 15.17l2.496-3.03c.317-.384.74-.626 1.208-.766M11.42 15.17l-4.655 5.653a2.548 2.548 0 11-3.586-3.586l6.837-5.63m5.108-.233c.55-.164 1.163-.188 1.743-.14a4.5 4.5 0 004.486-6.336l-3.276 3.277a3.004 3.004 0 01-2.25-2.25l3.276-3.276a4.5 4.5 0 00-6.336 4.486c.091 1.076-.071 2.264-.904 2.95l-.102.085m-1.745 1.437L5.909 7.5H4.5L2.25 3.75l1.5-1.5L7.5 4.5v1.409l4.26 4.26m-1.745 1.437l1.745-1.437m6.615 8.206L15.75 15.75M4.867 19.125h.008v.008h-.008v-.008z"
              stroke-linecap="round" stroke-linejoin="round"></path>
        </svg>
        Admin
      </button>

      <button
          class="relative inline-flex items-center w-full px-4 py-2 text-sm font-medium rounded-b-lg focus:z-10 focus:ring-2 border-gray-600 hover:bg-gray-600 hover:text-white focus:ring-gray-500 focus:text-white">
        <svg aria-hidden="true" class="w-4 h-4 mr-2" fill="none" stroke="currentColor" stroke-width="1.5"
             viewBox="0 0 24 24"
             xmlns="http://www.w3.org/2000/svg">
          <path
              d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 011.37.49l1.296 2.247a1.125 1.125 0 01-.26 1.431l-1.003.827c-.293.24-.438.613-.431.992a6.759 6.759 0 010 .255c-.007.378.138.75.43.99l1.005.828c.424.35.534.954.26 1.43l-1.298 2.247a1.125 1.125 0 01-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.57 6.57 0 01-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.02-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 01-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 01-1.369-.49l-1.297-2.247a1.125 1.125 0 01.26-1.431l1.004-.827c.292-.24.437-.613.43-.992a6.932 6.932 0 010-.255c.007-.378-.138-.75-.43-.99l-1.004-.828a1.125 1.125 0 01-.26-1.43l1.297-2.247a1.125 1.125 0 011.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.281z"
              stroke-linecap="round" stroke-linejoin="round"></path>
          <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" stroke-linecap="round" stroke-linejoin="round"></path>

        </svg>
        Einstellungen
      </button>
    </div>

  </div>
</template>

<style scoped>

</style>