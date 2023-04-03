import { createRouter, createWebHistory } from "vue-router";
import Index from "../views/IndexView.vue";
import Search from "../views/SearchView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: "/", redirect: "/index" },
    {
      path: "/index",
      name: "index",
      component: Index,
    },
    {
      path: "/search",
      name: "search",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: Search,
    },
  ],
});

export default router;
