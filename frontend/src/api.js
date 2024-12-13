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
  return api.get('/rooms/room_info')
}

// 办理入住
export function checkIn(room_number, guest_name, guest_id_number) {
  return api.post('/bookings/checkin', { room_number, guest_name, guest_id_number })
}

// 办理退房
export function checkOut(booking_id) {  // 修改为booking_id
  return api.post(`/bookings/${booking_id}/checkout`, {})
}

// 设置目标温度
export function setTemperature(room_number, target_temperature) {
  return api.post(`/rooms/${room_number}/set_temperature`, { temperature: target_temperature })
}

// 设置风速
export function setWindSpeed(room_number, wind_speed) {
  return api.post(`/rooms/${room_number}/set_wind_speed`, { wind_speed })
}

// 设置模式
export function setMode(room_number, mode) {
  return api.post(`/rooms/${room_number}/set_mode`, { mode })
}

// 开机
export function turnOn(room_number) {
  return api.post(`/rooms/${room_number}/turn_on`, {})
}

// 关机
export function turnOff(room_number) {
  return api.post(`/rooms/${room_number}/turn_off`, {})
}

export default api
