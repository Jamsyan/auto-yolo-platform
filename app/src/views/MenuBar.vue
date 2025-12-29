<script setup>
import {RouterLink} from 'vue-router'
</script>

<template>
  <nav class="menu-bar">
    <router-link to="/">数据采集</router-link>
    <router-link to="/">数据标注</router-link>
    <router-link to="/">训练监控</router-link>
    <router-link to="/">云资源配置</router-link>
    <router-link to="/">关于</router-link>
  </nav>
</template>

<style scoped>
.menu-bar{
  display: flex;
  flex-direction: row;
  background: #ffffff;
  box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.29),-1px -1px 3px rgba(184, 182, 182, 0.83);
  border-radius:10px;
  padding: 0 0 0 20px;
}

.menu-bar a {
  color: #303030;
  font-size: 15px;
  text-decoration: none;
  border-radius: 10px 10px 0 0;
  margin: 10px 15px 0 15px;
  padding: 10px 10px 10px 10px;
  border-bottom: 4px solid transparent;

  &:hover {
    transition: all 0.4s ease;
    background: rgba(95, 198, 172, 0.42);
    border-bottom: 4px solid rgba(14, 154, 102, 0.42);
    box-shadow: -1px -1px 3px rgba(184, 182, 182, 0.83),1px 0 2px rgba(161, 161, 161, 0.46);
  }
  &:focus {
    animation: focusframe 1s ease;
    background-image:linear-gradient(to top,#A8E6CF,#1B9E85);
  }
}
</style>