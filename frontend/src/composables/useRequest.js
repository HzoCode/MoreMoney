import { ref } from "vue";

/**
 * 封装 API 调用，统一管理 loading / error 状态
 *
 * 用法:
 *   const { loading, error, execute } = useRequest()
 *   const data = await execute(() => api.listTrades())
 */
export function useRequest() {
  const loading = ref(false);
  const error = ref(null);

  async function execute(fn) {
    loading.value = true;
    error.value = null;
    try {
      return await fn();
    } catch (e) {
      error.value = e.message || "请求失败";
      throw e;
    } finally {
      loading.value = false;
    }
  }

  return { loading, error, execute };
}
