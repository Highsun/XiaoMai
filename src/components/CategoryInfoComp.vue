<template>
  <div class="category-card" @click="goDetail">
    <!-- 使用后端 image_url 字段（带有 /uploads/ 前缀） -->
    <img :src="concert.image_url" alt="海报" class="category-poster" />

    <div class="category-info">
      <div class="category-title-row">
        <span class="category-title">{{ concert.name }}</span>
        <span v-if="concert.tag" class="category-tag">{{ concert.tag }}</span>
      </div>

      <div class="category-meta">
        <div class="category-meta-row">
          <span class="category-label">艺人：</span>
          <span class="category-artist">
            {{ (concert.artists && concert.artists.length > 0) ? concert.artists.join('、') : '-' }}
          </span>
        </div>
        <div class="category-meta-row">
          <span class="category-label">场馆：</span>
          <span>{{ concert.location }}</span>
        </div>
        <div class="category-meta-row">
          <span class="category-label">时间：</span>
          <span>{{ concert.date }}</span>
        </div>
      </div>

      <div class="category-bottom-row">
        <span class="category-price">{{ concert.price }}</span>
        <span :class="['category-status', { soldout: concert.status === '已售罄' }]">
          {{ concert.status }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const props = defineProps({
  concert: {
    type: Object,
    required: true,
  },
})

const router = useRouter()

function goDetail() {
  // 跳转到详情页
  if (props.concert.id) {
    router.push(`/buy-tickets/${props.concert.id}`)
  }
}
</script>

<style scoped>
.category-card {
  display: flex;
  align-items: flex-start;
  background: #fff;
  border-radius: 20px;
  box-shadow: 0 4px 18px 0 rgba(55, 188, 119, 0.07);
  padding: 18px 24px;
  margin-bottom: 16px;
  transition:
    box-shadow 0.2s,
    transform 0.2s;
  cursor: pointer;
}
.category-card:hover {
  box-shadow: 0 8px 24px 0 rgba(55, 188, 119, 0.15);
  transform: translateY(-2px) scale(1.02);
}

.category-poster {
  width: 88px;
  height: 120px;
  object-fit: cover;
  border-radius: 14px;
  margin-right: 22px;
  background: #f4f7f5;
  flex-shrink: 0;
}

.category-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.category-title-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}
.category-title {
  font-size: 18px;
  font-weight: 700;
  color: #222;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 320px;
}
.category-tag {
  background: #d7f6e3;
  color: #33b979;
  font-size: 13px;
  border-radius: 9px;
  padding: 2px 10px;
  margin-left: 4px;
}

.category-meta {
  font-size: 14px;
  color: #666;
  margin-bottom: 12px;
}
.category-meta-row {
  display: flex;
  gap: 6px;
  margin-bottom: 2px;
}
.category-label {
  color: #3bc586;
  font-weight: 500;
}

.category-bottom-row {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-top: auto;
}
.category-price {
  font-size: 17px;
  font-weight: bold;
  color: #3bc586;
}
.category-status {
  font-size: 14px;
  color: #3bc586;
  padding: 2px 12px;
  border-radius: 12px;
  background: #eafcf3;
  font-weight: 500;
}
.category-status.soldout {
  color: #bbb;
  background: #f5f5f5;
}
</style>
