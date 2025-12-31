<script setup>
/* eslint-disable no-undef */
defineProps({
  files: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['click'])

function handleFileClick(fileName) {
  emit('click', fileName)
}
</script>

<template>
  <div class="open-file-path-item">
    <div 
      v-for="file in files" 
      :key="file.name" 
      class="file-item"
      @click="handleFileClick(file.name)"
    >
      <span class="file-name">{{ file.name }}</span>
      <span class="file-type">{{ file.type }}</span>
      <span class="file-size">{{ file.size }}</span>
    </div>
  </div>
</template>

<style scoped>
.open-file-path-item {
  width: 75%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
</style>