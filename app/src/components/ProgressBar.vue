<script setup>
import {ref} from "vue";
const progress = ref(20);
</script>

<template>
  <div class="progress-bar">
    <div class="inner-bar" :style="{width: progress + '%'}"></div>
  </div>
</template>

<style scoped>
.progress-bar {
  width: 100%;
  height: 15px;
  background: white;
  border-radius: 10px;
  overflow: hidden;
}
.inner-bar {
  height: 100%;
  background: #0896c5;
  transition: width 1s ease;
}
</style>