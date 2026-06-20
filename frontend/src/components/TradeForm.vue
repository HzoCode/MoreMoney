<script setup>
import { reactive, watch, ref } from "vue";
import { today } from "../utils/format";

const props = defineProps({
  editData: { type: Object, default: null },
});

const emit = defineEmits(["save", "cancel"]);

const form = reactive({
  trade_date: today(),
  stock_code: "",
  stock_name: "",
  direction: "买入",
  price: "",
  quantity: "",
  amount: "",
  position_pct: "",
  pnl: "",
  pnl_pct: "",
  reason: "",
  notes: "",
});

const editId = ref(null);

watch(
  () => [form.price, form.quantity],
  ([p, q]) => {
    const price = parseFloat(p);
    const qty = parseInt(q);
    if (price > 0 && qty > 0) {
      form.amount = (price * qty).toFixed(2);
    }
  }
);

watch(
  () => props.editData,
  (data) => {
    if (data) {
      editId.value = data.id;
      Object.assign(form, {
        trade_date: data.trade_date,
        stock_code: data.stock_code,
        stock_name: data.stock_name,
        direction: data.direction,
        price: String(data.price),
        quantity: String(data.quantity),
        amount: String(data.amount),
        position_pct: data.position_pct != null ? String(data.position_pct) : "",
        pnl: data.pnl != null ? String(data.pnl) : "",
        pnl_pct: data.pnl_pct != null ? String(data.pnl_pct) : "",
        reason: data.reason || "",
        notes: data.notes || "",
      });
    } else {
      reset();
    }
  },
  { immediate: true }
);

function reset() {
  editId.value = null;
  Object.assign(form, {
    trade_date: today(),
    stock_code: "",
    stock_name: "",
    direction: "买入",
    price: "",
    quantity: "",
    amount: "",
    position_pct: "",
    pnl: "",
    pnl_pct: "",
    reason: "",
    notes: "",
  });
}

function parseOrNull(v) {
  const t = String(v).trim();
  return t === "" ? null : parseFloat(t);
}

function submit() {
  emit("save", {
    id: editId.value,
    data: {
      trade_date: form.trade_date,
      stock_code: form.stock_code.trim(),
      stock_name: form.stock_name.trim(),
      direction: form.direction,
      price: parseFloat(form.price),
      quantity: parseInt(form.quantity),
      amount: parseFloat(form.amount),
      position_pct: parseOrNull(form.position_pct),
      pnl: parseOrNull(form.pnl),
      pnl_pct: parseOrNull(form.pnl_pct),
      reason: form.reason.trim() || null,
      notes: form.notes.trim() || null,
    },
  });
  reset();
}
</script>

<template>
  <div class="card">
    <div class="card-header">
      <h2>{{ editId ? "编辑交易" : "新增交易" }}</h2>
    </div>
    <form class="form" @submit.prevent="submit">
      <div class="form-row">
        <label class="form-group">
          <span class="form-label">交易日期</span>
          <input type="date" v-model="form.trade_date" required />
        </label>
        <label class="form-group">
          <span class="form-label">股票代码</span>
          <input type="text" v-model="form.stock_code" placeholder="如 600519" maxlength="10" required />
        </label>
        <label class="form-group">
          <span class="form-label">股票名称</span>
          <input type="text" v-model="form.stock_name" placeholder="如 贵州茅台" maxlength="50" required />
        </label>
        <label class="form-group">
          <span class="form-label">方向</span>
          <span class="radios">
            <label class="radio"><input type="radio" v-model="form.direction" value="买入" /> 买入</label>
            <label class="radio"><input type="radio" v-model="form.direction" value="卖出" /> 卖出</label>
          </span>
        </label>
      </div>

      <div class="form-row">
        <label class="form-group">
          <span class="form-label">价格</span>
          <input type="number" v-model="form.price" step="0.001" min="0.001" placeholder="0.000" required />
        </label>
        <label class="form-group">
          <span class="form-label">数量（股）</span>
          <input type="number" v-model="form.quantity" step="1" min="1" placeholder="100" required />
        </label>
        <label class="form-group">
          <span class="form-label">成交金额</span>
          <input type="number" v-model="form.amount" step="0.01" min="0.01" placeholder="自动计算" required />
        </label>
        <label class="form-group">
          <span class="form-label">仓位占比（%）</span>
          <input type="number" v-model="form.position_pct" step="0.01" min="0" max="100" placeholder="可选" />
        </label>
      </div>

      <div class="form-row">
        <label class="form-group">
          <span class="form-label">盈亏金额</span>
          <input type="number" v-model="form.pnl" step="0.01" placeholder="盈利为正，亏损为负" />
        </label>
        <label class="form-group">
          <span class="form-label">盈亏百分比（%）</span>
          <input type="number" v-model="form.pnl_pct" step="0.01" placeholder="如 5.5 或 -3.2" />
        </label>
      </div>

      <div class="form-row">
        <label class="form-group" style="flex:2">
          <span class="form-label">交易理由</span>
          <textarea v-model="form.reason" rows="2" placeholder="买入/卖出的逻辑和依据"></textarea>
        </label>
        <label class="form-group" style="flex:2">
          <span class="form-label">心得备注</span>
          <textarea v-model="form.notes" rows="2" placeholder="交易后的感悟、反思"></textarea>
        </label>
      </div>

      <div class="form-actions">
        <button type="submit" class="btn btn-primary">{{ editId ? "更新" : "保存" }}</button>
        <button v-if="editId" type="button" class="btn btn-secondary" @click="reset(); emit('cancel')">取消编辑</button>
        <button type="button" class="btn btn-text" @click="reset">清空表单</button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.form { padding: 20px; }
.form-label { font-size: 13px; font-weight: 500; color: var(--text-secondary); }
.radios { display: flex; gap: 16px; padding-top: 6px; }
.radio { display: flex; align-items: center; gap: 4px; font-size: 14px; cursor: pointer; }
.form-actions { display: flex; gap: 8px; }
</style>
