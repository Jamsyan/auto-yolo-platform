<script setup>
</script>

<template>
  <div class="menu-box">
    <div class="app-title"></div>
    <nav class="menu-bar">
      <div>
        <router-link class="menu-bar-items" to="/">数据采集</router-link>
        <router-link class="menu-bar-items" to="/">数据标注</router-link>
        <router-link class="menu-bar-items" to="/">训练监控</router-link>
        <router-link class="menu-bar-items" to="/">云资源配置</router-link>
        <router-link class="menu-bar-items" to="/">关于</router-link>
      </div>
    </nav>
  </div>
</template>

<style scoped>
.menu-box {
  display: grid;
  grid-template-rows: auto auto;
}
.app-title {
  display: flex;
  box-shadow: 3px 3px 2px rgba(0,0,0,0.3), -3px -3px 4px rgba(90, 90, 90, 0.67);
  border-radius: 5px;
  margin: 0 0 0 0;
}
.menu-bar{
  background: #ffffff;
  box-shadow:6px 6px 8px rgba(0,0,0,0.3),-2px -2px 8px rgba(138, 138, 138, 0.67);
  border-radius: 6px;
  margin: 0 0 0 0;
}
.menu-bar-items {
  display: inline-block;
  padding: 10px 8px 10px 8px;
  margin: 8px 10px 8px 10px;
  color: #4e4c4c;
  font-size: 15px;
  font-weight: bold;
  border-bottom: 3px solid transparent;
  border-radius: 6px;
  transition: all 0.3s ease;
  &:hover {
    box-shadow: 5px 5px 5px rgba(0,0,0,0.3), -2px -2px 3px rgba(189, 186, 186, 0.74);
  }
}
</style>