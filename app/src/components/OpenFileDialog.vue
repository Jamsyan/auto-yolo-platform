<script setup>
import {defineProps, ref, watch} from "vue"

const props = defineProps({
  title: {
    type: String,
    default: "打开文件"
  }
})

const filedialog = ref(null)
let model = ref(false)

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
  { name: "folder1", type: "folder", size: "0 KB" },
  { name: "folder2", type: "folder", size: "0 KB" }
]

// 当前选中的文件
const selectedFile = ref("")

// 文件类型筛选
const fileTypes = [
  { label: "所有文件 (*.*)", value: "*" },
  { label: "图片文件 (*.jpg, *.png)", value: "image" },
  { label: "文本文件 (*.txt)", value: "txt" },
  { label: "文件夹", value: "folder" }
]

const selectedFileType = ref("*")

// 当前路径
const currentPath = ref("/")

function showDialog () {
  if (model.value === true) {
    filedialog.value.showModal()
  }
}

function closeDialog () {
  model.value = false
}

function confirmSelection () {
  // 这里可以添加确认选择的逻辑
  console.log("Selected file:", selectedFile.value)
  closeDialog()
}

function handleFileClick (fileName) {
  selectedFile.value = fileName
}

function handleFolderClick (folderName) {
  // 这里可以添加进入文件夹的逻辑
  console.log("Enter folder:", folderName)
  currentPath.value = currentPath.value + folderName + "/"
}

watch(model, showDialog)

</script>

<template>
  <dialog class="openfiledialog" ref="filedialog" v-if="model">
    <!-- 顶部标题栏 -->
    <div class="dialog-header">
      <div class="title">{{ props.title }}</div>
    </div>
    
    <!-- 中间内容区 -->
    <div class="dialog-body">
      <!-- 左侧导航栏 -->
      <div class="left-sidebar">
        <div class="sidebar-section">
          <div class="section-title">常用位置</div>
          <div 
            class="sidebar-item" 
            v-for="folder in folders" 
            :key="folder.path"
            @click="handleFolderClick(folder.name)"
          >
            {{ folder.name }}
          </div>
        </div>
      </div>
      
      <!-- 右侧内容区 -->
      <div class="right-content">
        <!-- 路径栏 -->
        <div class="path-bar">
          {{ currentPath }}
        </div>
        
        <!-- 文件列表 -->
        <div class="file-list">
          <div 
            class="file-item" 
            v-for="file in files" 
            :key="file.name"
            @click="file.type === 'folder' ? handleFolderClick(file.name) : handleFileClick(file.name)"
            :class="{ 'selected': selectedFile === file.name }"
          >
            <div class="file-icon">{{ file.type === 'folder' ? '📁' : '📄' }}</div>
            <div class="file-name">{{ file.name }}</div>
            <div class="file-size">{{ file.size }}</div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 底部操作栏 -->
    <div class="dialog-bottom">
      <div class="bottom-left">
        <div class="file-name-input">
          <label for="filename">文件名:</label>
          <input 
            type="text" 
            id="filename" 
            v-model="selectedFile"
            placeholder="输入文件名"
          >
        </div>
        <div class="file-type-select">
          <label for="filetype">文件类型:</label>
          <select 
            id="filetype" 
            v-model="selectedFileType"
          >
            <option 
              v-for="type in fileTypes" 
              :key="type.value"
              :value="type.value"
            >
              {{ type.label }}
            </option>
          </select>
        </div>
      </div>
      <div class="bottom-right">
        <button @click="closeDialog">取消</button>
        <button @click="confirmSelection" class="confirm-btn">确认</button>
      </div>
    </div>
  </dialog>
</template>

<style scoped>
.openfiledialog {
  display: flex;
  flex-direction: column;
  width: 800px;
  height: 600px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  padding: 0;
  overflow: hidden;
  font-family: Arial, sans-serif;
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: #f5f5f5;
  border-bottom: 1px solid #ddd;
}

.dialog-header .title {
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.dialog-body {
  display: flex;
  flex: 1;
  overflow: hidden;
}

/* 左侧导航栏样式 */
.left-sidebar {
  width: 200px;
  background-color: #f5f5f5;
  border-right: 1px solid #ddd;
  overflow-y: auto;
  padding: 10px 0;
}

.sidebar-section {
  margin-bottom: 20px;
}

.section-title {
  padding: 5px 15px;
  font-size: 12px;
  color: #666;
  font-weight: bold;
  text-transform: uppercase;
}

.sidebar-item {
  padding: 8px 15px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.sidebar-item:hover {
  background-color: #e0e0e0;
}

/* 右侧内容区样式 */
.right-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.path-bar {
  padding: 10px 15px;
  background-color: #fafafa;
  border-bottom: 1px solid #ddd;
  font-size: 14px;
  color: #333;
}

.file-list {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
}

.file-item {
  display: flex;
  align-items: center;
  padding: 8px 10px;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.file-item:hover {
  background-color: #f0f0f0;
}

.file-item.selected {
  background-color: #e3f2fd;
  border: 1px solid #2196f3;
}

.file-icon {
  margin-right: 10px;
  font-size: 18px;
}

.file-name {
  flex: 1;
  font-size: 14px;
}

.file-size {
  font-size: 12px;
  color: #666;
  margin-left: 10px;
}

/* 底部操作栏样式 */
.dialog-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background-color: #f5f5f5;
  border-top: 1px solid #ddd;
}

.bottom-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.file-name-input, .file-type-select {
  display: flex;
  align-items: center;
  gap: 8px;
}

.file-name-input label, .file-type-select label {
  font-size: 14px;
  color: #333;
}

.file-name-input input, .file-type-select select {
  padding: 6px 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.file-name-input input {
  width: 200px;
}

.bottom-right {
  display: flex;
  gap: 10px;
}

.bottom-right button {
  padding: 8px 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.bottom-right button:hover {
  background-color: #e0e0e0;
}

.bottom-right .confirm-btn {
  background-color: #2196f3;
  color: white;
  border-color: #2196f3;
}

.bottom-right .confirm-btn:hover {
  background-color: #1976d2;
}
</style>