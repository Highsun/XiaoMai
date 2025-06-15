<template>
  <Navbar />
  <div class="ticket-container" v-if="concertData">
    <PosterSection />
    <!-- 传入 concertData 到 FormSection -->
    <FormSection :concert="concertData" />
    <InfoSection />
  </div>
  <ConcertInfo />
  <Footer />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

import Navbar from '../components/NavbarComp.vue'
import PosterSection from '../components/buy_tickets_comps/PosterSection.vue'
import FormSection   from '../components/buy_tickets_comps/FormSection.vue'
import InfoSection   from '../components/buy_tickets_comps/InfoSection.vue'
import ConcertInfo   from '../components/ConcertInfoComp.vue'
import Footer        from '../components/FooterComp.vue'

const route       = useRoute()
const concertData = ref(null)

onMounted(async () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
  const id = route.params.id
  try {
    const res = await axios.get(`/api/shows/${id}`)
    if (res.data.code === 0) {
      concertData.value = res.data.data
    } else {
      console.warn('获取演出信息失败:', res.data.message)
    }
  } catch (err) {
    console.error('请求出错:', err)
  }
})
</script>

<style scoped>
.ticket-container {
  margin: 64px 60px 30px 60px;
  padding-top: 10px;
  display: flex;
  overflow: hidden;
  background: #fff;
}
</style>
