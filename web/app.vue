<script setup lang="ts">
import { ref } from 'vue'

const output = ref('')  // 用于存储 API 返回的结果

const runCommand = async () => {
  try {
    // 使用 useFetch 调用 FastAPI 的 API
    const { data, error } = await useFetch('/api/run-mysqlsh-help/')
    
    if (error.value) {
      // 如果有错误，打印并显示错误信息
      console.error(error.value)
      output.value = `Error: ${error.value.data.detail || error.value.message}`
    } else {
      // 成功调用后，将返回的数据赋给 output
      output.value = data.value.output
    }
  } catch (e) {
    console.error(e)
    output.value = `Unexpected error: ${e.message}`
  }
}
// 清空输出
const clearOutput = () => {
  output.value = ''
}
</script>

<template>
  <div>
    <h1>Run mysqlsh --help</h1>
    <button @click="runCommand">Run Command</button>
    <button @click="clearOutput" style="margin-left: 10px;">Clear Output</button>
    <pre v-if="output">{{ output }}</pre>
  </div>
</template>

<style scoped>
button {
  margin-bottom: 20px;
  padding: 5px 10px;
  cursor: pointer;
}

pre {
  background-color: #f5f5f5;
  padding: 10px;
  border-radius: 5px;
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>