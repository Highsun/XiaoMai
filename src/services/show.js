import axios from 'axios'

axios.defaults.baseURL = 'http://localhost:8888'
export function fetchAllShows() {
  return axios.get('/api/shows/')
}
