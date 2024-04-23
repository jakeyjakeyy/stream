<!-- Stream, Chat, About <user> -->
<script setup lang="ts">
import SideNav from "@/components/SideNav.vue";
import { ref, onMounted } from "vue";

const width = ref(0);
const height = ref(0);

const isLive = ref(false);

const updateDimensions = () => {
  width.value = window.innerWidth - 240;
  height.value = window.innerHeight;
};

onMounted(async () => {
  const route = window.location.pathname.split("/").pop();
  document.title = `${route}'s Stream`;

  window.addEventListener("resize", updateDimensions);
  updateDimensions();

  const info = await fetch(`http://localhost:8000/api/info/${route}`);
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
        src="http://10.0.0.169/live/jake/index.m3u8"
        controls
        autoplay
        :width="width"
        :height="height"
      />
      <div v-else>
        <h1>Stream is offline</h1>
      </div>
    </div>
  </div>
</template>

<style>
.row {
  display: flex;
  flex-direction: row;
}
.stream {
  display: flex;
  justify-content: center;
  align-items: start;
}
</style>
