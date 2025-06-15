<template>
  <div class="info-page">
    <!-- 左侧导航 -->
    <nav class="info-sidebar">
      <ul>
        <li
          v-for="item in navItems"
          :key="item.id"
          :class="{ active: activeSection === item.id }"
          @click="scrollTo(item.id)"
        >
          {{ item.label }}
        </li>
      </ul>
    </nav>

    <!-- 主内容 -->
    <div class="info-content">
      <!-- 购票须知 -->
      <section id="ticket" class="info-section" ref="ticketRef">
        <h2>购票须知</h2>
        <div>
          <span style="font-size: 14px; color: #555">限购规则</span><br />
          每笔订单最多购买4张、每个账号最多购买4张。<br /><br />

          <span style="font-size: 14px; color: #555">退票/换票规则</span><br />
          本项目支持有条件退款，具体可申请退票的期间、退票手续费等退票条件以项目主办方提供的退票政策为准，详见服务说明或项目详情页公示的退票政策。<br /><br />

          <span style="font-size: 14px; color: #555">入场规则</span><br />
          须携带购票时对应证件验证入场。<br /><br />

          <span style="font-size: 14px; color: #555">儿童购票</span><br />
          儿童一律凭票入场。<br /><br />

          <span style="font-size: 14px; color: #555">发票说明</span><br />
          演出开始前，前往【订单详情】页面提交发票申请。我们会将电子发票发送至您的邮箱。<br /><br />

          <span style="font-size: 14px; color: #555">实名购票规则</span><br />
          一张门票对应一个证件；证件支持：台湾居民来往大陆通行证/外国人永久居留身份证/港澳居民来往内地通行证/港澳台居民居住证/护照/身份证。<br /><br />

          <span style="font-size: 14px; color: #555">异常排单规则</span><br />
          对于异常订购行为，小麦网有权在订单成立或者生效之后取消相应订单。异常订购行为包括但不限于以下情形：<br />
          （1）通过同一ID订购超出限购张数的订单。<br />
          （2）经合理判断认为非真实消费者的下单行为，包括但不限于通过批量相同或虚构的支付账号、收货地址（包括下单时填写及最终实际收货地址）、收件人、电话号码订购超出限购张数的订单。<br /><br />

          <span style="font-size: 14px; color: #555">温馨提示</span><br />
          （1）购买前请您提前规划好行程，做好相应准备，以免影响您的正常观演，感谢您的理解和配合。<br />
          （2）若演出受不可抗力影响延期或取消，小麦将对演出票订单按照项目官方通知方案进行处理，其他因观演发生的费用需由您自行承担。<br /><br />
        </div>
      </section>

      <!-- 观演须知 -->
      <section id="entry" class="info-section" ref="entryRef">
        <h2>观演须知</h2>
        <div>
          <span style="font-size: 14px; color: #555">演出时长</span><br />
          约120分钟（以现场为准）<br /><br />
          <span style="font-size: 14px; color: #555">入场时间</span><br />
          请于演出前约120分钟入场。<br /><br />
          <span style="font-size: 14px; color: #555">最低演出曲目</span><br />
          20<br /><br />
          <span style="font-size: 14px; color: #555">最低演出时长</span><br />
          120分钟<br /><br />
          <span style="font-size: 14px; color: #555">禁止携带物品</span><br />
          由于安保和版权的原因，大多数演出、展览及比赛场所禁止携带食品、饮料、专业摄录设备、打火机等物品，请您注意现场工作人员和广播的提示，予以配合。<br /><br />
          <span style="font-size: 14px; color: #555">寄存说明</span><br />
          无寄存处,请自行保管携带物品，谨防贵重物品丢失。<br /><br />
          <span style="font-size: 14px; color: #555">重要提示</span><br />
          演出现场气氛热烈，请您务必根据自身身体状况酌情是否购票参与观演，特别是患有心脏类疾病、急性心脑血管疾病、心肌炎、高血压等相关疾病的人群，请您务必遵照医嘱，结合病史及个人身体状况进行观演，观演期间请自行承担身体健康相关责任。<br /><br />
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'

const navItems = [
  { id: 'ticket', label: '购票须知' },
  { id: 'entry', label: '观演须知' },
]

const activeSection = ref(navItems[0].id)
const detailsRef = ref(null)
const ticketRef = ref(null)
const entryRef = ref(null)
let observer = null

function scrollTo(id) {
  const el = document.getElementById(id)
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

onMounted(() => {
  nextTick(() => {
    observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            activeSection.value = entry.target.id
            break
          }
        }
      },
      {
        root: null,
        rootMargin: '0px 0px -70% 0px',
        threshold: 0.1,
      },
    )

    const sectionRefs = [detailsRef.value, ticketRef.value, entryRef.value]
    sectionRefs.forEach((el) => {
      if (el) {
        observer.observe(el)
      }
    })
  })
})

onUnmounted(() => {
  if (observer) {
    observer.disconnect()
  }
})
</script>
