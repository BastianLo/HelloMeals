<script setup lang="ts">

import {useRouter} from "vue-router";
import {usePantryStore} from "@/stores/PantryStore";
import RefreshSwiper from "@/components/common/RefreshSwiper.vue";

const store = usePantryStore()

const classesDefault = "text-center py-1.5 text-xs font-medium text-white hover:bg-gray-700 rounded-lg"
const classesFocused = "text-center py-1.5 text-xs font-medium bg-gray-300 text-gray-900 rounded-lg"

const isFocused = (name: string) => {
  return useRouter().currentRoute.value.name === name
}

const load = () => {
  store.fetchPantryIngredients()
  store.fetchShoppingListIngredients()
  store.fetchAvailablePantries()
  store.fetchJoinedPantry()
}

load()
</script>

<template>
  <RefreshSwiper @refresh="load()"/>
  <div class="fixed bottom-20 left-1/2 transform -translate-x-1/2 z-50 max-w-screen-lg" v-if="store.joinedPantryId">
    <div class="w-full">
      <div class="grid max-w-xs grid-cols-2 gap-1 p-1 mx-auto my-2 rounded-lg bg-gray-600 w-64" role="group">
        <RouterLink :to="{ name: 'PantryPantry' }" :class="isFocused('PantryPantry') ? classesFocused : classesDefault"
                    class="relative">
          Vorrat
          <div v-if="store.PantryIngredients.length > 0"
               class="absolute inline-flex items-center justify-center w-6 h-6 text-xs font-bold text-white bg-red-500 border-2 rounded-full -top-2 -right-0 border-slate-800">
            {{ store.PantryIngredients.length }}
          </div>
        </RouterLink>
        <RouterLink :to="{ name: 'PantryShoppingList' }"
                    :class="isFocused('PantryShoppingList') ? classesFocused : classesDefault"
                    class="relative">
          <div v-if="store.ShoppingListIngredients.length > 0"
               class="absolute inline-flex items-center justify-center w-6 h-6 text-xs font-bold text-white bg-red-500 border-2 rounded-full -top-2 -right-0 border-slate-800">
            {{ store.ShoppingListIngredients.length }}
          </div>
          Einkaufsliste
        </RouterLink>
      </div>
    </div>
  </div>
  <RouterView/>
</template>

<style scoped>

</style>