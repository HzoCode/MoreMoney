<script setup>
import { useRoute } from "vue-router";
const route = useRoute();
</script>

<template>
  <header class="header">
    <span class="logo">A股交易记录</span>
    <nav class="nav">
      <router-link to="/trades" :class="{ active: route.path === '/trades' }">
        交易记录
      </router-link>
      <router-link
        to="/reviews"
        :class="{ active: route.path === '/reviews' }"
      >
        每日复盘
      </router-link>
      <router-link
        to="/summary"
        :class="{ active: route.path === '/summary' }"
      >
        汇总统计
      </router-link>
    </nav>
  </header>
</template>

<style scoped>
.header {
  background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%);
  color: #fff;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 56px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  position: sticky;
  top: 0;
  z-index: 100;
}

.logo {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.nav {
  display: flex;
  gap: 4px;
  height: 100%;
}

.nav a {
  display: flex;
  align-items: center;
  padding: 0 20px;
  color: rgba(255, 255, 255, 0.75);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
  position: relative;
}

.nav a:hover {
  color: #fff;
  background: rgba(255, 255, 255, 0.1);
}

.nav a.active {
  color: #fff;
}

.nav a.active::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 12px;
  right: 12px;
  height: 3px;
  background: #fff;
  border-radius: 3px 3px 0 0;
}
</style>
