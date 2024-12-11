<!-- frontend/src/views/RoomsView.vue -->

<template>
  <div>
    <el-row>
      <el-col :span="24">
        <el-button type="primary" @click="showCheckIn=true" class="mr-2">办理入住</el-button>
        <el-button type="warning" @click="showCheckOut=true">办理退房</el-button>
      </el-col>
    </el-row>

    <div class="room-cards-grid">
      <RoomCard
        v-for="room in rooms"
        :key="room.roomNumber"
        :room="room"
        @refresh="updateRoomData"
      />
    </div>

    <!-- 移除错误的 <el-loading> 组件 -->
    <!-- <el-loading :fullscreen="true" :text="'加载中...'" v-if="loading"></el-loading> -->

    <CheckInModal
      :visible.sync="showCheckIn"
      @refresh="updateRoomData"
    />
    <CheckOutModal
      :visible.sync="showCheckOut"
      @refresh="updateRoomData"
    />
  </div>
</template>

<script>
import { ref } from 'vue'
import { fetchRoomInfo } from '../api'
import RoomCard from '../components/RoomCard.vue'
import CheckInModal from '../components/CheckInModal.vue'
import CheckOutModal from '../components/CheckOutModal.vue'
import { ElLoading, ElNotification } from 'element-plus'

export default {
  name: 'RoomsView',
  components: { RoomCard, CheckInModal, CheckOutModal },
  data() {
    return {
      rooms: [],
      showCheckIn: false,
      showCheckOut: false,
      loading: false // 可以移除或保留，根据需要
    }
  },
  methods: {
    async updateRoomData() {
      // 显示加载动画
      const loadingInstance = ElLoading.service({
        lock: true,
        text: '加载中...',
        background: 'rgba(0, 0, 0, 0.7)',
      })

      try {
        const res = await fetchRoomInfo()
        console.log('Fetched room info:', res.data)
        this.rooms = res.data
      } catch (err) {
        console.error('Error fetching room info:', err)
        ElNotification.error({
          title: '错误',
          message: '获取房间信息失败'
        })
      } finally {
        // 关闭加载动画
        loadingInstance.close()
      }
    }
  },
  mounted() {
    this.updateRoomData()
    // 定期更新房间数据
    setInterval(this.updateRoomData, 10000)
  }
}
</script>

<style scoped>
.room-cards-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr); /* 五列布局 */
  gap: 10px; /* 网格间距 */
  margin-top: 20px;
}

@media (max-width: 1600px) {
  .room-cards-grid {
    grid-template-columns: repeat(4, 1fr); /* 四列布局 */
  }
}

@media (max-width: 1200px) {
  .room-cards-grid {
    grid-template-columns: repeat(3, 1fr); /* 三列布局 */
  }
}

@media (max-width: 768px) {
  .room-cards-grid {
    grid-template-columns: repeat(2, 1fr); /* 两列布局 */
  }
}

@media (max-width: 480px) {
  .room-cards-grid {
    grid-template-columns: 1fr; /* 单列布局 */
  }
}

.mr-2 {
  margin-right: 10px;
}
</style>
