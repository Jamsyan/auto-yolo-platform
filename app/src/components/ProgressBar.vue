<script setup>
import {reactive} from "vue";
const progress = reactive({
  task_id: "",
  labels: "",
  totel: "",
  time: "",
})

</script>

<template>
  <div>
    <div class="progress-bar">
      <div class="inner-bar" :style="{width: progress + '%'}"></div>
    </div>
  </div>
</template>

<style scoped>
.box {
  width: 100%;
  display: grid;
  grid-template-rows: 10% 90%;
}
.progress-bar {
  width: 100px;
  height: 15px;
  background: white;
  border-radius: 10px;
  overflow: hidden;
}
.inner-bar {
  height: 100%;
  background: #0896c5;
  transition: width 1s ease;
}
</style>