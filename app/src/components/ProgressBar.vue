<script setup>
import SubProgressBar from "./subcompoents/SubProgressBar.vue";
import {inject,computed} from "vue"
const submit = inject("pbarsubmit")
const data = computed(() => submit.value.task_list || [])
</script>

<template>
  <div class="box">
    <SubProgressBar
        v-for="item in data"
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
  border-radius: 18px;
  box-shadow: 8px 8px 5px rgba(39, 39, 39, 0.33), -3px -3px 8px rgba(126, 126, 126, 0.6);
  margin: 30px auto auto auto;
}
</style>