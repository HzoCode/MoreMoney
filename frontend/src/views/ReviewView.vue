<script setup>
import { ref, onMounted } from "vue";
import { api } from "../api";
import { useRequest } from "../composables/useRequest";
import ReviewForm from "../components/ReviewForm.vue";
import ReviewHistory from "../components/ReviewHistory.vue";

const reviews = ref([]);
const reviewData = ref(null);
const { loading, execute } = useRequest();

async function loadReviews() {
  try {
    reviews.value = await execute(() => api.listReviews());
  } catch (e) {
    alert("加载复盘记录失败: " + e.message);
  }
}

async function handleSave(data) {
  try {
    await execute(() => api.upsertReview(data));
    reviewData.value = null;
    await loadReviews();
  } catch (e) {
    alert("保存复盘失败: " + e.message);
  }
}

async function handleSelect(dateStr) {
  try {
    reviewData.value = await execute(() => api.getReview(dateStr));
  } catch (e) {
    alert("加载复盘失败: " + e.message);
  }
}

onMounted(loadReviews);
</script>

<template>
  <div class="layout">
    <ReviewForm :reviewData="reviewData" @save="handleSave" />
    <div>
      <div v-if="loading" class="loading">加载中...</div>
      <ReviewHistory v-else :reviews="reviews" @select="handleSelect" />
    </div>
  </div>
</template>

<style scoped>
.layout {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 20px;
  align-items: start;
}

@media (max-width: 768px) {
  .layout { grid-template-columns: 1fr; }
}
</style>
