<!-- Stream, Chat, About <user> -->
<script setup lang="ts">
import SideNav from "@/components/SideNav.vue";
import Chat from "@/components/Chat.vue";
import About from "@/components/About.vue";
import { ref, onMounted } from "vue";
const serverURL = import.meta.env.VITE_BACKEND_URL;

const width = ref(0);
const height = ref(0);

const isLive = ref(false);

const streamInfo = ref<any>({});

const updateDimensions = () => {
  const aspectRatio = 16 / 9;
  const sideNavWidth = 240;
  const chatWidth = 240;
  const availableWidth = window.innerWidth - sideNavWidth - chatWidth;
  const availableHeight = window.innerHeight;

  // Calculate the maximum width and height while maintaining aspect ratio
  const maxWidth = Math.floor(availableHeight * aspectRatio);
  const maxHeight = Math.floor(availableWidth / aspectRatio);

  // Choose the smaller dimension to fit within the screen
  const setWidth = Math.min(maxWidth, availableWidth);
  const setHeight = Math.min(maxHeight, availableHeight);

  // Update the width and height refs
  width.value = setWidth;
  height.value = setHeight;
};

onMounted(async () => {
  const route = window.location.pathname.split("/").pop();
  document.title = `${route}'s Stream`;

  window.addEventListener("resize", updateDimensions);
  updateDimensions();

  const info = await fetch(`http://${serverURL}:8000/api/info/${route}`);
  const data = await info.json();
  streamInfo.value = data;

  // console.log(data);
  isLive.value = data.isLive;
});
</script>

<template>
  <div class="row">
    <SideNav />
    <div class="streamContainer">
      <div class="videoContainer">
        <div class="videoPlayer">
          <video-player
            v-if="isLive"
            :src="`http://${serverURL}/live/jake/index.m3u8`"
            controls
            autoplay
            :width="width"
            :height="height"
          />
          <div v-else>
            <img
              class="image is-16by9"
              :width="width"
              :height="height"
              src="https://bulma.io/assets/images/placeholders/1280x960.png"
              alt="Placeholder image"
            />
          </div>
        </div>
        <About
          v-if="Object.keys(streamInfo).length > 0"
          :streamInfo="streamInfo"
        />
        <div v-else class="skeleton block about" />
      </div>
      <div class="chatContainer">
        <Chat />
      </div>
    </div>
  </div>
</template>

<style>
.row {
  display: flex;
  flex-direction: row;
  height: 100%;
}
.streamContainer {
  display: flex;
  justify-content: center;
  align-items: start;
  width: 100%;
  height: 100vh;
}
.videoContainer {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  height: 100vh;
  overflow-y: scroll;
}
.chatContainer {
  display: fixed;
  height: 100vh;
}
</style>
