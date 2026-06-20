<script setup>
defineProps({
  summary: { type: Object, required: true },
});
</script>

<template>
  <div class="stat-grid">
    <div class="stat-card">
      <div class="sc-label">{{ summary.title }}</div>
      <div class="sc-value">{{ summary.total_trades }}</div>
      <div class="sc-sub">总交易次数（买{{ summary.buy_count }} / 卖{{ summary.sell_count }}）</div>
    </div>
    <div class="stat-card">
      <div class="sc-label">总盈亏</div>
      <div class="sc-value" :class="{ profit: summary.total_pnl > 0, loss: summary.total_pnl < 0 }">
        {{ summary.total_pnl >= 0 ? "+" : "" }}{{ summary.total_pnl.toFixed(2) }}
      </div>
      <div class="sc-sub">
        买卖总金额: {{ summary.total_buy_amount.toLocaleString() }} /
        {{ summary.total_sell_amount.toLocaleString() }}
      </div>
    </div>
    <div class="stat-card">
      <div class="sc-label">胜率</div>
      <div class="sc-value">{{ summary.win_rate }}%</div>
      <div class="sc-sub">盈{{ summary.win_count }}笔 / 亏{{ summary.loss_count }}笔</div>
    </div>
    <div class="stat-card">
      <div class="sc-label">最大盈亏</div>
      <div class="sc-value profit" v-if="summary.biggest_win > 0">+{{ summary.biggest_win.toFixed(2) }}</div>
      <div class="sc-value" v-else>-</div>
      <div class="sc-sub">最大亏损: {{ summary.biggest_loss.toFixed(2) }}</div>
    </div>
  </div>
</template>

<style scoped>
.stat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}
.stat-card {
  background: var(--card-bg);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 20px;
  text-align: center;
}
.sc-label { font-size: 12px; color: var(--text-secondary); margin-bottom: 6px; letter-spacing: .5px; }
.sc-value { font-size: 28px; font-weight: 700; }
.sc-sub { font-size: 13px; color: var(--text-secondary); margin-top: 4px; }
</style>
