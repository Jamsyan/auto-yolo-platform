<script setup>
import {inject,defineProps} from "vue";
const update = inject("pbarupdate")
const props = defineProps({
  task_ID: String,
  task_name: String,
})

console.log('update类型:', typeof update) // 应该是 'object'
console.log('update值:', update) // 应该显示 RefImpl 对象
console.log('update.value:', update.value) // 应该显示实际数据

const data = update.value[props.task_ID]??{
  time_all: "00:00:00",
  time_left: "00:00:00",
  task_log: null,
  index: 0,
}
const time_all = data.time_all
const time_left = data.time_left
const task_log = data.task_log
const index = data.index

</script>

<template>
  <div class="inside-box-1">
    <div class="task-title">{{props.task_ID}}{{props.task_name}}</div>
  </div>
  <div class="inside-box-2">
    <div class="task-time">
      {{time_all}}|{{time_left}}
    </div>
    <div class="progress-bar">
      <div class="inner-bar" :style="{width: index + '%'}"></div>
    </div>
  </div>
  <div class="inside-box-3">
    <div class="task-log">{{task_log}}</div>
  </div>
</template>

<style scoped>
.inside-box-1  {
}

.inside-box-2 {
  display: flex;
  min-height: 40px;
  height: 40px;
  flex-direction: row;
}
.inside-box-3 {
}

.task-title {
  text-align: left;
  margin: auto auto auto 10px;
}

.task-time {
  text-align: left;
  margin: auto auto auto 10px;
}

.task-log {
  text-align: left;
  margin: auto auto auto 10px;
}

.progress-bar {
  width: 80%;
  height: 50%;
  background: #cdcdcd;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 2px 2px 2px rgba(221, 221, 221, 0.2);
  margin: auto 10px auto 10px;
  transition: all 2s ease;
}

.inner-bar {
  height: 100%;
  background-image: linear-gradient(to right, #A8E6CF,#1B9E85);
  transition: all 2s ease;
  animation: flowLight 3s linear infinite;
}

@keyframes flowLight {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}
</style>