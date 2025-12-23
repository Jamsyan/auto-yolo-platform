<script setup>
import {inject,computed} from "vue";
const submit = inject("pbarsubmit")
const update = inject("pbarupdate")

const pbar = computed(() => ({
  task_ID: submit.value?.task_ID||null,
  total: submit.value?.total||null,
  index: update.value?.index||0,
  time_all: update.value?.time_all||"00:00:00",
  time_left: update.value?.time_left||"00:00:00",
  task_log: update.value?.task_log||null,
}))

</script>

<template>
  <div class="box">

    <div class="inside-box-1">

      <div class="task-title">{{pbar.task_ID}}</div>

    </div>

    <div class="inside-box-2">

      <div class="task-time">{{pbar.time_all}}|{{pbar.time_left}}</div>
      <div class="progress-bar">
        <div class="inner-bar" :style="{width: update.index + '%'}"></div>
      </div>

    </div>

    <div class="inside-box-3">

      <div class="task-log">{{pbar.task_log}}</div>

    </div>

  </div>
</template>

<style scoped>
.box {
  display: flex;
  flex-direction: column;
  width: 100%;
  font-size: 18px;
  font-weight: bold;
  margin-top: 20px;
  border-radius: 15px;
  box-shadow: 8px 8px 8px rgba(0, 0, 0, 0.34), -8px -8px 8px rgba(126, 126, 126, 0.6);
}
.inside-box-1  {}
.inside-box-2 {
  display: flex;
  height: 40px;
  flex-direction: row;
}
.inside-box-3 {}
.task-title {
  text-align: left;
  margin: auto;
  margin-left: 10px;
}
.task-time {
  text-align: left;
  margin: auto;
  margin-left: 10px;
}

.task-log {
  text-align: left;
  margin: auto;
  margin-left: 10px;
}

.progress-bar {
  width: 80%;
  height: 50%;
  background: #cdcdcd;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 2px 2px 2px rgba(221, 221, 221, 0.2);
  margin: auto;
  margin-left: 0;
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