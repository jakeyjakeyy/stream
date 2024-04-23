<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
const message = ref("");
const messages = ref<any>([]);
let socket: WebSocket | null = null;
const username = document.location.pathname.split("/").pop();

onMounted(() => {
  socket = new WebSocket(`ws://localhost:8000/ws/chat/`);

  socket.onmessage = function (event) {
    messages.value.push(event.data);
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
    socket.send(message.value);
    message.value = "";
  }
};
</script>

<template>
  <div class="chat box">
    <div class="chat-messages">
      <div class="chat-message">lole</div>
    </div>
    <div class="chat-input">
      <textarea
        type="text"
        class="textarea message-input"
        placeholder="Type a message..."
        rows="1"
      />
      <button class="button is-fullwidth">Send</button>
    </div>
  </div>
</template>

<style>
.chat {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 240px;
  height: 100%;
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
