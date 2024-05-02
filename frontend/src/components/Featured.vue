<script setup lang="ts">
import { ref, onMounted } from "vue";
const serverURL = import.meta.env.VITE_BACKEND_URL;

const featured = ref<any[]>([]);

onMounted(async () => {
  const response = await fetch(`http://${serverURL}:8000/api/featured`);
  const data = await response.json();
  featured.value = data.featured;
});
</script>

<template>
  <div class="featured">
    <h1>Featured</h1>
    <div class="fixed-grid has-1-cols-mobile has-5-cols-desktop">
      <div class="grid">
        <div v-for="feature in featured" class="card cell">
          <RouterLink :to="'/watch/' + feature.username">
            <div class="card-image">
              <figure class="image is-4by3">
                <img
                  src="https://bulma.io/assets/images/placeholders/1280x960.png"
                  alt="Placeholder image"
                />
              </figure>
            </div>
            <div class="card-content">
              <div class="media">
                <div class="media-left">
                  <figure class="image is-48x48">
                    <img
                      src="https://bulma.io/assets/images/placeholders/96x96.png"
                      alt="Placeholder image"
                    />
                  </figure>
                </div>
                <div class="media-content">
                  <p class="title is-4">{{ feature.username }}</p>
                </div>
              </div>

              <div class="content has-text-grey-light">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                Phasellus nec iaculis mauris.
                <br />
                <time datetime="2016-1-1">{{ feature.started_at }}</time>
              </div>
            </div>
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
.featured {
  width: 100%;
}
</style>
