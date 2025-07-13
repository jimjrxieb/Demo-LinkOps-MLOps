// src/store/useTaskStore.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useTaskStore = defineStore('task', () => {
  // State
  const tasks = ref([])
  const taskQueue = ref([])
  const currentTask = ref(null)
  const taskHistory = ref([])

  // Getters
  const getPendingTasks = computed(() => {
    return tasks.value.filter(task => task.status === 'pending')
  })

  const getProcessingTasks = computed(() => {
    return tasks.value.filter(task => task.status === 'processing')
  })

  const getCompletedTasks = computed(() => {
    return tasks.value.filter(task => task.status === 'completed')
  })

  const getFailedTasks = computed(() => {
    return tasks.value.filter(task => task.status === 'failed')
  })

  const getTaskById = computed(() => {
    return (id) => tasks.value.find(task => task.id === id)
  })

  // Actions
  const createTask = (taskData) => {
    const task = {
      id: Date.now().toString(),
      ...taskData,
      status: 'pending',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      progress: 0,
      logs: []
    }
    
    tasks.value.push(task)
    taskQueue.value.push(task.id)
    
    return task
  }

  const updateTaskStatus = (taskId, status, progress = null) => {
    const task = tasks.value.find(t => t.id === taskId)
    if (task) {
      task.status = status
      task.updatedAt = new Date().toISOString()
      if (progress !== null) {
        task.progress = progress
      }
      
      if (status === 'completed' || status === 'failed') {
        taskHistory.value.push({ ...task })
      }
    }
  }

  const addTaskLog = (taskId, message, level = 'info') => {
    const task = tasks.value.find(t => t.id === taskId)
    if (task) {
      task.logs.push({
        id: Date.now(),
        message,
        level,
        timestamp: new Date().toISOString()
      })
    }
  }

  const setCurrentTask = (taskId) => {
    currentTask.value = taskId
  }

  const clearTaskQueue = () => {
    taskQueue.value = []
  }

  const removeTask = (taskId) => {
    const index = tasks.value.findIndex(t => t.id === taskId)
    if (index > -1) {
      tasks.value.splice(index, 1)
    }
    
    const queueIndex = taskQueue.value.indexOf(taskId)
    if (queueIndex > -1) {
      taskQueue.value.splice(queueIndex, 1)
    }
  }

  return {
    // State
    tasks,
    taskQueue,
    currentTask,
    taskHistory,
    
    // Getters
    getPendingTasks,
    getProcessingTasks,
    getCompletedTasks,
    getFailedTasks,
    getTaskById,
    
    // Actions
    createTask,
    updateTaskStatus,
    addTaskLog,
    setCurrentTask,
    clearTaskQueue,
    removeTask
  }
}) 