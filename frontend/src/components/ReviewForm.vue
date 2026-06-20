<script setup>
import { reactive, watch } from "vue";
import { today } from "../utils/format";

const props = defineProps({
  reviewData: { type: Object, default: null },
});

const emit = defineEmits(["save"]);

const form = reactive({
  review_date: today(),
  market_review: "",
  self_review: "",
  tomorrow_outlook: "",
  tomorrow_plan: "",
});

watch(
  () => props.reviewData,
  (data) => {
    if (data) {
      Object.assign(form, {
        review_date: data.review_date,
        market_review: data.market_review || "",
        self_review: data.self_review || "",
        tomorrow_outlook: data.tomorrow_outlook || "",
        tomorrow_plan: data.tomorrow_plan || "",
      });
    } else {
      Object.assign(form, {
        review_date: today(),
        market_review: "",
        self_review: "",
        tomorrow_outlook: "",
        tomorrow_plan: "",
      });
    }
  },
  { immediate: true }
);

function submit() {
  emit("save", {
    review_date: form.review_date,
    market_review: form.market_review.trim() || null,
    self_review: form.self_review.trim() || null,
    tomorrow_outlook: form.tomorrow_outlook.trim() || null,
    tomorrow_plan: form.tomorrow_plan.trim() || null,
  });
  form.review_date = today();
  form.market_review = "";
  form.self_review = "";
  form.tomorrow_outlook = "";
  form.tomorrow_plan = "";
}
</script>

<template>
  <div class="card">
    <div class="card-header"><h2>每日复盘</h2></div>
    <form class="form" @submit.prevent="submit">
      <label class="form-group">
        <span class="form-label">复盘日期</span>
        <input type="date" v-model="form.review_date" required />
      </label>
      <label class="form-group">
        <span class="form-label">盘面回顾</span>
        <textarea v-model="form.market_review" rows="3" placeholder="大盘走势、热点板块、成交量等"></textarea>
      </label>
      <label class="form-group">
        <span class="form-label">自我复盘</span>
        <textarea v-model="form.self_review" rows="3" placeholder="今日操作回顾、做得好的、做得不好的"></textarea>
      </label>
      <label class="form-group">
        <span class="form-label">明日预期</span>
        <textarea v-model="form.tomorrow_outlook" rows="3" placeholder="对明天大盘和个股的走势预判"></textarea>
      </label>
      <label class="form-group">
        <span class="form-label">明日计划</span>
        <textarea v-model="form.tomorrow_plan" rows="3" placeholder="明天具体的操作计划"></textarea>
      </label>
      <div class="form-actions">
        <button type="submit" class="btn btn-primary">保存复盘</button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.form {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.form-label { font-size: 13px; font-weight: 500; color: var(--text-secondary); }
.form-actions { display: flex; gap: 8px; }
</style>
