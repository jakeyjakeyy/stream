<!-- Stream, Chat, About <user> -->
<script setup lang="ts">
import SideNav from "@/components/SideNav.vue";
import Chat from "@/components/Chat.vue";
import { ref, onMounted } from "vue";
const serverURL = import.meta.env.VITE_BACKEND_URL;

const width = ref(0);
const height = ref(0);

const isLive = ref(false);

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
  console.log(data);
  isLive.value = data.isLive;
});
</script>

<template>
  <div class="row">
    <SideNav />
    <div class="stream">
      <video-player
        v-if="isLive"
        :src="`http://${serverURL}/live/jake/index.m3u8`"
        controls
        autoplay
        :width="width"
        :height="height"
      />
      <div v-else>
        <h1>Stream is offline</h1>
      </div>
      <Chat />
    </div>
  </div>
</template>

<style>
.row {
  display: flex;
  flex-direction: row;
  height: 100%;
}
.stream {
  display: flex;
  justify-content: center;
  align-items: start;
  width: 100%;
}
</style>
