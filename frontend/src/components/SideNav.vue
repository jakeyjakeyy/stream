<!-- Stream, Chat, About <user> -->
<script setup lang="ts"></script>

<template>
  <div class="side-nav">
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
          <router-link to="/stream">Stream</router-link>
        </li>
      </ul>
    </aside>
  </div>
</template>

<style>
.menu {
  width: 240px;
}
</style>
