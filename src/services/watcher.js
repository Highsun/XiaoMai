import axios from 'axios'

export async function fetchWatchers() {
  const res = await axios.get('/api/user/watchers')
  return res.data.data
}
export async function createWatcher(watcher) {
  const res = await axios.post('/api/user/watchers', watcher)
  return res.data.data
}
export async function updateWatcher(wid, watcher) {
  const res = await axios.put(`/api/user/watchers/${wid}`, watcher)
  return res.data.data
}
export async function deleteWatcher(wid) {
  await axios.delete(`/api/user/watchers/${wid}`)
}
export async function changePassword(old_password, new_password) {
  const res = await axios.put('/api/user/password', { old_password, new_password })
  return res.data
}
