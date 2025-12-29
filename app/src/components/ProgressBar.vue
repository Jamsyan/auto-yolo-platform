<script setup>
import ProgressBarItem from "./subcompoents/ProgressBarItem.vue";
import {computed, inject, onUnmounted, ref, watch} from "vue"
import {pbarsubmit, pbarupdate} from "@/api/api"

const submit = inject("pbarsubmit")
const update = inject("pbarupdate")

// 存储最后更新时间
const lastUpdateTime = ref(Date.now())
let timeoutId = null

const data = computed(() => submit.value.task_list || [])

// 监听整个update对象的变化，而不仅仅是update_list
watch(() => update.value, () => {
  // 更新最后活动时间
  lastUpdateTime.value = Date.now()
  
  // 清除之前的定时器
  if (timeoutId) {
    clearTimeout(timeoutId)
  }
  
  // 设置10秒后复写初始数据的定时器
  timeoutId = setTimeout(() => {
    const now = Date.now()
    // 如果10秒内没有新的数据更新，则复写初始数据
    if (now - lastUpdateTime.value >= 10000) {
      console.log("10秒内无更新，复写初始数据");
      // 复写pbarupdate为初始状态
      pbarupdate.value.update_list = [{
        "task_id": null,
        "time_all": "00:00:00",
        "time_left": "00:00:00",
        "index": 0
      }]
      
      // 复写pbarsubmit为初始状态
      pbarsubmit.value.task_list = [{
        "task_id": null,
        "task_name": null,
      }]
    }
  }, 10000)
}, { deep: true })

// 组件卸载时清理定时器
onUnmounted(() => {
  if (timeoutId) {
    clearTimeout(timeoutId)
  }
})
</script>

<template>
  <div class="pbar-boxs">
    <ProgressBarItem
        v-for="item in data"
        :key="item.task_id"
        :task_ID="item.task_id"
        :task_name="item.task_name"
    />
  </div>
</template>

<style scoped>
.pbar-boxs {
  width: 100%;
  border-radius: 18px;
  box-shadow: 2px 2px 2px rgba(39, 39, 39, 0.33), -1px -1px 4px rgba(126, 126, 126, 0.6);
}
</style>