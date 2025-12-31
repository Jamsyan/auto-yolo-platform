<script setup>
import {onMounted, provide} from "vue";
import {RouterView} from 'vue-router';
import MenuBar from "./views/MenuBar.vue";
import {pbarsubmit, pbarupdate} from "./api/api.js"

provide("pbarsubmit", pbarsubmit);
provide("pbarupdate", pbarupdate);

onMounted(()=> {
  const socket = new WebSocket("ws://localhost:8000/api/");
  socket.onopen = () => {
    socket.send(200) //连接成功
    console.log('连接成功')
    }
  socket.onerror = () => {
    console.log("连接丢失",404)
    setTimeout(2000)
  }
  socket.onmessage = function(event) {
    const data = JSON.parse(event.data)
    // console.log("数据",data)
    // console.log("数据类型",typeof data)
    // console.log("内部数据",data.type)
    if (data.type === "keep") {socket.send(200)} // 连接成功
    else if (data.type === "ProgressBar.submit") {Object.assign(pbarsubmit.value, data)}
    else if (data.type === "ProgressBar.update") {Object.assign(pbarupdate.value, data)}
    };
})

</script>

<template>
  <div class = 'app'>
    <div class="app_top"><MenuBar/></div>
    <div class="app_center"><router-view></router-view></div>
    <div class="app_bottom"></div>
  </div>
</template>

<style>
.app {
}

.app_top {}
.app_center {
  display: flex;
  flex-direction: column;
  margin-top: 20px;
}
.app_bottom {
}
</style>
