<script setup>
import NavHeader from "./components/NavHeader.vue";
</script>

<template>
  <NavHeader />
  <main class="main">
    <router-view />
  </main>
</template>

<style>
:root {
  --primary: #1a73e8;
  --primary-hover: #1557b0;
  --danger: #dc2626;
  --danger-hover: #b91c1c;
  --success: #16a34a;
  --bg: #f0f2f5;
  --card-bg: #ffffff;
  --text: #1f2937;
  --text-secondary: #6b7280;
  --border: #e5e7eb;
  --input-bg: #f9fafb;
  --radius: 8px;
  --shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.06);
}

*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC",
    "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
}

.main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px 24px 40px;
}
</style>
