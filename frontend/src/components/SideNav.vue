<!-- Stream, Chat, About <user> -->
<script setup lang="ts">
import { onMounted, ref } from "vue";
import LoginModal from "./LoginModal.vue";
import { useCookies } from "vue3-cookies";
import RefreshToken from "@/utils/RefreshToken";
const { cookies } = useCookies();
const loggedIn = ref(false);
const following = ref<any[]>([]);

onMounted(async () => {
  if (cookies.get("access_token") && cookies.get("refresh_token")) {
    loggedIn.value = true;
    const refresh = await RefreshToken();
    if (refresh?.message === "Please log in again") {
      loggedIn.value = false;
      cookies.remove("access_token");
      cookies.remove("refresh_token");
      alert("Please log in again");
    }
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
    <aside class="menu">
      <p class="menu-label">Routes</p>
      <ul class="menu-list">
        <li>
          <LoginModal v-if="loggedIn === false" />
        </li>
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
      <p class="menu-label">Account</p>
      <ul class="menu-list">
        <li>
          <router-link to="/account">Account</router-link>
        </li>
        <li>
          <LoginModal v-if="loggedIn === true" />
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
