<script setup>
import { fmtMoney, fmtPct, truncate } from "../utils/format";

defineProps({
  trades: { type: Array, default: () => [] },
});

const emit = defineEmits(["edit", "delete"]);
</script>

<template>
  <div class="card">
    <div class="card-header"><h2>交易列表</h2></div>
    <div class="table-wrap">
      <table v-if="trades.length" class="table">
        <thead>
          <tr>
            <th>日期</th>
            <th>代码</th>
            <th>名称</th>
            <th>方向</th>
            <th>价格</th>
            <th>数量</th>
            <th>金额</th>
            <th>仓位%</th>
            <th>盈亏</th>
            <th>盈亏%</th>
            <th>理由</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in trades" :key="t.id">
            <td>{{ t.trade_date }}</td>
            <td>{{ t.stock_code }}</td>
            <td>{{ t.stock_name }}</td>
            <td>
              <span class="badge" :class="t.direction === '买入' ? 'badge-buy' : 'badge-sell'">
                {{ t.direction }}
              </span>
            </td>
            <td>{{ t.price }}</td>
            <td>{{ t.quantity.toLocaleString() }}</td>
            <td>{{ t.amount.toLocaleString() }}</td>
            <td>{{ t.position_pct != null ? t.position_pct + "%" : "-" }}</td>
            <td :class="fmtMoney(t.pnl).cls">{{ fmtMoney(t.pnl).text }}</td>
            <td :class="fmtPct(t.pnl_pct).cls">{{ fmtPct(t.pnl_pct).text }}</td>
            <td :title="t.reason || ''">{{ truncate(t.reason, 15) }}</td>
            <td class="actions-cell">
              <button class="btn btn-text btn-xs" @click="emit('edit', t)">编辑</button>
              <button class="btn btn-text btn-xs" style="color:var(--danger)" @click="emit('delete', t.id)">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else class="empty-msg">暂无交易记录</p>
    </div>
  </div>
</template>

<style scoped>
.actions-cell { white-space: nowrap; }
</style>
