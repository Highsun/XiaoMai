import axios from 'axios'

// 获取个人信息
export function getProfile() {
  return axios.get('/api/auth/profile', {
    headers: {
      Authorization: 'Bearer ' + localStorage.getItem('access_token')
    }
  })
}

// 保存个人信息
export function saveProfile(data) {
  return axios.post('/api/auth/profile', data, {
    headers: {
      Authorization: 'Bearer ' + localStorage.getItem('access_token')
    }
  })
}
