import "./assets/main.css";

import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import VueVideoPlayer from "@videojs-player/vue";
import "video.js/dist/video-js.css";
import { OhVueIcon, addIcons } from "oh-vue-icons";
import { BiSuitHeart, BiSuitHeartFill } from "oh-vue-icons/icons";

addIcons(BiSuitHeart, BiSuitHeartFill);

const app = createApp(App);

app.use(router);
app.use(VueVideoPlayer);
app.component("v-icon", OhVueIcon);

app.mount("#app");
