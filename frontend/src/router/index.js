import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import AboutView from "../views/AboutView.vue";
import LoginView from "../views/LoginView.vue";
import AddTransactionView from "../views/transactions/AddTransactionView.vue";
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
      component: AboutView,
    },
    {
      path: "/inspect",
      name: "Inspect",
      component: AboutView,
    },
    { 
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: NotFound 
    }
  ],
});

export default router;
