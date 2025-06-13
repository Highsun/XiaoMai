// src/services/auth.js
import axios from 'axios'

/**
 * 注册接口
 * @param {{ username: string, email: string, password: string, confirmPassword: string }} user
 */
export function register(user) {
  return axios.post('/api/auth/register', user)
}

/**
 * 登录接口
 * @param {{ account: string, password: string }} credentials
 */
export function login(credentials) {
  return axios.post('/api/auth/login', credentials)
}

/**
 * 获取当前登录用户基本信息
 */
export function fetchUserInfo() {
  return axios.get('/api/auth/userinfo')
}

/**
 * 获取当前用户资料
 */
export function getProfile() {
  return axios.get('/api/auth/profile')
}

/**
 * 更新当前用户资料
 * @param {{ realname: string, gender: string, birthday: string, phone: string, province: string, city: string, district: string, address: string }} profile
 */
export function updateProfile(profile) {
  return axios.put('/api/auth/profile', profile)
}

/**
 * 修改密码
 * @param {{ old_password: string, new_password: string, confirm_password: string }} passwords
 */
export function changePassword(passwords) {
  return axios.put('/api/auth/password', passwords)
}

/**
 * 注销账号
 */
export function deleteAccount() {
  return axios.delete('/api/auth/delete-account');
}
