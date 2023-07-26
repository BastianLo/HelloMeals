<!-- pages/recipes.vue -->
<template>
  <div>
    <h1>Recipes</h1>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else>
      <ul>
        <li v-for="recipe in recipes" :key="recipe.id">
          {{ recipe.title }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  title: 'Home',
  public: false
})
import {onMounted, ref} from 'vue';

const recipes = ref([]);
const loading = ref(true);
const error = ref('');

onMounted(async () => {
  try {
    const {data} = await $http.$get('/api/Recipe');
    recipes.value = data;
    loading.value = false;
  } catch (err) {
    error.value = 'Error fetching recipes';
    loading.value = false;
  }
});
</script>
