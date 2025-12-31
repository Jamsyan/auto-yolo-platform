<script setup>
/* eslint-disable no-undef */
import OpenFileDirItem from './subcompoents/OpenFileDirItem.vue'
import OpenFilePathItem from './subcompoents/OpenFilePathItem.vue'

// 关闭对话框
function closeDialog() {
  model.value = false
}

// 确认选择
function confirmSelection() {
  console.log("Selected file:", selectedFile.value)
  closeDialog()
}

// 处理文件夹点击
function handleFolderClick(folderName) {
  console.log("Enter folder:", folderName)
}

// 处理文件点击
function handleFileClick(fileName) {
  selectedFile.value = fileName
}
</script>

<template>
  <dialog class="openfiredialog" v-if="model">
    <div class="dialog-header">打开文件</div>
    <div class="dialog-body">
      <OpenFileDirItem :folders="folders" @click="handleFolderClick"/>
      <OpenFilePathItem :files="files" @click="handleFileClick"/>
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
  width: 800px;
  height: 600px;
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