<script setup lang="ts">
import { useCookies } from "vue3-cookies";
const serverURL = import.meta.env.VITE_BACKEND_URL;
const { cookies } = useCookies();
import RefreshToken from "@/utils/RefreshToken";
const handleSub = async () => {
  let i = 0;
  while (i < 2) {
    const res = await fetch(`http://${serverURL}:8000/api/subscribe`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${cookies.get("access_token")}`,
      },
      body: JSON.stringify({
        target: window.location.pathname.split("/").pop(),
        subscribe: true,
      }),
    });
    const data = await res.json();
    if (data.code === "token_not_valid") {
      await RefreshToken();
    } else {
      break;
    }
    i++;
  }
};
</script>

<template>
  <div class="subscribe">
    <button class="subscribeButton button" @click="handleSub">Subscribe</button>
  </div>
</template>

<style scoped></style>
