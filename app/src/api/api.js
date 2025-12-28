import {ref} from 'vue';

export const pbarsubmit = ref({
        "type": "null",
        "task_list": [{
            "task_id": null,  // 修复：使用task_id以匹配后端
            "task_name": null,
        }]
    });

export const pbarupdate = ref({
        "type": "null",
        "update_list":[{
            "task_id": null,  // 修复：使用task_id以匹配后端
            "time_all": "00:00:00",
            "time_left": "00:00:00",
            "index": 0
        }]
    });