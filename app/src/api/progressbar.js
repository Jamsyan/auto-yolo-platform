export function submit(message) {
    console.log(message.task)
    return {
        "type": message.type,
        "task": message.task,
    }
}

export function update(message) {
    return  {
        "type": message.type,
        "task_ID": message.task_ID,
        "time_all": message.time_all,
        "time_left": message.time_left,
        "task_log": message.task_log,
        "index": message.index
    }
}