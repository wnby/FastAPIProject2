<!-- frontend/src/components/RoomCard.vue -->
<template>
  <div
    class="room-container animate__animated"
    :class="[
      cardAnimation,
      room.isPoweredOn ? 'active-room' : 'inactive-room',
      temperatureClass
    ]"
  >
    <div class="room-header">
      <h3>房间 {{ room.roomNumber }}</h3>
      <el-tooltip class="item" effect="dark" content="点击切换开关机状态" placement="top">
        <el-button
          type="text"
          :class="room.isPoweredOn ? 'button-off' : 'button-on'"
          @click="togglePower"
          :loading="loadingPower"
          icon="el-icon-switch"
        >
          {{ room.isPoweredOn ? '关' : '开' }}
        </el-button>
      </el-tooltip>
    </div>

    <div class="status-section">
      <div class="status-item">
        <i :class="temperatureIcon" class="status-icon"></i>
        <span>{{ room.ntem.toFixed(2) }} °C</span>
      </div>
      <div class="status-item">
        <i class="el-icon-finished status-icon"></i>
        <span>{{ room.windSpeed }}</span>
      </div>
      <div class="status-item">
        <i class="el-icon-dollar status-icon"></i>
        <span>{{ room.w.toFixed(2) }} 元</span>
      </div>
    </div>

    <div class="controls-section">
      <el-form label-width="80px" inline>
        <el-form-item label="温度">
          <el-input
            v-model.number="room.targetTemperature"
            type="number"
            :min="18"
            :max="30"
            style="width: 60px;"
            placeholder="18-30"
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="updateTemperature" :loading="loadingTemperature">设置</el-button>
        </el-form-item>
      </el-form>

      <!-- 风速按钮组 -->
      <el-form label-width="60px" inline>
        <el-form-item label="风速">
          <el-button-group>
            <el-button
              type="primary"
              :type="room.windSpeed === 'Low' ? 'primary' : 'default'"
              @click="setWindSpeed('Low')"
            >
              低
            </el-button>
            <el-button
              type="primary"
              :type="room.windSpeed === 'Medium' ? 'primary' : 'default'"
              @click="setWindSpeed('Medium')"
            >
              中
            </el-button>
            <el-button
              type="primary"
              :type="room.windSpeed === 'High' ? 'primary' : 'default'"
              @click="setWindSpeed('High')"
            >
              高
            </el-button>
          </el-button-group>
        </el-form-item>
      </el-form>

      <!-- 模式选择 -->
      <el-form label-width="60px" inline>
        <el-form-item label="模式">
          <el-select
            v-model="room.mode"
            placeholder="模式"
            @change="handleModeChange"
            style="width: 100px;"
          >
            <el-option label="制冷" value="Cooling"></el-option>
            <el-option label="制热" value="Heating"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
    </div>

    <transition name="fade">
      <div v-if="showDetails" class="room-details animate__animated animate__fadeIn">
        <p>当前温度: {{ room.ntem.toFixed(2) }} °C <i :class="temperatureIcon"></i></p>
        <p>目标温度: {{ room.targetTemperature }} °C</p>
        <p>当前风速: {{ room.windSpeed }}</p>
        <p>空调状态: {{ room.isPoweredOn ? '开机' : '关机' }}</p>
        <p>累计费用: {{ room.w.toFixed(2) }} 元</p>
      </div>
    </transition>

    <el-button type="text" @click="toggleDetails">
      {{ showDetails ? '隐藏详情' : '显示详情' }}
    </el-button>
  </div>
</template>

<script>
import { turnOn, turnOff, setTemperature, setWindSpeed, setMode } from '../api'
import debounce from 'lodash/debounce'
import { ElNotification } from 'element-plus' // 确保导入ElNotification

export default {
  name: 'RoomCard',
  props: {
    room: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      showDetails: false,
      cardAnimation: 'animate__fadeIn',
      loadingPower: false,
      loadingTemperature: false,
      loadingWindSpeed: false,
      loadingMode: false
    }
  },
  computed: {
    temperatureClass() {
      if (this.room.ntem < this.room.targetTemperature - 1) {
        return 'cooling';
      } else if (this.room.ntem > this.room.targetTemperature + 1) {
        return 'heating';
      } else {
        return 'comfortable';
      }
    },
    temperatureIcon() {
      if (this.temperatureClass === 'cooling') {
        return 'el-icon-sunny'; // 制冷图标
      } else if (this.temperatureClass === 'heating') {
        return 'el-icon-temperature'; // 制热图标
      } else {
        return 'el-icon-refresh'; // 温度舒适图标
      }
    },
    debounceUpdateTemperature() {
      return debounce(this.updateTemperature, 500)
    }
  },
  methods: {
    togglePower() {
      this.loadingPower = true
      if (this.room.isPoweredOn) {
        turnOff(this.room.roomNumber)
          .then(() => {
            this.$emit('refresh')
            ElNotification.success({
              title: '成功',
              message: '空调已关闭'
            })
            this.animateCard()
          })
          .catch(err => {
            console.error(err)
            ElNotification.error({
              title: '错误',
              message: '关闭空调失败'
            })
          })
          .finally(() => {
            this.loadingPower = false
          })
      } else {
        turnOn(this.room.roomNumber)
          .then(() => {
            this.$emit('refresh')
            ElNotification.success({
              title: '成功',
              message: '空调已开启'
            })
            this.animateCard()
          })
          .catch(err => {
            console.error(err)
            ElNotification.error({
              title: '错误',
              message: '开启空调失败'
            })
          })
          .finally(() => {
            this.loadingPower = false
          })
      }
    },
    updateTemperature() {
      if (this.room.targetTemperature < 18 || this.room.targetTemperature > 30) {
        ElNotification.warning({
          title: '警告',
          message: '目标温度必须在18°C到30°C之间'
        })
        return
      }
      this.loadingTemperature = true
      setTemperature(this.room.roomNumber, this.room.targetTemperature)
        .then(() => {
          this.$emit('refresh')
          ElNotification.success({
            title: '成功',
            message: '目标温度已设置'
          })
          this.animateCard()
        })
        .catch(err => {
          console.error(err)
          ElNotification.error({
            title: '错误',
            message: '设置目标温度失败'
          })
        })
        .finally(() => {
          this.loadingTemperature = false
        })
    },
    setWindSpeed(speed) {
      if (this.room.windSpeed === speed) return // 无需更改
      this.loadingWindSpeed = true
      setWindSpeed(this.room.roomNumber, speed)
        .then(() => {
          this.$emit('refresh')
          ElNotification.success({
            title: '成功',
            message: '风速已设置'
          })
          this.animateCard()
        })
        .catch(err => {
          console.error(err)
          ElNotification.error({
            title: '错误',
            message: '设置风速失败'
          })
        })
        .finally(() => {
          this.loadingWindSpeed = false
        })
    },
    handleModeChange(val) {
      this.loadingMode = true
      setMode(this.room.roomNumber, val)
        .then(() => {
          this.$emit('refresh')
          ElNotification.success({
            title: '成功',
            message: '模式已设置'
          })
          this.animateCard()
        })
        .catch(err => {
          console.error(err)
          ElNotification.error({
            title: '错误',
            message: '设置模式失败'
          })
        })
        .finally(() => {
          this.loadingMode = false
        })
    },
    toggleDetails() {
      this.showDetails = !this.showDetails
    },
    animateCard() {
      this.cardAnimation = 'animate__flash'
      setTimeout(() => {
        this.cardAnimation = 'animate__fadeIn'
      }, 1000)
    }
  }
}
</script>

<style scoped>
.room-container {
  padding: 15px;
  border: 1px solid #dcdcdc;
  border-radius: 8px;
  background-color: rgba(255, 255, 255, 0.85); /* 增加不透明度 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.room-container:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.room-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.room-header h3 {
  margin: 0;
  font-size: 18px;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-weight: bold;
}

.status-section {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.status-item {
  display: flex;
  align-items: center;
}

.status-icon {
  font-size: 20px;
  margin-right: 5px;
}

.controls-section {
  display: flex;
  flex-direction: column;
  gap: 10px; /* 增加控件间距 */
}

.el-button {
  font-weight: bold;
}

.room-details p {
  display: flex;
  align-items: center;
  margin: 5px 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: #333;
  font-weight: 500;
}

/* 动态颜色类 */
.active-room {
  border-left: 5px solid #67C23A;
}

.inactive-room {
  border-left: 5px solid #F56C6C;
}

.cooling {
  background-color: rgba(135, 206, 235, 0.1); /* Light Sky Blue */
}

.heating {
  background-color: rgba(255, 99, 71, 0.1); /* Tomato */
}

.comfortable {
  background-color: rgba(144, 238, 144, 0.1); /* Light Green */
}

/* 按钮样式 */
.button-on {
  color: #67C23A;
  font-weight: bold;
  display: flex;
  align-items: center;
}

.button-off {
  color: #F56C6C;
  font-weight: bold;
  display: flex;
  align-items: center;
}

/* 过渡效果 */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* Shake 动画 */
@keyframes shake {
  0% { transform: translate(1px, 1px) rotate(0deg); }
  10% { transform: translate(-1px, -2px) rotate(-1deg); }
  20% { transform: translate(-3px, 0px) rotate(1deg); }
  30% { transform: translate(3px, 2px) rotate(0deg); }
  40% { transform: translate(1px, -1px) rotate(1deg); }
  50% { transform: translate(-1px, 2px) rotate(-1deg); }
  60% { transform: translate(-3px, 1px) rotate(0deg); }
  70% { transform: translate(3px, 1px) rotate(-1deg); }
  80% { transform: translate(-1px, -1px) rotate(1deg); }
  90% { transform: translate(1px, 2px) rotate(0deg); }
  100% { transform: translate(1px, -2px) rotate(-1deg); }
}

/* 动画类 */
.animate__fadeIn {
  animation-name: fadeIn;
}

.animate__flash {
  animation-name: flash;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes flash {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
</style>
