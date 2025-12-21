<script>
import ProgressBar from "./components/ProgressBar.vue";
import LayoutSidebar from "@/components/LayoutSidebar.vue";
export default {
  name: "App",
  components: {
    LayoutSidebar,
    ProgressBar,
  },
  data() {
    return {
      'progressnum': 10,
    };
  },
};
</script>

<template>
  <header>
    <div class="top-container">

  </div>
  </header>
  <main>
    <div class="main-container">
    <aside><LayoutSidebar/></aside>
  </div>
  </main>
  <footer>
    <div class="footer-container">
    <ProgressBar :progress = 'progressnum'/>
  </div>
  </footer>
</template>

<style>
.top-container {
  width: 1000px;
  height: 20%;
}
.main-container {
  width: 1000px;
  height: 60%;
}
.footer-container {
  width: 1000px;
  height: 20%;
}
</style>
