<script setup>
import SubProgressBar from "./subcompoents/SubProgressBar.vue";
import {inject} from "vue"
const submit = inject("pbarsubmit")

</script>

<template>
  <div class="box">
    <SubProgressBar
        v-for="item in submit.task"
        :key="item.task_ID"
        :task_ID="item.task_ID"
        :task_name="item.task_name"
    />
  </div>
</template>

<style scoped>
.box {
  display: flex;
  flex-direction: column;
  width: 100%;
  font-size: 18px;
  font-weight: bold;
  margin: 20px 0 0 0;
  border-radius: 18px;
  box-shadow: 8px 8px 8px rgba(0, 0, 0, 0.34), -8px -8px 8px rgba(126, 126, 126, 0.6);
}
</style>