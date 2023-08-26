<script setup lang="ts">

const emit = defineEmits(['refresh'])
import {onMounted, onUnmounted, ref} from 'vue';

const refreshing = ref(false);
let startY = 0;
let isDraggingAtTop = false;

const handleTouchStart = (event: TouchEvent) => {
  startY = event.touches[0].clientY;
  isDraggingAtTop = window.scrollY === 0;
};

const handleTouchMove = (event: TouchEvent) => {
  if (isDraggingAtTop && event.touches[0].clientY - startY > 200 && !refreshing.value) {
    refreshing.value = true;
    emit('refresh')

    setTimeout(() => {
      refreshing.value = false;
    }, 2000);
  }
};

const handleTouchEnd = () => {
  startY = 0;
  isDraggingAtTop = false;
};

onMounted(() => {
  document.addEventListener('touchstart', handleTouchStart);
  document.addEventListener('touchmove', handleTouchMove);
  document.addEventListener('touchend', handleTouchEnd);
});

onUnmounted(() => {
  document.removeEventListener('touchstart', handleTouchStart);
  document.removeEventListener('touchmove', handleTouchMove);
  document.removeEventListener('touchend', handleTouchEnd);
});

</script>