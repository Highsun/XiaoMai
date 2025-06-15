<template>
  <Navbar />
  <div class="ticket-container">
    <PosterSection />
    <FormSection />
    <InfoSection />
  </div>
  <ConcertInfo />
  <Footer />
</template>

<script setup>
import Navbar from '../components/NavbarComp.vue'
import PosterSection from '../components/buy_tickets_comps/PosterSection.vue'
import FormSection from '../components/buy_tickets_comps/FormSection.vue'
import InfoSection from '../components/buy_tickets_comps/InfoSection.vue'
import ConcertInfo from '../components/ConcertInfoComp.vue'
import Footer from '../components/FooterComp.vue'
import { onMounted } from 'vue'
onMounted(() => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
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
