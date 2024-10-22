<script setup lang="ts">
import { ref } from 'vue'

const output = ref('')  // 用于存储 API 返回的结果


const runCommand = async () => {
  output.value = ''  // 每次运行命令时，先清空输出
  
  try {
    // 使用 fetch API 调用 FastAPI 流式输出
    const response = await fetch('/api/run-mysqlsh-help');
    
    if (!response.ok) {
      output.value = `Error: ${response.statusText}`;
      return;
    }

    // 处理流式响应
    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');

    let done = false;
    while (!done) {
      const { value, done: streamDone } = await reader.read();
      done = streamDone;
      // 解码并追加流数据
      output.value += decoder.decode(value, { stream: true });
    }
  } catch (error) {
    console.error(error);
    output.value = `Error: ${error.message}`;
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