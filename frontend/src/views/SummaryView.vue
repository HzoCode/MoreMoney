<script setup>
import { ref, onMounted } from "vue";
import { api } from "../api";
import { useRequest } from "../composables/useRequest";
import { fmtMoney, fmtPct, truncate, today } from "../utils/format";
import SummaryCards from "../components/SummaryCards.vue";

const period = ref("daily");
const summary = ref(null);
const { loading, execute } = useRequest();

const dailyDate = ref(today());
const now = new Date();
const weekYear = ref(now.getFullYear());
const weekNum = ref(1);
const monthYear = ref(now.getFullYear());
const monthNum = ref(now.getMonth() + 1);
const yearVal = ref(now.getFullYear());

const monthOptions = [
  [1, "1月"], [2, "2月"], [3, "3月"], [4, "4月"],
  [5, "5月"], [6, "6月"], [7, "7月"], [8, "8月"],
  [9, "9月"], [10, "10月"], [11, "11月"], [12, "12月"],
];

async function loadSummary() {
  const params = { period: period.value };
  if (period.value === "daily") params.date_param = dailyDate.value;
  else if (period.value === "weekly") { params.year = weekYear.value; params.week = weekNum.value; }
  else if (period.value === "monthly") { params.year = monthYear.value; params.month = monthNum.value; }
  else if (period.value === "yearly") params.year = yearVal.value;
  try {
    summary.value = await execute(() => api.getSummary(params));
  } catch (e) {
    alert("查询汇总失败: " + e.message);
  }
}

onMounted(loadSummary);
</script>

<template>
  <div class="card">
    <div class="card-header"><h2>汇总统计</h2></div>
    <div class="controls">
      <label class="form-group">
        <span class="ctrl-label">统计周期</span>
        <select v-model="period">
          <option value="daily">按日</option>
          <option value="weekly">按周</option>
          <option value="monthly">按月</option>
          <option value="yearly">按年</option>
        </select>
      </label>

      <label v-if="period === 'daily'" class="form-group">
        <span class="ctrl-label">日期</span>
        <input type="date" v-model="dailyDate" />
      </label>

      <template v-if="period === 'weekly'">
        <label class="form-group"><span class="ctrl-label">年份</span><input type="number" v-model.number="weekYear" min="2000" max="2100" /></label>
        <label class="form-group"><span class="ctrl-label">周数</span><input type="number" v-model.number="weekNum" min="1" max="53" /></label>
      </template>

      <template v-if="period === 'monthly'">
        <label class="form-group"><span class="ctrl-label">年份</span><input type="number" v-model.number="monthYear" min="2000" max="2100" /></label>
        <label class="form-group"><span class="ctrl-label">月份</span>
          <select v-model.number="monthNum">
            <option v-for="[v, label] in monthOptions" :key="v" :value="v">{{ label }}</option>
          </select>
        </label>
      </template>

      <label v-if="period === 'yearly'" class="form-group">
        <span class="ctrl-label">年份</span>
        <input type="number" v-model.number="yearVal" min="2000" max="2100" />
      </label>

      <label class="form-group" style="align-self:flex-end">
        <span class="ctrl-label">&nbsp;</span>
        <button class="btn btn-primary" @click="loadSummary">查询</button>
      </label>
    </div>
  </div>

  <div v-if="loading" class="loading">加载中...</div>

  <template v-if="summary && !loading">
    <SummaryCards :summary="summary" />

    <div class="card">
      <div class="card-header"><h3>个股统计</h3></div>
      <div class="table-wrap">
        <table v-if="summary.stocks.length" class="table">
          <thead>
            <tr><th>股票</th><th>交易次数</th><th>总盈亏</th></tr>
          </thead>
          <tbody>
            <tr v-for="s in summary.stocks" :key="s.name">
              <td>{{ s.name }}</td>
              <td>{{ s.count }}</td>
              <td :class="fmtMoney(s.total_pnl).cls">{{ fmtMoney(s.total_pnl).text }}</td>
            </tr>
          </tbody>
        </table>
        <p v-else class="empty-msg">无数据</p>
      </div>
    </div>

    <div class="card">
      <div class="card-header"><h3>交易明细</h3></div>
      <div class="table-wrap">
        <table v-if="summary.trades.length" class="table">
          <thead>
            <tr><th>日期</th><th>代码</th><th>名称</th><th>方向</th><th>金额</th><th>盈亏</th><th>盈亏%</th><th>理由</th></tr>
          </thead>
          <tbody>
            <tr v-for="t in summary.trades" :key="t.id">
              <td>{{ t.trade_date }}</td>
              <td>{{ t.stock_code }}</td>
              <td>{{ t.stock_name }}</td>
              <td>
                <span class="badge" :class="t.direction === '买入' ? 'badge-buy' : 'badge-sell'">{{ t.direction }}</span>
              </td>
              <td>{{ t.amount.toLocaleString() }}</td>
              <td :class="fmtMoney(t.pnl).cls">{{ fmtMoney(t.pnl).text }}</td>
              <td :class="fmtMoney(t.pnl_pct).cls">{{ fmtPct(t.pnl_pct).text }}</td>
              <td :title="t.reason || ''">{{ truncate(t.reason, 20) }}</td>
            </tr>
          </tbody>
        </table>
        <p v-else class="empty-msg">无数据</p>
      </div>
    </div>
  </template>
</template>

<style scoped>
.controls { padding: 16px 20px; display: flex; gap: 16px; flex-wrap: wrap; align-items: flex-end; }
.ctrl-label { font-size: 13px; font-weight: 500; color: var(--text-secondary); }
</style>
