// frontend/src/api.js

import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

// 获取所有房间信息
export function fetchRoomInfo() {
  return api.get('/rooms/room_info') // 修改为正确的URL
}

// 办理入住
export function checkIn(room_number, guest_name, guest_id_number) {
  return api.post('/bookings/checkin', { room_number, guest_name, guest_id_number }) // 修改为正确的URL
}

// 办理退房
export function checkOut(room_number) {
  return api.post('/bookings/checkout', { room_number }) // 修改为正确的URL
}

// 设置目标温度
export function setTemperature(room_number, target_temperature) {
  return api.post('/rooms/set_temperature', { room_number, target_temperature }) // 确认后端是否有对应路由
}

// 设置风速
export function setWindSpeed(room_number, wind_speed) {
  return api.post('/rooms/set_wind_speed', { room_number, wind_speed }) // 确认后端是否有对应路由
}

// 设置模式
export function setMode(room_number, mode) {
  return api.post('/rooms/set_mode', { room_number, mode }) // 确认后端是否有对应路由
}

// 开机
export function turnOn(room_number) {
  return api.post('/rooms/turnOn', { room_number, is_on: true }) // 确认后端是否有对应路由
}

// 关机
export function turnOff(room_number) {
  return api.post('/rooms/turnOff', { room_number, is_on: false }) // 确认后端是否有对应路由
}
