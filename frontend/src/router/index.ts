import { createRouter, createWebHistory } from "vue-router";
import StreamView from "../views/StreamView.vue";
import HomeView from "../views/HomeView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/watch/:username",
      name: "watch",
      component: StreamView,
    },
  ],
});

export default router;
