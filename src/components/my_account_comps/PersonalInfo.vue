<template>
  <div class="personal-info">
    <div class="form-group" v-for="field in fields" :key="field.key">
      <label :for="field.key">{{ field.label }}</label>
      <!-- 性别 -->
      <select
        v-if="field.key === 'gender'"
        :id="field.key"
        v-model="formData[field.key]"
        :style="{ color: formData.gender ? '#333' : '#aaa' }"
      >
        <option disabled value="">请选择性别</option>
        <option value="男">男</option>
        <option value="女">女</option>
        <option value="保密">保密</option>
      </select>
      <!-- 出生日期 -->
      <input
        v-else-if="field.key === 'birthday'"
        type="date"
        :id="field.key"
        v-model="formData[field.key]"
        :max="today"
      />
      <!-- 省份与城市 -->
      <div
        v-else-if="field.key === 'location'"
        class="location-select-row"
        style="display: flex; gap: 12px"
      >
        <!-- 省 -->
        <select v-model="selectedProvince" @change="onProvinceChange" id="province-select">
          <option disabled value="">请选择省份</option>
          <option v-for="province in provinces" :key="province" :value="province">
            {{ province }}
          </option>
        </select>
        <!-- 市 -->
        <select
          v-model="selectedCity"
          @change="onCityChange"
          :disabled="!selectedProvince"
          id="city-select"
        >
          <option disabled value="">请选择城市</option>
          <option v-for="city in cities" :key="city" :value="city">
            {{ city }}
          </option>
        </select>
        <!-- 区/县 -->
        <select
          v-model="selectedDistrict"
          @change="onDistrictChange"
          :disabled="!selectedCity"
          id="district-select"
        >
          <option disabled value="">请选择区/县</option>
          <option v-for="district in districts" :key="district" :value="district">
            {{ district }}
          </option>
        </select>
      </div>
      <!-- 普通输入框 -->
      <input
        v-else
        type="text"
        :id="field.key"
        :placeholder="`请输入${field.label}`"
        v-model="formData[field.key]"
      />
    </div>
  </div>
  <div class="form-actions">
    <button class="save-btn" @click="saveChanges">保存修改</button>
    <button class="cancel-btn" @click="cancelChanges">取消</button>
  </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted } from 'vue'
import locationData from '../../assets/data/location-L3.json'

const fields = [
  { key: 'name', label: '姓名' },
  { key: 'gender', label: '性别' },
  { key: 'birthday', label: '出生日期' },
  { key: 'phone', label: '手机号' },
  { key: 'location', label: '省份与城市' },
  { key: 'address', label: '详细地址' },
]

// 表单初始值 TODO: 接入后端数据
const formData = reactive({
  name: '',
  gender: '保密',
  birthday: '',
  location: '',
})

// 保存原始数据（用于取消）
const originalData = {
  name: formData.name,
  gender: formData.gender,
  birthday: formData.birthday,
  location: formData.location,
}

// 地区数据
const provinces = Object.keys(locationData)

const selectedProvince = ref('')
const selectedCity = ref('')
const selectedDistrict = ref('')

// 地区列表
const cities = computed(() => {
  return selectedProvince.value ? Object.keys(locationData[selectedProvince.value]) : []
})

const districts = computed(() => {
  if (selectedProvince.value && selectedCity.value) {
    return locationData[selectedProvince.value][selectedCity.value] || []
  }
  return []
})

// 初始化省市区
onMounted(() => {
  initLocationFromString(formData.location)
})

// 监听地区变化
function onProvinceChange() {
  selectedCity.value = ''
  selectedDistrict.value = ''
  updateLocation()
}

function onCityChange() {
  selectedDistrict.value = ''
  updateLocation()
}

function onDistrictChange() {
  updateLocation()
}

// 更新 location 字符串
function updateLocation() {
  formData.location = [selectedProvince.value, selectedCity.value, selectedDistrict.value]
    .filter(Boolean)
    .join(' / ')
}

// 根据字符串回显省市区
function initLocationFromString(str) {
  const parts = str.split(' / ')
  selectedProvince.value = parts[0] || ''
  selectedCity.value = parts[1] || ''
  selectedDistrict.value = parts[2] || ''
}

// 日期限制（最大值设为今天）
const today = new Date().toISOString().split('T')[0]

// 保存修改
function saveChanges() {
  updateLocation()
  fields.forEach((field) => {
    originalData[field.key] = formData[field.key]
  })
  alert('保存成功')
}

// 取消修改，回滚数据
function cancelChanges() {
  fields.forEach((field) => {
    formData[field.key] = originalData[field.key]
  })
  initLocationFromString(formData.location)
}
</script>

<style scoped>
/* 我的账号 */
.personal-info {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0px 24px;
  margin-top: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-size: 14px;
  margin-bottom: 6px;
  color: #333;
}

.form-group input {
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: #42b983;
}

.form-group select {
  display: block;
  width: 100%;
  height: 36px;
  padding: 0 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 14px;
  color: #333;
  background-color: #fff;
  appearance: none;
}

.form-group select:focus {
  outline: none;
  border-color: #42b983;
}

.form-group input[type='date'] {
  height: 36px;
}

.location-select-row select {
  flex: 1;
  padding: 8px 12px;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 14px;
  color: #333;
  background-color: #fff;
  appearance: none;
}

.location-select-row select:disabled {
  color: #aaa;
  background-color: #f9f9f9;
  cursor: not-allowed;
}

.form-actions {
  margin-top: 12px;
  display: flex;
  justify-content: flex-end;
  gap: 16px;
}

.save-btn,
.cancel-btn {
  padding: 10px 20px;
  width: auto;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  white-space: nowrap;
  text-align: center;
  transition: background 0.3s;
}

.save-btn {
  background-color: #42b983;
  color: white;
}

.save-btn:hover {
  background-color: #369c74;
}

.cancel-btn {
  background-color: #f0f0f0;
  color: #333;
}

.cancel-btn:hover {
  background-color: #e0e0e0;
}
</style>
