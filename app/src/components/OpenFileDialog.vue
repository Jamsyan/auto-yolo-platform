<script setup>
import {defineProps, ref, watch} from "vue"

const props = defineProps({
  title:String
})

const filedialog = ref(null)
let model = ref(false)

function showDialog () {
  model.value = true
  if (model.value === true) {
    filedialog.value.showModal()
    console.log('model:',model.value)
  }
}

function closeDialog () {
  if (model.value === true) {
    model.value = false
  }
}

watch(model,showDialog)

</script>

<template>
  <dialog class="openfiledialog" ref="filedialog" v-if="model">
    <div class="dialog-header">
      <div class="title">{{props.title}}</div>
    </div>
    <div class="dialog-body"></div>
    <div class="dialog-buttom">
      <button @click="closeDialog">关闭</button>
    </div>
  </dialog>
</template>

<style scoped>
.openfiledialog {
  display: flex;
  flex-direction: column;
  width: 300px;
  height: 400px;
}

.dialog-header {
  display: flex;
  flex-direction: row;

}
</style>