<script setup>
import {inject,defineProps,computed} from "vue";
const update = inject("pbarupdate")
const props = defineProps({
  task_ID: String,
  task_name: String,
})

const taskData = computed(() => {
  const data = update.value.update_list || []
  let updates
  for (let item of data) {
    if (item.task_id === props.task_ID || props.task_ID === null) {
      updates = item
    }}
  return updates
})

const time_all = computed(() => {
  const data = taskData.value;
  return data && data.time_all ? data.time_all : "00:00:00"
})
const time_left = computed(() => {
  const data = taskData.value;
  return data && data.time_left ? data.time_left : "00:00:00"
})
const index = computed(() => {
  const data = taskData.value;
  return data && data.index ? data.index : "0%"
})
</script>

<template>
  <div class="task-title" >{{props.task_name}}</div>
  <div class="center-box">
    <div class="progress-bar">
      <div class="inner-bar" :style="{width: index}"></div>
    </div>
    <div>{{time_all}}|{{time_left}}</div>
  </div>
</template>

<style scoped>
.task-title,.center-box {
  margin-left: 12px;
  margin-right: 12px;
}
.task-title {
  padding-left: 10px;
  margin-top: 3px;
}
.center-box {
  display: flex;
  margin-bottom: 3px;
}

.progress-bar {
  width: 100%;
  height: 18px;
  background: #cdcdcd;
  border-radius: 20px;
  overflow: hidden;
  transition: all 2s ease;
  margin:auto 12px auto 0;
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