<script setup>
import {ref, defineProps, defineEmits} from 'vue'
import OpenFileDirItem from './subcompoents/OpenFileDirItem.vue'
import OpenFilePathItem from './subcompoents/OpenFilePathItem.vue'

defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'confirm'])

// 定义必要的变量
const folders = ref([])
const files = ref([])
const selectedFile = ref('')

// 实现方法
function closeDialog() {
  emit('update:modelValue', false)
}

function confirmSelection() {
  emit('confirm', selectedFile.value)
  emit('update:modelValue', false)
}

</script>

<template>
  <dialog class="openfiredialog" v-if="modelValue">
    <div class="dialog-header">打开文件</div>
    <div class="dialog-body">
      <OpenFileDirItem :folders="folders"/>
      <OpenFilePathItem :files="files"/>
    </div>
    <div class="dialog-footer">
      <label for="filename">文件名:</label>
      <input type="text" id="filename" v-model="selectedFile" placeholder="输入文件名">
      <button @click="closeDialog">取消</button>
      <button @click="confirmSelection" class="confirm-btn">确认</button>
    </div>
  </dialog>
</template>

<style scoped>
.openfiredialog {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000;
  display: flex;
  flex-direction: column;
  width: 90%;
  height: 80%;
  border: none;
  border-radius: 10px;
  padding: 0;
  overflow: hidden;
  background-color: white;
  box-shadow: 4px 4px 12px rgba(0, 0, 0, 0.41),-2px -2px 8px rgba(97, 97, 97, 0.21);
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: #f5f5f5;
  border-bottom: 1px solid #ddd;
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.dialog-body {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.dialog-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background-color: #f5f5f5;
  border-top: 1px solid #ddd;
}

</style>