import { createRouter, createWebHistory } from "vue-router";
import Index from "../views/IndexView.vue";
import Search from "../views/SearchView.vue";
import Plant from "../views/PlantView.vue";
import Database from "../views/DatabaseView.vue";
import ResultList from "../views/ResultListView.vue";
import Classifacation from "../views/ClassificationView.vue";
import Distribution from "../views/DistributionView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: "/", redirect: "/index" },
    { path: "/TODO", redirect: "/index" },
    {
      path: "/index",
      name: "index",
      component: Index,
    },
    {
      path: "/search",
      name: "search",
      component: Search,
    },
    {
      path: "/database",
      name: "database",
      component: Database,
    },
    {
      path: "/plant/:canonicalName",
      name: "plant",
      component: Plant,
      props: true,
    },
    {
      path: "/query",
      name: "query",
      component: ResultList,
      props: (route) => ({ queryValue: route.query.queryValue }),
    },
    {
      path: "/classification",
      name: "classification",
      component: Classifacation,
      props: (route) => ({ openFolder: route.query.openFolder }),
    },
    {
      path: "/distribution",
      name: "distribution",
      component: Distribution,
    },
  ],
});

export default router;
