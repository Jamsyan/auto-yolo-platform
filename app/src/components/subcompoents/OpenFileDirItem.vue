<script setup>
/* eslint-disable no-undef */
import {sendMessages} from "@/api/WsConnManger";

defineProps({
  folders: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['click'])

function handleFolderClick(folderName) {
  emit('click', folderName)
  const text = {
    'type':'openfile.checkdir',
    'path':folderName
  }
  sendMessages(text)
}
</script>

<template>
  <div class="open-file-dir-item">
    <div 
      v-for="folder in folders" 
      :key="folder.path" 
      class="dir-item"
      @click="handleFolderClick(folder.name)"
    >
      {{ folder.name }}
    </div>
  </div>
</template>

<style scoped>
.open-file-dir-item {
  width: 25%;
  background-color: #f5f5f5;
  border-right: 1px solid #ddd;
  overflow-y: auto;
  padding: 10px 0;
}
</style>