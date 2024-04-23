<!-- Stream, Chat, About <user> -->
<script setup lang="ts">
import { onMounted, ref } from "vue";
import LoginModal from "./LoginModal.vue";
import { useCookies } from "vue3-cookies";
const { cookies } = useCookies();
const loggedIn = ref(false);
const following = ref<any[]>([]);

onMounted(async () => {
  if (cookies.get("access_token") && cookies.get("refresh_token")) {
    loggedIn.value = true;
    const refresh = await fetch("http://localhost:8000/api/token/refresh", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        refresh: cookies.get("refresh_token"),
      }),
    });
    const data = await refresh.json();
    cookies.set("access_token", data.access);
  }

  if (loggedIn.value === true) {
    const response = await fetch("http://localhost:8000/api/account", {
      headers: {
        Authorization: `Bearer ${cookies.get("access_token")}`,
      },
    });
    const data = await response.json();
    following.value = data.following;
  }
});
</script>

<template>
  <div class="side-nav">
    <LoginModal />
    <aside class="menu">
      <p class="menu-label">Routes</p>
      <ul class="menu-list">
        <li>
          <router-link to="/" exact>Home</router-link>
        </li>
      </ul>
      <p class="menu-label">Following</p>
      <ul class="menu-list">
        <li v-for="user in following" :key="user">
          <router-link :to="'/watch/' + user.username">{{
            user.username
          }}</router-link>
        </li>
      </ul>
    </aside>
  </div>
</template>

<style>
.menu {
  max-height: 100vh;
  width: 240px;
}
</style>
