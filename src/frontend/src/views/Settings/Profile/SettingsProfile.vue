<script setup lang="ts">

import {useAuthStore} from "@/stores/AuthStore";

const logout = async () => {
  await useAuthStore().logout()
  window.location.reload();
}
</script>

<template>
  <div class="flex justify-center mt-4">

    <div
        class="w-48 text-gray-900 bg-white border border-gray-200 rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white">
      <button @click="logout()"
              class="relative inline-flex items-center w-full px-4 py-2 text-sm font-medium border-b border-gray-200 rounded-t-lg hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-2 focus:ring-blue-700 focus:text-blue-700 dark:border-gray-600 dark:hover:bg-gray-600 dark:hover:text-white dark:focus:ring-gray-500 dark:focus:text-white">
        <svg class="w-4 h-4 mr-2" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5"
             viewBox="0 0 24 24"
             xmlns="http://www.w3.org/2000/svg">
          <path
              d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75"
              stroke-linecap="round" stroke-linejoin="round"></path>
        </svg>
        Abmelden
      </button>
    </div>
  </div>
</template>

<style scoped>

</style>