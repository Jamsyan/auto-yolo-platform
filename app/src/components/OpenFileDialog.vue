<script setup>
import OpenFileDirItem from './subcompoents/OpenFileDirItem.vue'
import OpenFilePathItem from './subcompoents/OpenFilePathItem.vue'
import {defineExpose, ref} from 'vue'

// 控制对话框显示的变量
const model = ref(false)

// 模拟文件夹数据
const folders = [
  { name: "桌面", path: "/Desktop" },
  { name: "文档", path: "/Documents" },
  { name: "下载", path: "/Downloads" },
  { name: "图片", path: "/Pictures" },
  { name: "视频", path: "/Videos" }
]

// 模拟文件数据
const files = [
  { name: "file1.jpg", type: "jpg", size: "1.2 MB" },
  { name: "file2.png", type: "png", size: "2.3 MB" },
  { name: "file3.txt", type: "txt", size: "456 KB" },
  { name: "file4.mp4", type: "mp4", size: "10.5 MB" },
  { name: "file5.pdf", type: "pdf", size: "2.1 MB" }
]

// 当前选中的文件
const selectedFile = ref("")

// 暴露model属性给父组件
defineExpose({
  model
})

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
      <OpenFileDirItem :folders="folders" @folder-click="handleFolderClick"/>
      <OpenFilePathItem :files="files" @file-click="handleFileClick"/>
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