<script setup>
import ProgressBar from "@/components/ProgressBar.vue";
</script>

<template>
  <div class="box">
    <div class="box-1">
      <button>导入</button>
      <button>保存</button>
      <button>开始采集</button>
      <button>采集模式</button>
    </div>
    <div class="box-2"></div>
    <div class="box-3"><ProgressBar /></div>
  </div>
</template>

<style scoped>
.box {
  height: 100%;
  width: 100%;
  box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.29),-1px -1px 3px rgba(184, 182, 182, 0.83);
  border-radius: 18px;
}

.box-1 {
  margin: 15px 0 0 20px;
}

.box-1 button {
  display: inline-block;
  background: white;
  border: 0;
  padding: 5px 10px 5px 10px;
  border-radius: 10px;
  box-shadow: 2px 2px 2px rgba(0, 0, 0, 0.45),-1px -1px 4px rgba(0, 0, 0, 0.45);
  margin: 0 10px 0 10px;
}

.box-3 {
  margin: 10px 10px 15px 10px;
}

</style>