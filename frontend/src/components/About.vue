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
const editAbout = ref(false);
const updatedTitle = ref(props.streamInfo.title);
const updatedAbout = ref(props.streamInfo.about);

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

const fetchUpdate = async (edit: string, body: any) => {
  fetch(`http://${serverURL}:8000/api/update`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${cookies.get("access_token")}`,
    },
    body: JSON.stringify({
      [edit]: body,
    }),
  });
};
const toggleEdit = () => {
  editTitle.value = !editTitle.value;
  if (updatedTitle.value !== props.streamInfo.title) {
    fetchUpdate("title", updatedTitle.value);
    props.streamInfo.title = updatedTitle.value;
  }
};
const toggleEditAbout = () => {
  editAbout.value = !editAbout.value;
  if (updatedAbout.value !== props.streamInfo.about) {
    fetchUpdate("about", updatedAbout.value);
    props.streamInfo.about = updatedAbout.value;
  }
};
const getRows = (text: string) => {
  // so the aboutTextArea doesnt collapse on edit
  const lineBreaks = (text.match(/\n/g) || []).length;
  return lineBreaks + 1;
};
const uploadImage = (type: string) => {
  console.log(`Uplading ${type} image`);
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
                @click="uploadImage('profile')"
                src="https://bulma.io/assets/images/placeholders/96x96.png"
                alt="Placeholder image"
              />
            </figure>
          </div>
          <div class="media-content">
            <p class="title is-4">{{ props.streamInfo.name }}</p>
            <textarea
              v-if="ownsPage && editTitle"
              id="titleTextArea"
              class="subtitle is-6"
              v-model="updatedTitle"
              @blur="toggleEdit"
              rows="1"
              autofocus
            />
            <p
              v-else
              class="subtitle is-6"
              style="cursor: pointer"
              @click="toggleEdit"
            >
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
      <textarea
        class="subtitle is-6"
        v-if="ownsPage && editAbout"
        id="aboutTextArea"
        v-model="updatedAbout"
        @blur="toggleEditAbout"
        :rows="getRows(props.streamInfo.about)"
        autofocus
      />
      <p v-else @click="toggleEditAbout" style="cursor: pointer">
        {{ props.streamInfo.about }}
      </p>
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
  margin-bottom: 25px;
}
.card {
  width: 100%;
  margin-bottom: 10px;
}
.about {
  width: 100%;
  white-space: pre-wrap;
}

textarea {
  width: 100%;
  resize: none;
  height: 100%;
  border: none;
  background-color: transparent;
  color: white;
  outline: none;
  cursor: text;
}
#titleTextArea {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
