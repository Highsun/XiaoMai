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
        :disabled="disabled"
        @focus="onFocusAny"
        @change="onUserInput"
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
        :disabled="disabled"
        @focus="onFocusAny"
        @input="onUserInput"
      />
      <!-- 省份与城市 -->
      <div
        v-else-if="field.key === 'location'"
        class="location-select-row"
        style="display: flex; gap: 12px"
      >
        <!-- 省 -->
        <select
          v-model="selectedProvince"
          id="province-select"
          @focus="onFocusAny"
          @change="handleProvinceChange"
        >
          <option disabled value="">请选择省份</option>
          <option v-for="province in provinces" :key="province" :value="province">
            {{ province }}
          </option>
        </select>
        <!-- 市 -->
        <select
          v-model="selectedCity"
          id="city-select"
          :disabled="!selectedProvince || disabled"
          @focus="onFocusAny"
          @change="handleCityChange"
        >
          <option disabled value="">请选择城市</option>
          <option v-for="city in cities" :key="city" :value="city">
            {{ city }}
          </option>
        </select>
        <!-- 区/县 -->
        <select
          v-model="selectedDistrict"
          id="district-select"
          :disabled="!selectedCity || disabled"
          @focus="onFocusAny"
          @change="handleDistrictChange"
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
        :disabled="disabled"
        @focus="onFocusAny"
        @input="onUserInput"
      />
    </div>
  </div>
<div class="form-actions">
  <button
    v-if="isTouched && !disabled"
    class="save-btn"
    @click="saveChanges"
    :disabled="!isDirty || disabled"
  >
    保存修改
  </button>
  <button
    v-if="isTouched && !disabled"
    class="cancel-btn"
    @click="cancelChanges"
  >
    取消
  </button>
</div>


</template>

<script setup>
import { reactive, ref, computed, onMounted, watch } from 'vue'
import locationData from '../../assets/data/location-L3.json'
import { defineProps } from 'vue'
import { getProfile, saveProfile } from '@/services/user'
import { userStore } from '@/stores/userStore.js'

const props = defineProps({
  disabled: Boolean
})

const isTouched = ref(false)
function onFocusAny() {
  isTouched.value = true
}

const fields = [
  { key: 'realname', label: '姓名' },
  { key: 'gender', label: '性别' },
  { key: 'birthday', label: '出生日期' },
  { key: 'phone', label: '手机号' },
  { key: 'location', label: '省份与城市' },
  { key: 'address', label: '详细地址' },
]

// 地区数据
const provinces = Object.keys(locationData)
const selectedProvince = ref('')
const selectedCity = ref('')
const selectedDistrict = ref('')

// 地区列表
const cities = computed(() => selectedProvince.value ? Object.keys(locationData[selectedProvince.value]) : [])
const districts = computed(() => selectedProvince.value && selectedCity.value ? locationData[selectedProvince.value][selectedCity.value] || [] : [])

// 日期限制
const today = new Date().toISOString().split('T')[0]

// 支持所有字段
const formData = reactive({
  realname: '',
  gender: '保密',
  birthday: '',
  phone: '',
  province: '',
  city: '',
  district: '',
  address: '',
  location: '', // 仅用于省市区回显，不提交到后端
})
// originalData 用普通对象，专做快照
let originalData = {}

// 检测脏数据
const isDirty = computed(() => {
  for (const key of ['realname', 'gender', 'birthday', 'phone', 'province', 'city', 'district', 'address']) {
    if (formData[key] !== originalData[key]) return true
  }
  return false
})

// 初始化省市区
function updateLocation() {
  formData.location = [selectedProvince.value, selectedCity.value, selectedDistrict.value].filter(Boolean).join(' / ')
  formData.province = selectedProvince.value
  formData.city = selectedCity.value
  formData.district = selectedDistrict.value
}
function initLocationFromString(province, city, district) {
  selectedProvince.value = province || ''
  selectedCity.value = city || ''
  selectedDistrict.value = district || ''
  formData.location = [province, city, district].filter(Boolean).join(' / ')
}

// 省市区选择监听
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

// 加载用户信息
async function loadUserInfo() {
  try {
    const { data } = await getProfile()
    formData.realname = data.realname || ''
    formData.gender = data.gender || '保密'
    formData.birthday = data.birthday || ''
    formData.phone = data.phone || ''
    formData.province = data.province || ''
    formData.city = data.city || ''
    formData.district = data.district || ''
    formData.address = data.address || ''
    initLocationFromString(formData.province, formData.city, formData.district)
    // 深拷贝保存快照
    originalData = JSON.parse(JSON.stringify(formData))
  } catch (err) {
    Object.keys(formData).forEach(k => formData[k] = '')
    originalData = {}
    initLocationFromString('', '', '')
  }
}

// 保存
async function saveChanges() {
  updateLocation()
  try {
    await saveProfile({
      realname: formData.realname,
      gender: formData.gender,
      birthday: formData.birthday,
      phone: formData.phone,
      province: formData.province || '',
      city: formData.city || '',
      district: formData.district || '',
      address: formData.address
    })
    // 保存后用深拷贝快照
    originalData = JSON.parse(JSON.stringify(formData))
    isTouched.value = false
    alert('保存成功')
  } catch (err) {
    alert('保存失败: ' + (err.response?.data?.msg || err.message))
  }
}

function cancelChanges() {
  // 恢复所有字段
  Object.keys(formData).forEach(key => {
    formData[key] = originalData[key] ?? ''
  })
  // 恢复省市区选择
  initLocationFromString(formData.province, formData.city, formData.district)
  isTouched.value = false
}

onMounted(() => {
  loadUserInfo()
  initLocationFromString(formData.province, formData.city, formData.district)
})
watch(() => userStore.isLoggedIn, val => {
  if (val) loadUserInfo()
  else {
    Object.keys(formData).forEach(k => formData[k] = '')
    originalData = {}
    initLocationFromString('', '', '')
  }
})

function handleProvinceChange() {
  onFocusAny()
  onUserInput()
  onProvinceChange()
}
function handleCityChange() {
  onFocusAny()
  onUserInput()
  onCityChange()
}
function handleDistrictChange() {
  onFocusAny()
  onUserInput()
  onDistrictChange()
}
function onUserInput() {
  isTouched.value = true
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
