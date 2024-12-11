<!-- frontend/src/components/Header.vue -->
<template>
  <el-header>
    <div class="header-content">
      <!-- 替换为你的酒店 Logo，如果没有 Logo，可以移除 <img> 标签 -->
      <img src="@/assets/hotel-logo.jpg" alt="Hotel Logo" class="logo" />
      <h1>酒店空调管理系统</h1>
    </div>
  </el-header>
</template>

<script>
export default {
  name: 'Header',
}
</script>

<style scoped>
.header-content {
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo {
  height: 50px;
  margin-right: 20px;
}

h1 {
  color: white;
  font-size: 24px;
  margin: 0;
}
</style>
