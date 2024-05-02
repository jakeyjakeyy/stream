<script setup lang="ts">
import Follow from "./Follow.vue";
const props = defineProps<{
  streamInfo: {
    isLive: boolean;
    title: string;
    about: string;
    name: string;
  };
}>();
const serverURL = import.meta.env.VITE_BACKEND_URL;
import { onMounted, ref, watch } from "vue";
import { useCookies } from "vue3-cookies";
const { cookies } = useCookies();
const loggedIn = ref(false);
const ownsPage = ref(false);
const editTitle = ref(false);
const updatedTitle = ref(props.streamInfo.title);

onMounted(async () => {
  if (cookies.get("access_token") && cookies.get("refresh_token")) {
    loggedIn.value = true;
    const response = await fetch(`http://${serverURL}:8000/api/whoami`, {
      headers: {
        Authorization: `Bearer ${cookies.get("access_token")}`,
      },
    });
    const data = await response.json();
    if (data.username === window.location.pathname.split("/").pop()) {
      ownsPage.value = true;
    }
  }
});
const toggleEdit = () => {
  editTitle.value = !editTitle.value;
  if (updatedTitle.value !== props.streamInfo.title) {
    fetch(`http://${serverURL}:8000/api/update`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${cookies.get("access_token")}`,
      },
      body: JSON.stringify({
        title: updatedTitle.value,
      }),
    });
    props.streamInfo.title = updatedTitle.value;
  }
};
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
            <textarea
              v-if="ownsPage && editTitle"
              v-model="updatedTitle"
              @blur="toggleEdit"
            />
            <p v-else class="subtitle is-6" @click="toggleEdit">
              {{ props.streamInfo.title }}
            </p>
          </div>
          <div class="media-right">
            <Follow />
          </div>
        </div>
      </div>
    </div>
    <div class="about box">
      <p>
        {{ props.streamInfo.about }}
      </p>
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

textarea {
  width: 100%;
  resize: none;
  height: 100%;
  border: none;
  background-color: transparent;
  color: white;
  font-weight: bold;
  font-family: "Roboto", sans-serif;
  padding: 0;
  margin: 0;
  outline: none;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  cursor: pointer;
}
</style>
