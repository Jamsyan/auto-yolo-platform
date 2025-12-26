<script setup>
import {provide,ref} from "vue";
import ProgressBar from "./components/ProgressBar.vue";
import MenuBar from "./views/MenuBar.vue";

const pbarsubmit = ref({
  "type": "null",
  task: [
       {
         "task_ID": null,
         "task_name": null,
         "total": 0
       }
  ]
});

const pbarupdate = ref({});

provide("pbarsubmit", pbarsubmit);
provide("pbarupdate", pbarupdate);




</script>

<template>
  <div class = 'app'>
    <div class="app_top">
      <MenuBar />
    </div>
    <div class="app_center">
      <router-view />
    </div>
    <div class="app_bottom">
      <ProgressBar />
    </div>
  </div>
</template>

<style>
.app {
}
.app_top {}
.app_center {
  display: grid;
  grid-template-columns: 30% 70%;
}
.app_bottom {}
</style>
