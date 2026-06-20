/**
 * 金额格式化 → { cls: 'profit'|'loss'|'', text: '+123.45'|'-123.45'|'-' }
 */
export function fmtMoney(n) {
  if (n == null || isNaN(n)) return { cls: "", text: "-" };
  const num = parseFloat(n);
  const cls = num > 0 ? "profit" : num < 0 ? "loss" : "";
  const sign = num > 0 ? "+" : "";
  return { cls, text: `${sign}${num.toFixed(2)}` };
}

/**
 * 百分比格式化 → { cls, text }
 */
export function fmtPct(n) {
  if (n == null || isNaN(n)) return { cls: "", text: "-" };
  const num = parseFloat(n);
  const cls = num > 0 ? "profit" : num < 0 ? "loss" : "";
  const sign = num > 0 ? "+" : "";
  return { cls, text: `${sign}${num.toFixed(2)}%` };
}

/**
 * 字符串截断
 */
export function truncate(s, max) {
  if (!s) return "-";
  return s.length > max ? s.slice(0, max) + "..." : s;
}

/**
 * 日期转 YYYY-MM-DD
 */
export function today() {
  return new Date().toISOString().slice(0, 10);
}
