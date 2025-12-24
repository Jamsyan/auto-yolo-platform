<script setup>
import {inject} from "vue";
import SubProgressBar from "./subcompoents/SubProgressBar.vue";

const submit = inject("pbarsubmit");

let show = true;
if (submit.task && submit.task.length >= 2) {
  show = false;
}

console.log(submit.task);
</script>

<template>
  <div class="box">
    <SubProgressBar
        v-for="task in submit.task"
        :key="task.task_ID"
        :task_ID="task.task_ID"
        :task_name="task.task_name"
        :show=show
    />
  </div>
</template>

<style scoped>
.box {
  width: 100%;
  min-height: 60px;
  font-size: 18px;
  font-weight: bold;
  margin-top: 20px;
  border-radius: 15px;
  box-shadow: 8px 8px 8px rgba(0, 0, 0, 0.34), -8px -8px 8px rgba(126, 126, 126, 0.6);
}
</style>