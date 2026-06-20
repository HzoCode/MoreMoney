<script setup>
import { ref, reactive, onMounted } from "vue";
import { api } from "../api";
import { useRequest } from "../composables/useRequest";
import TradeForm from "../components/TradeForm.vue";
import TradeTable from "../components/TradeTable.vue";

const trades = ref([]);
const editData = ref(null);
const deleteId = ref(null);
const { loading, execute } = useRequest();

const filters = reactive({
  start_date: "",
  end_date: "",
  stock_code: "",
});

async function loadTrades() {
  try {
    trades.value = await execute(() => api.listTrades(filters));
  } catch (e) {
    alert("加载交易记录失败: " + e.message);
  }
}

async function handleSave({ id, data }) {
  try {
    await execute(() => (id ? api.updateTrade(id, data) : api.createTrade(data)));
    editData.value = null;
    await loadTrades();
  } catch (e) {
    alert("保存失败: " + e.message);
  }
}

function handleEdit(trade) {
  editData.value = { ...trade };
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function handleCancelEdit() {
  editData.value = null;
}

async function confirmDelete() {
  if (!deleteId.value) return;
  try {
    await execute(() => api.deleteTrade(deleteId.value));
    deleteId.value = null;
    await loadTrades();
  } catch (e) {
    alert("删除失败: " + e.message);
  }
}

function resetFilters() {
  filters.start_date = "";
  filters.end_date = "";
  filters.stock_code = "";
  loadTrades();
}

onMounted(loadTrades);
</script>

<template>
  <TradeForm :editData="editData" @save="handleSave" @cancel="handleCancelEdit" />

  <div class="card">
    <div class="card-header">
      <h2>交易列表</h2>
      <div class="filter-bar">
        <input type="date" v-model="filters.start_date" />
        <span class="filter-sep">至</span>
        <input type="date" v-model="filters.end_date" />
        <input type="text" v-model="filters.stock_code" placeholder="股票代码筛选" maxlength="10" />
        <button class="btn btn-secondary btn-sm" @click="loadTrades">筛选</button>
        <button class="btn btn-text btn-sm" @click="resetFilters">重置</button>
      </div>
    </div>
    <div v-if="loading" class="loading">加载中...</div>
    <TradeTable v-else :trades="trades" @edit="handleEdit" @delete="(id) => (deleteId = id)" />
  </div>

  <div v-if="deleteId" class="modal-overlay" @click.self="deleteId = null">
    <div class="modal-content">
      <h3>确认删除</h3>
      <p>确定要删除这条交易记录吗？此操作不可撤销。</p>
      <div class="modal-actions">
        <button class="btn btn-danger" @click="confirmDelete">确认删除</button>
        <button class="btn btn-secondary" @click="deleteId = null">取消</button>
      </div>
    </div>
  </div>
</template>
