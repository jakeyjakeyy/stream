<!-- Stream, Chat, About <user> -->
<script setup lang="ts">
import LoginModal from "./LoginModal.vue";
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
        <li>
          <router-link to="/watch/jake">jake</router-link>
        </li>
      </ul>
    </aside>
  </div>
</template>

<style>
.menu {
  height: 100vh;
  width: 240px;
}
</style>
