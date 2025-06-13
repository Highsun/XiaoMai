<template>
  <div class="spectator-manager">
    <h2 class="spectator-title">观演人管理</h2>
    <p style="font-size: 15px; margin-bottom: 10px">
      您最多可添加 10 位观演人，观演人信息将用于购票和入场验证。
    </p>

    <!-- 列表 -->
    <div
      v-for="(spectator, index) in spectators"
      :key="spectator.id || index"
      class="spectator-row"
    >
      <div class="spectator-field">
        <input
          v-model="spectator.realname"
          type="text"
          placeholder="姓名"
          class="spectator-input"
          :readonly="!spectator.editable"
        />
        <div v-if="spectator.errors?.realname" class="error-msg">
          {{ spectator.errors.realname }}
        </div>
      </div>

      <div class="spectator-field">
        <input
          v-model="spectator.id_number"
          type="text"
          placeholder="身份证号"
          class="spectator-input"
          :readonly="!spectator.editable"
        />
        <div v-if="spectator.errors?.id_number" class="error-msg">
          {{ spectator.errors.id_number }}
        </div>
      </div>

      <div class="spectator-field">
        <input
          v-model="spectator.phone"
          type="text"
          placeholder="手机号"
          class="spectator-input"
          :readonly="!spectator.editable"
        />
        <div v-if="spectator.errors?.phone" class="error-msg">
          {{ spectator.errors.phone }}
        </div>
      </div>

      <button class="spectator-icon-btn" @click="onDelete(spectator, index)">
        <i class="fas fa-minus"></i> 删除
      </button>
      <button class="spectator-icon-btn" @click="onToggleEdit(spectator, index)">
        <i class="fas" :class="spectator.editable ? 'fa-save' : 'fa-edit'"></i>
        {{ spectator.editable ? '保存' : '编辑' }}
      </button>
    </div>

    <div class="add-row" v-if="spectators.length < 10">
      <button class="add-btn" @click="onAdd">
        <i class="fas fa-plus"></i> 添加观演人
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import {
  fetchWatchers,
  createWatcher,
  updateWatcher,
  deleteWatcher,
} from '@/services/watcher'

const spectators = ref([])

// 拉取已有观演人列表
async function load() {
  try {
    const list = await fetchWatchers()
    // 标记所有项为只读状态
    spectators.value = list.map(w => ({
      ...w,
      editable: false,
      errors: {},
    }))
  } catch (err) {
    console.error('加载观演人失败', err)
  }
}
onMounted(load)

// 添加新观演人
async function onAdd() {
  if (spectators.value.length >= 10) return
  // 先在后端创建空白记录
  try {
    const w = await createWatcher({ realname: '', id_number: '', phone: '' })
    spectators.value.push({
      ...w,
      editable: true,
      errors: {},
    })
  } catch (err) {
    console.error('添加观演人失败', err)
  }
}

// 删除观演人
async function onDelete(item, idx) {
  if (item.id) {
    try {
      await deleteWatcher(item.id)
    } catch (err) {
      console.error('删除失败', err)
      return
    }
  }
  spectators.value.splice(idx, 1)
}

// 切换 编辑/保存
async function onToggleEdit(item, idx) {
  // 切到保存：校验并调用更新
  if (item.editable) {
    const errors = validateSpectator(item)
    if (Object.keys(errors).length) {
      item.errors = errors
      return
    }
    try {
      // 如果已有 id，就更新；否则新建
      if (item.id) {
        const updated = await updateWatcher(item.id, {
          realname: item.realname,
          id_number: item.id_number,
          phone: item.phone,
        })
        Object.assign(item, updated)
      } else {
        const created = await createWatcher({
          realname: item.realname,
          id_number: item.id_number,
          phone: item.phone,
        })
        Object.assign(item, created)
      }
      item.errors = {}
      item.editable = false
    } catch (err) {
      console.error('保存失败', err)
    }
  } else {
    // 切到编辑
    item.editable = true
    item.errors = {}
  }
}

// 前端校验
function validateSpectator(s) {
  const errors = {}

  if (!/^[\u4e00-\u9fa5]{2,6}$/.test(s.realname)) {
    errors.realname = '姓名需为 2-6 个汉字'
  }
  if (
    !/^[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]$/.test(
      s.id_number
    )
  ) {
    errors.id_number = '请输入有效的身份证号'
  }
  if (!/^1[3-9]\d{9}$/.test(s.phone)) {
    errors.phone = '请输入有效的手机号'
  }
  return errors
}
</script>

<style scoped>
.spectator-manager {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

.spectator-title {
  font-size: 16px;
  font-weight: bold;
  text-align: left;
  margin-bottom: 0;
}

.spectator-row {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.spectator-input {
  flex: 1 1 auto;
  min-width: 0;
  padding: 6px 10px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 100%;
  box-sizing: border-box;
}

.spectator-field {
  flex: 1 1 0;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.spectator-icon-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  width: auto;
  min-width: 0;
  background-color: #fff;
  color: #222;
  border: 1px solid #ccc;
  padding: 6px 10px;
  font-size: 14px;
  cursor: pointer;
  border-radius: 4px;
  transition:
    background 0.2s,
    color 0.2s,
    border-color 0.2s;
}

.spectator-icon-btn:hover {
  background-color: #42b983;
  color: #fff;
  border-color: #42b983;
}

.add-row {
  margin-top: 6px;
}

.add-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background-color: #42b983;
  color: white;
  padding: 8px 14px;
  font-size: 14px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  width: auto;
  min-width: 0;
}

.add-btn:hover {
  background-color: #369d6f;
}
.spectator-manager { /* … */ }
.spectator-row     { /* … */ }
.spectator-input   { /* … */ }
.spectator-icon-btn{ /* … */ }
.add-btn           { /* … */ }
.error-msg {
  color: #c00;
  font-size: 12px;
  margin-top: 4px;
}
</style>
