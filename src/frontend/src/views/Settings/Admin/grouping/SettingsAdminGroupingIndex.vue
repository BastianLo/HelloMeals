<script setup lang="ts">

</script>

<template>
  <div class="flex justify-center">

    <div
        class="w-48 border rounded-lg bg-gray-700 border-gray-600 text-white">
      <router-link :to="{ name: 'SettingsAdminGroupingTags' }"
                   class="relative inline-flex items-center w-full px-4 py-2 text-sm font-medium border-b rounded-t-lg focus:z-10 focus:ring-2 border-gray-600 hover:bg-gray-600 hover:text-white focus:ring-gray-500 focus:text-white">
        <svg class="w-4 h-4 mr-2" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5"
             viewBox="0 0 24 24"
             xmlns="http://www.w3.org/2000/svg">
          <path
              d="M9.568 3H5.25A2.25 2.25 0 003 5.25v4.318c0 .597.237 1.17.659 1.591l9.581 9.581c.699.699 1.78.872 2.607.33a18.095 18.095 0 005.223-5.223c.542-.827.369-1.908-.33-2.607L11.16 3.66A2.25 2.25 0 009.568 3z"
              stroke-linecap="round" stroke-linejoin="round"></path>
          <path d="M6 6h.008v.008H6V6z" stroke-linecap="round" stroke-linejoin="round"></path>
        </svg>
        Tags
      </router-link>
      <router-link :to="{ name: 'SettingsAdminGroupingIngredients' }"
                   class="relative inline-flex items-center w-full px-4 py-2 text-sm font-medium rounded-b-lg focus:z-10 focus:ring-2 border-gray-600 hover:bg-gray-600 hover:text-white focus:ring-gray-500 focus:text-white">
        <svg aria-hidden="true" class="w-4 h-4 mr-2" fill="none" stroke="currentColor" stroke-width="1.5"
             viewBox="0 0 24 24"
             xmlns="http://www.w3.org/2000/svg">
          <path
              d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 01-1.12-1.243l1.264-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z"
              stroke-linecap="round" stroke-linejoin="round"></path>
        </svg>
        Zutaten
      </router-link>
    </div>

  </div>
</template>

<style scoped>

</style>