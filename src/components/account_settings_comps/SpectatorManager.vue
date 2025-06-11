<template>
  <div class="spectator-manager">
    <h2 class="spectator-title">观演人管理</h2>
    <p style="font-size: 15px; margin-bottom: 10px">
      您最多可添加 10 位观演人，观演人信息将用于购票和入场验证。
    </p>

    <div v-for="(spectator, index) in spectators" :key="index" class="spectator-row">
      <div class="spectator-field">
        <input
          v-model="spectator.name"
          type="text"
          placeholder="姓名"
          class="spectator-input"
          :readonly="!spectator.editable"
        />
        <div v-if="spectator.errors?.name" class="error-msg">
          {{ spectator.errors.name }}
        </div>
      </div>

      <div class="spectator-field">
        <input
          v-model="spectator.id"
          type="text"
          placeholder="身份证号"
          class="spectator-input"
          :readonly="!spectator.editable"
        />
        <div v-if="spectator.errors?.id" class="error-msg">
          {{ spectator.errors.id }}
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

      <button class="spectator-icon-btn" @click="removeSpectator(index)">
        <i class="fas fa-minus"></i> 删除
      </button>
      <button class="spectator-icon-btn" @click="toggleEdit(index)">
        <i class="fas" :class="spectator.editable ? 'fa-save' : 'fa-edit'"></i>
        {{ spectator.editable ? '保存' : '编辑' }}
      </button>
    </div>

    <div class="add-row" v-if="spectators.length < 10">
      <button class="add-btn" @click="addSpectator"><i class="fas fa-plus"></i> 添加观演人</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const spectators = ref([{ name: '', id: '', phone: '', editable: true, errors: {} }])

function addSpectator() {
  if (spectators.value.length < 10) {
    spectators.value.push({
      name: '',
      id: '',
      phone: '',
      editable: true,
      errors: {},
    })
  }
}

function removeSpectator(index) {
  spectators.value.splice(index, 1)
}

function toggleEdit(index) {
  const person = spectators.value[index]

  if (person.editable) {
    // 正在“保存” -> 校验
    const errors = validateSpectator(person)
    if (Object.keys(errors).length === 0) {
      person.editable = false
    }
    person.errors = errors
  } else {
    // 切换到“编辑”
    person.editable = true
    person.errors = {}
  }
}

function validateSpectator(spectator) {
  const errors = {}

  // 姓名：2~18个汉字
  const nameRegex = /^[\u4e00-\u9fa5]{2,6}$/
  if (!nameRegex.test(spectator.name)) {
    errors.name = '姓名需为 2-6 个汉字'
  }

  // 身份证号：中国大陆18位，支持末尾X/x
  const idRegex = /^[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]$/
  if (!idRegex.test(spectator.id)) {
    errors.id = '请输入有效的身份证号'
  }

  // 手机号：以1开头的11位数字
  const phoneRegex = /^1[3-9]\d{9}$/
  if (!phoneRegex.test(spectator.phone)) {
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
</style>
