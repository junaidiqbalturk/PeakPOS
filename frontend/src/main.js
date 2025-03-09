import { createApp } from "vue";
import App from "./App.vue";
import router from "./router"; // Import router

import vuetify from "./plugins/vuetify"; // Import Vuetify

const app = createApp(App);
app.use(router); // Use Vue Router
app.use(vuetify);
app.mount("#app");
