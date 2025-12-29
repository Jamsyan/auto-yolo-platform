<script setup>
import FileMenuBarItem from "@/components/subcompoents/FileMenuBarItem.vue";
</script>

<template>
  <div class="filemenubar">
    <div id="in-box"><FileMenuBarItem/></div>
  </div>
</template>

<style scoped>
.filemenubar {
  //border: 5px ridge rgba(202, 199, 199, 0.3);
  margin: 10px 6px 10px 12px;
  padding: 5px 5px 5px 5px;
  border-radius: 10px;
  box-shadow:
      3px 3px 4px rgba(0, 0, 0, 0.31),
      -2px -2px 2px rgba(136, 136, 136, 0.4);
  #in-box {
    display: flex;
    flex-direction: row;
    width: 100%;
    height: 100%;
    min-width: 100px;
    min-height: 400px;
    border-radius: 12px;
    box-shadow:
      inset 1px 1px 2px rgba(145, 145, 145, 0.37),
      inset -2px -2px 4px rgba(39, 39, 39, 0.22);
  }
}
</style>