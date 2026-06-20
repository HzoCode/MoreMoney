<script setup>
import { truncate } from "../utils/format";

defineProps({
  reviews: { type: Array, default: () => [] },
});

const emit = defineEmits(["select"]);
</script>

<template>
  <div class="card review-card">
    <div class="card-header"><h2>历史复盘</h2></div>
    <div class="list">
      <div
        v-for="r in reviews"
        :key="r.id"
        class="item"
        @click="emit('select', r.review_date)"
      >
        <div class="item-date">{{ r.review_date }}</div>
        <div class="item-preview">
          {{ truncate(r.market_review || r.self_review, 40) }}
        </div>
      </div>
      <p v-if="!reviews.length" class="empty-msg">暂无复盘记录</p>
    </div>
  </div>
</template>

<style scoped>
.review-card { position: sticky; top: 76px; }
.list { padding: 12px 16px; max-height: 600px; overflow-y: auto; }
.item {
  padding: 12px;
  border: 1px solid var(--border);
  border-radius: 6px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: all 0.15s;
}
.item:hover { border-color: var(--primary); background: #f8faff; }
.item-date { font-weight: 600; font-size: 14px; margin-bottom: 4px; }
.item-preview {
  font-size: 12px;
  color: var(--text-secondary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
