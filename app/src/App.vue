<script setup>
import {onMounted, provide} from "vue";
import ProgressBar from "./components/ProgressBar.vue";
import MenuBar from "./views/MenuBar.vue";
import {pbarsubmit, pbarupdate} from "./api/api.js"

provide("pbarsubmit", pbarsubmit);
provide("pbarupdate", pbarupdate);

onMounted(()=> {
  const socket = new WebSocket("ws://localhost:8000/api/");
  socket.onopen = () => {
    socket.send(200) //连接成功
    console.log('连接成功')

    socket.onmessage = function(event) {
      const data = JSON.parse(event.data)
      // console.log("数据",data)
      // console.log("数据类型",typeof data)
      // console.log("内部数据",data.type)
      if (data.type === "keep") {socket.send(200)} // 连接成功
      else if (data.type === "ProgressBar.submit") {Object.assign(pbarsubmit.value, data)}
      else if (data.type === "ProgressBar.update") {Object.assign(pbarupdate.value, data)}
    };}})

</script>

<template>
  <div class = 'app'>
    <div class="app_top"><MenuBar /></div>
    <div class="app_center"></div>
    <div class="app_bottom"><ProgressBar /></div>
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
.app_bottom {
}
</style>
