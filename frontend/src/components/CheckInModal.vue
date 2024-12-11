<!-- frontend/src/components/CheckInModal.vue -->
<template>
  <el-dialog
    title="办理入住"
    :visible.sync="visible"
    width="500px"
    :before-close="handleClose"
    :modal-append-to-body="false"
    :show-close="true"
  >
    <el-form :model="form" ref="form" label-width="120px">
      <el-form-item label="房间号" prop="room_number">
        <el-input
          v-model.number="form.room_number"
          type="number"
          min="1"
          placeholder="请输入房间号"
        ></el-input>
      </el-form-item>
      <el-form-item label="客人姓名" prop="guest_name">
        <el-input
          v-model="form.guest_name"
          placeholder="请输入客人姓名"
        ></el-input>
      </el-form-item>
      <el-form-item label="客人身份证号" prop="guest_id_number">
        <el-input
          v-model="form.guest_id_number"
          placeholder="请输入身份证号"
        ></el-input>
      </el-form-item>
    </el-form>
    <span slot="footer" class="dialog-footer">
      <el-button @click="visible = false">取消</el-button>
      <el-button type="primary" :loading="loading" @click="checkInAction">确认</el-button>
    </span>
  </el-dialog>
</template>

<script>
import { checkIn } from '../api'

export default {
  name: 'CheckInModal',
  props: {
    visible: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      form: {
        room_number: 1,
        guest_name: '',
        guest_id_number: ''
      },
      loading: false
    }
  },
  methods: {
    checkInAction() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          this.loading = true
          checkIn(this.form.room_number, this.form.guest_name, this.form.guest_id_number)
            .then(res => {
              this.$emit('refresh')
              this.$notify.success({
                title: '成功',
                message: '办理入住成功'
              })
              this.visible = false
              this.resetForm()
            })
            .catch(err => {
              console.error(err)
              this.$notify.error({
                title: '错误',
                message: err.response?.data?.detail || '办理入住失败'
              })
            })
            .finally(() => {
              this.loading = false
            })
        } else {
          console.log('验证失败')
          return false
        }
      })
    },
    handleClose(done) {
      this.resetForm()
      done()
    },
    resetForm() {
      this.form = {
        room_number: 1,
        guest_name: '',
        guest_id_number: ''
      }
      this.$refs.form.resetFields()
    }
  }
}
</script>

<style scoped>
.dialog-footer {
  text-align: right;
}
</style>
