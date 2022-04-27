import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import AboutView from "../views/AboutView.vue";

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
      path: "/add",
      name: "Add",
      component: AboutView,
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
  ],
});

export default router;
