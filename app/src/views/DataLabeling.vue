<script setup>
import ProgressBar from "@/components/ProgressBar.vue";
import FileMenuBar from "@/components/FileMenuBar.vue";
</script>

<template>
  <div class="datalabeling">
    <div id="dlbox1">
      <button>导入</button>
      <button>保存</button>
      <button>开始标注</button>
      <button>标注模式</button>
      <button>标签管理</button>
    </div>
    <div id="dlbox2">
      <FileMenuBar/>
      <div id="labelarea"></div>
    </div>
    <div id="dlbox3"><ProgressBar /></div>
  </div>
</template>

<style scoped>
.datalabeling {
  height: 100%;
  width: 100%;
  box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.29),-1px -1px 3px rgba(184, 182, 182, 0.83);
  border-radius: 10px;
  overflow: hidden;
}

#dlbox1 {
  box-shadow: 0 2px 2px rgba(0,0,0,0.2);
  padding: 10px 20px 10px 20px;
}

#dlbox1 button {
  display: inline-block;
  background: white;
  border: 0;
  padding: 5px 10px 5px 10px;
  border-radius: 10px;
  box-shadow: 2px 2px 2px rgba(0, 0, 0, 0.45),-1px -1px 4px rgba(0, 0, 0, 0.45);
  margin: 0 10px 0 10px;
}

#dlbox2 {
  display: flex;
  flex-direction: row;
  #labelarea {}
}

#dlbox3 {
  box-shadow: 0 -2px rgba(0,0,0,0.2);
  padding: 10px 10px 10px 10px;
}
</style>