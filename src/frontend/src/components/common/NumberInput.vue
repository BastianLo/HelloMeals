<template>
  <div class="inline-flex">
    <div
        class="select-none border py-2 px-4 cursor-pointer bg-gray-700 hover:bg-gray-600 rounded-l text-white"
        @mousedown="startDecrease"
        @mouseup="stopChange"
        @mouseleave="stopChange"
    >
      -
    </div>

    <input
        class="border p-2 text-center outline-none bg-gray-800 text-white w-16 [&::-webkit-inner-spin-button]:appearance-none"
        type="text"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
    />

    <div
        class="select-none border py-2 px-4 cursor-pointer bg-gray-700 hover:bg-gray-600 rounded-r text-white"
        @mousedown="startIncrease"
        @mouseup="stopChange"
        @mouseleave="stopChange"
    >
      +
    </div>
  </div>
</template>

<script setup lang="ts">
import {defineEmits, defineProps} from 'vue';

const props = defineProps(['modelValue']);
const emit = defineEmits(['update:modelValue']);

let intervalId: number | null = null;

const increase = () => {
  emit('update:modelValue', parseInt(props.modelValue) + 1);
};

const decrease = () => {
  emit('update:modelValue', parseInt(props.modelValue) - 1);
};

const startIncrease = () => {
  increase();
  intervalId = setInterval(increase, 200);
};

const startDecrease = () => {
  decrease();
  intervalId = setInterval(decrease, 200);
};

const stopChange = () => {
  if (intervalId !== null) {
    clearInterval(intervalId);
    intervalId = null;
  }
};
</script>
