<!-- frontend/src/components/CheckOutModal.vue -->
<template>
  <el-dialog
    title="办理退房"
    :visible.sync="visible"
    width="400px"
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
    </el-form>
    <span slot="footer" class="dialog-footer">
      <el-button @click="visible = false">取消</el-button>
      <el-button type="primary" :loading="loading" @click="checkOutAction">确认</el-button>
    </span>
  </el-dialog>
</template>

<script>
import { checkOut } from '../api'

export default {
  name: 'CheckOutModal',
  props: {
    visible: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      form: {
        room_number: 1
      },
      loading: false
    }
  },
  methods: {
    checkOutAction() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          this.loading = true
          checkOut(this.form.room_number)
            .then(res => {
              this.$emit('refresh')
              this.$notify.success({
                title: '成功',
                message: `退房成功，总费用：${res.data.total_cost.toFixed(2)} 元`
              })
              this.visible = false
              this.resetForm()
            })
            .catch(err => {
              console.error(err)
              this.$notify.error({
                title: '错误',
                message: err.response?.data?.detail || '办理退房失败'
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
        room_number: 1
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
