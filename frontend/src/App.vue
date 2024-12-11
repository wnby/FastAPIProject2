<!-- frontend/src/App.vue -->
<template>
  <el-container style="height:100vh; position: relative;">
    <!-- 可选：添加背景视频 -->
    <!--
    <video autoplay muted loop id="background-video">
      <source src="@/assets/background.mp4" type="video/mp4">
      Your browser does not support HTML5 video.
    </video>
    -->
    <Header />
    <el-main>
      <RoomsView/>
    </el-main>
  </el-container>
</template>

<script>
import RoomsView from './views/RoomsView.vue'
import Header from './components/Header.vue'

export default {
  name: 'App',
  components: { RoomsView, Header }
}
</script>

<style>
/* 可选：背景视频样式 */
/*
#background-video {
  position: fixed;
  right: 0;
  bottom: 0;
  min-width: 100%;
  min-height: 100%;
  z-index: -1;
  opacity: 0.3;
}
*/
</style>
