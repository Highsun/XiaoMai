<template>
  <div>
    <NavbarComp />

    <div class="fav-list">
      <router-link
        v-for="item in favorites"
        :key="item.id"
        :to="`/buy-tickets/${item.id}`"
        class="favorite-info-card"
      >
        <img
          class="favorite-cover"
          :src="item.img"
          :alt="item.title"
        />
        <div class="favorite-title">{{ item.title }}</div>
        <div class="favorite-date">{{ item.date }}</div>
        <div class="favorite-price">￥{{ item.price }}</div>
      </router-link>

      <div
        v-if="favorites.length === 0"
        class="no-fav-tip"
      >
        暂无收藏，快去添加吧～
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import NavbarComp from '../components/NavbarComp.vue'
import axios from 'axios'

const favorites = ref([])

function formatPrice(p) {
  if (typeof p === 'string') return p.replace(/元$/, '')
  if (Array.isArray(p) && p.length) {
    const mn = Math.min(...p)
    const mx = Math.max(...p)
    return mn === mx ? `${mn}` : `${mn}-${mx}`
  }
  return p != null ? String(p) : '--'
}

function formatDate(show) {
  const s = show.start_date
  const e = show.end_date
  return e && e !== s ? `${s} - ${e}` : s
}

onMounted(async () => {
  try {
    const res = await axios.get('/api/favorites/list', {
      headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
    })
    if (res.data.code === 0 && Array.isArray(res.data.data)) {
      favorites.value = res.data.data.map(fav => {
        const show = fav.show
        return {
          id:    show.id,
          title: show.title,
          date:  formatDate(show),
          price: formatPrice(show.price),
          img:   show.image_url
        }
      })
    }
  } catch (err) {
    console.error('获取收藏列表失败', err)
    favorites.value = []
  }
})
</script>

<style scoped>
.fav-list {
  display: grid;
  grid-template-columns: repeat(4, 208px);
  gap: 24px;
  justify-content: center;
  padding: 165px 0 54px;
}
.favorite-info-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 208px;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 16px rgba(56,186,118,0.10);
  overflow: hidden;
  cursor: pointer;
  text-decoration: none;
  transition: box-shadow .2s, transform .1s;
}
.favorite-info-card:hover {
  box-shadow: 0 7px 28px rgba(56,186,118,0.18);
  transform: translateY(-3px) scale(1.025);
}
.favorite-cover {
  width: 100%;
  height: 140px;
  object-fit: cover;
  object-position: top center;
  background: #f6f8f7;
}
.favorite-title {
  margin: 12px 8px 4px;
  font-size: 15px;
  font-weight: 700;
  color: #2e8461;
  text-align: center;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.favorite-date {
  font-size: 12px;
  color: #7ec6a7;
  text-align: center;
  margin-bottom: 1px;
}
.favorite-price {
  font-size: 13.5px;
  font-weight: 700;
  color: #26ad62;
  background: #f4fcef;
  border-radius: 8px;
  padding: 1.5px 18px;
  margin: 6px 0 12px;
  box-shadow: 0 1px 3px rgba(230,245,234,0.67);
}
.no-fav-tip {
  grid-column: 1 / -1;
  text-align: center;
  color: #bbb;
  margin-top: 40px;
  font-size: 14px;
}
@media (max-width: 1100px) {
  .fav-list { grid-template-columns: repeat(3, 208px) }
}
@media (max-width: 780px) {
  .fav-list { grid-template-columns: repeat(2, 208px) }
}
@media (max-width: 540px) {
  .fav-list {
    grid-template-columns: 1fr;
    padding: 18px 0 36px;
  }
  .favorite-info-card { width: 90vw }
}
</style>
