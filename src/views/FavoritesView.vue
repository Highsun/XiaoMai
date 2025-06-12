<template>
  <div>
    <NavbarComp />
    <div class="fav-list">
      <div
        class="favorite-info-card"
        v-for="(item, idx) in favorites"
        :key="idx"
      >
        <img class="favorite-cover" :src="item.img" :alt="item.name" />
        <div class="favorite-title">{{ item.name }}</div>
        <div class="favorite-date">{{ item.date }}</div>
        <div class="favorite-price">￥{{ item.price }}</div>
      </div>
    </div>
  </div>
</template>


<script setup>
import NavbarComp from '../components/NavbarComp.vue'
import CategoryInfoComp from '../components/CategoryInfoComp.vue'

// 收藏数据
const favorites = [
  {
    name: 'JJ20 FINAL LAP 世界巡回演唱会',
    date: '2025.06.28-07.13',
    location: '北京市·国家体育场-鸟巢',
    price: 380,
    img: '/uploads/concerts/JJ20.jpeg',
  },
  {
    name: '周杰伦《嘉年华》巡回演唱会',
    date: '2025.06.27-06.29',
    location: '中国香港·香港启德体育园主场馆',
    price: 1100,
    img: '/uploads/concerts/Jay.png',
  },
  {
    name: '陶喆 Soul Power II 世界巡回演唱会',
    date: '2025.08.09-08.10',
    location: '深圳市·深圳湾体育中心“春茧”体育场',
    price: 380,
    img: '/uploads/concerts/DT.png',
  },
  {
    name: '王力宏「最好的地方」巡回演唱会',
    date: '2025.07.05-07.06',
    location: '苏州市·苏州奥林匹克体育中心体育馆',
    price: 480,
    img: '/uploads/concerts/WLH.png',
  },
  {
    name: 'G.E.M. 邓紫棋 I AM GLORIA 世界巡回演唱会 2.0',
    date: '2025.07.05',
    location: '烟台市·烟台体育公园体育场',
    price: 380,
    img: '/uploads/concerts/GEM.jpeg',
  },
  {
    name: '孙燕姿《就在日落以后》演唱会',
    date: '2025.06.13/06.15',
    location: '北京市·国家体育场-鸟巢',
    price: 480,
    img: '/uploads/concerts/SYZ.jpeg',
  },
  {
    name: '汪苏泷 2025 巡回演唱会「十万伏特 2.0」',
    date: '2025.06.27-06.29',
    location: '太原市·山西体育中心体育场',
    price: 380,
    img: '/uploads/concerts/WSL.jpeg',
  },
  {
    name: '凤凰传奇「吉祥如意」2025 巡回演唱会',
    date: '2025.06.27-06.29',
    location: '天津市·天津奥林匹克中心体育场',
    price: 380,
    img: '/uploads/concerts/FHCQ.jpeg',
  }
]
</script>


<style scoped>
.fav-container {
  max-width: 1200px;
  margin: 38px auto 0 auto;
  min-height: 75vh;
  padding: 0 3vw 48px 3vw;
  display: flex;
  flex-direction: column;
}

/* 标题区样式 */
.fav-header {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 32px;
  margin-top: 12px;
}
.fav-icon {
  color: #fcbb32;
  font-size: 34px;
}
.fav-title-text {
  font-size: 2.15rem;
  font-weight: 700;
  color: #2e8461;
  letter-spacing: 2px;
}
.fav-line {
  flex: 1 1 auto;
  height: 2.5px;
  background: linear-gradient(90deg,#bbeeda,#f7d286 70%,#fff 100%);
  margin-left: 18px;
  border-radius: 2px;
  max-width: 400px;
}

/* 卡片列表布局 */
.fav-list {
  display: grid;
  grid-template-columns: repeat(4, 208px);
  gap: 24px 24px;
  justify-content: center;
  padding-top: 165px;
  padding-bottom: 54px;
}

.favorite-info-card {
  width: 208px;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 16px 0 rgba(56,186,118,0.10);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: box-shadow 0.17s, transform 0.12s;
  cursor: pointer;
  position: relative;
}

.favorite-info-card:hover {
  box-shadow: 0 7px 28px 0 rgba(56,186,118,0.18);
  transform: translateY(-3px) scale(1.025);
}

.favorite-cover {
  width: 100%;
  height: 140px;
  object-fit: cover;
  object-position: top center;
  display: block;
  background: #f6f8f7;
}

.favorite-title {
  font-size: 15px;
  font-weight: 700;
  color: #2e8461;
  margin-top: 12px;
  margin-bottom: 4px;
  text-align: center;
  padding: 0 8px;
  min-height: 38px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.favorite-date {
  font-size: 12px;
  color: #7ec6a7;
  margin-bottom: 1px;
  text-align: center;
  letter-spacing: 0.5px;
}

.favorite-price {
  font-size: 13.5px;
  font-weight: 700;
  color: #26ad62;
  background: #f4fcef;
  border-radius: 8px;
  margin: 6px 0 12px 0;
  padding: 1.5px 18px;
  text-align: center;
  letter-spacing: 1.2px;
  box-shadow: 0 1px 3px #e6f5eeab;
}

/* 响应式适配 */
@media (max-width: 1100px) {
  .fav-list {
    grid-template-columns: repeat(3, 208px);
  }
}
@media (max-width: 780px) {
  .fav-list {
    grid-template-columns: repeat(2, 208px);
  }
}
@media (max-width: 540px) {
  .fav-list {
    grid-template-columns: 1fr;
    padding: 18px 0 36px 0;
  }
  .favorite-info-card {
    width: 90vw;
    min-width: 0;
  }
}
</style>
