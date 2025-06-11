<template>
  <div>
    <NavbarComp />

    <div class="category-container">
      <!-- 左3/4：筛选+列表 -->
      <div class="main-content">
        <!-- 筛选条 -->
        <div class="filter-bar card">
  <div class="filter-row">
    <!-- 城市 -->
    <div class="filter-city-wrap">
      <span class="filter-title">城市：</span>
      <div class="filter-options city-options" :class="{ expanded: showAllCities }">
        <span
          v-for="city in displayedCities"
          :key="city"
          :class="['filter-option', {active: city === selectedCity}]"
          @click="selectCity(city)"
        >{{ city }}</span>
        <span
          class="filter-option more-btn"
          @click="toggleShowCities"
          v-if="!showAllCities"
        >更多 <span style="font-size:12px;">▼</span></span>
        <span
          class="filter-option more-btn"
          @click="toggleShowCities"
          v-if="showAllCities"
        >收起 <span style="font-size:12px;">▲</span></span>
      </div>
    </div>
    <!-- 时间 -->
    <div class="filter-time-wrap">
      <span class="filter-title">时间：</span>
      <div class="filter-options time-options">
        <span
          v-for="time in times"
          :key="time"
          :class="['filter-option', {active: time === selectedTime}]"
          @click="selectTime(time)"
        >{{ time }}</span>
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
            :to="`/concert/${item.id}`"
            class="recommend-link"
            style="text-decoration:none;"
          >
            <RecommendCard :concert="item" />
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import NavbarComp from '../components/NavbarComp.vue'
import CategoryInfoComp from '../components/CategoryInfoComp.vue'
import RecommendCard from '../components/RecommendCard.vue'
import dayjs from 'dayjs'
import isSameOrAfter from 'dayjs/plugin/isSameOrAfter'
import isSameOrBefore from 'dayjs/plugin/isSameOrBefore'
dayjs.extend(isSameOrAfter)
dayjs.extend(isSameOrBefore)
import isBetween from 'dayjs/plugin/isBetween'
dayjs.extend(isBetween)

const hotCities = [
  '全部', '成都', '上海', '北京', '杭州', '苏州', '重庆', '昆明', '西安', '广州', '德阳',
  '三亚', '南京', '长沙', '厦门', '洛阳', '深圳', '武汉', '沈阳'
];
const allCities = [
  '全部', '成都', '上海', '北京', '杭州', '苏州', '重庆', '昆明', '西安', '广州', '德阳', '三亚',
  '南京', '长沙', '厦门', '洛阳', '深圳', '武汉', '沈阳', '天津', '郑州', '哈尔滨', '长春', '大连', '济南', '青岛', '太原', '石家庄', '福州', '南昌', '合肥', '南宁', '海口',
  '兰州', '呼和浩特', '银川', '乌鲁木齐', '拉萨', '贵阳', '西宁', '湛江', '珠海', '中山', '佛山', '汕头', '江门',
  '东莞', '惠州', '茂名', '肇庆', '揭阳', '韶关', '阳江', '清远', '汕尾', '潮州', '梅州', '河源', '云浮', '肇庆',
  '珠海', '桂林', '柳州', '北海', '南宁', '玉林', '梧州', '百色', '贺州', '钦州', '防城港', '贵港', '来宾',
  '常州', '无锡', '徐州', '连云港', '盐城', '扬州', '镇江', '泰州', '淮安', '宿迁', '南通', '宜兴',
  '宁波', '温州', '嘉兴', '湖州', '绍兴', '金华', '舟山', '台州', '丽水', '衢州', '义乌',
  '芜湖', '蚌埠', '淮南', '马鞍山', '铜陵', '安庆', '黄山', '滁州', '阜阳', '宿州', '巢湖', '六安', '亳州', '池州', '宣城',
  '合肥', '安庆', '淮北', '淮南', '滁州', '六安', '亳州', '宿州', '池州', '铜陵', '巢湖', '宣城', '蚌埠', '马鞍山', '黄山',
  '南昌', '赣州', '九江', '宜春', '上饶', '吉安', '抚州', '景德镇', '萍乡', '新余', '鹰潭',
  '厦门', '漳州', '泉州', '三明', '南平', '龙岩', '宁德', '莆田', '福清',
  '济南', '青岛', '烟台', '潍坊', '临沂', '淄博', '济宁', '泰安', '东营', '威海', '日照', '德州', '聊城', '滨州', '菏泽', '枣庄',
  '郑州', '洛阳', '新乡', '焦作', '安阳', '开封', '平顶山', '鹤壁', '濮阳', '许昌', '漯河', '三门峡', '南阳', '商丘', '信阳', '周口', '驻马店',
  '长沙', '株洲', '湘潭', '衡阳', '邵阳', '岳阳', '常德', '张家界', '益阳', '郴州', '永州', '怀化', '娄底', '湘西',
  '南宁', '桂林', '柳州', '梧州', '北海', '防城港', '钦州', '贵港', '玉林', '百色', '贺州', '河池', '来宾', '崇左',
  '昆明', '曲靖', '玉溪', '保山', '昭通', '丽江', '普洱', '临沧', '楚雄', '红河', '文山', '西双版纳', '大理', '德宏', '怒江', '迪庆',
  '贵阳', '六盘水', '遵义', '安顺', '铜仁', '毕节', '黔西南', '黔东南', '黔南',
  '海口', '三亚', '儋州', '琼海', '万宁', '文昌', '东方', '定安', '屯昌', '澄迈', '临高', '白沙', '昌江', '乐东', '陵水', '保亭', '琼中',
  '拉萨', '日喀则', '昌都', '林芝', '山南', '那曲', '阿里',
  '西安', '咸阳', '宝鸡', '铜川', '渭南', '延安', '汉中', '榆林', '安康', '商洛',
  '兰州', '嘉峪关', '金昌', '白银', '天水', '武威', '张掖', '平凉', '酒泉', '庆阳', '定西', '陇南', '临夏', '甘南',
  '银川', '石嘴山', '吴忠', '固原', '中卫',
  '西宁', '海东', '海北', '黄南', '海南', '果洛', '玉树', '海西',
  '呼和浩特', '包头', '乌海', '赤峰', '通辽', '鄂尔多斯', '呼伦贝尔', '巴彦淖尔', '乌兰察布', '兴安', '锡林郭勒', '阿拉善',
  '乌鲁木齐', '克拉玛依', '吐鲁番', '哈密', '昌吉', '博尔塔拉', '巴音郭楞', '阿克苏', '克孜勒苏', '喀什', '和田', '伊犁', '塔城', '阿勒泰',
  // 港澳台
  '香港', '澳门', '台北', '高雄', '台中', '台南', '新北', '桃园', '基隆', '新竹', '嘉义', '屏东', '南投', '宜兰', '花莲', '台东', '澎湖', '金门', '连江',
  // 海外
  '东京', '大阪', '首尔', '曼谷', '新加坡', '吉隆坡', '马尼拉', '雅加达', '洛杉矶', '纽约', '伦敦', '巴黎', '柏林', '悉尼', '墨尔本', '温哥华', '多伦多',
];
const showAllCities = ref(false);

const displayedCities = computed(() => showAllCities.value ? allCities : hotCities);

function toggleShowCities() {
  showAllCities.value = !showAllCities.value;
}
const times = ['全部', '今天', '明天', '本周末', '一个月内']

const selectedCity = ref('全部')
const selectedTime = ref('全部')

const selectCity = city => selectedCity.value = city
const selectTime = time => selectedTime.value = time

// TODO:演唱会数据
const concerts = ref([
  {
    id: 1,
    name: "【成都】新蜂音乐节·成都站",
    tag: "音乐节",
    artist: "薛之谦, 潘玮柏, 黄子弘凡",
    location: "成都露天音乐公园北广场",
    date: "2025.07.05-07.06",
    price: "189-1197元",
    status: "售票中",
    poster: "fengmusic.png"
  },
  {
    id: 2,
    name: "【北京】开心水花摇滚音乐大戏《燃烧PLUS》",
    tag: "演唱会",
    artist: "张三, 李四, 王五",
    location: "地坛剧场剧场",
    date: "2025.06.29-07.06",
    price: "80-1080元",
    status: "售票中",
    poster: "rockshow.png"
  },
  {
    id: 3,
    name: "【沈阳】汽水音乐Chill派对",
    tag: "音乐节",
    artist: "李志, 万能青年旅店, 八三夭, 八仙乐队, 芳文",
    location: "沈阳航空航天大学体育场",
    date: "2025.06.14-06.15",
    price: "98元",
    status: "售票中",
    poster: "chillparty.png"
  },
  {
    id: 4,
    name: "【哈尔滨】五月天 2025五月天25周年巡回演唱会",
    tag: "演唱会",
    artist: "五月天",
    location: "哈尔滨国际会展体育中心体育场",
    date: "2025.06.13-06.15",
    price: "355-1555元",
    status: "售票中",
    poster: "mayday.png"
  },
  {
    id: 5,
    name: "【青岛】林忆莲《回忆 Resonance》2025巡回演唱会",
    tag: "演唱会",
    artist: "林忆莲",
    location: "青岛市体育中心体育场",
    date: "2025.06.29",
    price: "266-1288元",
    status: "售罄",
    poster: "linyilian.png"
  },
  {
    id: 6,
    name: "【上海】陶喆 Soul Power II 世界巡回演唱会",
    tag: "演唱会",
    artist: "陶喆",
    location: "上海梅赛德斯奔驰文化中心",
    date: "2025.07.12",
    price: "399-1299元",
    status: "售票中",
    poster: "taozhe.png"
  },
  {
    id: 7,
    name: "【深圳】李荣浩 年少有为 演唱会",
    tag: "演唱会",
    artist: "李荣浩",
    location: "深圳湾体育中心",
    date: "2025.07.20",
    price: "299-999元",
    status: "售票中",
    poster: "lironghao.png"
  },
  {
    id: 8,
    name: "【杭州】周杰伦 嘉年华巡回演唱会",
    tag: "演唱会",
    artist: "周杰伦",
    location: "杭州奥体中心",
    date: "2025.08.02",
    price: "520-2025元",
    status: "售票中",
    poster: "jaychou.png"
  },
  {
    id: 9,
    name: "【广州】薛之谦 天外来物巡回演唱会",
    tag: "演唱会",
    artist: "薛之谦",
    location: "广州体育馆",
    date: "2025.08.08",
    price: "299-1599元",
    status: "售票中",
    poster: "xuezhiqian.png"
  },
  {
    id: 10,
    name: "【北京】五月天 Just Rock It！演唱会",
    tag: "演唱会",
    artist: "五月天",
    location: "北京鸟巢",
    date: "2025.06.28",
    price: "599-1599元",
    status: "售票中",
    poster: "maydaybj.png"
  }
])

// TODO:右侧推荐数据
const recommendedConcerts = ref([
  {
    id: 100,
    name: "李荣浩 年少有为 演唱会",
    date: "2025.06.30",
    poster: "lironghao.png",
    price: "299元起"
  },
  {
    id: 101,
    name: "薛之谦 天外来物巡回演唱会",
    date: "2025.07.15",
    poster: "xuezhiqian.png",
    price: "399元起"
  },
  {
    id: 102,
    name: "周杰伦 嘉年华巡回演唱会",
    date: "2025.08.02",
    poster: "jaychou.png",
    price: "520元起"
  }
])

const filteredConcerts = computed(() => {
  let res = concerts.value

  // 城市筛选
  if (selectedCity.value !== '全部') {
    res = res.filter(c => c.name.includes(selectedCity.value))
  }

  // 时间筛选
  if (selectedTime.value !== '全部') {
    const now = dayjs()
    let rangeStart, rangeEnd

    switch (selectedTime.value) {
      case '今天':
        rangeStart = now.startOf('day')
        rangeEnd = now.endOf('day')
        break
      case '明天':
        rangeStart = now.add(1, 'day').startOf('day')
        rangeEnd = now.add(1, 'day').endOf('day')
        break
      case '本周末':
        // 本周六~周日
        rangeStart = now.day(6).startOf('day') // 周六
        rangeEnd = now.day(7).endOf('day')     // 周日
        break
      case '一个月内':
        rangeStart = now
        rangeEnd = now.add(1, 'month').endOf('day')
        break
      default:
        rangeStart = null
        rangeEnd = null
    }

    res = res.filter(c => {
      let [start, end] = c.date.split('-')
      start = start.trim()
      end = end ? end.trim() : start

      if (/^\d{2}\.\d{2}$/.test(end)) {
        end = start.slice(0, 5) + end
      }

      let startDay = dayjs(start, 'YYYY.MM.DD')
      let endDay = dayjs(end, 'YYYY.MM.DD')

      return endDay.isSameOrAfter(rangeStart) && startDay.isSameOrBefore(rangeEnd)
    })
  }

  return res
})

</script>






<style scoped>

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
  box-shadow: 0 2px 14px rgba(80,180,120,0.08);
  height: auto;
  flex-shrink: 0;
  position: sticky;
  top: 60px;
}

.card {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 2px 14px rgba(80,180,120,0.08);
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
  transition: background 0.15s, color 0.15s;
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
.recommend-date, .recommend-price {
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
