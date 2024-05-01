<script setup lang="ts">
const props = defineProps<{
  streamInfo: {
    isLive: boolean;
    title: string;
    about: string;
    name: string;
  };
}>();
</script>

<template>
  <div class="aboutContainer">
    <div class="card">
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
            <p class="title is-4">{{ props.streamInfo.name }}</p>
            <p class="subtitle is-6">{{ props.streamInfo.title }}</p>
          </div>
        </div>
      </div>
    </div>
    <div class="about box">
      <p>{{ props.streamInfo.about }}</p>
    </div>
    <div class="about box">
      <p>More about blalbalabla {{ props.streamInfo.about }}</p>
    </div>
  </div>
</template>

<style scoped>
.aboutContainer {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: start;
  width: 100%;
  height: 100%;
}
.card {
  width: 100%;
  margin-bottom: 10px;
}
.about {
  width: 100%;
}
</style>
