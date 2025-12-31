<script setup>
import {defineProns} from 'vue'
import {sendMessages} from "@/api/WsConnManger";

const props = defineProns({
  datas:{
    name:String,
    path:String
  }
})

function send_dirname() {
  let dir_name = props.datas.name
  const text = {
    'type':'openfile.checkdir',
    'path':dir_name
  }
  sendMessages(text)
}
</script>

<template>
  <div class="open-file-dir-item" @click="send_dirname">{{props.datas.name}}</div>
</template>

<style scoped>
.open-file-dir-item {
  width: 25%;
  background-color: #f5f5f5;
  border-right: 1px solid #ddd;
  overflow-y: auto;
  padding: 10px 0;
}
</style>