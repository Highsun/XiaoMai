<template>
  <section class="hero-section">
    <div class="hero-main">
      <div class="nav-btn left-btn" @click="prevSlide">
        <i class="fa-solid fa-circle-chevron-left"></i>
      </div>

      <!-- 左侧文字内容 -->
      <div
        class="hero-content"
        :key="slides[current].title"
        :class="['fade-slide', animationDirection]"
      >
        <h1 class="title">{{ slides[current].title }}</h1>
        <p class="subtitle" v-html="slides[current].description"></p>

        <button class="btn-ticket" @click="goToTickets">立即购票</button>
      </div>

      <!-- 右侧图片内容 -->
      <div class="hero-image">
        <img
          :src="slides[current].img"
          :key="slides[current].img"
          :alt="slides[current].title"
          :class="['fade-slide-img', animationDirection]"
        />
      </div>

      <div class="nav-btn right-btn" @click="nextSlide">
        <i class="fa-solid fa-circle-chevron-right"></i>
      </div>
    </div>

    <!-- 指示器 -->
    <div class="hero-indicator">
      <span
        v-for="(slide, i) in slides"
        :key="i"
        class="dot"
        :class="{ active: i === current }"
        @click="goTo(i)"
      ></span>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

// TODO: 后期替换为动态数据
const slides = [
  {
    title: '林俊杰 JJ20 FINAL LAP 世界巡回演唱会',
    description: `《JJ20 世界巡回演唱会》，自2022年11月在新加坡首演以来，便获得了极高评价。2025年，林俊杰将呈现他全新的《JJ20 FINAL LAP 世界巡回演唱会》，此轮巡演的最终回标志着林俊杰20周年音乐生涯的里程碑。<br/><br/>
    立即购票，锁定你的专属座位！⬇️`,
    img: '/uploads/hero_section/JJ20.jpeg',
  },
  {
    title: '周杰伦《嘉年华》巡回演唱会',
    description: `亚洲天王周杰伦和他震撼人心的嘉年华演唱会即将登陆！这场演出将汇聚他最具代表性的经典金曲，并结合崭新的舞台设计，势必掀起一场无与伦比的音乐狂欢！<br/><br/>
    立即购票，锁定你的专属座位！⬇️`,
    img: '/uploads/hero_section/Jay.jpg',
  },
  {
    title: '陶喆 Soul Power II 世界巡回演唱会',
    description: `台湾R&B教父陶喆携“Soul Power II”世界巡演时隔20年回归！全场交织《爱很简单》《普通朋友》《就是爱你》等跨时代经典与全新编曲，现场即兴与升级舞美共同缔造沉浸式视听盛宴。<br/><br/>
    立即购票，锁定你的专属座位！⬇️`,
    img: '/uploads/hero_section/SP2.jpg',
  },
]

const current = ref(0)
const animationDirection = ref('fade-left')

let interval = null

function resetInterval() {
  clearInterval(interval)
  interval = setInterval(() => changeSlide('left'), 5000)
}

function changeSlide(direction) {
  animationDirection.value = direction === 'left' ? 'fade-left' : 'fade-right'

  if (direction === 'left') {
    current.value = (current.value + 1) % slides.length
  } else if (direction === 'right') {
    current.value = (current.value - 1 + slides.length) % slides.length
  }
}

function nextSlide() {
  changeSlide('left')
  resetInterval()
}

function prevSlide() {
  changeSlide('right')
  resetInterval()
}

function goTo(i) {
  animationDirection.value = i > current.value ? 'fade-left' : 'fade-right'
  current.value = i
  resetInterval()
}

function goToTickets() {
  // TODO: 跳转购票页面的逻辑
  console.log('跳转购票页')
}

onMounted(() => {
  resetInterval()
})

onBeforeUnmount(() => {
  clearInterval(interval)
})
</script>
