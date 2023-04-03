import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import Varlet from "@varlet/ui";
import "@varlet/ui/es/style";

import "./assets/main.css";

const app = createApp(App);

app.use(router);
app.use(Varlet);

app.mount("#app");
