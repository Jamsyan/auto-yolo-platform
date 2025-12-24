<script setup>
import {inject,defineProps} from "vue";

const props = defineProps({
  task_ID: String,
  task_name: String,
  show: Boolean
})

const update = inject("pbarupdate");
const time_all = update[props.task_ID].time_all;
const time_left = update[props.task_ID].time_left;
const task_log = update[props.task_ID].task_log;
const index = update[props.task_ID].index;

</script>

<template>
<div class="inside-box-1">
  <div class="task-title" v-if="show">{{props.task_ID}}|{{props.task_name}}</div>
</div>
<div class="inside-box-2">
  <div class="task-time">
    {{time_all}}|{{time_left}}
  </div>
  <div class="progress-bar">
    <div class="inner-bar" :style="{width: index + '%'}"></div>
  </div>
</div>
<div class="inside-box-3" v-if="task_log && show">
  <div class="task-log">{{task_log}}</div>
</div>
</template>

<style scoped>

.inside-box-1  {}

.inside-box-2 {
  display: flex;
  height: 40px;
  flex-direction: row;
}
.inside-box-3 {}

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
  margin: auto auto auto 0;
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