<script setup>
import {ref,inject} from 'vue';
import ProgressBar from "@/components/ProgressBar.vue";
import FileMenuBar from "@/components/FileMenuBar.vue";
import OpenFileDialog from "@/components/OpenFileDialog.vue";

// 获取websocket注入
const websocket = inject("websocket");

// 控制对话框显示的变量
const isDialogVisible = ref(false);

function sendMessages(message) {
  return websocket.sendMessage(message);
}

function showdialog() {
  isDialogVisible.value = true;
  const data = {type: "Dialog.openfile",}
  sendMessages(data)
}

// 处理文件选择确认
function handleFileConfirm(filename) {
  console.log('Selected file:', filename);
}

</script>

<template>
  <div class="datacollection">
    <div id="dcbox1">
      <button @click="showdialog">导入</button>
      <button>保存</button>
      <button>开始采集</button>
      <button>采集模式</button>
      <button>对象标签</button>
    </div>
    <div id="dcbox2">
      <FileMenuBar/>
      <div id="showbox"></div>
    </div>
    <div id="dcbox3"><ProgressBar /></div>
    <OpenFileDialog v-model="isDialogVisible" @confirm="handleFileConfirm" />
  </div>
</template>

<style scoped>
.datacollection {
  height: 100%;
  width: 100%;
  box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.29),-1px -1px 3px rgba(184, 182, 182, 0.83);
  border-radius: 10px;
  overflow: hidden;
}

#dcbox1 {
  box-shadow: 0 2px 2px rgba(0,0,0,0.2);
  padding: 10px 20px 10px 20px;
}

#dcbox1 button {
  display: inline-block;
  background: white;
  border: 0;
  padding: 5px 10px 5px 10px;
  border-radius: 10px;
  box-shadow: 2px 2px 2px rgba(0, 0, 0, 0.45),-1px -1px 4px rgba(0, 0, 0, 0.45);
  margin: 0 10px 0 10px;
  &:hover {

  }
  &:focus {

  }
}

#dcbox2 {
  display: flex;
  flex-direction: row;
  #showbox {}
}

#dcbox3 {
  box-shadow: 0 -2px rgba(0,0,0,0.2);
  padding: 10px 10px 10px 10px;
}

</style>