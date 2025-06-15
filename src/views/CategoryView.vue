<template>
  <div>
    <NavbarComp />

    <div class="category-container">
      <!-- 左3/4：筛选+列表 -->
      <div class="main-content">
        <!-- 筛选条：仅在非搜索模式下显示 -->
        <div class="filter-bar card" v-if="!isSearching">
          <div class="filter-row">
            <!-- 城市 -->
            <div class="filter-city-wrap">
              <span class="filter-title">城市：</span>
              <div class="filter-options city-options" :class="{ expanded: showAllCities }">
                <span
                  v-for="city in displayedCities"
                  :key="city"
                  :class="['filter-option', { active: city === selectedCity }]"
                  @click="selectCity(city)"
                >
                  {{ city }}
                </span>
                <span
                  class="filter-option more-btn"
                  @click="toggleShowCities"
                  v-if="!showAllCities"
                >
                  更多 <span style="font-size: 12px">▼</span>
                </span>
                <span class="filter-option more-btn" @click="toggleShowCities" v-if="showAllCities">
                  收起 <span style="font-size: 12px">▲</span>
                </span>
              </div>
            </div>

            <!-- 时间 -->
            <div class="filter-time-wrap">
              <span class="filter-title">时间：</span>
              <div class="filter-options time-options">
                <span
                  v-for="time in times"
                  :key="time"
                  :class="['filter-option', { active: time === selectedTime }]"
                  @click="selectTime(time)"
                >
                  {{ time }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- 列表 -->
        <div class="category-list">
          <CategoryInfoComp
            v-for="concert in filteredConcerts"
            :key="concert.id"
            :concert="concert"
          />
        </div>
      </div>

      <!-- 右1/4：推荐区 -->
      <div class="sidebar card">
        <div class="recommend-title">你可能喜欢</div>
        <div class="recommend-list">
          <router-link
            v-for="item in recommendedConcerts"
            :key="item.id"
            :to="`/buy-tickets/${item.id}`"
            class="recommend-link"
            style="text-decoration: none"
          >
            <RecommendCard :concert="item" />
          </router-link>
        </div>
      </div>
    </div>

    <Footer />
  </div>
</template>

<script setup>
import axios from 'axios'
import { onMounted, ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import NavbarComp from '../components/NavbarComp.vue'
import CategoryInfoComp from '../components/CategoryInfoComp.vue'
import RecommendCard from '../components/RecommendCard.vue'
import dayjs from 'dayjs'
import isSameOrAfter from 'dayjs/plugin/isSameOrAfter'
import isSameOrBefore from 'dayjs/plugin/isSameOrBefore'
import isBetween from 'dayjs/plugin/isBetween'
import Footer from '../components/FooterComp.vue'
dayjs.extend(isSameOrAfter)
dayjs.extend(isSameOrBefore)
dayjs.extend(isBetween)

// 引入城市数据
import hotCities from '../assets/data/hotCities.json'
import allCities from '../assets/data/allCities.json'

const concerts = ref([])

// 推荐区（不影响此问题，可留空或自行替换）
const recommendedConcerts = ref([
  {
    id: 15,
    name: '李荣浩 年少有为 演唱会',
    date: '2025.06.30',
    poster: 'lironghao.png',
    price: '299元起',
  },
  {
    id: 17,
    name: '薛之谦 天外来物巡回演唱会',
    date: '2025.07.15',
    poster: 'xuezhiqian.png',
    price: '399元起',
  },
  {
    id: 2,
    name: '周杰伦 嘉年华巡回演唱会',
    date: '2025.08.02',
    poster: 'jaychou.png',
    price: '520元起',
  },
])

const showAllCities = ref(false)
const displayedCities = computed(() => (showAllCities.value ? allCities : hotCities))
const toggleShowCities = () => {
  showAllCities.value = !showAllCities.value
}

const times = ['全部', '今天', '明天', '本周末', '一个月内']
const selectedCity = ref('全部')
const selectedTime = ref('全部')
const selectCity = (c) => (selectedCity.value = c)
const selectTime = (t) => (selectedTime.value = t)

const route = useRoute()
const router = useRouter()

const searchInput = ref(route.query.q?.toString() || '')
watch(
  () => route.query.q,
  (newQ) => {
    const val = newQ?.toString() || ''
    if (val !== searchInput.value) {
      searchInput.value = val
    }
  },
  { immediate: true },
)
watch(searchInput, (newVal) => {
  if (newVal.trim() === '' && route.query.q) {
    const nq = { ...route.query }
    delete nq.q
    router.replace({ path: route.path, query: nq })
  }
})

const searchKeyword = computed(() => (route.query.q?.toString() || '').trim())
const isSearching = computed(() => !!searchKeyword.value)

/** 规范化日期显示：start_date/end_date => 'YYYY.MM.DD' 或 'YYYY.MM.DD - YYYY.MM.DD' */
function beautifyDate(start, end) {
  if (!start) return ''
  const s = (start || '').replace(/-/g, '.')
  const e = (end || '').replace(/-/g, '.')
  return e && e !== s ? `${s} - ${e}` : s
}
/** 规范化价格显示 */
function beautifyPrice(p) {
  if (typeof p === 'string') return p
  if (Array.isArray(p) && p.length > 0) {
    return p.length === 1 ? `${p[0]}元` : `${Math.min(...p)}-${Math.max(...p)}元`
  }
  return p ? `${p}元` : ''
}

// !!! 适配后端的所有字段
onMounted(async () => {
  try {
    const res = await axios.get('/api/shows/')
    if (res.data.code !== 0) throw new Error(res.data.message)

    const statusMap = {
      hot: '热卖中',
      upcoming: '即将上架',
      soldout: '已售罄',
      sold_out: '已售罄',
    }

    concerts.value = res.data.data.map((item) => ({
      id: item.id,
      name: item.title,
      tag: item.tag,
      artists: item.artist_names || [],
      artist: item.artist_names && item.artist_names.length > 0 ? item.artist_names.join('、') : '',
      location: item.location,
      date: beautifyDate(item.start_date, item.end_date),
      price: beautifyPrice(item.price),
      status: statusMap[item.status] || item.status || '',
      image_url: item.image_url,
      // 可扩展字段
      // sessions:  item.sessions,
      // price_tiers: item.price_tiers,
      // map_url:   item.map_url,
    }))
  } catch (err) {
    console.error('获取演出列表失败', err)
  }
})

/** 综合搜索 + 筛选逻辑 */
const filteredConcerts = computed(() => {
  let list = concerts.value

  // 搜索模式
  if (isSearching.value) {
    const terms = searchKeyword.value.toLowerCase().split(/\s+/)
    return list.filter((c) =>
      terms.every((t) => [c.name, c.artist, c.location].join(' ').toLowerCase().includes(t)),
    )
  }

  // 城市筛选
  if (selectedCity.value !== '全部') {
    list = list.filter((c) => c.location.includes(selectedCity.value))
  }

  // 时间筛选
  if (selectedTime.value !== '全部') {
    const now = dayjs()
    let start, end

    switch (selectedTime.value) {
      case '今天':
        start = now.startOf('day')
        end = now.endOf('day')
        break
      case '明天':
        start = now.add(1, 'day').startOf('day')
        end = now.add(1, 'day').endOf('day')
        break
      case '本周末':
        start = now.day(6).startOf('day')
        end = now.day(7).endOf('day')
        break
      case '一个月内':
        start = now
        end = now.add(1, 'month').endOf('day')
        break
      default:
        start = null
        end = null
    }

    list = list.filter((c) => {
      let [s, e] = c.date.split('-').map((t) => t.trim())
      if (/^\d{4}\.\d{2}\.\d{2}$/.test(e) === false) {
        // 单日期或 MM.DD 缩写的情况
        e = s
      }
      const sd = dayjs(s, 'YYYY.MM.DD')
      const ed = dayjs(e, 'YYYY.MM.DD')
      return ed.isSameOrAfter(start) && sd.isSameOrBefore(end)
    })
  }

  return list
})
</script>

<style scoped>
/* 样式原样 */
.category-container {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: space-between;
  padding: 32px 5vw 0 5vw;
  min-height: 80vh;
  gap: 24px;
}

.main-content {
  flex: 1 1 0;
  min-width: 0;
  display: flex;
  flex-direction: column;
  max-width: 1100px;
  box-sizing: border-box;
}

.sidebar {
  width: 300px;
  min-width: 220px;
  max-width: 340px;
  margin-left: auto;
  padding: 22px 20px;
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 2px 14px rgba(80, 180, 120, 0.08);
  height: auto;
  flex-shrink: 0;
  position: sticky;
  top: 60px;
}

.card {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 2px 14px rgba(80, 180, 120, 0.08);
  margin-bottom: 24px;
}

/* ——筛选区域—— */
.filter-bar {
  padding: 18px 24px 4px 24px;
  margin-bottom: 22px;
}
.filter-row {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 10px;
}
.filter-city-wrap,
.filter-time-wrap {
  display: block;
  margin-bottom: 0;
}

.filter-title {
  font-weight: bold;
  color: #444;
  margin-right: 8px;
  min-width: 46px;
  white-space: nowrap;
  flex-shrink: 0;
  font-size: 16px;
  display: inline-block;
  margin-bottom: 8px;
  vertical-align: top;
}

.filter-options {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  align-items: flex-start;
  box-sizing: border-box;
  margin-top: 2px;
}

.city-options {
  min-width: 0;
}
.time-options {
  min-width: 180px;
}

.filter-option,
.filter-option.more-btn {
  padding: 4px 14px;
  border-radius: 16px;
  background: #f3f5f7;
  color: #37ba77;
  cursor: pointer;
  font-size: 12px;
  transition:
    background 0.15s,
    color 0.15s;
  margin-right: 0;
  margin-bottom: 6px;
  user-select: none;
  border: none;
  line-height: 20px;
  box-sizing: border-box;
}

.filter-option.active {
  background: #37ba77;
  color: #fff;
  font-weight: bold;
}

.filter-option.more-btn {
  background: #eafcf3;
  color: #1db77e;
  border: 0px dashed #82d5ad;
  font-weight: 400;
  margin-left: 0;
}

.category-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 推荐标题和推荐列表样式 */
.recommend-title {
  font-size: 17px;
  font-weight: 600;
  margin-bottom: 16px;
  color: #2e8461;
  letter-spacing: 1px;
}

.recommend-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.recommend-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px solid #f1f1f1;
}
.recommend-img {
  width: 48px;
  height: 64px;
  border-radius: 8px;
  object-fit: cover;
  background: #f7f7f7;
}
.recommend-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.recommend-name {
  font-size: 15px;
  color: #34495e;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.recommend-date,
.recommend-price {
  font-size: 13px;
  color: #3bc586;
}

.recommend-link {
  display: block;
  color: inherit;
  text-decoration: none;
  cursor: pointer;
}
.recommend-link:active,
.recommend-link:visited {
  color: inherit;
}
</style>
