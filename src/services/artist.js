import axios from 'axios'

export function fetchAllArtists() {
  return axios.get('/api/artists/')
}
