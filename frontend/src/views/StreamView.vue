<!-- Stream, Chat, About <user> -->
<script setup lang="ts">
import SideNav from "@/components/SideNav.vue";
import { ref, onMounted } from "vue";

const width = ref(0);
const height = ref(0);

const updateDimensions = () => {
  width.value = window.innerWidth - 240;
  height.value = window.innerHeight;
};

onMounted(() => {
  window.addEventListener("resize", updateDimensions);
  updateDimensions();
});
</script>

<template>
  <div class="row">
    <SideNav />
    <div class="stream">
      <video-player
        src="http://10.0.0.169/live/jake/index.m3u8"
        controls
        :width="width"
        :height="height"
      />
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
  align-items: center;
}
</style>
