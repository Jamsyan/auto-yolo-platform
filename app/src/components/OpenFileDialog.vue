<script setup>
import {defineProps, defineExpose, ref, onBeforeUnmount} from "vue"

const props = defineProps({
  title: {
    type: String,
    default: "打开文件"
  }
})

// 控制对话框显示的变量
let model = ref(false)

// 暴露model属性给父组件
defineExpose({
  model
})

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
const currentPath = ref("")

// 关闭对话框动画时长（毫秒）
const closeAnimationDuration = 300

// 关闭对话框
function closeDialog () {
  console.log("开始关闭对话框...")
  
  // 执行关闭动画
  const dialogElement = document.querySelector('.openfiledialog')
  if (dialogElement) {
    dialogElement.style.transition = `opacity ${closeAnimationDuration}ms ease-out`
    dialogElement.style.opacity = '0'
    
    // 动画结束后销毁控件
    setTimeout(() => {
      destroyDialog()
    }, closeAnimationDuration)
  } else {
    // 如果没有找到元素，直接销毁
    destroyDialog()
  }
}

// 销毁对话框
function destroyDialog () {
  console.log("开始销毁对话框...")
  
  // 关闭对话框
  model.value = false
  
  // 释放内存占用的变量及资源
  selectedFile.value = ""
  selectedFileType.value = "*"
  currentPath.value = ""
  
  console.log("对话框销毁完成")
}

// 确认选择
function confirmSelection () {
  // 这里可以添加确认选择的逻辑
  console.log("Selected file:", selectedFile.value)
  closeDialog()
}

// 处理文件点击
function handleFileClick (fileName) {
  selectedFile.value = fileName
}

// 处理文件夹点击
function handleFolderClick (folderName) {
  // 这里可以添加进入文件夹的逻辑
  console.log("Enter folder:", folderName)
  currentPath.value = currentPath.value + folderName + "/"
}

// 组件销毁前清理资源
onBeforeUnmount(() => {
  console.log("组件即将销毁，清理资源...")
  // 这里可以添加更多清理逻辑，如解绑事件监听器、清除定时器等
})

</script>

<template>
  <dialog class="openfiledialog" v-if="model">
    <!-- 顶部标题栏 -->
    <div class="dialog-header">
      <div class="title">{{ props.title }}</div>
    </div>
    
    <!-- 中间内容区 -->
    <div class="dialog-body">
      <!-- 左侧导航栏 -->
      <div class="left-sidebar">
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
      
      <!-- 右侧内容区 -->
      <div class="right-content">
        <!-- 路径栏 -->
        <div class="path-bar">{{ currentPath }}</div>
        
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
      <div class="file-controls">
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
      <div class="dialog-buttons">
        <button @click="closeDialog">取消</button>
        <button @click="confirmSelection" class="confirm-btn">确认</button>
      </div>
    </div>
  </dialog>
</template>

<style scoped>
.openfiledialog {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000;
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
  background-color: white;
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

.file-controls {
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

.dialog-buttons {
  display: flex;
  gap: 10px;
}

.dialog-buttons button {
  padding: 8px 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.dialog-buttons button:hover {
  background-color: #e0e0e0;
}

.dialog-buttons .confirm-btn {
  background-color: #2196f3;
  color: white;
  border-color: #2196f3;
}

.dialog-buttons .confirm-btn:hover {
  background-color: #1976d2;
}
</style>