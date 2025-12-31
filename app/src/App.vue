<script setup>
import {onMounted, onUnmounted, provide} from 'vue';
import {getMessages, initConnection, sendMessages, wsManager} from './api/WsConnManger';
import {RouterView} from 'vue-router';
import MenuBar from "./views/MenuBar.vue";
import {pbarsubmit, pbarupdate} from "./api/api.js"

provide("pbarsubmit", pbarsubmit);
provide("pbarupdate", pbarupdate);

// 初始化连接
function initializeWebSocket() {
    initConnection();
    getMessages(function(event) {
        const data = JSON.parse(event.data);
        console.log('收到消息:', data);
        if (data.type === 'keep') {sendMessages(200)}
        else if (data.type === "ProgressBar.submit") {Object.assign(pbarsubmit.value, data)}
        else if (data.type === "ProgressBar.update") {Object.assign(pbarupdate.value, data)}
    });
}

onMounted(function() {
    console.log('组件挂载,初始化WebSocket');
    initializeWebSocket();
});

// 在组件卸载时清理
onUnmounted(function() {
    console.log('组件卸载,关闭WebSocket');
    wsManager.close();
});

// 提供WebSocket相关功能给子组件
provide('websocket', {
    sendMessage: sendMessages,
    isConnected: function() { return wsManager.isConnected; }
});

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
