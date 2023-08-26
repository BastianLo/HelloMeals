<script setup lang="ts">

const emit = defineEmits(['refresh'])

import {ref} from "vue";

const refreshing = ref(false);
let startY = 0;
let isDraggingAtTop = false;

const handleTouchStart = (event: TouchEvent) => {
  startY = event.touches[0].clientY;
  isDraggingAtTop = window.scrollY === 0;
};

const handleTouchMove = (event: TouchEvent) => {
  if (isDraggingAtTop && event.touches[0].clientY - startY > 200 && !refreshing.value) {
    refreshing.value = true
    emit('refresh')
    setTimeout(() => {
      refreshing.value = false;
    }, 1000);
  }
};

const handleTouchEnd = () => {
  startY = 0;
  isDraggingAtTop = false;
};

</script>

<template>

  <div
      class="refresh-container absolute w-full h-full"
      @touchstart="handleTouchStart"
      @touchmove="handleTouchMove"
      @touchend="handleTouchEnd"
  >
    <!--
    <div v-if="refreshing" class="refresh-indicator">
      <div class="animate-spin rounded-full h-6 w-6 border-t-2 border-blue-500"></div>
      Refreshing...
    </div>
    -->
  </div>
</template>


<style scoped>

</style>