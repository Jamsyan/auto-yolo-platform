<script setup>
import {ref} from 'vue';
import {RouterLink} from 'vue-router'

// 当前激活的菜单项
const activeMenu = ref('/');
// 设置激活菜单项
const setActiveMenu = (path) => {
  activeMenu.value = path;
};
</script>

<template>
  <nav class="menu-bar">
    <router-link 
      to="/datacollection"
      class="menu-item"
      :class="{ active: activeMenu === '/data_collection' }"
      @click="setActiveMenu('/data_collection')"
    >
      数据采集
    </router-link>
    <router-link 
      to="/datalabeling"
      class="menu-item"
      :class="{ active: activeMenu === '/datalabeling' }"
      @click="setActiveMenu('/datalabeling')"
    >
      数据标注
    </router-link>
    <router-link 
      to="/" 
      class="menu-item"
      :class="{ active: activeMenu === 'training' }"
      @click="setActiveMenu('training')"
    >
      训练监控
    </router-link>
    <router-link 
      to="/" 
      class="menu-item"
      :class="{ active: activeMenu === 'cloud' }"
      @click="setActiveMenu('cloud')"
    >
      云资源配置
    </router-link>
    <router-link 
      to="/" 
      class="menu-item"
      :class="{ active: activeMenu === 'about' }"
      @click="setActiveMenu('about')"
    >
      关于
    </router-link>
  </nav>
</template>

<style scoped>
.menu-bar{
  display: flex;
  flex-direction: row;
  box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.29),-1px -1px 3px rgba(184, 182, 182, 0.83);
  border-radius:10px;
  padding: 0 0 0 20px;
}

.menu-item {
  color: #303030;
  font-size: 15px;
  text-decoration: none;
  border-radius: 10px 10px 0 0;
  margin: 10px 15px 0 15px;
  padding: 10px 10px 10px 10px;
  border-bottom: 4px solid transparent;
  transition: all 0.2s ease-in;
  overflow: hidden;
}

.menu-item:hover {
  box-shadow: 0 1px 2px rgba(2,2,3,0.2),-1px -1px 2px rgba(0,0,0,0.4);
}

/* 激活状态样式 */
.menu-item.active {
  border-bottom: 4px solid #1B9E85;
  box-shadow: 0 1px 2px rgba(2,2,3,0.2),-1px -1px 2px rgba(0,0,0,0.4);
}
</style>