<template>
  <footer class="footer">
    <div class="footer-container">
      <!-- 左侧 Logo -->
      <div class="footer-left">
        <div class="footer-brand-wrapper">
          <!-- TODO: 添加小麦LOGO -->
          <img src="../assets/logo.png" alt="logo" class="footer-logo" />
          <div class="footer-text">
            <h1 class="footer-brand">小麦</h1>
            <p class="footer-slogan">看演出，上小麦！</p>
          </div>
        </div>
      </div>

      <!-- 右侧链接与信息 -->
      <div class="footer-right">
        <div class="footer-section">
          <h3>联系我们</h3>
          <ul>
            <li>Email: support@xiaomai.com</li>
            <li>电话: 123-456-7890</li>
            <li>地址: 成都市郫都区西源大道2006号</li>
          </ul>
        </div>

        <!-- TODO: 绑定页面跳转 -->
        <div class="footer-section">
          <h3>快速导航</h3>
          <div class="footer-links">
            <ul>
              <li><a href="#">关于小麦</a></li>
              <li><a href="#">隐私政策</a></li>
              <li><a href="javascript:void(0)" @click="goToHelp">帮助中心</a></li>
            </ul>
            <ul>
              <li><a href="#">在线客服</a></li>
              <li><a href="#">联系合作</a></li>
              <li><a href="#">人才招聘</a></li>
            </ul>
          </div>
        </div>

        <!-- TODO: 绑定账号 -->
        <div class="footer-section">
          <h3>关注我们</h3>
          <div class="footer-social">
            <a
              href="https://github.com/Highsun/XiaoMai"
              class="social-icon fab fa-github"
              target="_blank"
            ></a>
            <a href="#" class="social-icon fab fa-weibo"></a>
            <a href="#" class="social-icon fab fa-tiktok"></a>
          </div>
        </div>
      </div>
    </div>

    <div class="footer-bottom">
      <p>&copy; 2025 XiaoMai. 保留所有权利.</p>
    </div>
  </footer>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()

// 跳转到帮助中心
function goToHelp() {
  router.push({ name: 'Dashboard', query: { view: 'help' } })
}
</script>
