<script setup lang="ts">
import {Recipe} from '@/types/Recipe';
import RecipeCard from "@/components/Recipe/RecipeCard.vue";

defineProps<{
  title: string;
  recipes: Recipe[];
  seeAllTo?: string;
}>()
</script>

<template>
  <section class="mb-12" v-if="recipes.length > 0">
    <div class="flex items-center justify-between mb-4 px-1">
      <h2 class="text-xl font-semibold text-white" v-text="title"></h2>
      <router-link v-if="seeAllTo" :to="seeAllTo"
                   class="text-sm text-blue-400 hover:text-blue-300 whitespace-nowrap">
        Alle anzeigen &rarr;
      </router-link>
    </div>
    <div class="flex gap-4 overflow-x-auto pb-4 -mx-1 px-1">
      <div v-for="recipe in recipes" :key="recipe.helloFreshId" class="shrink-0 w-72">
        <RecipeCard :recipe="recipe"/>
      </div>
    </div>
  </section>
</template>
