import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import AboutView from "../views/AboutView.vue";
import LoginView from "../views/LoginView.vue";
import AddTransactionView from "../views/transactions/AddTransactionView.vue";
import InspectTransactions from "../views/transactions/InspectTransactions.vue";
import StatsView from "../views/stats/StatsView.vue";
import DailyAvgView from "../views/stats/DailyAvgView.vue";
import CategoryAvgView from "../views/stats/CategoryAvgView.vue";
import NotFound from "../views/NotFound.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "Home",
      component: HomeView,
    },
    {
      path: "/about",
      name: "About",
      component: AboutView,
    },
    {
      path: "/login",
      name: "Login",
      component: LoginView,
    },
    {
      path: "/add",
      name: "Add",
      component: AddTransactionView,
    },
    {
      path: "/stats",
      name: "Stats",
      component: StatsView,
      children: [
        {
          path: "daily",
          name: "DailyAvgs",
          component: DailyAvgView,
        },
        {
          path: "category",
          name: "CategorySums",
          component: CategoryAvgView,
        },
      ],
    },
    {
      path: "/inspect",
      name: "Inspect",
      component: InspectTransactions,
    },
    {
      path: "/:pathMatch(.*)*",
      name: "NotFound",
      component: NotFound,
    },
  ],
});

export default router;
