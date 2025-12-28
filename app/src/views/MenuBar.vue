<script setup>
</script>

<template>
  <div class="menu-box">
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

.menu-bar{
  background: #ffffff;
  box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.29),-1px -1px 3px rgba(184, 182, 182, 0.83);
  border-radius: 15px;
  margin: 0 0 0 0;
}
.menu-bar-items {
  display: inline-block;
  padding: 10px 8px 10px 8px;
  margin: 8px 10px 8px 10px;
  color: #303030;
  font-size: 15px;
  font-weight: bold;
  border-bottom: 3px solid transparent;
  border-radius: 15px;
  transition: all 0.3s ease;
  &:hover {
    background: rgba(179, 179, 179, 0.37);
    box-shadow: 5px 5px 5px rgba(0,0,0,0.3), -2px -2px 3px rgba(189, 186, 186, 0.74);
  }
}
</style>