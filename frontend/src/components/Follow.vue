<script setup lang="ts">
const serverURL = import.meta.env.VITE_BACKEND_URL;
import { onMounted, ref } from "vue";
import { useCookies } from "vue3-cookies";
const { cookies } = useCookies();
const loggedIn = ref(false);
const isFollowing = ref(false);

onMounted(async () => {
  if (cookies.get("access_token") && cookies.get("refresh_token")) {
    loggedIn.value = true;
    // check if we follow the user
    const response = await fetch(`http://${serverURL}:8000/api/account`, {
      headers: {
        Authorization: `Bearer ${cookies.get("access_token")}`,
      },
    });
    const data = await response.json();
    const username = window.location.pathname.split("/").pop();
    for (const user of data.following) {
      if (user.username === username) {
        isFollowing.value = true;
        break;
      }
    }
  }
});

const follow = async () => {
  const username = window.location.pathname.split("/").pop();
  const response = await fetch(`http://${serverURL}:8000/api/follow`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${cookies.get("access_token")}`,
    },
    body: JSON.stringify({ username, follow: !isFollowing.value }),
  });
  if (response.status === 200) {
    isFollowing.value = !isFollowing.value;
  }
};
</script>

<template>
  <div class="follow">
    <v-icon
      v-if="isFollowing"
      name="bi-suit-heart-fill"
      scale="1.25"
      color="red"
      @click="follow"
    />
    <v-icon v-else name="bi-suit-heart" scale="1.25" @click="follow" />
  </div>
</template>

<style scoped>
.follow {
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}
</style>
