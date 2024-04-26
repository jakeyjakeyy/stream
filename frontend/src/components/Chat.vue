<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from "vue";
import { useCookies } from "vue3-cookies";
const { cookies } = useCookies();
const serverURL = import.meta.env.VITE_BACKEND_URL;
const message = ref("");
const messages = ref<any>([]);
let socket: WebSocket | null = null;
const username = document.location.pathname.split("/").pop();

onMounted(() => {
  socket = new WebSocket(`ws://${serverURL}:8000/ws/chat/${username}/`);

  socket.onmessage = function (event) {
    messages.value.push(JSON.parse(event.data));
    console.log("WebSocket message", event);
  };

  socket.onclose = function (event) {
    console.log("WebSocket closed", event);
  };
});

onUnmounted(() => {
  if (socket) {
    socket.close();
  }
});

const sendMessage = () => {
  if (socket && message.value) {
    socket.send(
      JSON.stringify({
        message: message.value,
        access: cookies.get("access_token"),
      })
    );
    message.value = "";
  }
};

watch(messages.value, () => {
  console.log("Messages updated", messages.value);
});
</script>

<template>
  <div class="chat box">
    <div class="chat-messages">
      <div v-for="chatMessage in messages" class="chat-message">
        {{ chatMessage.username }}: {{ chatMessage.message }}
      </div>
    </div>
    <div class="chat-input">
      <textarea
        type="text"
        class="textarea message-input"
        placeholder="Type a message..."
        v-model="message"
        rows="1"
      />
      <button class="button is-fullwidth" @click="sendMessage">Send</button>
    </div>
  </div>
</template>

<style>
.chat {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 240px;
  height: 100vh;
  background-color: #2c2f33;
  color: white;
}
.chat-messages {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 0 10px;
  overflow-y: auto;
  height: 100%;
}

.chat-input {
  display: flex;
  flex-direction: column;
}

.message-input {
  width: 100%;
  resize: none;
}
</style>
