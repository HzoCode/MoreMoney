import { createRouter, createWebHistory } from "vue-router";
import TradeView from "../views/TradeView.vue";
import ReviewView from "../views/ReviewView.vue";
import SummaryView from "../views/SummaryView.vue";

const routes = [
  { path: "/", redirect: "/trades" },
  { path: "/trades", name: "trades", component: TradeView },
  { path: "/reviews", name: "reviews", component: ReviewView },
  { path: "/summary", name: "summary", component: SummaryView },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
