<template>
  <section class="category-container">
    <div class="category-header">
      <h2 class="category-title">{{ title }}</h2>
      <a class="more-link" @click.prevent="goToCategory">浏览更多</a>
    </div>

    <div class="scroll-wrapper">
      <div class="scroll-btn-wrapper left-btn-wrapper">
        <button class="scroll-btn" @click="scrollLeft" aria-label="向左滚动">
          <i class="fa-solid fa-chevron-left"></i>
        </button>
      </div>

      <div class="scroll-container" ref="scrollContainer">
        <ArtistCard
          v-for="(artist, index) in artists"
          :key="index"
          :name="artist.name"
          :img="artist.img"
          :link="artist.link"
        />
      </div>

      <div class="scroll-btn-wrapper right-btn-wrapper">
        <button class="scroll-btn" @click="scrollRight" aria-label="向右滚动">
          <i class="fa-solid fa-chevron-right"></i>
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import ArtistCard from '../components/ArtistCardComp.vue'

defineProps({
  title: String,
  artists: {
    type: Array,
    default: () => [],
  },
})

const router = useRouter()
const scrollContainer = ref(null)

function goToCategory() {
  router.push('/category')
}

function scrollLeft() {
  scrollContainer.value.scrollBy({ left: -300, behavior: 'smooth' })
}
function scrollRight() {
  scrollContainer.value.scrollBy({ left: 300, behavior: 'smooth' })
}
</script>
