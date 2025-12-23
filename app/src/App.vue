<script setup>
import { onMounted,provide,ref} from "vue";
import ProgressBar from "./components/ProgressBar.vue";
import MenuBar from "./views/MenuBar.vue";
import {submit, update} from "@/api/progressbar.js";

const pbarsubmit = ref({});
const pbarupdate = ref({});

provide("pbarsubmit", submit);
provide("pbarupdate", update);

onMounted(()=> {
  const socket = new WebSocket("ws://localhost:8000/api/");
  socket.onmessage = function(event) {
    console.log("收到消息:", event.data);
    const eventData = JSON.parse(event.data);
    if (eventData.type === "ProgressBar.submit") {
      const newdata = submit(eventData)
      Object.assign(pbarsubmit.value, newdata)
    }
    else if (eventData.type === "ProgressBar.update") {
      const newdata = update(eventData)
      Object.assign(pbarupdate.value, newdata)
    }
  };
})


</script>

<template>
  <div class = 'app'>
    <div class="app_top">
      <MenuBar />
    </div>
    <div class="app_center">
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
