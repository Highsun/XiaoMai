import axios from 'axios'

/**
 * 注册接口
 * @param {{ username: string, email: string, password: string, confirmPassword: string }} user
 */
export function register(user) {
  return axios.post('/api/auth/register', user)
}


export function login(credentials) {
  // credentials = { account, password }
  return axios.post('/api/auth/login', credentials);
}

