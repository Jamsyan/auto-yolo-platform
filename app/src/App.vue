<script>
import ProgressBar from "./components/ProgressBar.vue";
import MenuBar from "./views/MenuBar.vue";
export default {
  name: "App",
  components: {
    MenuBar,
    ProgressBar,
  },
};

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
