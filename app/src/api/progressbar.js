export function submit(message) {
    return {
        "type": message.type,
        "tesk_ID": message.task_ID,
        "total": message.total,
    }
}

export function update(message) {
    return  {
        "type": message.type,
        "time_all": message.time_all,
        "time_left": message.time_left,
        "task_log": message.task_log,
        "index": message.index
    }
}